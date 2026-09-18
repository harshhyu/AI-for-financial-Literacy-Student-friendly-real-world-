"""Financial literacy AI assistant.

Uses keyword matching against a static knowledge base to answer common
beginner financial questions. No external APIs or AI services required.

This assistant provides EDUCATIONAL information only.
It does not give personalised financial advice or investment recommendations.
"""

import random

from financial_literacy_app.data.financial_concepts import (
    CATEGORY_TIPS,
    CONCEPT_DEFINITIONS,
    GENERAL_TIPS,
)
from financial_literacy_app.utils.exceptions import EmptyQuestionError
from financial_literacy_app.utils.validators import validate_question


class FinancialAI:
    """A simple rule-based financial literacy assistant.

    Matches keywords in a user's question to predefined educational
    explanations. All responses are general and educational — not
    personalised financial advice.
    """

    # Extra keyword aliases so users do not have to type the exact key.
    # Maps alternative words/phrases -> canonical key in CONCEPT_DEFINITIONS.
    _ALIASES: dict[str, str] = {
        "budget": "budgeting",
        "plan my money": "budgeting",
        "money plan": "budgeting",
        "save": "saving",
        "savings": "saving",
        "how to save": "saving",
        "need": "needs vs wants",
        "want": "needs vs wants",
        "needs": "needs vs wants",
        "wants": "needs vs wants",
        "essential": "needs vs wants",
        "emergency": "emergency fund",
        "rainy day": "emergency fund",
        "unexpected": "emergency fund",
        "interest rate": "interest",
        "loan": "interest",
        "borrow": "interest",
        "credit": "interest",
        "spend wisely": "responsible spending",
        "impulse": "responsible spending",
        "thoughtful": "responsible spending",
        "50 30 20": "50/30/20 rule",
        "503020": "50/30/20 rule",
        "50-30-20": "50/30/20 rule",
        "track": "expense tracking",
        "tracking": "expense tracking",
        "record expenses": "expense tracking",
        "where does my money go": "expense tracking",
        "debt": "debt",
        "owe": "debt",
        "credit card": "debt",
        "repay": "debt",
        "borrow money": "debt",
    }

    def answer_question(self, question: str) -> str:
        """Return an educational answer to a financial question.

        Searches for topic keywords in the question and returns the
        matching explanation. Returns a helpful fallback if nothing matches.

        Args:
            question: The user's raw question string.

        Returns:
            A plain-English educational explanation string.

        Raises:
            EmptyQuestionError: If the question is blank or whitespace-only.
        """
        clean = validate_question(question)
        lower = clean.lower()

        # 1. Check direct concept definition keys first.
        for key in CONCEPT_DEFINITIONS:
            if key in lower:
                return CONCEPT_DEFINITIONS[key]

        # 2. Check keyword aliases.
        for alias, canonical_key in self._ALIASES.items():
            if alias in lower:
                return CONCEPT_DEFINITIONS[canonical_key]

        # 3. Nothing matched — return a friendly fallback.
        topics = ", ".join(self.get_all_topics())
        return (
            "🤔 I'm not sure about that specific question, but I can help with "
            "these financial topics:\n\n"
            f"👉 {topics}\n\n"
            "Try asking something like:\n"
            "• 'What is budgeting?'\n"
            "• 'How do I save money?'\n"
            "• 'What is an emergency fund?'\n"
            "• 'Explain the 50/30/20 rule'\n\n"
            "📌 Remember: this assistant provides general educational information "
            "only — not personalised financial advice."
        )

    def get_random_tip(self) -> str:
        """Return a randomly selected general financial tip.

        Returns:
            A tip string from GENERAL_TIPS.
        """
        return random.choice(GENERAL_TIPS)

    def get_tips_for_category(self, category: str) -> list[str]:
        """Return spending tips relevant to a specific expense category.

        Args:
            category: An expense category name (e.g. 'Food', 'Travel').

        Returns:
            A list of tip strings. Falls back to GENERAL_TIPS if the
            category is not found in CATEGORY_TIPS.
        """
        return CATEGORY_TIPS.get(category, GENERAL_TIPS[:3])

    def get_all_topics(self) -> list[str]:
        """Return a sorted list of all topic keywords the assistant knows about.

        Returns:
            A sorted list of topic keyword strings.
        """
        return sorted(CONCEPT_DEFINITIONS.keys())
