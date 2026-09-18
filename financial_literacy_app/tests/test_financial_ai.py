"""Unit tests for the FinancialAI assistant."""

import pytest

from financial_literacy_app.core.financial_ai import FinancialAI
from financial_literacy_app.utils.exceptions import EmptyQuestionError


@pytest.fixture
def ai():
    """Return a fresh FinancialAI instance."""
    return FinancialAI()


# ---------------------------------------------------------------------------
# answer_question — known topics
# ---------------------------------------------------------------------------

class TestAnswerQuestionKnownTopics:
    def test_budgeting_question(self, ai):
        answer = ai.answer_question("What is budgeting?")
        assert "budget" in answer.lower()
        assert len(answer) > 0

    def test_saving_question(self, ai):
        answer = ai.answer_question("How do I start saving money?")
        assert len(answer) > 0

    def test_needs_vs_wants(self, ai):
        answer = ai.answer_question("What is the difference between needs and wants?")
        assert len(answer) > 0

    def test_emergency_fund(self, ai):
        answer = ai.answer_question("Tell me about emergency funds")
        assert len(answer) > 0

    def test_interest(self, ai):
        answer = ai.answer_question("How does interest work?")
        assert len(answer) > 0

    def test_responsible_spending(self, ai):
        answer = ai.answer_question("What is responsible spending?")
        assert len(answer) > 0

    def test_50_30_20_rule(self, ai):
        answer = ai.answer_question("Explain the 50/30/20 rule")
        assert len(answer) > 0

    def test_debt_question(self, ai):
        answer = ai.answer_question("What should I know about debt?")
        assert len(answer) > 0

    def test_alias_save_matches_saving(self, ai):
        answer = ai.answer_question("How do I save more?")
        assert len(answer) > 0

    def test_alias_budget_matches_budgeting(self, ai):
        answer = ai.answer_question("Help me make a budget plan")
        assert len(answer) > 0


# ---------------------------------------------------------------------------
# answer_question — fallback for unknown topics
# ---------------------------------------------------------------------------

class TestAnswerQuestionFallback:
    def test_unknown_question_returns_fallback(self, ai):
        answer = ai.answer_question("What is the meaning of life?")
        # Fallback should mention available topics.
        assert "topics" in answer.lower() or "not sure" in answer.lower()

    def test_fallback_is_non_empty(self, ai):
        answer = ai.answer_question("xyzzy random nonsense")
        assert len(answer) > 0

    def test_fallback_is_not_none(self, ai):
        answer = ai.answer_question("Tell me something random")
        assert answer is not None


# ---------------------------------------------------------------------------
# answer_question — empty input
# ---------------------------------------------------------------------------

class TestAnswerQuestionEmptyInput:
    def test_empty_string_raises(self, ai):
        with pytest.raises(EmptyQuestionError):
            ai.answer_question("")

    def test_whitespace_only_raises(self, ai):
        with pytest.raises(EmptyQuestionError):
            ai.answer_question("    ")

    def test_none_raises(self, ai):
        with pytest.raises(EmptyQuestionError):
            ai.answer_question(None)


# ---------------------------------------------------------------------------
# get_random_tip
# ---------------------------------------------------------------------------

class TestGetRandomTip:
    def test_returns_non_empty_string(self, ai):
        tip = ai.get_random_tip()
        assert isinstance(tip, str)
        assert len(tip) > 0

    def test_returns_different_tips_over_time(self, ai):
        # With 14 tips, running 50 times should produce at least 2 distinct values.
        tips = {ai.get_random_tip() for _ in range(50)}
        assert len(tips) > 1


# ---------------------------------------------------------------------------
# get_tips_for_category
# ---------------------------------------------------------------------------

class TestGetTipsForCategory:
    def test_returns_list_for_valid_category(self, ai):
        tips = ai.get_tips_for_category("Food")
        assert isinstance(tips, list)
        assert len(tips) > 0

    def test_returns_list_for_travel(self, ai):
        tips = ai.get_tips_for_category("Travel")
        assert isinstance(tips, list)
        assert len(tips) > 0

    def test_returns_list_for_unknown_category(self, ai):
        tips = ai.get_tips_for_category("Unknown Category")
        assert isinstance(tips, list)
        assert len(tips) > 0

    @pytest.mark.parametrize("category", ["Food", "Travel", "Shopping", "Education", "Entertainment", "Other"])
    def test_all_valid_categories_return_tips(self, ai, category):
        tips = ai.get_tips_for_category(category)
        assert len(tips) > 0


# ---------------------------------------------------------------------------
# get_all_topics
# ---------------------------------------------------------------------------

class TestGetAllTopics:
    def test_returns_sorted_list(self, ai):
        topics = ai.get_all_topics()
        assert topics == sorted(topics)

    def test_returns_non_empty_list(self, ai):
        topics = ai.get_all_topics()
        assert len(topics) > 0

    def test_includes_key_topics(self, ai):
        topics = ai.get_all_topics()
        assert "budgeting" in topics
        assert "saving" in topics
        assert "debt" in topics
