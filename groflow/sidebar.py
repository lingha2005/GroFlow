"""Sidebar: profile, global Gemini API key, Trust Points balance and a way back home."""
import streamlit as st

from groflow.config import APP_ICON, APP_NAME, AVATAR_URL, DEMO_BUSINESS, DEMO_USER_NAME, HOME
from groflow.state import go_to


def render_sidebar() -> None:
    with st.sidebar:
        st.title(f"{APP_ICON} {APP_NAME}")
        st.image(AVATAR_URL, width=100)
        st.write(f"**Hello, {DEMO_USER_NAME}!**")
        st.caption(f"Owner: {DEMO_BUSINESS}")

        st.write("---")
        # key="api_key" stores the value in st.session_state.api_key for every page to use
        st.text_input("🔑 Enter Gemini API Key", type="password", key="api_key")

        st.write("---")
        st.metric("Trust Points Balance", st.session_state.points, delta="10 pts")
        st.write("---")

        if st.button("🏠 Back to Home"):
            go_to(HOME)
