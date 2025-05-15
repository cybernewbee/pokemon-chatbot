from collections import Counter
from typing import List
from src.bedrock_chatbot import chat_with_claude  # Or replace with your own LLM wrapper
import pandas as pd

def get_team_synergy(pokemon_list: List[dict]) -> str:
    """
    Rule-based team synergy analysis.
    Summarizes shared types, offensive strengths, and weaknesses.
    """
    type_strengths = Counter()
    type_weaknesses = Counter()
    all_types = []

    for p in pokemon_list:
        if "error" in p:
            continue
        type_strengths.update(p.get("strong_against", []))
        type_weaknesses.update(p.get("weak_to", []))
        all_types.extend(p.get("types", []))

    top_strong = type_strengths.most_common(3)
    top_weak = type_weaknesses.most_common(3)

    summary = []
    if all_types:
        summary.append("🛡️ **Team Type Composition:** " + ", ".join(sorted(set(all_types))))
    if top_strong:
        summary.append("🗡️ **Strong Against:** " + ", ".join(f"{t} (x{n})" for t, n in top_strong))
    if top_weak:
        summary.append("🔥 **Weak To:** " + ", ".join(f"{t} (x{n})" for t, n in top_weak))

    if any(count >= 3 for _, count in top_weak):
        summary.append("⚠️ Consider adding a Pokémon to cover your team's shared weakness.")

    return "\n\n".join(summary) if summary else "_Not enough data to analyze team._"


def llm_team_synergy_summary(pokemon_list: List[dict]) -> str:
    """
    Uses LLM to generate a narrative team synergy summary.
    """
    prompt = "Analyze the following Pokémon team for type coverage, synergy, shared weaknesses, and give suggestions to improve balance.\n\n"

    for p in pokemon_list:
        if "error" in p:
            continue
        prompt += f"- {p['name']} (Types: {', '.join(p['types'])})\n"
        prompt += f"  • Strong Against: {', '.join(p.get('strong_against', []))}\n"
        prompt += f"  • Weak To: {', '.join(p.get('weak_to', []))}\n\n"

    prompt += "Now summarize this team using natural language with clear suggestions."

    try:
        return chat_with_claude(prompt)
    except Exception as e:
        return f"_LLM summary failed: {e}_"

all_types = ['normal', 'fire', 'water', 'electric', 'grass', 'ice', 'fighting', 'poison', 'ground',
             'flying', 'psychic', 'bug', 'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy']

def build_team_defense_matrix(team):
    df = pd.DataFrame(index=[p["name"] for p in team], columns=all_types, data=1.0)
    for p in team:
        for t in p.get("weak_to", []):
            df.loc[p["name"], t] = 2.0
        for t in p.get("resists", []):
            df.loc[p["name"], t] = 0.5
        for t in p.get("immune_to", []):
            df.loc[p["name"], t] = 0.0
    return df

def build_team_offense_matrix(team):
    df = pd.DataFrame(index=[p["name"] for p in team], columns=all_types, data=1.0)
    for p in team:
        for t in p.get("strong_against", []):
            df.loc[p["name"], t] = 2.0
        for t in p.get("not_effective_against", []):
            df.loc[p["name"], t] = 0.5
        for t in p.get("no_effect_against", []):
            df.loc[p["name"], t] = 0.0
    return df
