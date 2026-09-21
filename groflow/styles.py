"""The GroFlow look: beige and earthy, with hover-lift buttons."""
import streamlit as st

APP_CSS = """
<style>
/* MAIN THEME: Beige & Earthy */
.stApp {
    background-color: #F9F5EB; /* Light Beige */
    background-image: url("https://www.transparenttextures.com/patterns/concrete-wall.png");
}

/* SIDEBAR: Darker Beige + Dark Text */
[data-testid="stSidebar"] {
    background-color: #E6DCC3;
    border-right: 2px solid #6B8E23;
}

/* TEXT COLORS: Force Dark Brown everywhere */
h1, h2, h3, h4, h5, h6, p, li, .stMarkdown, label {
    color: #4B3621 !important; /* Coffee Brown */
    font-family: 'Helvetica', sans-serif;
}

/* FIX: Make Metrics (Trust Points) Dark Brown */
[data-testid="stMetricValue"], [data-testid="stMetricLabel"] {
    color: #4B3621 !important;
}

/* NAVIGATION BUTTONS (The "Hover Card" Effect) */
div.stButton > button {
    width: 100%;
    height: 60px;
    border-radius: 12px;
    background-color: #FDFBF7; /* Cream Card */
    color: #4B3621;
    border: 2px solid #6B8E23; /* Olive Border */
    font-weight: bold;
    font-size: 18px;
    transition: all 0.3s ease-in-out;
}

/* HOVER STATE: Lift up and turn Olive */
div.stButton > button:hover {
    background-color: #6B8E23; /* Olive Fill */
    color: white !important;
    border-color: #556B2F;
    transform: translateY(-5px) scale(1.02); /* Pop up effect */
    box-shadow: 0px 10px 20px rgba(107, 142, 35, 0.4);
}

/* HOME BUTTON (Specific Style) */
[data-testid="stSidebar"] button {
    background-color: #4B3621;
    color: white;
}
</style>
"""


def inject_styles() -> None:
    st.markdown(APP_CSS, unsafe_allow_html=True)
