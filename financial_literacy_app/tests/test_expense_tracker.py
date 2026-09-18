"""Unit tests for the ExpenseTracker class."""

import json
import os
import pytest
from datetime import date, timedelta

from financial_literacy_app.core.expense_tracker import ExpenseTracker
from financial_literacy_app.utils.exceptions import (
    ExpenseNotFoundError,
    InvalidIncomeError,
    InvalidGoalError,
)


@pytest.fixture
def tracker(tmp_path):
    """Return a fresh ExpenseTracker using a temporary JSON file."""
    data_file = str(tmp_path / "test_expenses.json")
    return ExpenseTracker(data_file=data_file)


def today() -> str:
    return str(date.today())


def yesterday() -> str:
    return str(date.today() - timedelta(days=1))


# ---------------------------------------------------------------------------
# Income
# ---------------------------------------------------------------------------

class TestSetIncome:
    def test_set_valid_income(self, tracker):
        tracker.set_income(1500.0)
        assert tracker.monthly_income == 1500.0

    def test_income_persists_to_json(self, tmp_path):
        data_file = str(tmp_path / "persist.json")
        t1 = ExpenseTracker(data_file=data_file)
        t1.set_income(2000.0)
        # Create a second tracker pointing to the same file.
        t2 = ExpenseTracker(data_file=data_file)
        assert t2.monthly_income == 2000.0

    def test_zero_income_raises(self, tracker):
        with pytest.raises(InvalidIncomeError):
            tracker.set_income(0)

    def test_negative_income_raises(self, tracker):
        with pytest.raises(InvalidIncomeError):
            tracker.set_income(-100)


# ---------------------------------------------------------------------------
# Add expense
# ---------------------------------------------------------------------------

class TestAddExpense:
    def test_add_single_expense(self, tracker):
        expense = tracker.add_expense(50.0, "Food", "Lunch", today())
        assert expense.amount == 50.0
        assert expense.category == "Food"
        assert len(tracker.get_all_expenses()) == 1

    def test_add_multiple_expenses(self, tracker):
        tracker.add_expense(10.0, "Food", "Snack", today())
        tracker.add_expense(20.0, "Travel", "Bus", yesterday())
        assert len(tracker.get_all_expenses()) == 2

    def test_expense_gets_unique_id(self, tracker):
        e1 = tracker.add_expense(10.0, "Food", "", today())
        e2 = tracker.add_expense(10.0, "Food", "", today())
        assert e1.expense_id != e2.expense_id

    def test_future_date_raises(self, tracker):
        from financial_literacy_app.utils.exceptions import InvalidDateError
        future = str(date.today() + timedelta(days=1))
        with pytest.raises(InvalidDateError):
            tracker.add_expense(10.0, "Food", "", future)

    def test_zero_amount_raises(self, tracker):
        from financial_literacy_app.utils.exceptions import InvalidExpenseError
        with pytest.raises(InvalidExpenseError):
            tracker.add_expense(0.0, "Food", "", today())


# ---------------------------------------------------------------------------
# Remove expense
# ---------------------------------------------------------------------------

class TestRemoveExpense:
    def test_remove_existing_expense(self, tracker):
        expense = tracker.add_expense(30.0, "Shopping", "T-shirt", today())
        tracker.remove_expense(expense.expense_id)
        assert len(tracker.get_all_expenses()) == 0

    def test_remove_nonexistent_id_raises(self, tracker):
        with pytest.raises(ExpenseNotFoundError):
            tracker.remove_expense("nonexistent-id-000")

    def test_clear_all_expenses(self, tracker):
        tracker.add_expense(10.0, "Food", "", today())
        tracker.add_expense(20.0, "Travel", "", today())
        tracker.clear_all_expenses()
        assert tracker.get_all_expenses() == []


# ---------------------------------------------------------------------------
# Calculations
# ---------------------------------------------------------------------------

class TestCalculations:
    def test_total_spending_zero_with_no_expenses(self, tracker):
        assert tracker.calculate_total_spending() == 0.0

    def test_total_spending_sum(self, tracker):
        tracker.add_expense(100.0, "Food", "", today())
        tracker.add_expense(50.0, "Travel", "", today())
        assert tracker.calculate_total_spending() == 150.0

    def test_remaining_money(self, tracker):
        tracker.set_income(500.0)
        tracker.add_expense(200.0, "Food", "", today())
        assert tracker.calculate_remaining_money() == 300.0

    def test_remaining_money_negative_when_overspending(self, tracker):
        tracker.set_income(100.0)
        tracker.add_expense(150.0, "Shopping", "", today())
        assert tracker.calculate_remaining_money() == -50.0

    def test_savings_is_zero_when_overspending(self, tracker):
        tracker.set_income(100.0)
        tracker.add_expense(200.0, "Shopping", "", today())
        assert tracker.calculate_savings() == 0.0

    def test_savings_positive_when_under_budget(self, tracker):
        tracker.set_income(500.0)
        tracker.add_expense(300.0, "Food", "", today())
        assert tracker.calculate_savings() == 200.0

    def test_savings_percentage(self, tracker):
        tracker.set_income(1000.0)
        tracker.add_expense(800.0, "Food", "", today())
        assert tracker.calculate_savings_percentage() == pytest.approx(20.0)

    def test_savings_percentage_zero_when_no_income(self, tracker):
        # Income defaults to 0 — should return 0, not crash.
        assert tracker.calculate_savings_percentage() == 0.0

    def test_savings_percentage_zero_when_fully_spent(self, tracker):
        tracker.set_income(500.0)
        tracker.add_expense(500.0, "Food", "", today())
        assert tracker.calculate_savings_percentage() == 0.0


# ---------------------------------------------------------------------------
# Category breakdown
# ---------------------------------------------------------------------------

class TestCategoryBreakdown:
    def test_single_category(self, tracker):
        tracker.add_expense(50.0, "Food", "", today())
        tracker.add_expense(30.0, "Food", "", today())
        breakdown = tracker.get_category_breakdown()
        assert breakdown == {"Food": 80.0}

    def test_multiple_categories(self, tracker):
        tracker.add_expense(50.0, "Food", "", today())
        tracker.add_expense(20.0, "Travel", "", today())
        tracker.add_expense(30.0, "Food", "", today())
        breakdown = tracker.get_category_breakdown()
        assert breakdown["Food"] == pytest.approx(80.0)
        assert breakdown["Travel"] == pytest.approx(20.0)

    def test_empty_breakdown_when_no_expenses(self, tracker):
        assert tracker.get_category_breakdown() == {}


# ---------------------------------------------------------------------------
# Savings goal
# ---------------------------------------------------------------------------

class TestSavingsGoal:
    def test_set_valid_goal(self, tracker):
        tracker.set_savings_goal(200.0)
        assert tracker.savings_goal == 200.0

    def test_zero_goal_raises(self, tracker):
        with pytest.raises(InvalidGoalError):
            tracker.set_savings_goal(0)

    def test_negative_goal_raises(self, tracker):
        with pytest.raises(InvalidGoalError):
            tracker.set_savings_goal(-100)

    def test_goal_progress_not_reached(self, tracker):
        tracker.set_income(500.0)
        tracker.set_savings_goal(300.0)
        tracker.add_expense(400.0, "Food", "", today())
        progress = tracker.get_goal_progress()
        assert progress["reached"] is False
        assert progress["saved"] == pytest.approx(100.0)

    def test_goal_progress_reached(self, tracker):
        tracker.set_income(500.0)
        tracker.set_savings_goal(100.0)
        tracker.add_expense(200.0, "Food", "", today())
        progress = tracker.get_goal_progress()
        assert progress["reached"] is True
        assert progress["percentage"] == pytest.approx(100.0)

    def test_goal_progress_percentage_capped_at_100(self, tracker):
        tracker.set_income(1000.0)
        tracker.set_savings_goal(100.0)
        # Saved 1000 toward a 100 goal — capped at 100%.
        progress = tracker.get_goal_progress()
        assert progress["percentage"] == 100.0

    def test_goal_progress_zero_when_no_goal_set(self, tracker):
        progress = tracker.get_goal_progress()
        assert progress["percentage"] == 0.0
        assert progress["reached"] is False


# ---------------------------------------------------------------------------
# Overspending
# ---------------------------------------------------------------------------

class TestIsOverspending:
    def test_not_overspending(self, tracker):
        tracker.set_income(500.0)
        tracker.add_expense(300.0, "Food", "", today())
        assert tracker.is_overspending() is False

    def test_is_overspending(self, tracker):
        tracker.set_income(100.0)
        tracker.add_expense(150.0, "Shopping", "", today())
        assert tracker.is_overspending() is True

    def test_not_overspending_when_exact(self, tracker):
        tracker.set_income(200.0)
        tracker.add_expense(200.0, "Food", "", today())
        assert tracker.is_overspending() is False
