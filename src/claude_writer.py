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
        f"You are a Pokémon walkthrough writer.\n"
        f"Based on the following snippets from trusted sources, write a detailed, article-style walkthrough "
        f"answering this player question:\n\n"
        f"---\n{user_question}\n---\n\n"
        f"The article should be structured and readable, like a game guide. Include helpful advice, stat, strengths, weaknesses, locations, and strategy where possible. "
        f"At the end, include a reference section with the source links.\n\n"
        f"### Source Material:\n{context}"
    )

    return chat_with_claude(prompt)
