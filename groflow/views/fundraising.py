"""Fundraising: a community marketplace where members vouch for businesses with Trust Points."""
import streamlit as st

from groflow.config import VOUCH_COST

PLACEHOLDER_IMAGE = "https://picsum.photos/400/300?random=99"


def render() -> None:
    _header()
    st.divider()
    _new_campaign_form()
    _campaign_grid()


def _header() -> None:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.header("💰 Community Marketplace")
        st.caption("Discover businesses, Vouch for quality, and help them unlock capital.")
    with col2:
        st.metric("Your Trust Points", st.session_state.points, delta="Available to spend")


def _new_campaign_form() -> None:
    with st.expander("➕ Create a New Campaign"):
        with st.form("new_campaign"):
            c1, c2 = st.columns([1, 2])
            with c1:
                uploaded_file = st.file_uploader("Product Image", type=["jpg", "png"])
            with c2:
                new_title = st.text_input("Campaign Title")
                new_desc = st.text_area("Description")
                new_goal = st.number_input("Goal (Points)", min_value=1, value=1000)

            if st.form_submit_button("Post Campaign"):
                if not new_title.strip():
                    st.error("Please give your campaign a title.")
                    return
                st.session_state.campaigns.append(
                    {
                        "name": new_title,
                        "owner": "You",
                        "desc": new_desc,
                        "points": 0,
                        "goal": new_goal,
                        "image": uploaded_file or PLACEHOLDER_IMAGE,
                        "funded_by_investors": False,
                        "investor_funding": 0,
                    }
                )
                st.toast("Campaign posted!", icon="🎉")
                st.rerun()


def _campaign_grid() -> None:
    columns = st.columns(3)
    for i, campaign in enumerate(st.session_state.campaigns):
        with columns[i % 3]:
            _campaign_card(i, campaign)


def _campaign_card(i: int, camp: dict) -> None:
    with st.container(border=True):
        if camp.get("image"):
            st.image(camp["image"], width="stretch")

        st.subheader(camp["name"])
        st.caption(f"by {camp['owner']}")
        st.write(camp.get("desc", ""))

        st.progress(min(camp["points"] / camp["goal"], 1.0))
        st.caption(f"🏆 {camp['points']} / {camp['goal']} Trust Points")

        if camp.get("funded_by_investors"):
            st.success(f"💼 Investor Funded: ${camp.get('investor_funding', 0)}")

        like_col, vouch_col = st.columns(2)
        with like_col:
            if st.button("❤️ Like", key=f"like_{i}"):
                st.toast("You liked this project!")

        with vouch_col:
            # Vouching costs YOU points and gives THEM points
            if camp["points"] >= camp["goal"]:
                st.success("Funded! 🎉")
            elif st.button(f"✨ Vouch ({VOUCH_COST})", key=f"vouch_{i}"):
                if st.session_state.points >= VOUCH_COST:
                    st.session_state.points -= VOUCH_COST
                    camp["points"] += VOUCH_COST
                    camp["community_vouches"] = camp.get("community_vouches", 0) + 1
                    st.rerun()
                else:
                    st.error("Not enough points!")

        with st.expander("💬 Comments"):
            st.text_input("Add a comment...", key=f"com_{i}")
            st.write("*Very cool project!* - @mike")
