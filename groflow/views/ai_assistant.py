"""AI Assistant: quick micro-actions and a monthly strategic roadmap."""
import json
import textwrap

import streamlit as st

from groflow.ai import GeminiError, ask_gemini

NO_KEY_MESSAGE = "Please enter your API Key in the sidebar first!"


def render() -> None:
    st.header("🤖 Constraint-Aware AI Assistant")
    st.caption("Your Virtual Business Manager")

    tab_quick, tab_monthly = st.tabs(["⚡ Quick Micro-Actions", "📅 Monthly Strategic Plan"])
    with tab_quick:
        _quick_actions_tab()
    with tab_monthly:
        _monthly_plan_tab()


# ---------------------------------------------------------------------------
# Tab 1: quick actions
# ---------------------------------------------------------------------------
def _quick_actions_tab() -> None:
    st.markdown("#### Instant Productivity")
    st.write("Got 15 minutes? Let's fill it with high-impact work.")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            energy_level = st.select_slider(
                "🔋 Your Current Energy Level",
                options=["Low (Tired)", "Medium", "High (Let's go!)"],
            )
            time_now = st.selectbox("⏳ Time You Have RIGHT NOW", ["10 Minutes", "30 Minutes", "1 Hour"])
        with col2:
            platform = st.multiselect(
                "📱 Platforms You Use",
                ["Instagram", "WhatsApp", "Email", "TikTok", "LinkedIn"],
                default=["Instagram"],
            )
            task_type = st.selectbox("🎯 Focus Area", ["Sales/Revenue", "Brand Awareness", "Admin/Cleanup"])

        if st.button("⚡ Generate Quick Wins", type="primary"):
            api_key = st.session_state.get("api_key")
            if not api_key:
                st.error(NO_KEY_MESSAGE)
                return

            prompt = (
                "Act as a productivity coach. "
                f"Context: Energy={energy_level}, Time={time_now}, Focus={task_type}, "
                f"Platforms={', '.join(platform)}.\n"
                'Give me exactly 3 "Micro-Actions" I can do RIGHT NOW. No fluff.'
            )
            with st.spinner("Finding high-impact tasks..."):
                try:
                    ai_text = ask_gemini(prompt, api_key)
                except GeminiError as err:
                    st.error(str(err))
                    return
            st.success("🚀 Ready to execute:")
            st.markdown(ai_text)


# ---------------------------------------------------------------------------
# Tab 2: monthly roadmap
# ---------------------------------------------------------------------------
def _monthly_plan_tab() -> None:
    st.markdown("#### Strategic Growth Engine")

    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            goal_text = st.text_input("🏆 Main Goal", placeholder="e.g. Launch Summer Collection")
            business_desc = st.text_input("🛒 What do you sell?", "Handmade Jewelry")
        with c2:
            duration = st.slider("🗓️ Duration (Weeks)", 4, 12, 4)
            budget_monthly = st.number_input("💰 Total Budget ($)", 0, 10000, 500)

        if st.button("📅 Draft Interactive Roadmap"):
            _generate_roadmap(business_desc, goal_text, duration, budget_monthly)

    _show_roadmap()


def _generate_roadmap(business: str, goal: str, weeks: int, budget: int) -> None:
    api_key = st.session_state.get("api_key")
    if not api_key:
        st.error(NO_KEY_MESSAGE)
        return

    prompt = textwrap.dedent(
        f"""\
        Act as a Project Manager.
        Context: Business={business}, Goal={goal}, Duration={weeks} weeks, Budget=${budget}.

        OUTPUT FORMAT INSTRUCTION:
        You must output ONLY valid JSON. Do not write intro text.
        Structure the JSON as a list of phases. Example:
        [
            {{"phase": "Week 1: Setup", "tasks": ["Task A", "Task B"]}},
            {{"phase": "Week 2: Launch", "tasks": ["Task C", "Task D"]}}
        ]
        Generate {weeks} phases (one per week).
        """
    )

    with st.spinner("🤖 AI is designing your tracker..."):
        try:
            raw_reply = ask_gemini(prompt, api_key)
        except GeminiError as err:
            st.error(str(err))
            return

    roadmap = _parse_roadmap(raw_reply)
    if roadmap is None:
        st.error("AI generated text instead of data. Please try again.")
        with st.expander("See the raw AI reply"):
            st.write(raw_reply)
        return

    st.session_state["generated_roadmap"] = roadmap
    st.rerun()


def _parse_roadmap(raw_text: str):
    """Turn the AI's reply into a list of {"phase": ..., "tasks": [...]}, or None if it isn't valid."""
    cleaned = raw_text.replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError:
        return None
    is_valid = isinstance(data, list) and all(
        isinstance(phase, dict) and "phase" in phase and "tasks" in phase for phase in data
    )
    return data if is_valid else None


def _show_roadmap() -> None:
    roadmap = st.session_state.get("generated_roadmap")
    if not roadmap:
        return

    st.divider()
    st.subheader(f"🚀 Your {len(roadmap)}-Week Action Plan")
    st.caption("This is your custom-built tracker. Check off items as you go!")

    for i, phase in enumerate(roadmap):
        with st.expander(f"📌 {phase['phase']}", expanded=True):
            for j, task in enumerate(phase["tasks"]):
                st.checkbox(task, key=f"roadmap_task_{i}_{j}")

    if st.button("🗑️ Clear Plan"):
        del st.session_state["generated_roadmap"]
        st.rerun()
