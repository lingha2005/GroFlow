"""Central place for names, paths and numbers, so nothing is hidden in the UI code.

Want to tweak how GroFlow behaves? Change it here.
"""
from pathlib import Path

# --- Paths ---------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
IMAGES_DIR = BASE_DIR / "assets" / "images"
HERO_IMAGE = IMAGES_DIR / "smallbusiness.jpg"

# --- App identity --------------------------------------------------------
APP_NAME = "GroFlow"
APP_ICON = "🌱"
APP_TAGLINE = "Growth. Funding. Freedom."

# --- Demo profile shown in the sidebar -----------------------------------
DEMO_USER_NAME = "Sarah"
DEMO_BUSINESS = "Sarah's Cakes"
AVATAR_URL = "https://api.dicebear.com/9.x/micah/svg?seed=Felix"

# --- Page names used by the router ---------------------------------------
HOME = "Home"
AI_ASSISTANT = "AI Assistant"
FUNDRAISING = "Fundraising"
INVESTOR_PORTAL = "Investor Portal"
ADAPTIVE_TRACKER = "Adaptive Tracker"

# --- Gemini API ----------------------------------------------------------
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_ENDPOINT = (
    "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
)
GEMINI_TIMEOUT_SECONDS = 60

# --- Trust Points economy ------------------------------------------------
STARTING_TRUST_POINTS = 120
VOUCH_COST = 10             # points a member spends to vouch for a campaign
FUNDING_THRESHOLD = 1000    # points a business needs to become investor-ready

# --- Investor portal -----------------------------------------------------
STARTING_INVESTOR_POOL = 5000
MONTHLY_ROI = 0.05          # simulated 5% monthly return
MIN_INVESTMENT = 500
MAX_INVESTMENT = 10000
DEFAULT_INVESTMENT = 2000
INVESTMENT_STEP = 500
