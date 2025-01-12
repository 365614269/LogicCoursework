# Tableau Logic Solver

This repository contains the implementation of a **Tableau-based logic solver** for propositional and first-order logic (FOL). The project was completed as part of the COMP0009 Logic course and earned a **final grade of 93.33/100**.

## Project Overview

The `tableau.py` program implements a tableau method to evaluate logical formulas for satisfiability. It supports both propositional and first-order logic, adhering to specific constraints and input/output formats as described in the coursework brief.

### Features:
- **Propositional Logic Parsing**:
  - Supports logical connectives: `~` (negation), `/\` (and), `\/` (or), and `=>` (implies).
  - Parses and validates formulas for correctness.
- **First-Order Logic Parsing**:
  - Handles quantifiers: `E` (existential) and `A` (universal).
  - Supports binary predicates with fixed arity (e.g., `P(x, y)`).
- **Satisfiability Determination**:
  - For propositional logic: Determines whether a formula is satisfiable.
  - For FOL: Identifies satisfiability or undetermined status (if the tableau requires more than 10 new constants).

## How to Run

1. **Prepare the Input File**: 
   - Create a file named `input.txt` in the same directory as `tableau.py`. 
   - The first line should be `PARSE` (for parsing) or `SAT` (for satisfiability determination), followed by logical formulas on subsequent lines.

2. **Run the Program**:
   ```bash
   python3 tableau.py > output.txt
   ```
   The output will be saved in `output.txt`.

## Assessment Criteria

The implementation was graded based on the following:
- Parsing of propositional formulas: **20/20**
- Satisfiability determination for propositional formulas: **20/20**
- Parsing of first-order logic formulas: **20/20**
- Satisfiability determination for FOL without infinite loops: **20/20**
- Satisfiability determination for FOL with up to 10 constants: **13.33/20**

## Constraints

- **No imports**: The file does not include any external libraries.
- **Single file submission**: The program is implemented entirely within `tableau.py`.
- **Timeout Limit**: Each test case must complete within 1 minute.

## Usage Notes

- Ensure compliance with the specified format for input and output files.
- The program has been tested against multiple public and secret test cases, achieving an overall accuracy of 93.33%.

## Acknowledgments

This project was part of the **COMP0009 Logic course** at UCL, completed in November 2024.

---

Feel free to modify this template to better fit your style or add any additional project-specific details!
