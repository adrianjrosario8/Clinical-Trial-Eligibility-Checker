import streamlit as st
import pandas as pd

from criteria_parser import parse_trial_criteria
from eligibility_engine import check_eligibility


st.title("Clinical Trial Eligibility Checker")


# -----------------------------
# Trial Criteria Input
# -----------------------------

trial_criteria = st.text_area(
    "Paste Trial Eligibility Criteria",
    """
Inclusion:
- Type 2 Diabetes

Exclusion:
- Type 1 Diabetes
- Gestational Diabetes
- Heart failure
- Infection
- Lung disease
"""
)

# Parse criteria
parsed_rules = parse_trial_criteria(trial_criteria)

st.subheader("Parsed Clinical Criteria")
st.json(parsed_rules)


# -----------------------------
# Upload CSV
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload Patient CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Rename possible variations
    df = df.rename(columns={
        "heart failure": "heart_failure",
        "lung disease": "lung_disease"
    })

    required_cols = [
        "age",
        "diagnosis",
        "glucose",
        "bmi",
        "heart_failure",
        "infection",
        "lung_disease"
    ]

    if not all(col in df.columns for col in required_cols):

        st.error(f"CSV must contain columns: {required_cols}")

        st.write("Detected columns:")
        st.write(list(df.columns))

        st.stop()

    st.subheader("Patient Data Preview")
    st.dataframe(df.head())

    # -----------------------------
    # Run Eligibility
    # -----------------------------

    if st.button("Run Eligibility Screening"):

        results = []

        with st.spinner("Processing patients..."):

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

                parsed = check_eligibility(
                    patient,
                    parsed_rules
                )

                results.append({
                    **patient,
                    **parsed
                })

        result_df = pd.DataFrame(results)

        st.success("Eligibility screening completed!")

        st.subheader("Eligibility Results")
        st.dataframe(result_df)

        # Download CSV
        csv = result_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Results CSV",
            csv,
            "eligibility_results.csv",
            "text/csv"
        )