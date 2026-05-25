CONDITION_KEYWORDS = [
    "type 2 diabetes", "type 1 diabetes", "gestational diabetes",
    "diabetes", "heart failure", "lung disease", "infection",
    "copd", "hypertension", "obesity", "cancer", "stroke",
    "kidney disease", "liver disease", "asthma"
]

MEDICATION_KEYWORDS = [
    "corticosteroid", "insulin", "metformin", "steroid",
    "warfarin", "aspirin", "ibuprofen"
]

MEASUREMENT_KEYWORDS = [
    "hba1c", "glucose", "bmi", "blood pressure", "creatinine"
]


def remove_subsumed(terms):
    """Remove shorter terms already contained in a longer term."""
    terms = sorted(terms, key=len, reverse=True)
    result = []
    for term in terms:
        if not any(term in longer for longer in result):
            result.append(term)
    return result


def extract_entities(text):

    structured = {
        "conditions": [],
        "medications": [],
        "measurements": [],
        "other": []
    }

    if not text or not text.strip():
        return structured

    text_lower = text.lower()

    # Primary: keyword matching
    for keyword in CONDITION_KEYWORDS:
        if keyword in text_lower:
            structured["conditions"].append(keyword)

    for keyword in MEDICATION_KEYWORDS:
        if keyword in text_lower:
            structured["medications"].append(keyword)

    for keyword in MEASUREMENT_KEYWORDS:
        if keyword in text_lower:
            structured["measurements"].append(keyword)

    # Remove subsumed terms — "diabetes" removed if
    # "type 2 diabetes" already present
    structured["conditions"] = remove_subsumed(
        structured["conditions"]
    )

    # Secondary: NER if available
    try:
        from transformers import pipeline as hf_pipeline
        ner_pipeline = hf_pipeline(
            "ner",
            model="samrawal/bert-base-uncased_clinical-ner",
            aggregation_strategy="simple"
        )
        entities = ner_pipeline(text)
        for entity in entities:
            label = entity["entity_group"].upper()
            word = entity["word"].lower().strip()

            # Filter subword artifacts and short fragments
            if len(word) < 3:
                continue
            if word.startswith("##"):
                continue
            if "##" in word:
                continue

            if label in ["DISEASE", "DISORDER", "PROBLEM"]:
                if word not in structured["conditions"]:
                    structured["conditions"].append(word)
            elif label in ["CHEMICAL", "DRUG", "TREATMENT"]:
                if word not in structured["medications"]:
                    structured["medications"].append(word)
            elif label in ["TEST", "MEASUREMENT"]:
                if word not in structured["measurements"]:
                    structured["measurements"].append(word)

    except Exception:
        pass

    # Final dedup
    for key in structured:
        structured[key] = list(dict.fromkeys(structured[key]))

    return structured