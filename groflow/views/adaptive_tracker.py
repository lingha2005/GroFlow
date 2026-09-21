"""Adaptive Tracker: compare revenue to goal and let the AI recalibrate a recovery plan."""
import textwrap

import pandas as pd
import streamlit as st

from groflow.ai import GeminiError, ask_gemini

# (checkbox label, name used in the AI prompt when the task was missed)
WEEKLY_TASKS = [
    ("Posted 3x on Socials", "Social Media Posts"),
    ("Sent Email Newsletter", "Email Newsletter"),
    ("Inventory Audit Done", "Inventory Audit"),
    ("Replied to Reviews", "Review Replies"),
]


def render() -> None:
    st.header("📈 Closed-Loop Adaptive Tracker")
    st.caption("Real-time accountability: If you miss targets, the AI recalibrates your roadmap.")

    target, current, days = _performance_inputs()
    missed_tasks, execution_score = _weekly_checklist()

    st.write("---")
    _burn_down_chart(current)

    gap = target - current
    if gap > 0:
        st.error(f"⚠️ You are behind by ${gap}. To catch up, you need ${gap / days:.2f}/day.")
        if st.button("🔄 AI Recalibrate Strategy", type="primary"):
            _recalibrate(target, current, gap, days, execution_score, missed_tasks)
    else:
        st.success("🎉 You are on track! Keep up the momentum.")
        st.balloons()


def _performance_inputs():
    with st.container(border=True):
        st.subheader("📊 Live Performance Data")
        col1, col2, col3 = st.columns(3)
        target = col1.number_input("Monthly Revenue Goal ($)", value=1000)
        current = col2.number_input("Current Revenue Achieved ($)", value=400)
        days = col3.slider("Days Remaining in Month", 1, 30, 10)
    return target, current, days


def _weekly_checklist():
    st.write("---")
    st.subheader("✅ Weekly Milestones Checklist")
    st.caption("Tick the tasks you actually completed this week. The AI analyzes your misses.")

    columns = st.columns(len(WEEKLY_TASKS))
    done = [col.checkbox(label) for col, (label, _) in zip(columns, WEEKLY_TASKS)]

    missed = [missed_name for (_, missed_name), ticked in zip(WEEKLY_TASKS, done) if not ticked]
    execution_score = int(sum(done) / len(WEEKLY_TASKS) * 100)

    st.progress(execution_score / 100)
    st.caption(f"Execution Score: {execution_score}%")
    return missed, execution_score


def _burn_down_chart(current: float) -> None:
    st.subheader("📉 Burn-Down Chart")
    # Simulated trend line that ends at the current revenue
    chart_data = pd.DataFrame(
        {
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Revenue Trend": [current * f for f in (0.1, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0)],
        }
    )
    st.line_chart(chart_data, x="Day", y="Revenue Trend", color="#6B8E23")


def _recalibrate(target, current, gap, days, execution_score, missed_tasks) -> None:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.error("Please enter your API Key in the sidebar to recalibrate!")
        return

    missed_text = ", ".join(missed_tasks) if missed_tasks else "None (Execution was perfect, but Revenue is low)"
    prompt = textwrap.dedent(
        f"""\
        Act as a Crisis Management Coach for a small business.

        CURRENT STATUS:
        - Goal: ${target} | Current: ${current} | Gap: ${gap}
        - Days Left: {days} days
        - Execution Score: {execution_score}%

        MISSED TASKS THIS WEEK:
        {missed_text}

        YOUR TASK:
        1. CALCULATE the new required Daily Revenue to hit the goal.
        2. ANALYZE why the gap exists based on the specific missed tasks (e.g., if they missed marketing, explain how that hurts sales).
        3. GENERATE a strict "Recovery Plan" for the next {days} days to catch up.

        Keep it encouraging but strict. Maximum Efficiency focus.
        """
    )

    with st.spinner("🤖 AI is analyzing your missed tasks and recalculating..."):
        try:
            result = ask_gemini(prompt, api_key)
        except GeminiError as err:
            st.error(str(err))
            return

    st.divider()
    st.subheader("🚀 Your AI Recovery Plan")
    st.markdown(result)
