# Student Grade Management System (Python)

A command-line Student Grade Management System developed for the Software Process Improvement (SPI) Personal Software Process (PSP) assignment.

## 1. Overview

This application accepts student identification details and subject marks, validates all user inputs, calculates total and average marks, assigns letter grades, and displays formatted individual and class-wide grade summaries.

## 2. Requirements

| ID | Requirement | Category |
| --- | --- | --- |
| R1 | Accept a non-empty student ID and normalize case/whitespace. | Input & Validation |
| R2 | Reject duplicate student IDs across stored records. | Input & Validation |
| R3 | Accept a student name containing alphabetic characters and normalize spaces. | Input & Validation |
| R4 | Accept marks for four default subjects (Mathematics, Programming, Database Systems, Software Engineering). | Input & Validation |
| R5 | Validate numeric marks within 0 to 100 inclusive and reject non-finite or non-numeric entries. | Input & Validation |
| R6 | Compute total marks and arithmetic average rounded to two decimal places. | Calculation |
| R7 | Assign standard letter grades (`A`, `B`, `C`, `D`, `F`) from the calculated average. | Calculation |
| R8 | Support looking up an individual student record by student ID. | Reporting |
| R9 | Compute class-wide statistics (student count, class average, highest, lowest, pass/fail counts). | Reporting |
| R10 | Provide an interactive menu-driven CLI loop with clear error messages and exit handling. | Interface |

## 3. System Design

The application is organized into 11 single-purpose functions in `grade_manager.py`:

1. `validate_student_id` – Normalizes and verifies uniqueness of student IDs.
2. `validate_student_name` – Normalizes whitespace and checks alphabetic content.
3. `validate_mark` – Parses numeric input and enforces finite `0–100` bounds.
4. `calculate_average` – Computes rounded arithmetic average for a mark list.
5. `determine_letter_grade` – Maps numeric average to letter grade (`A`–`F`).
6. `create_student_record` – Validates inputs and builds a complete student dictionary.
7. `find_student_by_id` – Case-insensitive lookup by student ID.
8. `calculate_class_summary` – Aggregates count, mean, min, max, and pass/fail totals.
9. `format_student_table` – Renders aligned tabular output and summary footer.
10. `_prompt_valid_input` – Reusable CLI validation retry loop.
11. `run_cli` – Main interactive menu dispatcher.

## 4. Grading Scale and Validation Rules

- **Grading Scale:** `A` (90.00–100.00), `B` (80.00–89.99), `C` (70.00–79.99), `D` (60.00–69.99), `F` (< 60.00).
- **Validation:** Empty IDs, duplicate IDs, blank/numeric-only names, non-numeric marks, `NaN`/`Inf`, and values outside `[0, 100]` raise `ValueError` with descriptive feedback.

## 5. Project Structure

```text
student-grade-management-system/
├── grade_manager.py        # Core application logic and CLI (164 non-blank, non-comment LOC; 11 functions)
├── test_grade_manager.py   # Automated unit test suite (22 tests)
├── psp/
│   └── estimates.md        # Pre-work PSP estimates
└── README.md               # Project specification, design, and usage (6 sections)
```

## 6. Usage and Running Tests

Run the interactive program:

```bash
python3 grade_manager.py
```

Run the automated unit test suite:

```bash
python3 -m unittest -v
```
