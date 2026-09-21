"""Home dashboard: hero section and the four module cards."""
import streamlit as st

from groflow.config import (
    ADAPTIVE_TRACKER,
    AI_ASSISTANT,
    APP_ICON,
    APP_NAME,
    APP_TAGLINE,
    FUNDRAISING,
    HERO_IMAGE,
    INVESTOR_PORTAL,
)
from groflow.state import go_to

# (box style, title, caption, button label, target page)
MODULES = [
    ("info", "🤖 **AI Manager**", "Generate instant marketing tasks.", "Launch AI Assistant →", AI_ASSISTANT),
    ("warning", "💰 **Fundraising**", "Unlock capital with Trust Points.", "Go to Marketplace →", FUNDRAISING),
    ("success", "📈 **Adaptive Tracker**", "Recalibrate your monthly goals.", "Open Tracker →", ADAPTIVE_TRACKER),
    ("error", "🏦 **Investor Portal**", "Fund businesses & earn returns.", "Access Investor Hub →", INVESTOR_PORTAL),
]


def render() -> None:
    # Hero section
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.title(f"{APP_ICON} {APP_NAME}")
        st.subheader(APP_TAGLINE)
        st.markdown(
            """
            **Welcome to your Command Center.**
            Select a module below to start automating your business.
            """
        )
    with col2:
        st.image(str(HERO_IMAGE), width="stretch")

    st.write("---")
    st.subheader("Select a Module")

    # Clickable module cards
    for column, (style, title, caption, button_label, target) in zip(
        st.columns(len(MODULES)), MODULES
    ):
        with column:
            getattr(st, style)(title)
            st.caption(caption)
            if st.button(button_label):
                go_to(target)
