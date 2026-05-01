import streamlit as st 
import json
import pandas as pd
from llm_utils import get_eligibility_response


# Prompt

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
    "reason": "1 line explanation"
}}
"""


# Parser 

def parse_llm_output(result):
    try:
        clean = result.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        decision_raw = data.get("decision", "").strip().upper()

        if decision_raw == "ELIGIBLE":
            decision = "ELIGIBLE"
        else:
            decision = "INELIGIBLE"

        return {
            "inclusion_check": data.get("inclusion_check", ""),
            "exclusion_check": data.get("exclusion_check", ""),
            "decision": decision,
            "reason": data.get("reason", "")
        }

    except Exception:
        return {
            "inclusion_check": "ERROR",
            "exclusion_check": "ERROR",
            "decision": "ERROR",
            "reason": result
        }


# UI

st.title("Clinical Trial Eligibility Checker")

mode = st.radio("Select Mode", ["Single Patient", "Batch CSV Upload"])


# Single Patient

if mode == "Single Patient":

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

        with st.spinner("Analyzing patient..."):
            result = get_eligibility_response(build_prompt(patient))
            data = parse_llm_output(result)

        st.subheader("Result")
        st.write(f"Inclusion Check: {data['inclusion_check']}")
        st.write(f"Exclusion Check: {data['exclusion_check']}")
        st.write(f"Decision: {data['decision']}")
        st.write(f"Reason: {data['reason']}")


# Batch Mode

else:

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        df.columns = df.columns.str.strip().str.lower()

        df = df.rename(columns={
            "heart failure": "heart_failure",
            "lung disease": "lung_disease"
        })

        required_cols = [
            "age", "diagnosis", "glucose", "bmi",
            "heart_failure", "infection", "lung_disease"
        ]

        if not all(col in df.columns for col in required_cols):
            st.error(f"CSV must contain: {required_cols}")
            st.write("Your columns:", list(df.columns))
            st.stop()

        st.write("Preview:")
        st.dataframe(df.head())

        if st.button("Run Batch Eligibility"):

            results = []

            with st.spinner("Processing batch..."):
                for _, row in df.iterrows():
                    patient = {
                        "age": row["age"],
                        "diagnosis": row["diagnosis"],
                        "glucose": row["glucose"],
                        "bmi": row["bmi"],
                        "heart_failure": row["heart_failure"],
                        "infection": row["infection"],
                        "lung_disease": row["lung_disease"]
                    }

                    result = get_eligibility_response(build_prompt(patient))
                    parsed = parse_llm_output(result)

                    results.append({**patient, **parsed})

            result_df = pd.DataFrame(results)

            st.success("Batch processing completed!")

            st.subheader("Batch Results")
            st.dataframe(result_df)

            csv = result_df.to_csv(index=False).encode("utf-8")

            st.download_button(
                "Download Results CSV",
                csv,
                "eligibility_results.csv",
                "text/csv"
            )