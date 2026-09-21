"""GroFlow entry point.  Run it with:  streamlit run app.py"""
import streamlit as st

from groflow.config import (
    ADAPTIVE_TRACKER,
    AI_ASSISTANT,
    APP_ICON,
    APP_NAME,
    FUNDRAISING,
    HOME,
    INVESTOR_PORTAL,
)
from groflow.sidebar import render_sidebar
from groflow.state import init_state
from groflow.styles import inject_styles
from groflow.views import adaptive_tracker, ai_assistant, fundraising, home, investor_portal

# Must be the first Streamlit command in the script
st.set_page_config(page_title=APP_NAME, page_icon=APP_ICON, layout="wide")

PAGES = {
    HOME: home.render,
    AI_ASSISTANT: ai_assistant.render,
    FUNDRAISING: fundraising.render,
    INVESTOR_PORTAL: investor_portal.render,
    ADAPTIVE_TRACKER: adaptive_tracker.render,
}

init_state()
inject_styles()
render_sidebar()

PAGES.get(st.session_state.page, home.render)()
