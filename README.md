# Clinical Trial Eligibility Decision-Support System

> A hybrid AI system for clinical trial patient screening that combines biomedical NER, deterministic rule logic, and LLM reasoning to evaluate eligibility from free-text trial criteria - at both single-patient and full cohort scale.

[![Live App](https://img.shields.io/badge/Live%20App-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://adrianjrosario8-clinical-trial-eligibility-checker-app-68w9r7.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python)](https://python.org)

---

## What This Project Does

Clinical trial screening requires teams to parse free-text inclusion and exclusion criteria, map them against patient records, and handle clinical edge cases across hundreds of patients. It is manual, inconsistent, and slow.

This system automates that pipeline end-to-end. It reads raw criteria text as a clinician would write it, extracts clinical entities using biomedical NER, structures them into a rule set, screens patients deterministically, and invokes an LLM only for ambiguous cases where rules cannot make a clear determination. Every decision is auditable and traceable to a specific clinical rule.

---

## System Architecture

The pipeline runs in four layers, each with a distinct responsibility.

**Layer 1 - Biomedical NER (HuggingFace/PyTorch):** Free-text inclusion and exclusion criteria are processed by a biomedical NER pipeline to extract clinical entities: diseases, medications, and measurements. Inclusion and exclusion sections are parsed separately so entities are correctly classified before any rule logic runs. A subsumed-term deduplication pass removes redundant entries (e.g. "diabetes" is removed when "type 2 diabetes" is already present).

**Layer 2 - Criteria Parser:** Extracted entities are structured into a rule set with required conditions, excluded conditions, excluded medications, and required measurements. The parser handles case-insensitive section splitting and falls back to direct bullet-point parsing if NER extraction is incomplete.

**Layer 3 - Deterministic Rule Engine:** Patient records are screened against the structured rules. Exclusions are evaluated first. Inclusion checks only run if no exclusions fire. This mirrors how clinical screeners actually work and produces clean, non-redundant reason strings.

**Layer 4 - LLM Fallback (Groq/LLaMA 3):** When the rule engine cannot make a clear determination, Groq/LLaMA 3 is invoked to generate a clinical reasoning response. The LLM is a targeted fallback, not a blanket decision layer - it never overrides the deterministic engine.

```
Free-text Criteria Input
          |
Biomedical NER (HuggingFace/PyTorch)
          |
Criteria Parser (Inclusion / Exclusion rule structuring)
          |
Deterministic Rule Engine (exclusion-first logic)
          | (ambiguous cases only)
LLM Reasoning (Groq / LLaMA 3)
          |
Eligibility Decision + Reason
          |
Single Patient Result or Batch CSV Download
```

---

## Example Output

Criteria entered as free text:

```
Inclusion:
- Type 2 Diabetes

Exclusion:
- Type 1 Diabetes
- Gestational Diabetes
- Heart failure
- Infection
- Lung disease
```

Extracted and structured automatically by the NER pipeline:

```json
{
  "inclusion_conditions": ["type 2 diabetes"],
  "exclusion_conditions": [
    "gestational diabetes",
    "type 1 diabetes",
    "heart failure",
    "lung disease",
    "infection"
  ]
}
```

Batch screening results across 8 patients processed in seconds:

| Age | Diagnosis   | Heart Failure | Decision   | Reason                                                          |
|-----|-------------|---------------|------------|-----------------------------------------------------------------|
| 45  | Type 2      | No            | ELIGIBLE   | All eligibility checks passed                                   |
| 60  | Type 1      | Yes           | INELIGIBLE | Excluded condition: Type 1; Excluded condition: heart failure   |
| 38  | Type 2      | No            | ELIGIBLE   | All eligibility checks passed                                   |
| 22  | Type 2      | No            | ELIGIBLE   | All eligibility checks passed                                   |
| 70  | Gestational | No            | INELIGIBLE | Excluded condition: Gestational                                 |
| 50  | Type 2      | No            | ELIGIBLE   | All eligibility checks passed                                   |
| 33  | Type 2      | No            | ELIGIBLE   | All eligibility checks passed                                   |
| 55  | Type 2      | Yes           | INELIGIBLE | Excluded condition: heart failure                               |

Results are downloadable as a CSV for clinical documentation workflows.

---

## Key Features

**Biomedical NER preprocessing:** Free-text criteria are processed by a HuggingFace biomedical NER pipeline (PyTorch) before any rule logic runs. Clinical entities are extracted, deduplicated, and structured automatically. No manual criteria formatting required.

**Auditability by design:** The deterministic rule engine and LLM reasoning layer are fully separated. Every decision is traceable to a specific inclusion or exclusion rule. The LLM never overrides the rule engine.

**Exclusion-first decision logic:** Exclusions are evaluated before inclusions. A patient flagged for an exclusion criterion is not additionally penalised for failing an inclusion check. This produces clean, non-redundant reason strings and mirrors real clinical screening practice.

**LLM as a targeted fallback:** Groq/LLaMA 3 is invoked only for genuinely ambiguous cases where the rule engine cannot make a clear determination. This prevents hallucinated eligibility decisions while still handling edge cases gracefully.

**Batch cohort processing:** Upload a CSV of any size and screen an entire patient cohort simultaneously. Results are downloadable as a CSV.

**Single patient evaluation:** Real-time eligibility check for individual patients with instant structured output.

**Robust data handling:** Column normalization, missing value handling, and flexible CSV input formats for real-world messy data.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Biomedical NER | HuggingFace Transformers, PyTorch |
| Criteria Parsing | Custom rule-structuring pipeline |
| LLM Reasoning | Groq / LLaMA 3 |
| Decision Engine | Deterministic Python rule engine |
| Frontend | Streamlit |
| Data Processing | pandas |

---

## What Differentiates This Project

**NER-driven criteria parsing:** Most eligibility screening prototypes require structured input. This system reads raw free-text criteria the way a clinician would write them and extracts the rules automatically using biomedical NER. The criteria input is a text box, not a form.

**Separation of logic and explanation:** The rule engine enforces clinical constraints deterministically. The LLM generates human-readable reasoning on top. These two layers never mix, which is the design principle that makes outputs auditable and consistent with regulatory standards in clinical AI.

**Exclusion-first architecture:** Reflects how clinical screening actually works. A patient is not simultaneously flagged for missing an inclusion criterion and meeting an exclusion criterion. The decision logic is clean and defensible.

**Production-oriented pipeline:** Handles column normalization, missing values, flexible CSV formats, and subsumed-term deduplication - the messy real-world inputs that toy prototypes ignore.

---

## Run Locally

```bash
git clone https://github.com/adrianjrosario8/Clinical-Trial-Eligibility-Checker.git
cd Clinical-Trial-Eligibility-Checker
pip install -r requirements.txt
streamlit run app.py
```

Add your Groq API key to `.streamlit/secrets.toml`:
```
GROQ_API_KEY = "your_key_here"
```

---

## Limitations and Future Work

- NER entity extraction depends on keyword coverage for less common clinical terms. Expanding the keyword list or fine-tuning on trial-specific corpora would improve recall on rare conditions.
- Age, BMI, and lab value thresholds (e.g. HbA1c > 7%) are not yet parsed from free text. Numeric constraint extraction is a planned addition.
- Future additions: confidence scoring per decision, multi-trial support, EHR system integration, REST API deployment.

---

## Clinical Note

This tool is for research and educational purposes only. Not for clinical decision making. All outputs should be reviewed by a qualified clinical professional before any use in patient care or trial recruitment.

---

## Author

**Adrian Jacob Rosario**
MS Pharmaceutical Sciences (Pharmacometrics and Systems Pharmacology), University of Pittsburgh

Building end-to-end pharmacovigilance AI systems at the intersection of pharmaceutical research and production ML engineering.

[GitHub Portfolio](https://github.com/adrianjrosario8) | [LinkedIn](https://www.linkedin.com/in/adrian-jacob-rosario-330a47235/)
