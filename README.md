# 🌱 GroFlow

**Growth. Funding. Freedom.**

GroFlow is a Streamlit web app that helps small-business owners plan, fund and track their growth. It combines an AI business manager (powered by Google Gemini) with a community *Trust Points* marketplace and an investor portal.

> **Note:** GroFlow is a working prototype. All data (campaigns, points, investments) is simulated and kept in memory, so it resets when the page is refreshed. No real money is involved.

---

## ✨ Modules

| Module | What it does |
|--------|--------------|
| 🤖 **AI Assistant** | *Quick Micro-Actions* suggests three things you can do right now, based on your energy, available time, focus area and platforms. *Monthly Strategic Plan* turns a goal and budget into a week-by-week roadmap with tick-off checklists. |
| 💰 **Fundraising** | A community marketplace where owners post campaigns and members **vouch** for them using Trust Points. |
| 🏦 **Investor Portal** | Businesses that reach 1000 Trust Points become investor-ready. Investors manage a liquidity pool, fund businesses and track their portfolio with a simulated 5% monthly return. |
| 📈 **Adaptive Tracker** | Compare revenue against your monthly goal, tick off weekly milestones to get an execution score, and let the AI build a recovery plan when you fall behind. |

### How Trust Points work

1. Every member starts with a balance of Trust Points.
2. Vouching for a campaign costs **10 points** and gives the campaign **10 points**.
3. Once a business reaches **1000 points**, it appears in the Investor Portal.
4. An investor can fund it from their liquidity pool.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or newer
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey) (needed only for the AI features)

### Run it locally

```bash
# 1. Clone the repository
git clone https://github.com/lingha2005/GroFlow.git
cd GroFlow

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start the app
streamlit run app.py
```

Then open the local URL shown in your terminal, paste your Gemini API key into the sidebar, and you're ready to go. The key is only kept for your current session and is never saved.

---

## 📁 Project Structure

```
GroFlow/
├── app.py                    # Entry point: page setup and the page router
├── requirements.txt          # Python dependencies
├── assets/
│   └── images/               # Marketplace and hero images
└── groflow/
    ├── config.py             # Constants: model name, ROI, thresholds, paths, page names
    ├── state.py              # Session-state defaults and navigation helper
    ├── data.py               # Demo campaigns that seed the marketplace
    ├── ai.py                 # The single place that calls the Gemini API
    ├── styles.py             # Custom CSS (beige and earthy theme)
    ├── sidebar.py            # Profile, API key input and Trust Points balance
    └── views/                # One file per screen
        ├── home.py
        ├── ai_assistant.py
        ├── fundraising.py
        ├── investor_portal.py
        └── adaptive_tracker.py
```

`app.py` stays tiny on purpose: it sets up the page, then hands over to whichever screen is active. To add a new screen, create a file in `groflow/views/` with a `render()` function, give it a name in `config.py`, and register it in the `PAGES` dictionary in `app.py`.

---

## ⚙️ Configuration

Everything you might want to tweak lives in [`groflow/config.py`](groflow/config.py): the Gemini model, starting Trust Points, the vouch cost, the investor-ready threshold, the simulated ROI and investment limits.

---

## 🛠️ Tech Stack

- [Python](https://www.python.org)
- [Streamlit](https://streamlit.io) for the UI
- [pandas](https://pandas.pydata.org) for tables and charts
- [Google Gemini API](https://ai.google.dev) (`gemini-2.5-flash`) for the AI features

---

## 👤 Author

Built by [@lingha2005](https://github.com/lingha2005).
