from src.bedrock_chatbot import chat_with_claude

def clarify_pokemon_names(pokemon_list: list[str]) -> list[str]:
    """
    Uses LLM to correct or confirm Pokémon names from user input.
    Returns a list of validated canonical names.
    """
    prompt = (
        "You're a Pokémon name resolver.\n"
        "The user may have made typos or used non-English names.\n"
        "For each name, return the corrected or best-match English name from the mainline Pokémon franchise.\n\n"
        f"User input Pokémon names: {pokemon_list}\n\n"
        "Return ONLY a JSON list of fixed names, like this:\n"
        "[\"gardevoir\", \"beldum\"]"
    )

    try:
        response = chat_with_claude(prompt)
        fixed = eval(response.strip())
        if isinstance(fixed, list):
            return fixed
    except Exception as e:
        print(f"[ERROR] Name clarification failed: {e}")
    
    return pokemon_list  # fallback to original
