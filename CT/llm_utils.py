import os

from groq import Groq
from dotenv import load_dotenv
import streamlit as st


load_dotenv()

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. "
        "Set it in environment variables or Streamlit secrets."
    )

client = Groq(api_key=api_key)


def get_eligibility_response(prompt):

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,
        max_tokens=256
    )

    return response.choices[0].message.content