"""Investor Portal: deploy capital into businesses that have earned enough Trust Points."""
from datetime import date

import pandas as pd
import streamlit as st

from groflow.config import (
    DEFAULT_INVESTMENT,
    FUNDING_THRESHOLD,
    INVESTMENT_STEP,
    MAX_INVESTMENT,
    MIN_INVESTMENT,
    MONTHLY_ROI,
)


def render() -> None:
    st.header("🏦 Investor Dashboard")
    st.caption("Deploy capital to vetted small businesses and earn returns while building community impact.")
    st.divider()

    _portfolio_overview()
    st.divider()
    _liquidity_pool_controls()
    st.divider()
    _investment_opportunities()
    st.divider()
    _my_portfolio()


def _total_invested() -> float:
    return sum(inv["amount"] for inv in st.session_state.investor_investments)


def _portfolio_overview() -> None:
    total_invested = _total_invested()
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Liquidity Pool", f"${st.session_state.investor_pool:,.0f}", delta="Available")
    with col2:
        st.metric("📊 Total Deployed", f"${total_invested:,.0f}")
    with col3:
        st.metric("🎯 Active Investments", len(st.session_state.investor_investments))
    with col4:
        st.metric(
            "💵 Expected Monthly Returns",
            f"${total_invested * MONTHLY_ROI:,.0f}",
            delta=f"{MONTHLY_ROI:.0%} ROI",
        )


def _liquidity_pool_controls() -> None:
    with st.expander("💳 Manage Liquidity Pool"):
        st.subheader("Add or Withdraw Capital")
        col_add, col_withdraw = st.columns(2)

        with col_add:
            st.markdown("#### Add Funds")
            add_amount = st.number_input("Amount to Add ($)", min_value=0, value=1000, step=100, key="add_funds")
            if st.button("➕ Add to Pool"):
                st.session_state.investor_pool += add_amount
                st.toast(f"Added ${add_amount:,.0f} to your liquidity pool!", icon="✅")
                st.rerun()

        with col_withdraw:
            st.markdown("#### Withdraw Funds")
            withdraw_amount = st.number_input(
                "Amount to Withdraw ($)", min_value=0, value=500, step=100, key="withdraw_funds"
            )
            if st.button("➖ Withdraw from Pool"):
                if withdraw_amount <= st.session_state.investor_pool:
                    st.session_state.investor_pool -= withdraw_amount
                    st.toast(f"Withdrew ${withdraw_amount:,.0f} from your pool!", icon="✅")
                    st.rerun()
                else:
                    st.error("Insufficient funds in liquidity pool!")


def _investment_opportunities() -> None:
    st.subheader("🔍 Investment-Ready Businesses")
    st.caption(f"Businesses that have reached {FUNDING_THRESHOLD}+ Trust Points and meet funding criteria")

    eligible = [c for c in st.session_state.campaigns if c["points"] >= FUNDING_THRESHOLD]
    if not eligible:
        st.info(f"No businesses have reached the {FUNDING_THRESHOLD} Trust Point threshold yet.")
        return

    for idx, business in enumerate(eligible):
        _business_card(idx, business)


def _business_card(idx: int, business: dict) -> None:
    with st.container(border=True):
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader(f"🌟 {business['name']}")
            st.caption(f"Owner: {business['owner']}")
            st.write(business["desc"])

            met1, met2, met3 = st.columns(3)
            met1.metric("Trust Points", business["points"])
            met2.metric("Community Vouches", business.get("community_vouches", 0))
            met3.metric("Monthly Revenue", f"${business.get('monthly_revenue', 0):,.0f}")
            st.caption(f"⏰ In Business: {business.get('months_in_business', 0)} months")

            if business.get("funded_by_investors"):
                st.success(f"✅ Already Funded: ${business.get('investor_funding', 0):,.0f}")
            else:
                st.info("⏳ Awaiting investor funding")

        with col_right:
            if business.get("image"):
                st.image(business["image"], width="stretch")

            if business.get("funded_by_investors"):
                st.success("✅ Funded")
                st.caption("This business has received funding")
                return

            st.markdown("#### Fund This Business")
            amount = st.number_input(
                "Investment Amount ($)",
                min_value=MIN_INVESTMENT,
                max_value=MAX_INVESTMENT,
                value=DEFAULT_INVESTMENT,
                step=INVESTMENT_STEP,
                key=f"invest_amount_{idx}",
            )
            st.caption(f"💡 Expected Monthly ROI: ${amount * MONTHLY_ROI:,.0f} ({MONTHLY_ROI:.0%})")

            if st.button(f"💼 Invest ${amount:,.0f}", key=f"invest_btn_{idx}", type="primary"):
                _invest(business, amount)


def _invest(business: dict, amount: float) -> None:
    if amount > st.session_state.investor_pool:
        st.error("Insufficient liquidity! Add more funds to your pool.")
        return

    st.session_state.investor_pool -= amount
    business["funded_by_investors"] = True
    business["investor_funding"] = amount
    st.session_state.investor_investments.append(
        {
            "business": business["name"],
            "amount": amount,
            "date": date.today().isoformat(),
            "status": "Active",
        }
    )
    st.toast(f"Successfully invested ${amount:,.0f} in {business['name']}!", icon="🎉")
    st.balloons()
    st.rerun()


def _my_portfolio() -> None:
    st.subheader("📋 My Investment Portfolio")
    if not st.session_state.investor_investments:
        st.info("You haven't made any investments yet. Browse opportunities above!")
        return

    inv_df = pd.DataFrame(st.session_state.investor_investments)
    st.dataframe(
        inv_df,
        width="stretch",
        column_config={
            "business": "Business Name",
            "amount": st.column_config.NumberColumn("Investment", format="$%d"),
            "date": "Investment Date",
            "status": "Status",
        },
    )

    total = inv_df["amount"].sum()
    col1, col2 = st.columns(2)
    col1.metric("Total Invested", f"${total:,.0f}")
    col2.metric("Expected Monthly Return", f"${total * MONTHLY_ROI:,.0f}")

