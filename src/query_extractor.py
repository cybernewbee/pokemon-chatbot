import json
from src.bedrock_chatbot import chat_with_claude

def extract_query_fields(user_query: str) -> dict:
    """
    Extract structured fields from a user's Pokémon-related query using Claude.
    Returns a dict with keys: game, pokemon, intent.
    """
    prompt = (
        "You are a Pokémon search assistant.\n"
        "Extract the following information from the user's query:\n"
        "- game: the Pokémon game mentioned (e.g., Pokémon Emerald)\n"
        "- pokemon: the Pokémon mentioned\n"
        "- intent: what the user wants to do (e.g., how to catch, where to find, moves, stats, type, strength, weaknesses, etc.)\n\n"
        "Return a JSON object ONLY with these keys.\n\n"
        f"User query: {user_query}"
    )

    try:
        response_text = chat_with_claude(prompt)
        return json.loads(response_text.strip())
    except Exception as e:
        return {"error": str(e)}
