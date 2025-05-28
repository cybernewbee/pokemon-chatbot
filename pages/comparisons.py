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

st.set_page_config(
    page_title="Compare Pokémon",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Background and styling
bg_base64 = image_to_base64("assets/pixel_bg0.png")
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-repeat: repeat;
        background-size: 1024px auto;
        background-attachment: fixed;
    }}
    .light-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.6);
        z-index: 0;
    }}
    .main > div {{
        position: relative;
        z-index: 1;
    }}
    .block-container {{ padding-top: 1rem; }}
    header, footer, #MainMenu {{ visibility: hidden; }}
    </style>
    <div class="light-overlay"></div>
""", unsafe_allow_html=True)

home_icon_b64 = image_to_base64("assets/back_to_home.png")
walkthrough_icon_b64 = image_to_base64("assets/to_walkthrough.png")
st.markdown(f"""
    <style>
    .page-nav {{
        display: flex;
        justify-content: space-between;
        margin-top: 0px;
        margin-bottom: 1rem;
    }}
    .page-nav img {{
        width: 150px;
        height: auto;
        cursor: pointer;
    }}
    </style>
    <div class="page-nav">
        <a href="/" target="_self">
            <img src="data:image/png;base64,{home_icon_b64}" alt="Home">
        </a>
        <a href="/walkthroughs" target="_self">
            <img src="data:image/png;base64,{walkthrough_icon_b64}" alt="Walkthrough">
        </a>
    </div>
""", unsafe_allow_html=True)

st.markdown(centered_image_html("assets/comparison_title.png", width=700), unsafe_allow_html=True)

# === Tab control using radio bound to session_state ===
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Compare Two Pokémon"

st.radio(
    "Choose a mode:",
    ["Compare Two Pokémon", "Team Analyzer"],
    key="active_tab",
    index=0 if st.session_state.active_tab == "Compare Two Pokémon" else 1
)

# === Compare Two Pokémon ===
if st.session_state.active_tab == "Compare Two Pokémon":
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

    p1 = st.session_state.p1
    p2 = st.session_state.p2

    for poke, col in zip([p1, p2], [col1, col2]):
        if poke and "error" in poke:
            col.error(poke["error"])
        elif poke:
            col.image(poke["sprites"].get("official_artwork"), caption=poke["name"])
            col.subheader("Type")
            col.write(", ".join(poke.get("types", [])))
            col.subheader("Strengths & Weaknesses")
            strong = poke.get("strong_against", [])
            weak = poke.get("weak_to", [])
            if strong:
                col.markdown(f"🗡️ **Strong Against:** {', '.join(strong)}")
            if weak:
                col.markdown(f"🔥 **Weak To:** {', '.join(weak)}")
            col.subheader("Abilities")
            for a in poke.get("abilities", []):
                col.write(f"• {a}")
            col.subheader("Base Stats")
            for stat, val in poke.get("stats", {}).items():
                col.write(f"{stat.title()}: {val}")
            col.subheader("Evolution Chain")
            for chain in poke.get("evolution_chain", []):
                col.write(chain)
            col.subheader("Games")
            col.write(", ".join(poke.get("associated_games", [])))
            col.subheader("Cry")
            col.audio(poke.get("cry_url"))

    def plot_radar_chart(p1, p2, labels):
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        angles += angles[:1]
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        for poke, color in zip([p1, p2], ["blue", "green"]):
            if poke and "error" not in poke:
                values = [poke["stats"].get(stat, 0) for stat in labels] + [poke["stats"].get(labels[0], 0)]
                ax.plot(angles, values, label=poke["name"], color=color)
                ax.fill(angles, values, alpha=0.25, color=color)

        ax.set_title("Radar Chart - Base Stats")
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([s.title() for s in labels])
        ax.set_yticklabels([])
        ax.legend(loc="upper right", bbox_to_anchor=(1.2, 1.1))
        st.pyplot(fig)

    if (p1 and "error" not in p1) or (p2 and "error" not in p2):
        st.subheader("Radar Chart Comparison")
        stat_order = ["hp", "attack", "defense", "special-attack", "special-defense", "speed"]
        plot_radar_chart(p1, p2, stat_order)

# === Team Analyzer ===
elif st.session_state.active_tab == "Team Analyzer":
    if "last_team_input" not in st.session_state:
        st.session_state.last_team_input = ""
        st.session_state.team_data = []
        st.session_state.team_names = []
    if "input_box" not in st.session_state:
        st.session_state.input_box = ""

    def update_team_input():
        team_input = st.session_state.input_box
        st.session_state.last_team_input = team_input

        team_names = [name.strip().lower() for name in team_input.split(",") if name.strip()]
        if 1 <= len(team_names) <= 6:
            clarified_names = clarify_pokemon_names(team_names)
            with st.spinner("Analyzing team..."):
                st.session_state.team_data = [get_pokemon_details(name) for name in clarified_names]
                st.session_state.team_names = clarified_names
        else:
            st.warning("Please enter 1 to 6 valid Pokémon names.")

    st.text_input(
        "Team Pokémon (comma-separated):",
        key="input_box",
        value=st.session_state.last_team_input,
        placeholder="e.g. Gardevoir, Metagross, Salamence",
        on_change=update_team_input
    )

    if st.session_state.team_data:
        def style_matrix(df):
            def color_cell(val):
                if val == 2.0:
                    return "background-color: #ffcccc"
                elif val == 0.5:
                    return "background-color: #ccffcc"
                elif val == 0.0:
                    return "background-color: #dddddd"
                else:
                    return ""
            return df.style.applymap(color_cell)

        with st.spinner("Analyzing team synergy and coverage..."):
            st.markdown("Rule-Based Team Summary")
            st.markdown(get_team_synergy(st.session_state.team_data))

            st.markdown("Team Strength Summary")
            st.markdown(llm_team_synergy_summary(st.session_state.team_data))

            st.markdown("Team Defense Matrix")
            df_def = build_team_defense_matrix(st.session_state.team_data)
            st.dataframe(style_matrix(df_def), use_container_width=True)

            st.markdown("Team Offense Matrix")
            df_off = build_team_offense_matrix(st.session_state.team_data)
            st.dataframe(style_matrix(df_off), use_container_width=True)

# Floating scroll-to-top button
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

st.markdown("<a name='top'></a>", unsafe_allow_html=True)
