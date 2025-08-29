import os
from typing import Optional

try:
    from langchain_openai import ChatOpenAI
except Exception:
    ChatOpenAI = None  # type: ignore

try:
    from langchain_ollama import ChatOllama
except Exception:
    ChatOllama = None  # type: ignore

from models import SymptomInput, TriageResult


def make_llm(provider: str, model: str, temperature: float):
    if provider == "OpenAI" and ChatOpenAI is not None and os.getenv("OPENAI_API_KEY"):
        return ChatOpenAI(model=model, temperature=temperature, api_key=os.getenv("OPENAI_API_KEY"))
    if provider == "Ollama" and ChatOllama is not None:
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        return ChatOllama(model=model, base_url=base_url, temperature=temperature)
    return None


def generate_advice(data: SymptomInput, triage: TriageResult, provider: str, openai_model: str, ollama_model: str, temperature: float, lang: str = "ru") -> Optional[str]:
    llm = make_llm(provider, openai_model if provider == "OpenAI" else ollama_model, temperature)
    if llm is None:
        return None

    symptoms_str = ", ".join(data.symptoms)
    conds = "; ".join([f"{h.condition} ({h.confidence:.2f})" for h in triage.possible_conditions[:5]])
    if lang == "ru":
        prompt = (
            "Вы — медицинский помощник. На основе введённых симптомов и эвристического триажа сформулируй вежливые и понятные рекомендации на русском. "
            "Добавь список вопросов врачу. Избегай категоричных диагнозов и укажи, что информация не заменяет визит к врачу.\n\n"
            f"Симптомы: {symptoms_str}\n"
            f"Возраст: {data.age or 'не указан'}, Пол: {data.sex or 'не указан'}, Дней: {data.duration_days or 'н/д'}, Тяжесть (1-10): {data.severity_1to10 or 'н/д'}\n"
            f"Вероятные состояния: {conds}\n"
            f"Базовые советы: {'; '.join(triage.self_care_advice)}\n"
            f"Вопросы врачу: {'; '.join(triage.doctor_questions)}\n"
            "Сформируй ответ в 2-4 абзацах и маркированном списке вопросов."
        )
    else:
        prompt = (
            "You are a medical assistant. Based on the entered symptoms and heuristic triage, provide polite and clear recommendations in English. "
            "Add questions to ask a doctor. Avoid definitive diagnoses and state that this is not a substitute for medical care.\n\n"
            f"Symptoms: {symptoms_str}\n"
            f"Age: {data.age or 'n/a'}, Sex: {data.sex or 'n/a'}, Days: {data.duration_days or 'n/a'}, Severity (1-10): {data.severity_1to10 or 'n/a'}\n"
            f"Likely conditions: {conds}\n"
            f"Baseline self-care: {'; '.join(triage.self_care_advice)}\n"
            f"Doctor questions: {'; '.join(triage.doctor_questions)}\n"
            "Respond in 2–4 short paragraphs and a bulleted list of questions."
        )
    try:
        resp = llm.invoke(prompt)
        return getattr(resp, "content", str(resp))
    except Exception as e:
        return f"LLM error: {str(e)}"


