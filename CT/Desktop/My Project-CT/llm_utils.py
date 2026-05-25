import streamlit as st
import google.generativeai as genai

genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", ""))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_eligibility_response(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"ERROR: {str(e)}"
