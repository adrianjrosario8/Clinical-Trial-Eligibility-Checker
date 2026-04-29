import streamlit as st
from llm_utils import get_eligibility_response


def rule_engine(p):
    reasons = []

    if p["diagnosis"] != "Type 2":
        reasons.append("Diabetes type is not Type 2")

    if p["heart_failure"] == "Yes":
        reasons.append("Heart failure present")

    if p["infection"] == "Yes":
        reasons.append("Infection present")

    if p["lung_disease"] == "Yes":
        reasons.append("Lung disease present")

    return reasons

def build_prompt(p, reasons):
    return f"""
Patient evaluation summary:

Age: {p['age']}
Diagnosis: {p['diagnosis']}
Glucose: {p['glucose']}
BMI: {p['bmi']}

Exclusion reasons detected:
{", ".join(reasons) if reasons else "None"}

Based on this, explain briefly why the patient is eligible or not eligible.
"""

def evaluate_with_llm(prompt):
    return get_eligibility_response(prompt)


st.title("🧪 Clinical Trial Eligibility Checker")

age = st.number_input("Age", 0, 120, 40)
diagnosis = st.selectbox("Diagnosis", ["Type 2", "Type 1", "Gestational"])
glucose = st.number_input("Glucose", 120)
bmi = st.number_input("BMI", 25.0)
hf = st.selectbox("Heart Failure", ["No", "Yes"])
inf = st.selectbox("Infection", ["No", "Yes"])
lung = st.selectbox("Lung Disease", ["No", "Yes"])


if st.button("Check Eligibility"):

    patient = {
        "age": age,
        "diagnosis": diagnosis,
        "glucose": glucose,
        "bmi": bmi,
        "heart_failure": hf,
        "infection": inf,
        "lung_disease": lung
    }

    st.markdown("### 🧾 Patient Summary")

    st.write(f"Age: {age}")
    st.write(f"Diagnosis: {diagnosis}")
    st.write(f"Glucose: {glucose}")
    st.write(f"BMI: {bmi}")
    st.write(f"Heart Failure: {hf}")
    st.write(f"Infection: {inf}")
    st.write(f"Lung Disease: {lung}")


    reasons = rule_engine(patient)

    eligible = len(reasons) == 0

    prompt = build_prompt(patient, reasons)

    explanation = evaluate_with_llm(prompt)

    
    st.markdown("### 📊 Result")

    if eligible:
        st.success("ELIGIBLE")
    else:
        st.error("NOT ELIGIBLE")

    st.write("Reason:")
    st.write(explanation)

    st.write("Inclusion Check:", "PASS" if eligible else "FAIL")
    st.write("Exclusion Check:", "NO" if eligible else "YES")
    st.write("Confidence:", "100")