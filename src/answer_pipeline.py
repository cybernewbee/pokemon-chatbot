from src.query_extractor import extract_query_fields
from src.google_api import search_walkthrough
from src.pokeapi import get_pokemon_details
from src.claude_writer import generate_walkthrough_article
from langdetect import detect
from src.reverse_lookup import reverse_lookup_pokemon_name
from src.clarify_names import clarify_pokemon_names

def answer_query(user_input: str) -> dict:
    """
    Master function that:
    1. Extracts structured fields from a user prompt
    2. Searches Google for walkthroughs
    3. Fetches Pokémon spec data from PokéAPI (if valid)
    Returns a combined dict.
    """
    # Step 1: Extract game, intent, and (maybe) Pokémon
    fields = extract_query_fields(user_input)
    if "error" in fields:
        return {"error": f"Keyword extraction failed: {fields['error']}"}

    game = fields.get("game")
    intent = fields.get("intent")

    pokemon = fields.get("pokemon")
    # Normalize to list
    if isinstance(pokemon, str):
        pokemon_list = [pokemon]
    elif isinstance(pokemon, list):
        pokemon_list = pokemon
    else:
        pokemon_list = []

    # 🧠 LLM clarification should happen AFTER extracting game + intent,
    # to ensure `fields` is fully processed before mutation.
    pokemon_list = clarify_pokemon_names(pokemon_list)

    # Step 2: Search walkthroughs using game + intent
    walkthroughs = []
    walkthrough_article = ""

    if game or intent:
        try:
            walkthroughs = search_walkthrough(game or "", intent or "")
        except Exception as e:
            print(f"[WARN] Google search failed: {e}")
            walkthroughs = []

        if walkthroughs:
            try:
                # If Pokémon names were clarified, rewrite the original query
                original_pokemon = fields.get("pokemon", [])
                clarified_query = user_input

                if isinstance(original_pokemon, str):
                    original_pokemon = [original_pokemon]

                # Attempt replacement only if both lists match length and differ
                if original_pokemon and len(original_pokemon) == len(pokemon_list):
                    for original, fixed in zip(original_pokemon, pokemon_list):
                        if original != fixed:
                            clarified_query = clarified_query.replace(original, fixed)

                # Generate article using clarified input
                walkthrough_article = generate_walkthrough_article(clarified_query, walkthroughs)
            except Exception as e:
                walkthrough_article = f"Failed to generate article: {e}"

    # Step 3: Normalize and fetch Pokémon info
    pokemon_list = []
    if isinstance(pokemon, str):
        pokemon_list = [pokemon]
    elif isinstance(pokemon, list):
        pokemon_list = pokemon

    pokemon_info = []
    for name in pokemon_list:
        if not name or name.lower() == "none":
            continue

        try:
            lang = detect(name)
            lang_map = {
                "zh-cn": "zh-Hans",
                "zh-tw": "zh-Hant",
                "ja": "ja"
            }
            lang_code = lang_map.get(lang)
            if lang_code:
                canonical = reverse_lookup_pokemon_name(name, lang_code=lang_code)
                if canonical:
                    name = canonical.lower()
        except Exception as e:
            print(f"[WARN] Language detection failed for '{name}': {e}")

        try:
            info = get_pokemon_details(name)
            pokemon_info.append(info)
        except Exception as e:
            pokemon_info.append({"error": f"Failed to fetch Pokémon info for {name}: {e}"})

    if not pokemon_info:
        pokemon_info = [{"error": "No specific Pokémon mentioned in the question."}]

    # Step 4: Return combined results
    return {
        "query_fields": fields,
        "walkthrough_results": walkthroughs,
        "walkthrough_article": walkthrough_article,
        "pokemon_info": pokemon_info
    }
