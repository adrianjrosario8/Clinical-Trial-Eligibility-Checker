from groq import Groq
import streamlit as st
import os

api_key = None

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("API key not found in Streamlit secrets or environment variables")

api_key = api_key.strip()

client = Groq(api_key=api_key)

st.write("API Key Loaded:", bool(api_key))

st.write("Using key:", str(api_key)[:10])


def get_eligibility_response(prompt: str):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a clinical assistant. "
                        "Return only valid JSON. "
                        "Clearly state inclusion, exclusion, decision, and reason."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"ERROR: {str(e)}"
    
    