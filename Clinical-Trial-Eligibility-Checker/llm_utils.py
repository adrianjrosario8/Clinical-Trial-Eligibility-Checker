import os
from groq import Groq
import streamlit as st


try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Please set it in environment variables or Streamlit secrets.")

client = Groq(api_key=api_key)