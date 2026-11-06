"""Unit tests for the Student Grade Management System."""

import unittest

from grade_manager import (
    calculate_average,
    calculate_class_summary,
    create_student_record,
    determine_letter_grade,
    find_student_by_id,
    format_student_table,
    validate_mark,
    validate_student_id,
    validate_student_name,
)


class TestValidation(unittest.TestCase):
    """Tests for student ID, name, and mark validation."""

    def test_valid_student_id_normalized(self):
        self.assertEqual(validate_student_id("  bits/0194/24 ", []), "BITS/0194/24")

    def test_empty_student_id_raises(self):
        with self.assertRaises(ValueError):
            validate_student_id("   ", [])

    def test_duplicate_student_id_raises(self):
        existing = [{"id": "BITS/0194/24", "name": "Fikir Samuel"}]
        with self.assertRaises(ValueError):
            validate_student_id("bits/0194/24", existing)

    def test_valid_student_name_collapses_spaces(self):
        self.assertEqual(validate_student_name("  Fikir   Samuel "), "Fikir Samuel")

    def test_empty_student_name_raises(self):
        with self.assertRaises(ValueError):
            validate_student_name("")

    def test_non_alphabetic_student_name_raises(self):
        with self.assertRaises(ValueError):
            validate_student_name("12345")

    def test_valid_mark_boundaries(self):
        self.assertEqual(validate_mark("0"), 0.0)
        self.assertEqual(validate_mark("100"), 100.0)
        self.assertEqual(validate_mark("87.456"), 87.46)

    def test_negative_mark_raises(self):
        with self.assertRaises(ValueError):
            validate_mark("-0.5")

    def test_over_hundred_mark_raises(self):
        with self.assertRaises(ValueError):
            validate_mark("100.1")

    def test_non_numeric_mark_raises(self):
        with self.assertRaises(ValueError):
            validate_mark("abc")

    def test_non_finite_mark_raises(self):
        for bad in ("nan", "inf", "-inf"):
            with self.assertRaises(ValueError):
                validate_mark(bad)


class TestCalculationsAndGrades(unittest.TestCase):
    """Tests for average calculation and letter grade mapping."""

    def test_calculate_average_rounds_to_two_decimals(self):
        self.assertEqual(calculate_average([85.0, 90.0, 92.0]), 89.0)
        self.assertEqual(calculate_average([80.0, 81.0, 82.5]), 81.17)

    def test_calculate_average_empty_raises(self):
        with self.assertRaises(ValueError):
            calculate_average([])

    def test_letter_grade_thresholds(self):
        cases = [
            (95.0, "A"),
            (90.0, "A"),
            (89.99, "B"),
            (80.0, "B"),
            (79.99, "C"),
            (70.0, "C"),
            (69.99, "D"),
            (60.0, "D"),
            (59.99, "F"),
            (0.0, "F"),
        ]
        for avg, expected in cases:
            with self.subTest(avg=avg):
                self.assertEqual(determine_letter_grade(avg), expected)

    def test_letter_grade_out_of_range_raises(self):
        for invalid in (-1.0, 101.0, float("nan")):
            with self.assertRaises(ValueError):
                determine_letter_grade(invalid)


class TestRecordsAndDisplay(unittest.TestCase):
    """Tests for record creation, lookup, summary statistics, and formatting."""

    def test_create_student_record_computes_totals(self):
        record = create_student_record(
            "bits/0194/24",
            "Fikir Samuel",
            {"Math": 92, "Programming": 88, "Database": 90},
        )
        self.assertEqual(record["id"], "BITS/0194/24")
        self.assertEqual(record["total"], 270.0)
        self.assertEqual(record["average"], 90.0)
        self.assertEqual(record["grade"], "A")

    def test_create_student_record_empty_marks_raises(self):
        with self.assertRaises(ValueError):
            create_student_record("BITS/0194/24", "Fikir Samuel", {})

    def test_find_student_by_id_found_and_missing(self):
        r1 = create_student_record("S01", "Abebe Bikila", {"Math": 80})
        self.assertEqual(find_student_by_id([r1], "s01")["name"], "Abebe Bikila")
        self.assertIsNone(find_student_by_id([r1], "S99"))

    def test_class_summary_empty(self):
        summary = calculate_class_summary([])
        self.assertEqual(summary["count"], 0)
        self.assertEqual(summary["class_average"], 0.0)

    def test_class_summary_multiple_students(self):
        r1 = create_student_record("S01", "Student One", {"Math": 90, "Prog": 90})
        r2 = create_student_record("S02", "Student Two", {"Math": 50, "Prog": 50})
        summary = calculate_class_summary([r1, r2])
        self.assertEqual(summary["count"], 2)
        self.assertEqual(summary["class_average"], 70.0)
        self.assertEqual(summary["highest_average"], 90.0)
        self.assertEqual(summary["lowest_average"], 50.0)
        self.assertEqual(summary["passed"], 1)
        self.assertEqual(summary["failed"], 1)

    def test_format_student_table_empty(self):
        self.assertEqual(format_student_table([]), "No student records available.")

    def test_format_student_table_includes_student_and_summary(self):
        r1 = create_student_record("S01", "Fikir Samuel", {"Math": 85, "Prog": 95})
        output = format_student_table([r1])
        self.assertIn("S01", output)
        self.assertIn("Fikir Samuel", output)
        self.assertIn("90.00", output)
        self.assertIn("Students: 1", output)


if __name__ == "__main__":
    unittest.main()
