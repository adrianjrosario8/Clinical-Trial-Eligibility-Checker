## Clinical Trial Eligibility Checker — AI-Powered Screening System

### Live Demo

https://adrianjrosario8-clinical-trial-eligibility-checker-app-xvqghk.streamlit.app/

This project is deployed and fully functional on Streamlit Cloud.

### Overview
> This project is an AI-assisted clinical trial eligibility screening system designed to simulate how healthcare teams evaluate patient eligibility at scale. It combines rule-based clinical logic with LLM-powered reasoning to produce structured, explainable decisions.

It supports:
-  Single patient evaluation
-  Batch processing via CSV upload
-  Structured, explainable outputs


### Problem Statement

Clinical trial screening is often:
- Manual
- Time-consuming
- Prone to inconsistency

Therefore teams must evaluate:

- Inclusion criteria
- Exclusion criteria
- Clinical edge cases

As a result, this creates bottlenecks in patient recruitment and trial efficiency.

### Solution

The system uses a hybrid decision engine combining rule-based logic with LLM reasoning.

- Rule-based clinical constraints (deterministic logic)
- LLM-assisted reasoning (Groq LLaMA 3)

It generates:

- Eligibility decisions (ELIGIBLE / INELIGIBLE)
- Inclusion/exclusion validation
- Human-readable clinical explanations

### Workflow

Patient Data → Rule-Based Validation → LLM Reasoning (Groq) → Structured JSON Output → Streamlit UI

The system ensures deterministic rule enforcement while using the LLM only for structured reasoning and explanation generation.
  
### Key Features

1. Eligibility Decision Engine
  
- Inclusion + exclusion validation
- Deterministic + LLM reasoning

2. Batch CSV Processing
  
- Upload multiple patient records
- Automated large-scale evaluation
- Download results as CSV

3. Explainable Outputs
  
- Clear eligibility classification
- One-line clinical reasoning
- Consistent structured format

4. Robust Data Handling
  
- Column normalization
- Missing value handling
- Flexible CSV input formats

### Example Output

| Age | Diagnosis | Decision   | Reason                       |
| --- | --------- | ---------- | ---------------------------- |
| 45  | Type 2    | ELIGIBLE   | Meets all inclusion criteria |
| 60  | Type 1    | INELIGIBLE | Exclusion: Type 1 diabetes   |

### Tech Stack

- Python
- Streamlit
- Pandas
- Groq API (LLaMA 3)

### Real-World Applications

- Clinical trial screening automation
- Healthcare decision support systems
- AI-assisted patient recruitment
- Biomedical data pipelines

### Why This Project Stands Out 

Unlike typical ML prototypes, this system focuses on real-world clinical workflow simulation with structured decision logic and explainable outputs.

- Works on real-world structured clinical data
- Supports batch-level inference
- Produces explainable AI outputs
- Mirrors real clinical workflow decision-making


### How to Run Locally

```bash
git clone https://github.com/adrianjrosario8/Clinical-Trial-Eligibility-Checker.git

cd Clinical-Trial-Eligibility-Checker

pip install -r requirements.txt

streamlit run app.py
```

### Setup
Set your API key:
setx GROQ_API_KEY "your_api_key_here"

### Future Improvements

- Confidence scoring for predictions
- Multi-trial support system
- EHR integration
- REST API deployment

### Author

Built as part of a portfolio focused on:
Healthcare AI, Clinical Data Science, and Explainable AI systems






