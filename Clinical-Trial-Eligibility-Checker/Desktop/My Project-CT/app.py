import streamlit as st
import json
from llm_utils import get_eligibility_response


def build_prompt(p):
    return f"""
Check eligibility:

Inclusion:
- Age >= 19
- Type 2 Diabetes
- Glucose <= 270
- BMI 18.5-40

Exclusion:
- Type 1 or gestational diabetes
- Severe heart failure
- Severe infection
- Lung disease

Patient:
Age: {p['age']}
Diagnosis: {p['diagnosis']}
Glucose: {p['glucose']}
BMI: {p['bmi']}
Heart Failure: {p['heart_failure']}
Infection: {p['infection']}
Lung Disease: {p['lung_disease']}

Return JSON:
{{
  "inclusion_check": "PASS/FAIL",
  "exclusion_check": "YES/NO",
  "decision": "ELIGIBLE or NOT_ELIGIBLE",
  "reason": "1 line explanation (not empty)"
}}
"""


st.title("Clinical Trial Eligibility Checker")

age = st.number_input("Age", 0, 100, 40)
diabetes = st.selectbox("Diabetes Type", ["Type 2", "Type 1", "Gestational"])
glucose = st.number_input("Glucose (mg/dL)", value=120)
bmi = st.number_input("BMI", value=25.0)
hf = st.selectbox("Heart Failure?", ["No", "Yes"])
inf = st.selectbox("Infection?", ["No", "Yes"])
lung = st.selectbox("Lung Disease?", ["No", "Yes"])


if st.button("Check Eligibility"):

    patient = {
        "age": age,
        "diagnosis": diabetes,
        "glucose": glucose,
        "bmi": bmi,
        "heart_failure": hf,
        "infection": inf,
        "lung_disease": lung
    }

    with st.spinner("Checking eligibility..."):
        result = get_eligibility_response(build_prompt(patient))

    st.subheader("Result")

    if result.startswith("ERROR"):
        if "quota" in result.lower():
            st.warning("⚠️ API limit reached. Please try again in a few seconds.")
        else:
            st.error(result)
    else:
        try:
            clean = result.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean)

            inclusion = data.get("inclusion_check", "")
            exclusion = data.get("exclusion_check", "")
            decision_raw = data.get("decision", "").upper()
            reason = data.get("reason", "")

            decision = "ELIGIBLE ✅" if "ELIGIBLE" in decision_raw and "NOT" not in decision_raw else "INELIGIBLE ❌"

            st.write(f"Inclusion Check: {inclusion}")
            st.write(f"Exclusion Check: {exclusion}")
            st.write(f"Decision: {decision}")
            st.write(f"Reason: {reason}")

        except:
            st.error("Failed to parse response")
            st.write(result)