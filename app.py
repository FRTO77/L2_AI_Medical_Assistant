import os
from datetime import datetime
from typing import Optional

import streamlit as st
from dotenv import load_dotenv

from models import SymptomInput
from triage import triage_symptoms
from faq import search_faq
from llm import generate_advice
from i18n import t, localize_triage, SYMPTOM_SUGGESTIONS


load_dotenv()

st.set_page_config(page_title="AI Medical Assistant", page_icon="🩺", layout="wide")


def main():
    # English-only UI
    lang = "en"

    st.title(t("title", lang))
    st.caption(t("disclaimer", lang))

    with st.sidebar:
        st.header(t("settings", lang))
        st.caption(t("settings_help", lang))
        provider = st.selectbox(t("provider", lang), ["OpenAI", "Ollama"], index=0 if os.getenv("LLM_PROVIDER", "OpenAI") == "OpenAI" else 1, help=t("provider_help", lang), key="provider_select")
        openai_model = st.text_input(t("openai_model", lang), os.getenv("OPENAI_MODEL", ""), placeholder=t("openai_model_ph", lang), help=t("openai_model_help", lang), key="openai_model_input")
        ollama_model = st.text_input(t("ollama_model", lang), os.getenv("OLLAMA_MODEL", ""), placeholder=t("ollama_model_ph", lang), help=t("ollama_model_help", lang), key="ollama_model_input")
        temperature = st.slider(t("temperature", lang), 0.0, 1.0, float(os.getenv("AI_TEMPERATURE", "0.2")), 0.05, help=t("temperature_help", lang))
        st.divider()
        st.header(t("faq", lang))
        st.caption(t("faq_desc", lang))
        faq_q = st.text_input(t("faq_search", lang), placeholder=t("faq_placeholder", lang), help=t("faq_search_help", lang), key="faq_search_input")
        if faq_q is not None:
            faq_items = search_faq(faq_q, limit=10, lang=lang)
            for it in faq_items:
                with st.expander(it.question):
                    st.write(it.answer)
                    if it.tags:
                        st.caption(", ".join(it.tags))

    st.subheader(t("symptoms_input", lang))
    st.caption(t("symptoms_desc", lang))
    col1, col2, col3 = st.columns(3)
    with col1:
        age = st.number_input(t("age", lang), min_value=0, max_value=120, value=30, help=t("age_help", lang))
        sex = st.selectbox(t("sex", lang), ["male", "female", "other"], index=0, help=t("sex_help", lang))
    with col2:
        duration_days = st.number_input(t("duration", lang), min_value=0, value=2, help=t("duration_help", lang))
        severity = st.slider(t("severity", lang), 1, 10, 5, help=t("severity_help", lang))
    with col3:
        notes = st.text_input(t("notes", lang), "", placeholder=t("notes_placeholder", lang), help=t("notes_help", lang), key="notes_input")

    suggestions = SYMPTOM_SUGGESTIONS.get(lang, SYMPTOM_SUGGESTIONS["en"])
    symptoms = st.tags(t("symptoms_tags", lang), suggestions=suggestions, help=t("symptoms_help", lang), key="symptoms_tags") if hasattr(st, "tags") else st.text_input(t("symptoms_csv", lang), ", ".join(suggestions[:2]), placeholder=t("symptoms_placeholder", lang), help=t("symptoms_help", lang), key="symptoms_csv_input")
    if isinstance(symptoms, str):
        symptoms_list = [s.strip() for s in symptoms.split(",") if s.strip()]
    else:
        symptoms_list = symptoms

    if st.button(t("analyze", lang), type="primary", help=t("analyze_help", lang)):
        data = SymptomInput(
            age=age or None,
            sex=sex,
            symptoms=symptoms_list,
            duration_days=duration_days or None,
            severity_1to10=severity or None,
            notes=notes or None,
        )
        triage = triage_symptoms(data)

        loc = localize_triage(triage, lang)
        st.subheader(t("triage_results", lang))
        st.caption(t("triage_desc", lang))
        st.write(f"{t('risk_level', lang)}: **{loc['risk_level']}**")
        st.write(t("possible_conditions", lang) + ":")
        for h in loc["possible_conditions"][:5]:
            st.write(f"- {h['condition']} — {h['confidence']:.2f}")
        if loc["self_care_advice"]:
            st.write(t("self_care", lang) + ":")
            for a in loc["self_care_advice"]:
                st.write(f"- {a}")
        if loc["doctor_questions"]:
            st.write(t("doctor_questions", lang) + ":")
            for q in loc["doctor_questions"]:
                st.write(f"- {q}")

        st.subheader(t("ai_recommendations", lang))
        st.caption(t("ai_reco_desc", lang))
        advice = generate_advice(
            data,
            triage,
            provider=provider,
            openai_model=openai_model,
            ollama_model=ollama_model,
            temperature=float(temperature),
            lang=lang,
        )
        if advice:
            st.write(advice)
        else:
            st.info(t("llm_offline", lang))

    st.divider()
    st.subheader(t("future", lang))
    for line in t("future_items", lang).split("\n"):
        st.write(line)


if __name__ == "__main__":
    main()


