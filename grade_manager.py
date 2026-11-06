"""CLI Student Grade Management System for PSP assignment."""

import math
from typing import Dict, List, Optional

DEFAULT_SUBJECTS = ("Mathematics", "Programming", "Database Systems", "Software Engineering")


def validate_student_id(student_id: str, existing_records: List[Dict]) -> str:
    """Validate and normalize a unique non-empty student ID."""
    cleaned = student_id.strip().upper()
    if not cleaned:
        raise ValueError("Student ID cannot be empty.")
    if any(record["id"] == cleaned for record in existing_records):
        raise ValueError(f"Student ID '{cleaned}' already exists.")
    return cleaned


def validate_student_name(name: str) -> str:
    """Validate and normalize a non-empty student name."""
    cleaned = " ".join(name.strip().split())
    if not cleaned:
        raise ValueError("Student name cannot be empty.")
    if not any(char.isalpha() for char in cleaned):
        raise ValueError("Student name must contain alphabetic characters.")
    return cleaned


def validate_mark(raw_value: str) -> float:
    """Parse and validate a numeric mark between 0 and 100 inclusive."""
    text = raw_value.strip()
    if not text:
        raise ValueError("Mark cannot be empty.")
    try:
        mark = float(text)
    except ValueError as exc:
        raise ValueError(f"Invalid numeric mark: '{raw_value}'.") from exc
    if not math.isfinite(mark) or mark < 0.0 or mark > 100.0:
        raise ValueError("Mark must be between 0 and 100.")
    return round(mark, 2)


def calculate_average(marks: List[float]) -> float:
    """Return the rounded arithmetic mean for a non-empty list of marks."""
    if not marks:
        raise ValueError("At least one mark is required to compute an average.")
    return round(sum(marks) / len(marks), 2)


def determine_letter_grade(average: float) -> str:
    """Map a numeric average (0-100) to a standard letter grade."""
    if not math.isfinite(average) or average < 0.0 or average > 100.0:
        raise ValueError("Average must be between 0 and 100.")
    grade_thresholds = (
        (90.0, "A"),
        (80.0, "B"),
        (70.0, "C"),
        (60.0, "D"),
    )
    for threshold, letter in grade_thresholds:
        if average >= threshold:
            return letter
    return "F"


def create_student_record(
    student_id: str,
    name: str,
    marks: Dict[str, float],
    existing_records: Optional[List[Dict]] = None,
) -> Dict:
    """Validate inputs and construct a complete student grade record."""
    records = existing_records or []
    valid_id = validate_student_id(student_id, records)
    valid_name = validate_student_name(name)
    if not marks:
        raise ValueError("At least one subject mark is required.")
    validated_marks = {
        subject: validate_mark(str(score)) for subject, score in marks.items()
    }
    total = round(sum(validated_marks.values()), 2)
    average = calculate_average(list(validated_marks.values()))
    letter_grade = determine_letter_grade(average)
    return {
        "id": valid_id,
        "name": valid_name,
        "marks": validated_marks,
        "total": total,
        "average": average,
        "grade": letter_grade,
    }


def find_student_by_id(records: List[Dict], student_id: str) -> Optional[Dict]:
    """Look up a student record by case-insensitive student ID."""
    target = student_id.strip().upper()
    for record in records:
        if record["id"] == target:
            return record
    return None


def calculate_class_summary(records: List[Dict]) -> Dict:
    """Compute aggregate statistics across all recorded students."""
    if not records:
        return {
            "count": 0,
            "class_average": 0.0,
            "highest_average": 0.0,
            "lowest_average": 0.0,
            "passed": 0,
            "failed": 0,
        }
    averages = [record["average"] for record in records]
    passed = sum(1 for record in records if record["grade"] != "F")
    return {
        "count": len(records),
        "class_average": round(sum(averages) / len(averages), 2),
        "highest_average": max(averages),
        "lowest_average": min(averages),
        "passed": passed,
        "failed": len(records) - passed,
    }


def format_student_table(records: List[Dict]) -> str:
    """Format all student grade records and summary into a readable table."""
    if not records:
        return "No student records available."
    header = f"{'ID':<12} {'Name':<22} {'Total':>8} {'Average':>8} {'Grade':>6}"
    divider = "-" * len(header)
    rows = [header, divider]
    for record in records:
        rows.append(
            f"{record['id']:<12} {record['name']:<22} "
            f"{record['total']:>8.2f} {record['average']:>8.2f} {record['grade']:>6}"
        )
    summary = calculate_class_summary(records)
    rows.append(divider)
    rows.append(
        f"Students: {summary['count']} | Class Avg: {summary['class_average']:.2f} | "
        f"High: {summary['highest_average']:.2f} | Low: {summary['lowest_average']:.2f} | "
        f"Pass: {summary['passed']} | Fail: {summary['failed']}"
    )
    return "\n".join(rows)


def _prompt_valid_input(prompt_text: str, validator) -> object:
    """Prompt repeatedly until the provided validator accepts the input."""
    while True:
        raw = input(prompt_text)
        try:
            return validator(raw)
        except ValueError as err:
            print(f"Input error: {err}")


def run_cli() -> None:
    """Run the interactive Student Grade Management System menu."""
    records: List[Dict] = []
    while True:
        print("\n=== Student Grade Management System ===")
        print("1. Add student and marks")
        print("2. Display all student grades")
        print("3. Search student by ID")
        print("4. Exit")
        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            student_id = _prompt_valid_input(
                "Enter Student ID: ", lambda raw: validate_student_id(raw, records)
            )
            name = _prompt_valid_input("Enter Student Name: ", validate_student_name)
            marks: Dict[str, float] = {}
            for subject in DEFAULT_SUBJECTS:
                marks[subject] = _prompt_valid_input(
                    f"Enter mark for {subject} (0-100): ", validate_mark
                )
            record = create_student_record(student_id, name, marks, records)
            records.append(record)
            print(
                f"Saved {record['name']} ({record['id']}) - "
                f"Average: {record['average']:.2f}, Grade: {record['grade']}"
            )
        elif choice == "2":
            print()
            print(format_student_table(records))
        elif choice == "3":
            query = input("Enter Student ID to search: ")
            match = find_student_by_id(records, query)
            if match is None:
                print("Student record not found.")
            else:
                print(format_student_table([match]))
        elif choice == "4":
            print("Exiting Student Grade Management System.")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    run_cli()
