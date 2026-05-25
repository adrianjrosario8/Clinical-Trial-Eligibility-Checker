from ner_utils import extract_entities


def parse_trial_criteria(text):

    parsed = {
        "inclusion_conditions": [],
        "exclusion_conditions": []
    }

    if not text or not text.strip():
        return parsed

    text_lower = text.lower()

    # Split on exclusion section (case-insensitive)
    inclusion_text = ""
    exclusion_text = ""

    if "exclusion:" in text_lower:
        split_index = text_lower.find("exclusion:")
        inclusion_text = text[:split_index]
        exclusion_text = text[split_index:]
    else:
        inclusion_text = text

    # Run entity extraction on each section
    inclusion_entities = extract_entities(inclusion_text)
    exclusion_entities = extract_entities(exclusion_text)

    parsed["inclusion_conditions"] = (
        inclusion_entities["conditions"]
    )
    parsed["exclusion_conditions"] = (
        exclusion_entities["conditions"]
    )

    # Fallback: parse bullet points directly if NER/keywords missed everything
    if not parsed["inclusion_conditions"]:
        for line in inclusion_text.splitlines():
            line = line.strip().lstrip("-").strip().lower()
            if len(line) > 2 and not line.startswith("inclusion"):
                parsed["inclusion_conditions"].append(line)

    if not parsed["exclusion_conditions"]:
        for line in exclusion_text.splitlines():
            line = line.strip().lstrip("-").strip().lower()
            if len(line) > 2 and not line.startswith("exclusion"):
                parsed["exclusion_conditions"].append(line)

    return parsed