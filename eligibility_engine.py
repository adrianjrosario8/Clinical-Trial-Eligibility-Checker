from llm_utils import get_eligibility_response


def check_eligibility(patient, parsed_rules):

    reasons = []

    patient_diagnosis = str(patient["diagnosis"]).lower().strip()

    exclusion_conditions = [
        c.lower() for c in parsed_rules["exclusion_conditions"]
    ]

    inclusion_conditions = [
        c.lower() for c in parsed_rules["inclusion_conditions"]
    ]

    # -------------------------
    # Exclusion checks first
    # -------------------------

    for exclusion in exclusion_conditions:
        if (
            exclusion in patient_diagnosis
            or patient_diagnosis in exclusion
        ):
            reasons.append(
                f"Excluded condition present: {patient['diagnosis']}"
            )

    if (
        str(patient.get("heart_failure", "")).lower() == "yes"
        and any("heart failure" in e for e in exclusion_conditions)
    ):
        reasons.append("Excluded condition present: heart failure")

    if (
        str(patient.get("infection", "")).lower() == "yes"
        and any("infection" in e for e in exclusion_conditions)
    ):
        reasons.append("Excluded condition present: infection")

    if (
        str(patient.get("lung_disease", "")).lower() == "yes"
        and any("lung disease" in e for e in exclusion_conditions)
    ):
        reasons.append("Excluded condition present: lung disease")

    # -------------------------
    # Inclusion checks only if no exclusions fired
    # -------------------------

    if not reasons and inclusion_conditions:

        matched = any(
            cond in patient_diagnosis or patient_diagnosis in cond
            for cond in inclusion_conditions
        )

        if not matched:
            reasons.append(
                f"Missing required condition: {patient['diagnosis']}"
            )

    # -------------------------
    # LLM fallback for ambiguous cases
    # -------------------------

    if not reasons and not inclusion_conditions:

        prompt = f"""
You are a clinical trial eligibility assistant.

Trial rules:
- Required conditions: {parsed_rules['inclusion_conditions']}
- Excluded conditions: {parsed_rules['exclusion_conditions']}

Patient profile:
- Diagnosis: {patient['diagnosis']}
- Age: {patient['age']}
- Heart failure: {patient['heart_failure']}
- Infection: {patient['infection']}
- Lung disease: {patient['lung_disease']}

Is this patient ELIGIBLE or INELIGIBLE?
Reply with ELIGIBLE or INELIGIBLE and one sentence reason.
"""
        llm_response = get_eligibility_response(prompt)

        if "INELIGIBLE" in llm_response.upper():
            return {
                "decision": "INELIGIBLE",
                "reason": f"LLM assessment: {llm_response.strip()}"
            }

    # -------------------------
    # Final decision
    # -------------------------

    if reasons:
        return {
            "decision": "INELIGIBLE",
            "reason": "; ".join(dict.fromkeys(reasons))
        }

    return {
        "decision": "ELIGIBLE",
        "reason": "All eligibility checks passed"
    }