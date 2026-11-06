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
