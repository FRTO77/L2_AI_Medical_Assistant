# AI Medical Assistant

Demo assistant for preliminary symptom assessment (triage). It suggests likely conditions, basic self‑care advice, and questions for the doctor. Includes a small medical FAQ and optional LLM explanations (OpenAI or Ollama).

Important: This is NOT medical advice. Always consult a healthcare professional for diagnosis and treatment.

## Features
- Symptoms → rule‑based triage (risk level, possible conditions, self‑care advice, doctor questions)
- FAQ with simple search (English dataset)
- Optional LLM integration (OpenAI/Ollama) for readable explanations and recommendations
- Future ideas: charts for temperature/blood pressure/pulse, patient history & PDF export

## Quickstart
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r AI_Medical_Assistant\requirements.txt

# Generate .env automatically (in the project folder):
python AI_Medical_Assistant\create_env.py

# Then run the app:
streamlit run AI_Medical_Assistant\app.py
```

## Configuration (.env)
Put your settings in `AI_Medical_Assistant\.env` (the generator creates a template). Keys:
```dotenv
# Which LLM to use: OpenAI or Ollama
LLM_PROVIDER=OpenAI

# OpenAI (if using OpenAI)
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4o-mini

# Ollama (if using local models)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:8b-instruct

# Model behavior
AI_TEMPERATURE=0.2
```

Notes:
- If you don’t set any LLM keys, the offline rule‑based triage still works.
- Do NOT commit `.env` to Git.

## Usage
1) Enter your symptoms (comma‑separated if the tag input isn’t available).
2) Fill optional fields: Age, Sex, Duration (days), Severity (1–10), Notes.
3) Click “Analyze symptoms” to see the triage results.
4) Optionally, search the FAQ in the sidebar.

## Project Structure
- `app.py` — Streamlit UI
- `models.py` — Pydantic schemas (input/output)
- `triage.py` — rule‑based triage engine (demo)
- `i18n.py` — UI text and localization helpers (currently used for English strings)
- `llm.py` — OpenAI/Ollama integration
- `faq.py`, `faq_en.json` — FAQ and simple search
- `create_env.py` — script to generate `.env` and `.env.example`
- `requirements.txt`, `.gitignore`

## Security & Disclaimer
- Keep secrets in `.env`; never commit them.
- LLM outputs are generative; verify important facts.
- This tool does not replace professional medical advice.

