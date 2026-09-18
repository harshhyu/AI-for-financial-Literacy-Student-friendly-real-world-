"""Custom exceptions for the Financial Literacy application."""


class InvalidIncomeError(Exception):
    """Raised when income is zero, negative, or non-numeric."""
    pass


class InvalidExpenseError(Exception):
    """Raised when an expense amount is zero, negative, or non-numeric."""
    pass


class InvalidDateError(Exception):
    """Raised when an expense date is in the future or not a valid date."""
    pass


class InvalidGoalError(Exception):
    """Raised when a savings goal is zero or negative."""
    pass


class ExpenseNotFoundError(Exception):
    """Raised when trying to remove an expense ID that does not exist."""
    pass


class EmptyQuestionError(Exception):
    """Raised when the AI assistant is asked an empty or whitespace-only question."""
    pass
