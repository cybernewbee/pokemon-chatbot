import streamlit as st
from src.answer_pipeline import answer_query
from utils import centered_image_html
from utils import image_to_base64
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(
    page_title="Walkthrough Assistant",  # 👈 THIS name defines the URL
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.markdown("<a name='top'></a>", unsafe_allow_html=True)

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
st.markdown(centered_image_html("assets/walkthrough_title.png", width=700), unsafe_allow_html=True)

home_icon_b64 = image_to_base64("assets/back_to_home.png")
compare_icon_b64 = image_to_base64("assets/to_compare.png")

st.markdown(f"""
    <style>
    .scrolling-nav {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
        padding: 0 40px;
        margin-top: -3.5rem;
        margin-bottom: 2rem;
    }}
    .scrolling-nav img {{
        width: 150px;
        height: auto;
        cursor: pointer;
    }}
    </style>

    <div class="scrolling-nav">
        <a href="/" target="_self">
            <img src="data:image/png;base64,{home_icon_b64}" alt="Home">
        </a>
        <a href="/walkthroughs" target="_self">
            <img src="data:image/png;base64,{compare_icon_b64}" alt="Walkthrough">
        </a>
    </div>
""", unsafe_allow_html=True)

with st.container():
    # Initialize state keys if needed
    if "last_query" not in st.session_state:
        st.session_state.last_query = ""
    if "result" not in st.session_state:
        st.session_state.result = None
    user_input = st.text_input(
        "Ask a question (e.g., 'Where do I catch Ralts and Beldum in Emerald?')",
        value=st.session_state.last_query,
    )
    
    if user_input != st.session_state.last_query:
        st.session_state.last_query = user_input
        with st.spinner("Thinking..."):
            st.session_state.result = answer_query(user_input)
    result = st.session_state.result
    if result:
        if "error" in result:
            st.error(result["error"])
        else:
            query_fields = result.get("query_fields", {})
            walkthroughs = result.get("walkthrough_results", [])
            walkthrough_article = result.get("walkthrough_article", "")
            pokemon_info_list = result.get("pokemon_info", [])

            #st.subheader("🧠 Extracted Query Fields")
            #st.json(query_fields)

            st.subheader("Walkthroughs")
            if walkthroughs:
                for item in walkthroughs:
                    st.markdown(f"**[{item['title']}]({item['link']})**\n\n{item['snippet']}")
            else:
                st.info("No walkthroughs found.")

            if walkthrough_article:
                st.subheader("Walkthrough Guide")
                st.markdown(walkthrough_article)

            st.markdown("---")


# Scroll-to-top floating button
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

    <a href="#top" class="scroll-top-btn">Back to Top</a>
""", unsafe_allow_html=True)

st.markdown("<a name='top'></a>", unsafe_allow_html=True)
