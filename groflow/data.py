"""Demo data that seeds the marketplace. Everything lives in memory and resets on refresh."""
from groflow.config import IMAGES_DIR


def _image(filename: str) -> str:
    return str(IMAGES_DIR / filename)


SEED_CAMPAIGNS = [
    {
        "name": "EcoWraps",
        "owner": "Sarah S.",
        "desc": "Replacing plastic wrap with organic beeswax sheets.",
        "points": 850,
        "goal": 1000,
        "image": _image("ecowraps.jpg"),
        "funded_by_investors": False,
        "investor_funding": 0,
        "community_vouches": 42,
        "monthly_revenue": 2500,
        "months_in_business": 8,
    },
    {
        "name": "WoodToys",
        "owner": "ToyCraft",
        "desc": "Safe, non-toxic toys made from reclaimed wood.",
        "points": 400,
        "goal": 1000,
        "image": _image("woodtoys.jpg"),
        "funded_by_investors": False,
        "investor_funding": 0,
        "community_vouches": 18,
        "monthly_revenue": 1800,
        "months_in_business": 5,
    },
    {
        "name": "KeralaSpices",
        "owner": "SpiceRoute",
        "desc": "Authentic homemade spice blends from Kerala.",
        "points": 1200,
        "goal": 1000,
        "image": _image("spices.jpg"),
        "funded_by_investors": False,
        "investor_funding": 0,
        "community_vouches": 65,
        "monthly_revenue": 3200,
        "months_in_business": 12,
    },
]
