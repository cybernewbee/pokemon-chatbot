import streamlit as st
import numpy as np
from src.pokeapi import get_pokemon_details
import pandas as pd
import matplotlib.pyplot as plt
from utils import centered_image_html
from utils import image_to_base64
from src.clarify_names import clarify_pokemon_names
from PIL import Image
from src.team_analyzer import (
        get_team_synergy,
        llm_team_synergy_summary,
        build_team_defense_matrix,
        build_team_offense_matrix
    )

import seaborn as sns
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Compare Pokémon",  # 👈 THIS name defines the URL
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("<a name='top'></a>", unsafe_allow_html=True)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; }
    header, h1 { display: none; }
    </style>
""", unsafe_allow_html=True)
# Hide streamlit bar
st.markdown("""
    <style>
    header, footer, #MainMenu {
        visibility: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Background
bg_base64 = image_to_base64("assets/pixel_bg0.png")

st.markdown(f"""
    <style>
    /* Background image for entire app */
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-repeat: repeat;
        background-size: 1024px auto;
        background-attachment: fixed;
    }}

    /* Light overlay to soften the background */
    .light-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.6);
        z-index: 0;
    }}

    /* Make sure all content appears above the overlay */
    .main > div {{
        position: relative;
        z-index: 1;
    }}
    </style>
    <div class="light-overlay"></div>
""", unsafe_allow_html=True)

# Render pixel-art title, centered
st.markdown(centered_image_html("assets/comparison_title.png", width=700), unsafe_allow_html=True)

home_icon_b64 = image_to_base64("assets/back_to_home.png")
walkthrough_icon_b64 = image_to_base64("assets/to_walkthrough.png")

st.markdown(f"""
    <style>
    .top-button-bar {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-top: 40px;
        padding: 0 50px;
    }}
    .top-button-bar img {{
        width: 150px;
        height: auto;
        cursor: pointer;
    }}
    </style>

    <div class="top-button-bar">
        <a href="/" target="_self">
            <img src="data:image/png;base64,{home_icon_b64}" alt="Home">
        </a>
        <a href="/walkthroughs" target="_self">
            <img src="data:image/png;base64,{walkthrough_icon_b64}" alt="Walkthrough">
        </a>
    </div>
""", unsafe_allow_html=True)

# Two taps
tab1, tab2 = st.tabs(["Compare Two Pokémon", "Team Analyzer"])
with tab1:

    if "last_compare" not in st.session_state:
        st.session_state.last_compare = ("", "")
        st.session_state.p1 = None
        st.session_state.p2 = None
    
    col1, col2 = st.columns(2)

    with col1:
        pokemon_1 = st.text_input("Enter first Pokémon name:", key="poke1")
    with col2:
        pokemon_2 = st.text_input("Enter second Pokémon name:", key="poke2")

    pokemon_1 = pokemon_1.strip().lower() if pokemon_1 else ""
    pokemon_2 = pokemon_2.strip().lower() if pokemon_2 else ""
    

    if (pokemon_1, pokemon_2) != st.session_state.last_compare:
        st.session_state.last_compare = (pokemon_1, pokemon_2)
        with st.spinner("Fetching Pokémon data..."):
            st.session_state.p1 = get_pokemon_details(pokemon_1) if pokemon_1 else None
            st.session_state.p2 = get_pokemon_details(pokemon_2) if pokemon_2 else None

        # Use local refs for rendering
    p1 = st.session_state.p1
    p2 = st.session_state.p2

    if p1 and "error" in p1:
        col1.error(p1["error"])
    if p2 and "error" in p2:
        col2.error(p2["error"])

    if p1 and "error" not in p1:
        col1.image(p1["sprites"].get("official_artwork"), caption=p1["name"])
        col1.subheader("Type")
        col1.write(", ".join(p1.get("types", [])))
        col1.subheader("Strengths & Weaknesses")
        strong = p1.get("strong_against", [])
        weak = p1.get("weak_to", [])
        if strong:
            col1.markdown(f"🗡️ **Strong Against:** {', '.join(strong)}")
        if weak:
            col1.markdown(f"🔥 **Weak To:** {', '.join(weak)}")

        col1.subheader("Abilities")
        for a in p1.get("abilities", []):
            col1.write(f"• {a}")
        col1.subheader("Base Stats")
        for stat, val in p1.get("stats", {}).items():
            col1.write(f"{stat.title()}: {val}")
        col1.subheader("Evolution Chain")
        for chain in p1.get("evolution_chain", []):
            col1.write(chain)
        col1.subheader("Games")
        col1.write(", ".join(p1.get("associated_games", [])))
        col1.subheader("Cry")
        col1.audio(p1.get("cry_url"))

    if p2 and "error" not in p2:
        col2.image(p2["sprites"].get("official_artwork"), caption=p2["name"])
        col2.subheader("Type")
        col2.write(", ".join(p2.get("types", [])))
        col2.subheader("Strengths & Weaknesses")
        strong = p2.get("strong_against", [])
        weak = p2.get("weak_to", [])
        if strong:
            col2.markdown(f"🗡️ **Strong Against:** {', '.join(strong)}")
        if weak:
            col2.markdown(f"🔥 **Weak To:** {', '.join(weak)}")
        col2.subheader("Abilities")
        for a in p2.get("abilities", []):
            col2.write(f"• {a}")
        col2.subheader("Base Stats")
        for stat, val in p2.get("stats", {}).items():
            col2.write(f"{stat.title()}: {val}")
        col2.subheader("Evolution Chain")
        for chain in p2.get("evolution_chain", []):
            col2.write(chain)
        col2.subheader("Games")
        col2.write(", ".join(p2.get("associated_games", [])))
        col2.subheader("Cry")
        col2.audio(p2.get("cry_url"))

    def plot_radar_chart(p1, p2, labels):
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        if p1 and "error" not in p1:
            p1_values = [p1["stats"].get(stat, 0) for stat in labels] + [p1["stats"].get(labels[0], 0)]
            ax.plot(angles, p1_values, label=p1["name"], color="blue")
            ax.fill(angles, p1_values, alpha=0.25, color="blue")

        if p2 and "error" not in p2:
            p2_values = [p2["stats"].get(stat, 0) for stat in labels] + [p2["stats"].get(labels[0], 0)]
            ax.plot(angles, p2_values, label=p2["name"], color="green")
            ax.fill(angles, p2_values, alpha=0.25, color="green")

        if (p1 and "error" not in p1) or (p2 and "error" not in p2):
            ax.set_title("Radar Chart - Base Stats")
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels([s.title() for s in labels])
            ax.set_yticklabels([])
            ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
            st.pyplot(fig)

    # Only call chart if at least one is valid
    if (p1 and "error" not in p1) or (p2 and "error" not in p2):
        st.subheader("Radar Chart Comparison")
        stat_order = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        plot_radar_chart(p1, p2, stat_order)
# Divider

with tab2:
    st.markdown("Enter up to 6 Pokémon to evaluate team synergy.")

    # Initialize session state
    if "last_team_input" not in st.session_state:
        st.session_state.last_team_input = ""
        st.session_state.team_data = []
        st.session_state.team_names = []

    team_input = st.text_input(
        "Team Pokémon (comma-separated):",
        value=st.session_state.last_team_input,
        placeholder="e.g. Gardevoir, Metagross, Salamence"
    )
    if team_input != st.session_state.last_team_input:
        st.session_state.last_team_input = team_input

        team_names = [name.strip().lower() for name in team_input.split(",") if name.strip()]
        if 1 <= len(team_names) <= 6:
            clarified_names = clarify_pokemon_names(team_names)
            with st.spinner("Analyzing team..."):
                st.session_state.team_data = [get_pokemon_details(name) for name in clarified_names]
                st.session_state.team_names = clarified_names
        else:
            st.warning("Please enter 1 to 6 valid Pokémon names.")
    
    if st.session_state.team_data:
    # Analyzer block
        def style_matrix(df):
            def color_cell(val):
                if val == 2.0:
                    return "background-color: #ffcccc"  # red for weakness
                elif val == 0.5:
                    return "background-color: #ccffcc"  # green for resist
                elif val == 0.0:
                    return "background-color: #dddddd"  # gray for immune
                else:
                    return ""
            return df.style.applymap(color_cell)

        st.markdown("Rule-Based Team Summary")
        st.markdown(get_team_synergy(st.session_state.team_data))

        st.markdown("Team Strength Summary")
        st.markdown(llm_team_synergy_summary(st.session_state.team_data))

        st.markdown("Team Defense Matrix")
        df_def = build_team_defense_matrix(st.session_state.team_data)
        styled_df_def = style_matrix(df_def)
        st.dataframe(styled_df_def, use_container_width=True)
        

        st.markdown("Team Offense Matrix")
        df_off = build_team_offense_matrix(st.session_state.team_data)
        styled_df_off = style_matrix(df_off)
        st.dataframe(styled_df_off, use_container_width=True)
    

# Inject floating buttons via HTML/CSS
st.markdown("""
    <style>
    .scroll-top-btn {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        background-color: white;
        color: black;
        padding: 10px 20px;
        border-radius: 10px;
        font-weight: bold;
        border: 1px solid #ccc;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
        cursor: pointer;
        z-index: 9999;
    }
    </style>

    <a href="#top" class="scroll-top-btn">⬆️ Top</a>
""", unsafe_allow_html=True)

# Add the scroll anchor at the top of your page
st.markdown("<a name='top'></a>", unsafe_allow_html=True)






