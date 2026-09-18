"""AI for Financial Literacy — Streamlit Application.

This is the entry point for the app. It contains only UI code.
All business logic lives in the core/ and utils/ modules.

Run with:
    streamlit run app.py
"""

import sys
import os

# Allow running from any working directory without installing the package.
# __file__ is  .../financial_literacy_app/app.py
# We need its PARENT (.../P1) on sys.path so that
# "from financial_literacy_app.core..." resolves correctly.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from datetime import date

import streamlit as st

from financial_literacy_app.core.expense_tracker import ExpenseTracker
from financial_literacy_app.core.financial_ai import FinancialAI
from financial_literacy_app.models.expense import VALID_CATEGORIES
from financial_literacy_app.utils.exceptions import (
    EmptyQuestionError,
    ExpenseNotFoundError,
    InvalidDateError,
    InvalidExpenseError,
    InvalidGoalError,
    InvalidIncomeError,
)

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="AI for Financial Literacy",
    page_icon="💰",
    layout="centered",
)

# ---------------------------------------------------------------------------
# Session state — initialise tracker and AI once per session
# ---------------------------------------------------------------------------

if "tracker" not in st.session_state:
    st.session_state.tracker = ExpenseTracker()

if "ai" not in st.session_state:
    st.session_state.ai = FinancialAI()

if "ai_answer" not in st.session_state:
    st.session_state.ai_answer = ""

if "random_tip" not in st.session_state:
    st.session_state.random_tip = ""

tracker: ExpenseTracker = st.session_state.tracker
ai: FinancialAI = st.session_state.ai

# ---------------------------------------------------------------------------
# App header
# ---------------------------------------------------------------------------

st.title("💰 AI for Financial Literacy")
st.caption(
    "A student-friendly app to track your spending, manage savings, "
    "and learn key financial concepts."
)
st.divider()

# ===========================================================================
# SECTION 1 — Income Setup
# ===========================================================================

st.header("1. 📥 Set Your Monthly Income")
st.write(
    "Enter your monthly income or allowance. This is the total amount "
    "of money you receive each month."
)

with st.form("income_form"):
    income_input = st.number_input(
        "Monthly Income / Allowance ($)",
        min_value=0.0,
        step=50.0,
        format="%.2f",
        value=float(tracker.monthly_income) if tracker.monthly_income > 0 else 0.0,
        help="Enter your total monthly income or allowance amount.",
    )
    submitted_income = st.form_submit_button("💾 Set Income")

if submitted_income:
    try:
        tracker.set_income(income_input)
        st.success(f"✅ Income set to **${tracker.monthly_income:,.2f}**")
    except InvalidIncomeError as e:
        st.error(f"❌ {e}")

if tracker.monthly_income > 0:
    st.info(f"💵 Current income: **${tracker.monthly_income:,.2f}** per month")

st.divider()

# ===========================================================================
# SECTION 2 — Add an Expense
# ===========================================================================

st.header("2. ➕ Add an Expense")
st.write("Record a new expense by filling in the details below.")

with st.form("expense_form"):
    col1, col2 = st.columns(2)

    with col1:
        expense_amount = st.number_input(
            "Amount ($)",
            min_value=0.0,
            step=1.0,
            format="%.2f",
            help="How much did you spend?",
        )
        expense_category = st.selectbox(
            "Category",
            options=VALID_CATEGORIES,
            help="Choose the category that best describes this expense.",
        )

    with col2:
        expense_description = st.text_input(
            "Description (optional)",
            max_chars=100,
            placeholder="e.g. Lunch at the canteen",
            help="A short note about what this expense was for.",
        )
        expense_date = st.date_input(
            "Date",
            value=date.today(),
            max_value=date.today(),
            help="The date this expense occurred (cannot be in the future).",
        )

    submitted_expense = st.form_submit_button("➕ Add Expense")

if submitted_expense:
    try:
        new_expense = tracker.add_expense(
            amount=expense_amount,
            category=expense_category,
            description=expense_description,
            date_str=str(expense_date),
        )
        st.success(
            f"✅ Added **${new_expense.amount:,.2f}** under **{new_expense.category}** "
            f"on {new_expense.date}"
        )
    except (InvalidExpenseError, InvalidDateError) as e:
        st.error(f"❌ {e}")

st.divider()

# ===========================================================================
# SECTION 3 — Expense Summary
# ===========================================================================

st.header("3. 📊 Your Expense Summary")

if tracker.monthly_income <= 0:
    st.warning("⚠️ Please set your income first to see accurate calculations.")
else:
    total_spent = tracker.calculate_total_spending()
    remaining = tracker.calculate_remaining_money()
    savings = tracker.calculate_savings()
    savings_pct = tracker.calculate_savings_percentage()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Spent", f"${total_spent:,.2f}")
    col2.metric(
        "Remaining",
        f"${remaining:,.2f}",
        delta=f"${remaining:,.2f}",
        delta_color="normal" if remaining >= 0 else "inverse",
    )
    col3.metric("Savings", f"${savings:,.2f}")
    col4.metric("Savings %", f"{savings_pct:.1f}%")

    if tracker.is_overspending():
        st.warning(
            "⚠️ **You are overspending!** Your total expenses exceed your income. "
            "Consider cutting back on non-essential spending."
        )

# Expense table
expenses = tracker.get_all_expenses()

if not expenses:
    st.info("📭 No expenses recorded yet. Add your first expense above!")
else:
    st.subheader("All Expenses")

    # Build display rows; show a delete button for each row.
    for expense in expenses:
        col_date, col_cat, col_desc, col_amt, col_del = st.columns(
            [1.5, 1.5, 2.5, 1.2, 0.8]
        )
        col_date.write(expense.date)
        col_cat.write(expense.category)
        col_desc.write(expense.description or "—")
        col_amt.write(f"${expense.amount:,.2f}")
        if col_del.button("🗑️", key=f"del_{expense.expense_id}", help="Delete this expense"):
            try:
                tracker.remove_expense(expense.expense_id)
                st.rerun()
            except ExpenseNotFoundError as e:
                st.error(f"❌ {e}")

    # Clear all button
    st.write("")
    if st.button("🗑️ Clear All Expenses", type="secondary"):
        tracker.clear_all_expenses()
        st.rerun()

st.divider()

# ===========================================================================
# SECTION 4 — Category Breakdown
# ===========================================================================

st.header("4. 🏷️ Spending by Category")

breakdown = tracker.get_category_breakdown()

if not breakdown:
    st.info("📭 No expenses to show yet.")
else:
    # Bar chart
    import pandas as pd

    df = pd.DataFrame(
        {"Category": list(breakdown.keys()), "Amount ($)": list(breakdown.values())}
    ).set_index("Category")
    st.bar_chart(df)

    # Category totals table
    st.subheader("Category Totals")
    for category, total in sorted(breakdown.items(), key=lambda x: x[1], reverse=True):
        st.write(f"**{category}**: ${total:,.2f}")

    # Tips for the highest-spend category
    top_category = max(breakdown, key=breakdown.__getitem__)
    tips = ai.get_tips_for_category(top_category)
    with st.expander(f"💡 Tips for reducing **{top_category}** spending"):
        for tip in tips:
            st.write(f"- {tip}")

st.divider()

# ===========================================================================
# SECTION 5 — Savings Goal
# ===========================================================================

st.header("5. 🎯 Savings Goal")
st.write(
    "Set a savings target and track your progress. "
    "Even a small goal builds a great habit!"
)

with st.form("goal_form"):
    goal_input = st.number_input(
        "Savings Goal ($)",
        min_value=0.0,
        step=10.0,
        format="%.2f",
        value=float(tracker.savings_goal) if tracker.savings_goal > 0 else 0.0,
        help="How much do you want to save this month?",
    )
    submitted_goal = st.form_submit_button("🎯 Set Goal")

if submitted_goal:
    try:
        tracker.set_savings_goal(goal_input)
        st.success(f"✅ Savings goal set to **${tracker.savings_goal:,.2f}**")
    except InvalidGoalError as e:
        st.error(f"❌ {e}")

if tracker.savings_goal > 0:
    progress = tracker.get_goal_progress()

    st.write(
        f"**Goal:** ${progress['goal']:,.2f} &nbsp;|&nbsp; "
        f"**Saved so far:** ${progress['saved']:,.2f}"
    )

    pct = progress["percentage"] / 100  # st.progress expects 0.0 – 1.0
    st.progress(min(pct, 1.0))
    st.caption(f"{progress['percentage']:.1f}% of goal reached")

    if progress["reached"]:
        st.success("🎉 Congratulations! You have reached your savings goal!")
    elif tracker.monthly_income > 0 and tracker.savings_goal > tracker.monthly_income:
        st.info(
            "ℹ️ Your savings goal is larger than your monthly income. "
            "That is perfectly fine — treat it as a multi-month goal!"
        )

st.divider()

# ===========================================================================
# SECTION 6 — Financial Literacy Assistant
# ===========================================================================

st.header("6. 🤖 Financial Literacy Assistant")
st.write(
    "Ask me anything about personal finance! I will give you a simple, "
    "beginner-friendly explanation. I cover topics like budgeting, saving, "
    "needs vs wants, emergency funds, interest, responsible spending, and more."
)
st.caption(
    "📌 This assistant provides **general educational information only** — "
    "not personalised financial advice or investment recommendations."
)

# Question input
question_input = st.text_input(
    "Your question",
    placeholder="e.g. What is budgeting? How do I save money? What is an emergency fund?",
)

col_ask, col_tip = st.columns([1, 1])

with col_ask:
    if st.button("💬 Ask", type="primary"):
        try:
            st.session_state.ai_answer = ai.answer_question(question_input)
        except EmptyQuestionError as e:
            st.error(f"❌ {e}")

with col_tip:
    if st.button("🎲 Give me a random tip"):
        st.session_state.random_tip = ai.get_random_tip()

# Display the AI answer
if st.session_state.ai_answer:
    st.info(st.session_state.ai_answer)

# Display the random tip
if st.session_state.random_tip:
    st.success(f"💡 **Tip:** {st.session_state.random_tip}")

# Topics the assistant knows about
with st.expander("📚 Topics I can explain"):
    topics = ai.get_all_topics()
    st.write(
        "Ask me about any of these topics by including the keyword in your question:"
    )
    cols = st.columns(2)
    for i, topic in enumerate(topics):
        cols[i % 2].write(f"• {topic}")

st.divider()

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

st.caption(
    "💰 AI for Financial Literacy | Built with Python & Streamlit | "
    "For educational purposes only — not professional financial advice."
)
