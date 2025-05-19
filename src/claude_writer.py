# src/claude_writer.py
from src.bedrock_chatbot import chat_with_claude

def generate_walkthrough_article(user_question: str, sources: list) -> str:
    """
    Given a user query and search results (titles/snippets/links),
    generate a long-form walkthrough article using Claude.
    """
    context_blocks = []
    for s in sources:
        title = s.get("title", "")
        snippet = s.get("snippet", "")
        link = s.get("link", "")
        context_blocks.append(f"### {title}\n{snippet}\nSource: {link}")

    context = "\n\n".join(context_blocks)
    
    prompt = (
        "You are a professional Pokémon walkthrough writer.\n\n"
        "Using the following snippets from trusted sources, write a clear, step-by-step game guide that answers this player question:\n"
        f"---\n{user_question}\n---\n\n"
        "Structure the answer like a walkthrough article. Be specific, not generic. Mention exact locations, route numbers, event triggers, battle tips, stats, and strategic advice.\n"
        "Avoid speculation unless clearly noted. Add context if helpful (e.g., evolution requirements, game version differences).\n\n"
        "### Source Material:\n"
        f"{context}\n\n"
        "At the end, include a 'References' section with the source links."
    )

    return chat_with_claude(prompt)
