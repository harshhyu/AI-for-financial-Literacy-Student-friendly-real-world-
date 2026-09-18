"""Static financial literacy knowledge base.

This file contains:
- CONCEPT_DEFINITIONS: plain-English explanations of key financial topics.
- GENERAL_TIPS: practical budgeting and saving tips.
- CATEGORY_TIPS: spending tips specific to each expense category.

No imports needed — this is pure data used by the FinancialAI class.
"""

# ---------------------------------------------------------------------------
# Concept definitions
# Each key is a topic keyword; the value is a beginner-friendly explanation.
# ---------------------------------------------------------------------------

CONCEPT_DEFINITIONS: dict[str, str] = {
    "budgeting": (
        "💰 What is Budgeting?\n\n"
        "A budget is simply a plan for your money. You decide in advance how much "
        "you will spend in different areas — like food, travel, and fun — so that "
        "you do not run out of money before the month ends.\n\n"
        "How to start:\n"
        "1. Write down how much money you receive each month.\n"
        "2. List all the things you need to spend money on.\n"
        "3. Make sure your spending does not exceed your income.\n\n"
        "A budget gives you control over your money instead of wondering where it all went."
    ),

    "saving": (
        "🏦 What is Saving?\n\n"
        "Saving means setting aside part of your income instead of spending all of it. "
        "Even saving a small amount regularly adds up over time — this is called the "
        "power of small habits.\n\n"
        "Why saving matters:\n"
        "- It gives you a safety net for unexpected expenses.\n"
        "- It helps you afford bigger things in the future.\n"
        "- It reduces financial stress.\n\n"
        "A simple rule: pay yourself first. As soon as you receive money, move a "
        "portion to savings before spending anything else."
    ),

    "needs vs wants": (
        "🛒 Needs vs Wants — What is the Difference?\n\n"
        "A NEED is something essential to survive or function — food, rent, "
        "medicine, basic clothing, transport to school or work.\n\n"
        "A WANT is something you would enjoy but could live without — a new phone, "
        "eating out, streaming subscriptions, the latest fashion.\n\n"
        "Why this matters:\n"
        "When money is tight, spend on needs first. Wants can wait or be budgeted "
        "for once your essentials and savings are covered.\n\n"
        "Ask yourself before buying: 'Do I need this, or do I just want it?'"
    ),

    "emergency fund": (
        "🆘 What is an Emergency Fund?\n\n"
        "An emergency fund is money you save specifically for unexpected situations — "
        "like a medical bill, a broken phone, or losing a part-time job.\n\n"
        "How much to save:\n"
        "- A starter goal: save enough to cover 1 month of essential expenses.\n"
        "- A stronger goal: save 3 to 6 months of expenses over time.\n\n"
        "Keep your emergency fund in a separate savings account so you are not "
        "tempted to spend it. Only use it for real emergencies — not wants!\n\n"
        "Having even a small emergency fund prevents you from falling into debt "
        "when life surprises you."
    ),

    "interest": (
        "📈 What is Interest?\n\n"
        "Interest is the cost of borrowing money — or the reward for saving it.\n\n"
        "Interest on savings:\n"
        "When you deposit money in a bank, the bank pays you interest as a reward "
        "for letting them use your money. Your savings grow over time.\n\n"
        "Interest on debt:\n"
        "When you borrow money (like a credit card or a loan), you pay interest on "
        "top of what you borrowed. The longer you take to repay, the more you pay.\n\n"
        "Example: If you borrow $100 at 10% interest per year, you owe $110 "
        "after one year.\n\n"
        "Key lesson: save money to earn interest; avoid unnecessary debt to avoid "
        "paying interest."
    ),

    "responsible spending": (
        "✅ What is Responsible Spending?\n\n"
        "Responsible spending means making thoughtful decisions about where your "
        "money goes, so it aligns with your values and goals.\n\n"
        "Habits of responsible spenders:\n"
        "- They compare prices before buying.\n"
        "- They wait 24 hours before making big purchases (avoiding impulse buys).\n"
        "- They avoid buying things just because they are on sale.\n"
        "- They track their spending so they know where their money goes.\n"
        "- They prioritise needs over wants.\n\n"
        "Responsible spending is not about being cheap — it is about being "
        "intentional with your money."
    ),

    "50/30/20 rule": (
        "📊 The 50/30/20 Budgeting Rule\n\n"
        "This is a simple, popular budgeting guideline:\n\n"
        "• 50% of your income → Needs\n"
        "  (rent, groceries, transport, utilities)\n\n"
        "• 30% of your income → Wants\n"
        "  (eating out, entertainment, shopping, hobbies)\n\n"
        "• 20% of your income → Savings & debt repayment\n"
        "  (emergency fund, savings goals, paying off loans)\n\n"
        "Example: If you earn $1,000 per month:\n"
        "- $500 for needs\n"
        "- $300 for wants\n"
        "- $200 for savings\n\n"
        "You do not need to follow this rule exactly — use it as a starting guide "
        "and adjust to your own situation."
    ),

    "expense tracking": (
        "📝 Why Track Your Expenses?\n\n"
        "Expense tracking means writing down every time you spend money. "
        "Most people are surprised by where their money actually goes!\n\n"
        "Benefits of tracking:\n"
        "- You see patterns in your spending (e.g. too much on coffee).\n"
        "- You can make better decisions about what to cut back on.\n"
        "- It keeps you accountable to your budget.\n"
        "- It removes the mystery of 'where did my money go?'\n\n"
        "How to track:\n"
        "Use this app! Record every expense as it happens. Review your "
        "category breakdown weekly to spot trends."
    ),

    "debt": (
        "⚠️ Basic Debt Awareness\n\n"
        "Debt means you owe money to someone else — a bank, a lender, or "
        "a credit card company.\n\n"
        "Not all debt is bad:\n"
        "- A student loan to fund education can be a worthwhile investment.\n"
        "- A small loan repaid on time builds your credit history.\n\n"
        "Debt becomes dangerous when:\n"
        "- You borrow more than you can repay.\n"
        "- You only pay the minimum on a credit card (interest builds up fast).\n"
        "- You borrow for wants, not needs.\n\n"
        "Golden rule: before borrowing, always ask — 'Can I comfortably repay "
        "this, including the interest?'"
    ),
}


# ---------------------------------------------------------------------------
# General budgeting and saving tips
# ---------------------------------------------------------------------------

GENERAL_TIPS: list[str] = [
    "💡 Record every expense as soon as it happens — small amounts add up quickly.",
    "💡 Before buying something, wait 24 hours. If you still want it, then decide.",
    "💡 Set a weekly spending limit for non-essential items like coffee or snacks.",
    "💡 Review your category breakdown each week to spot where you overspend.",
    "💡 Save a fixed percentage of your income as soon as you receive it.",
    "💡 Bring lunch from home instead of buying it — you can save a lot each month.",
    "💡 Unsubscribe from services you have not used in the last 30 days.",
    "💡 Compare prices before buying anything expensive — use multiple stores or apps.",
    "💡 Avoid shopping when you are bored, stressed, or hungry — you spend more.",
    "💡 Set a specific savings goal (e.g. a new laptop or a trip) to stay motivated.",
    "💡 Use the 50/30/20 rule as a simple starting guide for your budget.",
    "💡 Keep your emergency fund in a separate account so you are not tempted to spend it.",
    "💡 Track your net worth over time — knowing your progress is motivating.",
    "💡 Avoid paying full price — look for student discounts and deals.",
]


# ---------------------------------------------------------------------------
# Category-specific spending tips
# ---------------------------------------------------------------------------

CATEGORY_TIPS: dict[str, list[str]] = {
    "Food": [
        "🍽️ Plan your meals for the week and write a shopping list before going to the store.",
        "🍽️ Cook at home more often — even one extra home-cooked meal per week saves money.",
        "🍽️ Buy in bulk for staple items like rice, pasta, and canned goods when on sale.",
    ],
    "Travel": [
        "🚌 Use public transport or walk short distances instead of taking taxis or rideshares.",
        "🚌 Plan your trips in advance to find cheaper fares and avoid peak-hour prices.",
        "🚌 Carpool with friends or classmates to split fuel or ride costs.",
    ],
    "Shopping": [
        "🛍️ Write a shopping list and stick to it — avoid browsing when you are not looking for something specific.",
        "🛍️ Wait for sales or use student discount codes before making non-urgent purchases.",
        "🛍️ Ask yourself: 'Will I still use this in 6 months?' before buying.",
    ],
    "Education": [
        "📚 Look for free or discounted resources: library books, open-source textbooks, and free online courses.",
        "📚 Share textbooks with classmates or buy second-hand copies instead of new ones.",
        "📚 Use free software alternatives to expensive paid tools where possible.",
    ],
    "Entertainment": [
        "🎮 Set a monthly entertainment budget and stick to it so fun does not eat into savings.",
        "🎮 Look for free or low-cost events in your area — parks, community events, or free streaming.",
        "🎮 Share streaming subscriptions with housemates or family to split the cost.",
    ],
    "Other": [
        "📌 When spending appears in 'Other', ask yourself whether it could fit a named category.",
        "📌 Review your 'Other' expenses monthly — recurring ones may deserve their own budget line.",
        "📌 Avoid impulse purchases by giving yourself a 24-hour cooling-off period.",
    ],
}
