# src/reverse_lookup.py
import requests

def reverse_lookup_pokemon_name(local_name: str, lang_code: str = "zh-Hans") -> str:
    """
    Attempts to match a localized Pokémon name (e.g. '皮卡丘') to its English name
    by scanning all species entries and comparing localized name entries.
    
    lang_code options:
        - 'zh-Hans' → Simplified Chinese
        - 'zh-Hant' → Traditional Chinese
        - 'ja' → Japanese
        - 'en' → English
    """
    species_base_url = "https://pokeapi.co/api/v2/pokemon-species/"
    
    for i in range(1, 1026):  # ~1025 Pokémon as of Gen 9
        try:
            response = requests.get(f"{species_base_url}{i}/")
            if response.status_code != 200:
                continue
            data = response.json()
            for name_entry in data.get("names", []):
                if name_entry["language"]["name"] == lang_code and name_entry["name"] == local_name:
                    # Return the canonical English name
                    for entry in data["names"]:
                        if entry["language"]["name"] == "en":
                            return entry["name"].lower()
        except Exception:
            continue

    return None  # Not found
