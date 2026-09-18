# AI for Financial Literacy — Implementation Plan

## Top-Level Overview

**Goal:** Build a small, beginner-friendly "AI for Financial Literacy" web application using Python and Streamlit. The app helps students track income and expenses, visualise spending, manage a savings goal, and learn basic financial concepts through a simple Q&A assistant.

**Scope:**
- Pure Python with OOP, type hints, and Streamlit UI
- JSON file for simple data persistence (survives page refresh)
- Keyword-based AI assistant (no external APIs or LLMs required)
- pytest unit tests covering all business logic classes
- Single-user, single-month focus — no authentication, no database

**Non-Goals:**
- No investment advice or personalised financial recommendations
- No multi-user support
- No external API calls
- No deployment or Docker setup

---

## Project Architecture

```
financial_literacy_app/
│
├── app.py                  # Streamlit entry point — UI only
│
├── models/
│   └── expense.py          # Expense dataclass
│
├── core/
│   ├── expense_tracker.py  # Income, expense, savings logic
│   └── financial_ai.py     # Q&A assistant and tips
│
├── data/
│   ├── financial_concepts.py   # Static knowledge base (concepts + tips)
│   └── expenses.json           # Persisted expense/income data (auto-created)
│
├── utils/
│   ├── validators.py       # All input validation functions
│   └── exceptions.py       # Custom exception classes
│
└── tests/
    ├── test_expense_tracker.py
    ├── test_financial_ai.py
    └── test_validators.py
```

**Data flow:**
- `app.py` calls methods on `ExpenseTracker` and `FinancialAI`
- `ExpenseTracker` reads/writes `expenses.json` via a simple JSON helper
- `FinancialAI` looks up answers in `financial_concepts.py` (pure in-memory)
- All validation is done through `validators.py` before data reaches the core classes
- Custom exceptions from `exceptions.py` are caught in `app.py` and shown as friendly Streamlit error messages

---

## Sub-Tasks

---

### Sub-Task 1 — Project Scaffold and Custom Exceptions

**Intent:**
Set up the folder structure and define all custom exception classes. Getting the scaffold right first means every subsequent sub-task has a clean, consistent place to put code.

**Expected Outcomes:**
- All folders and `__init__.py` files exist
- `exceptions.py` defines all six custom exception classes
- The project runs `python app.py` without import errors (app.py can be an empty stub)

**Todo List:**
1. Create the folder structure: `models/`, `core/`, `data/`, `utils/`, `tests/`
2. Add empty `__init__.py` to each package folder
3. Create `utils/exceptions.py` with the following exception classes:
   - `InvalidIncomeError` — raised when income is zero, negative, or non-numeric
   - `InvalidExpenseError` — raised when expense amount is zero, negative, or non-numeric
   - `InvalidDateError` — raised when expense date is in the future
   - `InvalidGoalError` — raised when savings goal is zero or negative
   - `ExpenseNotFoundError` — raised when trying to remove an expense ID that does not exist
   - `EmptyQuestionError` — raised when the AI is asked an empty or whitespace-only question
4. Create a minimal stub `app.py` that imports Streamlit and prints a title

**Relevant Context:** No existing code. All exceptions inherit from Python's built-in `Exception`.

**Status:** [ ] pending

---

### Sub-Task 2 — Expense Data Model

**Intent:**
Define the `Expense` dataclass — the core data structure that every other module depends on. Keeping it as a simple dataclass makes it easy to serialise to/from JSON.

**Expected Outcomes:**
- `models/expense.py` defines a clean `Expense` dataclass with type hints
- The class has a method to convert to a plain dict (for JSON saving) and a class method to create an instance from a dict (for JSON loading)
- A UUID is auto-generated for `expense_id` if not supplied

**Todo List:**
1. Create `models/expense.py`
2. Define the `Expense` dataclass with these fields:
   - `expense_id: str` — UUID string, auto-generated
   - `amount: float` — positive expense amount
   - `category: str` — one of the six fixed categories
   - `description: str` — optional short note, default empty string
   - `date: str` — stored as ISO date string `YYYY-MM-DD`
3. Add a `VALID_CATEGORIES` constant list: `["Food", "Travel", "Shopping", "Education", "Entertainment", "Other"]`
4. Add a `to_dict()` method that returns a plain Python dict
5. Add a `from_dict(data: dict)` class method that reconstructs an `Expense` from a dict

**Relevant Context:** Used by `ExpenseTracker`, JSON persistence layer, and Streamlit UI display.

**Status:** [ ] pending

---

### Sub-Task 3 — Input Validators

**Intent:**
Centralise all input validation in one place so that the core classes stay clean and the UI can call the same rules. Validators raise the custom exceptions from Sub-Task 1.

**Expected Outcomes:**
- `utils/validators.py` contains standalone validation functions with type hints
- Each function either returns the cleaned/parsed value or raises the appropriate custom exception
- No Streamlit-specific code inside validators — they are pure Python

**Todo List:**
1. Create `utils/validators.py`
2. Implement `validate_income(value) -> float`:
   - Rejects non-numeric, zero, and negative values — raises `InvalidIncomeError`
   - Returns the float value if valid
3. Implement `validate_expense_amount(value) -> float`:
   - Rejects non-numeric, zero, and negative values — raises `InvalidExpenseError`
   - Returns the float value if valid
4. Implement `validate_date(date_str: str) -> str`:
   - Rejects future dates — raises `InvalidDateError`
   - Returns the ISO date string if valid
5. Implement `validate_savings_goal(value) -> float`:
   - Rejects non-numeric, zero, and negative values — raises `InvalidGoalError`
   - Returns the float value if valid
6. Implement `validate_description(text: str) -> str`:
   - Truncates to 100 characters and strips whitespace
   - Always returns a string (never raises — description is optional)
7. Implement `validate_question(text: str) -> str`:
   - Raises `EmptyQuestionError` if blank after stripping
   - Returns the stripped string if valid

**Relevant Context:** Called by `ExpenseTracker` methods and the Streamlit UI before submitting data to the tracker.

**Status:** [ ] pending

---

### Sub-Task 4 — Expense Tracker Core Logic

**Intent:**
Build the central `ExpenseTracker` class that holds all financial state (income, expenses, savings goal) and exposes clean methods for every calculation the UI needs.

**Expected Outcomes:**
- `core/expense_tracker.py` contains the `ExpenseTracker` class
- All financial calculations are correct and covered by unit tests
- The class loads from and saves to `data/expenses.json` automatically
- No Streamlit imports — pure Python business logic

**Todo List:**
1. Create `core/expense_tracker.py`
2. Define the `ExpenseTracker` class with these instance attributes:
   - `monthly_income: float` — default 0.0
   - `expenses: list[Expense]` — default empty list
   - `savings_goal: float` — default 0.0
   - `_data_file: str` — path to `data/expenses.json`
3. Implement `_load()` — reads JSON file on startup; if file does not exist, starts with defaults
4. Implement `_save()` — writes current state to JSON file after every mutation
5. Implement `set_income(amount: float)` — validates and sets income, then saves
6. Implement `add_expense(amount, category, description, date) -> Expense` — creates an `Expense`, appends to list, saves
7. Implement `remove_expense(expense_id: str)` — finds and removes by ID; raises `ExpenseNotFoundError` if not found
8. Implement `get_all_expenses() -> list[Expense]` — returns the full list
9. Implement `clear_all_expenses()` — empties the expense list and saves
10. Implement `calculate_total_spending() -> float` — sums all expense amounts
11. Implement `calculate_remaining_money() -> float` — income minus total spending (can be negative)
12. Implement `calculate_savings() -> float` — remaining money if positive, else 0.0
13. Implement `calculate_savings_percentage() -> float` — savings divided by income times 100; returns 0.0 if income is 0
14. Implement `get_category_breakdown() -> dict[str, float]` — returns a dict of category to total amount spent
15. Implement `set_savings_goal(amount: float)` — validates and sets goal, then saves
16. Implement `get_goal_progress() -> dict` — returns a dict with keys: `saved`, `goal`, `percentage`, `reached` (bool)
17. Implement `is_overspending() -> bool` — returns True if total spending exceeds income

**Relevant Context:** Uses `Expense` from `models/expense.py` and validators from `utils/validators.py`. Data persisted in `data/expenses.json`.

**Status:** [ ] pending

---

### Sub-Task 5 — Financial Concepts Knowledge Base

**Intent:**
Create the static knowledge base that powers the AI assistant. This is just a Python file containing dictionaries and lists — no external service, no API key, no network call.

**Expected Outcomes:**
- `data/financial_concepts.py` defines all static knowledge used by the AI
- Concepts are written in plain, beginner-friendly English
- The structure is easy to extend later

**Todo List:**
1. Create `data/financial_concepts.py`
2. Define `CONCEPT_DEFINITIONS: dict[str, str]` — maps keyword/topic to a plain-English explanation. Include at minimum:
   - `"budgeting"` — what a budget is and why it matters
   - `"saving"` — why saving money is important and how to start
   - `"needs vs wants"` — the difference between essential and non-essential spending
   - `"emergency fund"` — what it is, why to have one, how much to save
   - `"interest"` — simple explanation of how interest works (bank savings and debt)
   - `"responsible spending"` — making thoughtful spending decisions
   - `"50/30/20 rule"` — the popular budgeting guideline
   - `"expense tracking"` — why tracking spending matters
3. Define `GENERAL_TIPS: list[str]` — a list of at least 10 short, practical budgeting and saving tips
4. Define `CATEGORY_TIPS: dict[str, list[str]]` — maps each of the six expense categories to a list of 2-3 relevant saving tips

**Relevant Context:** Consumed exclusively by `FinancialAI` in Sub-Task 6. No imports needed — plain data.

**Status:** [ ] pending

---

### Sub-Task 6 — Financial AI Assistant

**Intent:**
Build the keyword-matching AI assistant that answers financial questions and returns tips. It uses only the static knowledge base — no external AI, no API key required.

**Expected Outcomes:**
- `core/financial_ai.py` contains the `FinancialAI` class
- `answer_question()` always returns a helpful string (never crashes or returns empty)
- Unrecognised questions return a polite fallback listing known topics
- Tips can be retrieved randomly or by category

**Todo List:**
1. Create `core/financial_ai.py`
2. Define the `FinancialAI` class with no required constructor arguments
3. Implement `answer_question(question: str) -> str`:
   - Strip and lowercase the question; raise `EmptyQuestionError` if blank
   - Search for keywords from `CONCEPT_DEFINITIONS` in the question text
   - Return the matching concept explanation if a keyword is found
   - If no keyword matches, return a friendly fallback message listing available topics
4. Implement `get_random_tip() -> str`:
   - Returns one randomly chosen tip from `GENERAL_TIPS`
5. Implement `get_tips_for_category(category: str) -> list[str]`:
   - Returns the tip list for the given category from `CATEGORY_TIPS`
   - Returns the general tips list if the category is not found
6. Implement `get_all_topics() -> list[str]`:
   - Returns the sorted list of all topic keywords from `CONCEPT_DEFINITIONS`
   - Used by the fallback message and the UI topic browser

**Relevant Context:** Uses `CONCEPT_DEFINITIONS`, `GENERAL_TIPS`, and `CATEGORY_TIPS` from `data/financial_concepts.py`. Validators `validate_question()` should be called before passing input here.

**Status:** [ ] pending

---

### Sub-Task 7 — Streamlit UI

**Intent:**
Build the complete Streamlit UI in `app.py`. The UI is organised into clearly labelled sections (not multi-page). It wires together the tracker and AI assistant, handles all exceptions gracefully, and shows friendly messages instead of raw errors.

**Expected Outcomes:**
- `app.py` is a fully working Streamlit app
- All six user-facing sections are present and functional
- Errors from validation or business logic are shown as `st.error()` messages
- Success events use `st.success()` messages
- Warnings (overspending, goal not reached) use `st.warning()`
- No business logic lives in `app.py` — it only calls methods on the core classes

**Todo List:**

1. Create `app.py` and initialise a single `ExpenseTracker` and `FinancialAI` instance using `st.session_state` so they persist across reruns

2. **Section 1 — Income Setup**
   - Number input for monthly income or allowance
   - "Set Income" button that calls `tracker.set_income()`
   - Display current income below the input

3. **Section 2 — Add Expense**
   - Number input for expense amount
   - Selectbox for category (uses `VALID_CATEGORIES`)
   - Text input for description
   - Date input for expense date
   - "Add Expense" button that calls `tracker.add_expense()`
   - Show success or error message

4. **Section 3 — Expense Summary**
   - Display total spending, remaining money, savings amount, and savings percentage as `st.metric()` widgets
   - If `is_overspending()` is True, show a red `st.warning()` banner
   - Show a `st.dataframe()` table of all expenses with a delete button per row

5. **Section 4 — Category Breakdown**
   - Display `get_category_breakdown()` as a `st.bar_chart()` or `st.table()`
   - Show category-wise tips from `get_tips_for_category()`

6. **Section 5 — Savings Goal**
   - Number input for savings goal amount
   - "Set Goal" button that calls `tracker.set_savings_goal()`
   - Show a `st.progress()` bar for goal progress
   - Show "Goal reached!" if `get_goal_progress()["reached"]` is True

7. **Section 6 — Financial Literacy Assistant**
   - Text input for the user's question
   - "Ask" button that calls `ai.answer_question()`
   - Display the answer in a styled text box
   - "Give me a tip" button that calls `ai.get_random_tip()`
   - Expandable section listing all available topics the user can ask about

**Relevant Context:**
- Uses `ExpenseTracker` from `core/expense_tracker.py`
- Uses `FinancialAI` from `core/financial_ai.py`
- Uses `VALID_CATEGORIES` from `models/expense.py`
- All custom exceptions from `utils/exceptions.py` are caught here and shown via `st.error()`

**Status:** [ ] pending

---

### Sub-Task 8 — Unit Tests

**Intent:**
Write pytest unit tests for all three testable modules: validators, expense tracker, and financial AI. Tests confirm that correct inputs produce correct outputs and that invalid inputs raise the right exceptions.

**Expected Outcomes:**
- `tests/test_validators.py` tests all six validation functions
- `tests/test_expense_tracker.py` tests all calculations and mutation methods
- `tests/test_financial_ai.py` tests question answering and tip retrieval
- All tests pass with `pytest tests/`
- No Streamlit or file I/O dependencies in tests (use a temp file or mock `_save`/`_load`)

**Todo List:**
1. Create `tests/__init__.py`

2. Write `tests/test_validators.py`:
   - Test valid income, expense, date, goal, description, question inputs return correct values
   - Test each invalid case raises the correct custom exception

3. Write `tests/test_expense_tracker.py`:
   - Use a temporary JSON file (via `tmp_path` pytest fixture) so tests do not touch real data
   - Test `set_income`, `add_expense`, `remove_expense`, `clear_all_expenses`
   - Test `calculate_total_spending`, `calculate_remaining_money`, `calculate_savings`, `calculate_savings_percentage`
   - Test `get_category_breakdown` with multiple categories
   - Test `set_savings_goal` and `get_goal_progress`
   - Test `is_overspending` returns True when total expenses exceed income
   - Test `remove_expense` raises `ExpenseNotFoundError` for an unknown ID
   - Test edge case: zero expenses gives zero totals
   - Test edge case: income of 0 gives savings percentage of 0 without crashing

4. Write `tests/test_financial_ai.py`:
   - Test `answer_question` returns a non-empty string for known topics
   - Test `answer_question` returns the fallback message for unrecognised input
   - Test `answer_question` raises `EmptyQuestionError` for blank input
   - Test `get_random_tip` returns a non-empty string
   - Test `get_tips_for_category` returns a list for valid and invalid categories
   - Test `get_all_topics` returns a sorted list

**Relevant Context:** Tests must be independent. Use `tmp_path` for any file I/O. Do not test Streamlit UI directly.

**Status:** [ ] pending

---

## Data Storage Approach

- **Format:** JSON (human-readable, no setup required, built into Python)
- **File:** `data/expenses.json`
- **Structure:**
  ```
  {
    "monthly_income": 1500.0,
    "savings_goal": 300.0,
    "expenses": [
      {
        "expense_id": "uuid-string",
        "amount": 50.0,
        "category": "Food",
        "description": "Lunch",
        "date": "2025-01-15"
      }
    ]
  }
  ```
- **When saved:** After every mutation (set income, add/remove expense, set goal, clear all)
- **When loaded:** Once on `ExpenseTracker` initialisation
- **Missing file:** If `expenses.json` does not exist, start with empty defaults and create the file on first save

---

## Financial Calculations Reference

| Calculation | Formula |
|---|---|
| Total Spending | Sum of all expense amounts |
| Remaining Money | monthly_income - total_spending (can be negative) |
| Savings Amount | max(0, remaining_money) |
| Savings Percentage | (savings_amount / monthly_income) * 100, or 0 if income is 0 |
| Goal Progress % | (savings_amount / savings_goal) * 100, capped at 100 |
| Goal Reached | savings_amount >= savings_goal |
| Is Overspending | total_spending > monthly_income |

---

## Validation Rules Reference

| Field | Rule | Exception |
|---|---|---|
| monthly_income | Must be numeric and > 0 | InvalidIncomeError |
| expense_amount | Must be numeric and > 0 | InvalidExpenseError |
| expense_date | Must not be a future date | InvalidDateError |
| savings_goal | Must be numeric and > 0 | InvalidGoalError |
| description | Optional; max 100 chars, stripped | None — always returns string |
| AI question | Must not be blank after stripping | EmptyQuestionError |

---

## Edge Cases to Handle

| Scenario | Handling |
|---|---|
| No expenses added | Show "No expenses yet" message in the summary table |
| Total spending exceeds income | Show overspending warning banner |
| Savings goal already reached | Show celebration message and full progress bar |
| Savings goal greater than income | Allow it with a note that it may be a multi-month goal |
| All expenses in one category | Category breakdown still renders with one bar |
| Unrecognised AI question | Return fallback with list of known topics |
| expenses.json missing or corrupt | Catch file/JSON errors, reset to defaults, recreate file |
| Income set to 0 | Blocked by validation — show error |
| Description over 100 chars | Silently truncated to 100 chars |

---

## Implementation Order

Complete the sub-tasks in this exact order. Each sub-task depends on the ones before it.

```
Sub-Task 1 — Scaffold and Exceptions        (foundation for everything)
Sub-Task 2 — Expense Data Model             (needed by tracker and tests)
Sub-Task 3 — Input Validators               (needed by tracker and AI)
Sub-Task 4 — Expense Tracker Core           (main business logic)
Sub-Task 5 — Knowledge Base                 (needed by AI assistant)
Sub-Task 6 — Financial AI Assistant         (depends on knowledge base)
Sub-Task 7 — Streamlit UI                   (wires everything together)
Sub-Task 8 — Unit Tests                     (validates all logic)
```
