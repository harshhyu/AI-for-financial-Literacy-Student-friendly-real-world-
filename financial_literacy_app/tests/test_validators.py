"""Unit tests for input validators."""

import pytest
from datetime import date, timedelta

from financial_literacy_app.utils.validators import (
    validate_income,
    validate_expense_amount,
    validate_date,
    validate_savings_goal,
    validate_description,
    validate_question,
)
from financial_literacy_app.utils.exceptions import (
    InvalidIncomeError,
    InvalidExpenseError,
    InvalidDateError,
    InvalidGoalError,
    EmptyQuestionError,
)


# ---------------------------------------------------------------------------
# validate_income
# ---------------------------------------------------------------------------

class TestValidateIncome:
    def test_valid_income_returns_float(self):
        assert validate_income(1500) == 1500.0

    def test_valid_income_as_string(self):
        assert validate_income("2000.50") == 2000.50

    def test_zero_raises(self):
        with pytest.raises(InvalidIncomeError):
            validate_income(0)

    def test_negative_raises(self):
        with pytest.raises(InvalidIncomeError):
            validate_income(-100)

    def test_non_numeric_raises(self):
        with pytest.raises(InvalidIncomeError):
            validate_income("abc")

    def test_none_raises(self):
        with pytest.raises(InvalidIncomeError):
            validate_income(None)


# ---------------------------------------------------------------------------
# validate_expense_amount
# ---------------------------------------------------------------------------

class TestValidateExpenseAmount:
    def test_valid_amount_returns_float(self):
        assert validate_expense_amount(50) == 50.0

    def test_valid_amount_as_string(self):
        assert validate_expense_amount("12.99") == 12.99

    def test_zero_raises(self):
        with pytest.raises(InvalidExpenseError):
            validate_expense_amount(0)

    def test_negative_raises(self):
        with pytest.raises(InvalidExpenseError):
            validate_expense_amount(-5)

    def test_non_numeric_raises(self):
        with pytest.raises(InvalidExpenseError):
            validate_expense_amount("free")

    def test_none_raises(self):
        with pytest.raises(InvalidExpenseError):
            validate_expense_amount(None)


# ---------------------------------------------------------------------------
# validate_date
# ---------------------------------------------------------------------------

class TestValidateDate:
    def test_today_is_valid(self):
        today = str(date.today())
        assert validate_date(today) == today

    def test_past_date_is_valid(self):
        past = str(date.today() - timedelta(days=30))
        assert validate_date(past) == past

    def test_future_date_raises(self):
        future = str(date.today() + timedelta(days=1))
        with pytest.raises(InvalidDateError):
            validate_date(future)

    def test_invalid_string_raises(self):
        with pytest.raises(InvalidDateError):
            validate_date("not-a-date")

    def test_none_raises(self):
        with pytest.raises(InvalidDateError):
            validate_date(None)


# ---------------------------------------------------------------------------
# validate_savings_goal
# ---------------------------------------------------------------------------

class TestValidateSavingsGoal:
    def test_valid_goal_returns_float(self):
        assert validate_savings_goal(500) == 500.0

    def test_valid_goal_as_string(self):
        assert validate_savings_goal("250.0") == 250.0

    def test_zero_raises(self):
        with pytest.raises(InvalidGoalError):
            validate_savings_goal(0)

    def test_negative_raises(self):
        with pytest.raises(InvalidGoalError):
            validate_savings_goal(-50)

    def test_non_numeric_raises(self):
        with pytest.raises(InvalidGoalError):
            validate_savings_goal("lots")


# ---------------------------------------------------------------------------
# validate_description
# ---------------------------------------------------------------------------

class TestValidateDescription:
    def test_normal_description_returned(self):
        assert validate_description("Lunch at the canteen") == "Lunch at the canteen"

    def test_strips_whitespace(self):
        assert validate_description("  coffee  ") == "coffee"

    def test_truncates_to_100_chars(self):
        long_text = "x" * 150
        result = validate_description(long_text)
        assert len(result) == 100

    def test_empty_string_returns_empty(self):
        assert validate_description("") == ""

    def test_none_returns_empty_string(self):
        assert validate_description(None) == ""


# ---------------------------------------------------------------------------
# validate_question
# ---------------------------------------------------------------------------

class TestValidateQuestion:
    def test_valid_question_returned_stripped(self):
        assert validate_question("  What is budgeting?  ") == "What is budgeting?"

    def test_empty_string_raises(self):
        with pytest.raises(EmptyQuestionError):
            validate_question("")

    def test_whitespace_only_raises(self):
        with pytest.raises(EmptyQuestionError):
            validate_question("   ")

    def test_none_raises(self):
        with pytest.raises(EmptyQuestionError):
            validate_question(None)
