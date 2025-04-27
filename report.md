
CS 4090 – Assignment 4
Streamlit To-Do Application: Dalton Jayaraj · April 2025
Project Overview
This assignment involved enhancing and testing a Streamlit-based To-Do list application. The objectives were to implement:
Foundational testing using pytest
Advanced pytest features (e.g., fixtures, parameterization, HTML reports, coverage)
Test-Driven Development (TDD) for new features
Behavior-Driven Development (BDD) with Gherkin scenarios via pytest-bdd
Property-based testing using Hypothesis
The final application includes all required task-management functionality and features sidebar buttons that run automated test suites, displaying results live in the UI.

Environment & Setup
The project was developed and tested in the following environment:
Tool/Library
Version
Notes
Python
3.13.2
Installed via Homebrew
Streamlit
1.34.0
Provides interactive UI
pytest
7.4.4
Pinned for pytest-bdd compatibility
pytest-cov
5.0.0
Coverage metrics
pytest-bdd
7.0.0
BDD features
hypothesis
6.102.0
Property-based testing
pytest-html
4.1.1
Optional HTML report generation

Setup Instructions:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py  # Launches UI with sidebar test-runner


Testing Strategy
1. Unit Testing & Coverage
File: tests/test_basic.py
Coverage Scope: CRUD operations, filters, persistence helpers, and edge cases
Command:
 pytest -q --cov=tasks --cov=app --cov-report=term-missing


Target Coverage: ≥ 90%
Achieved: 98% 

2. Pytest-Feature Showcase
File: tests/test_advanced.py
Parameterization: Tests High/Medium/Low task priorities
Fixtures: Reuses a shared task list
Monkey-Patching: Mocks datetime for testing
HTML Report: Generated with:
 pytest -q --html=unit_report.html

3. Test-Driven Development (TDD)
Feature: Overdue task detection
Process:
Wrote failing test in tests/test_tdd.py (date comparison failed)
Added get_overdue_tasks() in tasks.py
Made test pass by returning tasks with due date < today and not completed
Refactored by moving date logic to a helper function


4. Behavior-Driven Development (BDD)
File: tests/features/add_task.feature
Details: Gherkin scenarios translated to Python step definitions
Fix: Added empty_list fixture to resolve missing-fixture error

5. Property-Based Testing
File: tests/test_property.py
Tests:
Generates non-blank titles (≤ 20 characters)
Ensures add_task() never reuses IDs
Fixed empty-string bug by filtering whitespace titles

Here are some bug fixes found and their fixes
ID
Description
Symptom
Fix
B-01
Path vs. str in load_tasks()
TypeError in corrupt file test
Cast file_path to string
B-02
Missing fixture in BDD step
fixture 'empty_list' not found
Added target_fixture parameter
B-03
Deprecated pytest.main(stdout=)
UI crash on test-button click
Used subprocess.run()
B-04
pytest-bdd vs. pytest 8 issue
ImportError
Pinned pytest to 7.4.4
B-05
Hypothesis blank titles
ValueError: Title empty
Filtered whitespace in strategy
B-06
Deprecated st.experimental_rerun
Streamlit warning
Replaced with st.rerun()


Results & Metrics
Metric
Requirement
Achieved
Unit Coverage
≥ 90%
98%
Tests Passing
All suites
Yes
Bugs Fixed
Documented & patched
6 major, all resolved
TDD Features
≥ 3
Overdue detection, backups, test UI
BDD Scenarios
≥ 5 steps (1 scenario)
1 feature, 3 steps, passes
Property Tests
≥ 5 checks
2 functions with dynamic cases


Lessons Learned
Compatibility: pytest-bdd required pinning pytest to 7.x due to version lag.
Coverage Insights: Achieving 90%+ revealed untested error-handling paths.
Hypothesis Power: Quickly identified edge cases 
Streamlit Advantage: Sidebar test buttons provide clear visual feedback.
Modularity: Small fixtures enhance testability over global state, this was causing problem due to some other clashing dependency. 
Future Work
Add end-to-end UI tests with Playwright/Selenium.
Implement a CI pipeline 
Integrate a database with persistence tests.
Expand tag filtering UI (data-level support already exists).

How to test commands.

pytest -q --cov=tasks --cov=app --cov-report=term-missing

# Individual suites
pytest -q tests/test_basic.py
pytest -q tests/test_advanced.py --html=unit_report.html
pytest -q tests/features
pytest -q tests/test_property.py



