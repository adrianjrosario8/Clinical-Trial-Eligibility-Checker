from groq import Groq
import streamlit as st
import os

try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)


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