"""Everything that talks to the Gemini API lives here (and nowhere else)."""
import requests

from groflow.config import GEMINI_ENDPOINT, GEMINI_MODEL, GEMINI_TIMEOUT_SECONDS


class GeminiError(Exception):
    """Raised with a friendly, ready-to-display message when a Gemini call fails."""


def ask_gemini(prompt: str, api_key: str) -> str:
    """Send a prompt to Gemini and return the text of its reply.

    Raises GeminiError (with a user-friendly message) if anything goes wrong.
    """
    url = GEMINI_ENDPOINT.format(model=GEMINI_MODEL)
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key.strip(),  # header keeps the key out of URLs and logs
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(
            url, headers=headers, json=payload, timeout=GEMINI_TIMEOUT_SECONDS
        )
    except requests.RequestException as exc:
        raise GeminiError(f"⚠️ Connection failed: {exc}") from exc

    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError, ValueError) as exc:
            raise GeminiError(
                "⚠️ Gemini sent back an unexpected response. Please try again."
            ) from exc
    if response.status_code == 400:
        raise GeminiError("⚠️ Invalid API key (Error 400). Please check for spaces.")
    if response.status_code == 429:
        raise GeminiError("⏳ Too many requests. Wait 60 seconds.")
    raise GeminiError(f"⚠️ Google error {response.status_code}: {response.text}")
