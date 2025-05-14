from langchain.tools import tool
import requests

@tool
def get_pokemon_details(name: str) -> dict:
    """
    Retrieve detailed information about a specific Pokémon, including its evolution chain,
    location encounters, characteristics, associated games, and sprite images.
    Returns a dictionary suitable for rendering in Streamlit.
    """
    base_url = "https://pokeapi.co/api/v2"
    name = name.lower()
    result = {"name": name.title()}

    # Fetch basic Pokémon data
    pokemon_url = f"{base_url}/pokemon/{name}"
    response = requests.get(pokemon_url)
    if response.status_code != 200:
        result["error"] = f"Pokémon '{name}' not found."
        return result
    pokemon_data = response.json()

    # Extract sprite URLs
    sprites = pokemon_data.get('sprites', {})
    result["sprites"] = {
        "front_default": sprites.get('front_default'),
        "back_default": sprites.get('back_default'),
        "front_shiny": sprites.get('front_shiny'),
        "back_shiny": sprites.get('back_shiny'),
        "official_artwork": sprites.get('other', {}).get('official-artwork', {}).get('front_default')
    }

    # Fetch species data for evolution chain and characteristics
    species_url = pokemon_data['species']['url']
    species_response = requests.get(species_url)
    if species_response.status_code != 200:
        result["error"] = f"Species data for '{name}' not found."
        return result
    species_data = species_response.json()

    # Types
    types = [t["type"]["name"] for t in pokemon_data.get("types", [])]
    result["types"] = types

    # Evolution chain
    evolution_chain_url = species_data['evolution_chain']['url']
    evolution_response = requests.get(evolution_chain_url)
    if evolution_response.status_code != 200:
        result["evolution_chain"] = "No evolution chain data available."
    else:
        evolution_data = evolution_response.json()
        def parse_evolution(chain):
            evolutions = []

            def traverse(node, path):
                species_name = node['species']['name']
                current_path = path + [species_name]
                if not node['evolves_to']:
                    evolutions.append(current_path)
                else:
                    for next_evolution in node['evolves_to']:
                        traverse(next_evolution, current_path)

            traverse(chain, [])
            return evolutions

        evolution_paths = parse_evolution(evolution_data['chain'])
        result["evolution_chain"] = [" → ".join(path) for path in evolution_paths]

    # Location encounters
    encounters_url = f"{base_url}/pokemon/{name}/encounters"
    encounters_response = requests.get(encounters_url)
    if encounters_response.status_code == 200:
        encounters_data = encounters_response.json()
        locations = [encounter['location_area']['name'] for encounter in encounters_data]
        result["location_encounters"] = locations if locations else ["No known locations."]
    else:
        result["location_encounters"] = ["No known locations."]

    # Abilities
    abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]
    result["abilities"] = abilities

    # Associated games
    games = [game['version']['name'] for game in pokemon_data['game_indices']]
    result["associated_games"] = list(set(games))  # Remove duplicates

    # Base Stats
    stats = {}
    for stat_entry in pokemon_data.get("stats", []):
        stat_name = stat_entry["stat"]["name"]
        stat_value = stat_entry["base_stat"]
        stats[stat_name] = stat_value
    result["stats"] = stats

    # Get weaknesses and strengths from type data
    damage_relations = {
        "weak_to": set(),
        "strong_against": set()
    }

    for type_name in types:
        type_url = f"{base_url}/type/{type_name}"
        r = requests.get(type_url)
        if r.status_code != 200:
            continue
        type_data = r.json()

        for entry in type_data["damage_relations"]["double_damage_from"]:
            damage_relations["weak_to"].add(entry["name"])
        for entry in type_data["damage_relations"]["double_damage_to"]:
            damage_relations["strong_against"].add(entry["name"])

    result["weak_to"] = sorted(damage_relations["weak_to"])
    result["strong_against"] = sorted(damage_relations["strong_against"])

    # Cry
    result["cry_url"] = f"https://play.pokemonshowdown.com/audio/cries/{name.lower()}.ogg"

    return result

