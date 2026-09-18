"""Expense data model for the Financial Literacy application."""

from dataclasses import dataclass, field
from uuid import uuid4


# The six allowed expense categories.
VALID_CATEGORIES: list[str] = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Entertainment",
    "Other",
]


@dataclass
class Expense:
    """Represents a single expense entry.

    Attributes:
        amount:      The cost of the expense (must be > 0).
        category:    One of the VALID_CATEGORIES strings.
        description: A short optional note about the expense.
        date:        The date of the expense as an ISO string (YYYY-MM-DD).
        expense_id:  A unique identifier; auto-generated if not provided.
    """

    amount: float
    category: str
    description: str
    date: str
    expense_id: str = field(default_factory=lambda: str(uuid4()))

    def to_dict(self) -> dict:
        """Convert this Expense to a plain Python dictionary (for JSON saving)."""
        return {
            "expense_id": self.expense_id,
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Expense":
        """Reconstruct an Expense from a plain dictionary (for JSON loading)."""
        return cls(
            expense_id=data["expense_id"],
            amount=data["amount"],
            category=data["category"],
            description=data.get("description", ""),
            date=data["date"],
        )
