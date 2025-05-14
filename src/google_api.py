import requests
from src.config import get_env_var

GOOGLE_API_KEY = get_env_var("GOOGLE_API_KEY")
CX_ID = get_env_var("GOOGLE_CX_ID")


def search_walkthrough(game_name: str, topic: str, num_results: int = 5) -> list:
    """
    Search Google for game walkthroughs using Programmable Search Engine.
    Returns a list of dictionaries with title, snippet, and link.
    """
    if not GOOGLE_API_KEY or not CX_ID:
        raise ValueError("Missing GOOGLE_API_KEY or GOOGLE_CSE_ID in environment variables.")

    query = f"{game_name} {topic} site:gamefaqs.gamespot.com OR site:ign.com OR site:bulbapedia.bulbagarden.net"
    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": GOOGLE_API_KEY,
        "cx": CX_ID,
        "q": query,
        "num": num_results,
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Google API error: {response.status_code} - {response.text}")

    results = response.json().get("items", [])
    return [
        {
            "title": item.get("title"),
            "snippet": item.get("snippet"),
            "link": item.get("link")
        }
        for item in results
    ]





