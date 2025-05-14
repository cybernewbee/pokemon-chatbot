import os
from dotenv import load_dotenv
import streamlit as st

# Load local .env if it exists
load_dotenv()

def get_env_var(key: str, default: str = "") -> str:
    # Prefer Streamlit Secrets if available
    if key in st.secrets:
        return st.secrets[key]
    return os.getenv(key, default)
