"""All session_state defaults and navigation live here."""
import copy

import streamlit as st

from groflow.config import HOME, STARTING_INVESTOR_POOL, STARTING_TRUST_POINTS
from groflow.data import SEED_CAMPAIGNS


def init_state() -> None:
    """Create every session_state value the app needs (only if it doesn't exist yet)."""
    defaults = {
        "page": HOME,
        "points": STARTING_TRUST_POINTS,
        "investor_pool": STARTING_INVESTOR_POOL,
        "investor_investments": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    if "campaigns" not in st.session_state:
        # deepcopy so edits never leak back into the shared seed data
        st.session_state.campaigns = copy.deepcopy(SEED_CAMPAIGNS)


def go_to(page: str) -> None:
    """Switch to another page and redraw."""
    st.session_state.page = page
    st.rerun()
