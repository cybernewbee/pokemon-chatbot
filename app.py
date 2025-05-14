import streamlit as st
from utils import image_to_base64
# --- Page config ---
st.set_page_config(
    page_title="Pokémon Chatbot",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# background
bg_base64 = image_to_base64("assets/pixel_bg3.png")

st.markdown(f"""
    <style>
    /* Background image for entire app */
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-repeat: repeat;
        background-size: 720px auto;
        background-attachment: fixed;
    }}

    /* Light overlay to soften the background */
    .light-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.5);
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


# Hide header/title spacing
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
    }
    header, footer, #MainMenu {
        visibility: hidden;
    }
    h1 {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# --- Load images ---
title_img = image_to_base64("assets/pokeinfo_title.png")
walk_img = image_to_base64("assets/walkthrough_button.png")
compare_img = image_to_base64("assets/comparison_button.png")

# --- Display title image with homepage link ---
st.markdown(
    f"""
    <div style="text-align:center;">
        <a href="/" target="_self">
            <img src="data:image/png;base64,{title_img}" width="600">
        </a>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<br>", unsafe_allow_html=True)

# --- Navigation buttons ---
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <a href="/walkthroughs" target="_self">
                <img src="data:image/png;base64,{walk_img}" width="320">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="text-align:center;">
            <a href="/comparisons" target="_self">
                <img src="data:image/png;base64,{compare_img}" width="320">
            </a>
        </div>
        """,
        unsafe_allow_html=True
    )
import os
print("Available pages:")
for f in os.listdir("pages"):
    print(" -", f)

st.markdown("""
    <hr style="margin-top: 3rem; margin-bottom: 1rem;">

    <div style="text-align: center; font-size: 0.9rem; color: gray;">
        © 2025 cybernewbee. All rights reserved. <br>
        Powered by 
        <a href="https://streamlit.io" target="_blank">Streamlit</a>, 
        <a href="https://platform.openai.com" target="_blank">OpenAI</a>, 
        <a href="https://aws.amazon.com/bedrock/" target="_blank">AWS Bedrock</a>, 
        and <a href="https://pokeapi.co" target="_blank">PokéAPI</a>. <br>
        Pokémon is © <a href="https://www.nintendo.com/" target="_blank">Nintendo</a>, 
        <a href="https://www.gamefreak.co.jp/" target="_blank">Game Freak</a>, 
        and <a href="https://www.creatures.co.jp/" target="_blank">Creatures Inc.</a>. <br>
        <a href="https://github.com/cybernewbee/pokemon-chatbot" target="_blank">View source on GitHub</a>
    </div>
""", unsafe_allow_html=True)

