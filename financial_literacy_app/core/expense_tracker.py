"""Core expense tracking and financial calculations.

This module contains the ExpenseTracker class which manages:
- Monthly income
- Expense records
- Savings goal
- All financial calculations
- JSON persistence
"""

import json
import os
from datetime import date

from financial_literacy_app.models.expense import Expense
from financial_literacy_app.utils.exceptions import ExpenseNotFoundError
from financial_literacy_app.utils.validators import (
    validate_date,
    validate_description,
    validate_expense_amount,
    validate_income,
    validate_savings_goal,
)

# Default path for the JSON data file.
_DEFAULT_DATA_FILE = os.path.join(
    os.path.dirname(__file__), "..", "data", "expenses.json"
)


class ExpenseTracker:
    """Manages income, expenses, and savings for a single user.

    All state is automatically saved to a JSON file after every change,
    so data survives page refreshes and browser restarts.

    Attributes:
        monthly_income: The user's monthly income or allowance.
        expenses:       The list of recorded Expense objects.
        savings_goal:   The user's target savings amount.
    """

    def __init__(self, data_file: str = _DEFAULT_DATA_FILE) -> None:
        self.monthly_income: float = 0.0
        self.expenses: list[Expense] = []
        self.savings_goal: float = 0.0
        self._data_file: str = os.path.normpath(data_file)
        self._load()

    # ------------------------------------------------------------------
    # Persistence helpers
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Load state from the JSON file. Resets to defaults on any error."""
        try:
            with open(self._data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.monthly_income = float(data.get("monthly_income", 0.0))
            self.savings_goal = float(data.get("savings_goal", 0.0))
            self.expenses = [
                Expense.from_dict(e) for e in data.get("expenses", [])
            ]
        except (FileNotFoundError, json.JSONDecodeError, KeyError, ValueError):
            # If the file is missing or corrupt, start fresh.
            self.monthly_income = 0.0
            self.savings_goal = 0.0
            self.expenses = []

    def _save(self) -> None:
        """Save current state to the JSON file."""
        # Ensure the directory exists (important for first run).
        os.makedirs(os.path.dirname(self._data_file), exist_ok=True)
        data = {
            "monthly_income": self.monthly_income,
            "savings_goal": self.savings_goal,
            "expenses": [e.to_dict() for e in self.expenses],
        }
        with open(self._data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    # ------------------------------------------------------------------
    # Income
    # ------------------------------------------------------------------

    def set_income(self, amount: float) -> None:
        """Set the monthly income after validating the value.

        Args:
            amount: The monthly income or allowance.

        Raises:
            InvalidIncomeError: If amount is not a positive number.
        """
        self.monthly_income = validate_income(amount)
        self._save()

    # ------------------------------------------------------------------
    # Expenses
    # ------------------------------------------------------------------

    def add_expense(
        self,
        amount: float,
        category: str,
        description: str,
        date_str: str,
    ) -> Expense:
        """Create, store, and return a new Expense.

        Args:
            amount:      The expense cost (must be > 0).
            category:    One of the VALID_CATEGORIES.
            description: Short optional note (truncated to 100 chars).
            date_str:    Date in YYYY-MM-DD format (must not be future).

        Returns:
            The newly created Expense object.

        Raises:
            InvalidExpenseError: If amount is invalid.
            InvalidDateError:    If the date is in the future.
        """
        validated_amount = validate_expense_amount(amount)
        validated_date = validate_date(date_str)
        cleaned_description = validate_description(description)

        expense = Expense(
            amount=validated_amount,
            category=category,
            description=cleaned_description,
            date=validated_date,
        )
        self.expenses.append(expense)
        self._save()
        return expense

    def remove_expense(self, expense_id: str) -> None:
        """Remove an expense by its unique ID.

        Args:
            expense_id: The UUID string of the expense to remove.

        Raises:
            ExpenseNotFoundError: If no expense with that ID exists.
        """
        for expense in self.expenses:
            if expense.expense_id == expense_id:
                self.expenses.remove(expense)
                self._save()
                return
        raise ExpenseNotFoundError(
            f"No expense found with ID '{expense_id}'."
        )

    def get_all_expenses(self) -> list[Expense]:
        """Return a copy of all recorded expenses."""
        return list(self.expenses)

    def clear_all_expenses(self) -> None:
        """Remove every expense from the tracker."""
        self.expenses = []
        self._save()

    # ------------------------------------------------------------------
    # Financial calculations
    # ------------------------------------------------------------------

    def calculate_total_spending(self) -> float:
        """Return the sum of all expense amounts."""
        return sum(e.amount for e in self.expenses)

    def calculate_remaining_money(self) -> float:
        """Return income minus total spending (can be negative)."""
        return self.monthly_income - self.calculate_total_spending()

    def calculate_savings(self) -> float:
        """Return actual savings — remaining money if positive, else 0."""
        return max(0.0, self.calculate_remaining_money())

    def calculate_savings_percentage(self) -> float:
        """Return savings as a percentage of income.

        Returns 0.0 if income has not been set (avoids divide-by-zero).
        """
        if self.monthly_income <= 0:
            return 0.0
        return (self.calculate_savings() / self.monthly_income) * 100

    def get_category_breakdown(self) -> dict[str, float]:
        """Return total spending grouped by category.

        Returns:
            A dict mapping each category name to its total spend amount.
            Only categories with at least one expense are included.
        """
        breakdown: dict[str, float] = {}
        for expense in self.expenses:
            breakdown[expense.category] = (
                breakdown.get(expense.category, 0.0) + expense.amount
            )
        return breakdown

    # ------------------------------------------------------------------
    # Savings goal
    # ------------------------------------------------------------------

    def set_savings_goal(self, amount: float) -> None:
        """Set the savings goal after validating the value.

        Args:
            amount: The target savings amount (must be > 0).

        Raises:
            InvalidGoalError: If amount is not a positive number.
        """
        self.savings_goal = validate_savings_goal(amount)
        self._save()

    def get_goal_progress(self) -> dict:
        """Return a summary of progress toward the savings goal.

        Returns:
            A dict with:
            - saved (float):      How much has been saved so far.
            - goal (float):       The savings target.
            - percentage (float): Progress as a percentage (0–100, capped).
            - reached (bool):     True if the goal has been met.
        """
        saved = self.calculate_savings()
        goal = self.savings_goal
        if goal > 0:
            percentage = min((saved / goal) * 100, 100.0)
        else:
            percentage = 0.0
        return {
            "saved": saved,
            "goal": goal,
            "percentage": percentage,
            "reached": saved >= goal > 0,
        }

    # ------------------------------------------------------------------
    # Status helpers
    # ------------------------------------------------------------------

    def is_overspending(self) -> bool:
        """Return True if total spending exceeds monthly income."""
        return self.calculate_total_spending() > self.monthly_income
