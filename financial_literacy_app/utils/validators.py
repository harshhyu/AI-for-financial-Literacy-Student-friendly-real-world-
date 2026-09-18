"""Input validation functions for the Financial Literacy application.

All validators either return the cleaned value or raise a custom exception.
There is no Streamlit code here — these are pure Python functions.
"""

from datetime import date

from financial_literacy_app.utils.exceptions import (
    EmptyQuestionError,
    InvalidDateError,
    InvalidExpenseError,
    InvalidGoalError,
    InvalidIncomeError,
)


def validate_income(value: float | int | str) -> float:
    """Validate and return a monthly income value.

    Args:
        value: The income value to validate (numeric).

    Returns:
        The income as a positive float.

    Raises:
        InvalidIncomeError: If the value is not numeric, zero, or negative.
    """
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise InvalidIncomeError("Income must be a number.")

    if amount <= 0:
        raise InvalidIncomeError("Income must be greater than zero.")

    return amount


def validate_expense_amount(value: float | int | str) -> float:
    """Validate and return an expense amount.

    Args:
        value: The expense amount to validate (numeric).

    Returns:
        The expense amount as a positive float.

    Raises:
        InvalidExpenseError: If the value is not numeric, zero, or negative.
    """
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise InvalidExpenseError("Expense amount must be a number.")

    if amount <= 0:
        raise InvalidExpenseError("Expense amount must be greater than zero.")

    return amount


def validate_date(date_str: str) -> str:
    """Validate and return an expense date string.

    Args:
        date_str: A date string in YYYY-MM-DD format.

    Returns:
        The same ISO date string if it is today or in the past.

    Raises:
        InvalidDateError: If the date is in the future or not a valid date.
    """
    try:
        parsed = date.fromisoformat(date_str)
    except (ValueError, TypeError):
        raise InvalidDateError(f"'{date_str}' is not a valid date (use YYYY-MM-DD).")

    if parsed > date.today():
        raise InvalidDateError("Expense date cannot be in the future.")

    return date_str


def validate_savings_goal(value: float | int | str) -> float:
    """Validate and return a savings goal amount.

    Args:
        value: The savings goal to validate (numeric).

    Returns:
        The savings goal as a positive float.

    Raises:
        InvalidGoalError: If the value is not numeric, zero, or negative.
    """
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise InvalidGoalError("Savings goal must be a number.")

    if amount <= 0:
        raise InvalidGoalError("Savings goal must be greater than zero.")

    return amount


def validate_description(text: str) -> str:
    """Clean and return an expense description.

    Strips leading/trailing whitespace and truncates to 100 characters.
    Never raises — description is optional.

    Args:
        text: The raw description string.

    Returns:
        A cleaned string of at most 100 characters.
    """
    if not isinstance(text, str):
        return ""
    return text.strip()[:100]


def validate_question(text: str) -> str:
    """Validate and return a trimmed question for the AI assistant.

    Args:
        text: The raw question string entered by the user.

    Returns:
        The stripped question string.

    Raises:
        EmptyQuestionError: If the question is blank or whitespace-only.
    """
    if not isinstance(text, str) or not text.strip():
        raise EmptyQuestionError("Please type a question before asking.")

    return text.strip()
