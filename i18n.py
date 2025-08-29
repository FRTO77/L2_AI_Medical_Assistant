from __future__ import annotations

from typing import Dict, List
from models import TriageResult, ConditionHypothesis


UI_TEXT: Dict[str, Dict[str, str]] = {
    "title": {
        "ru": "🩺 AI Medical Assistant",
        "en": "🩺 AI Medical Assistant",
    },
    "disclaimer": {
        "ru": "Демонстрационный ассистент. Не является медицинским советом.",
        "en": "Demo assistant. Not medical advice.",
    },
    "settings": {"ru": "Настройки ИИ", "en": "AI Settings"},
    "provider": {"ru": "Провайдер", "en": "Provider"},
    "openai_model": {"ru": "OpenAI модель", "en": "OpenAI model"},
    "ollama_model": {"ru": "Ollama модель", "en": "Ollama model"},
    "temperature": {"ru": "Температура модели", "en": "Model temperature"},
    "faq": {"ru": "FAQ", "en": "FAQ"},
    "faq_search": {"ru": "Поиск по FAQ", "en": "Search FAQ"},
    "symptoms_input": {"ru": "Ввод симптомов", "en": "Symptoms Input"},
    "age": {"ru": "Возраст", "en": "Age"},
    "sex": {"ru": "Пол", "en": "Sex"},
    "duration": {"ru": "Длительность (дней)", "en": "Duration (days)"},
    "severity": {"ru": "Тяжесть (1-10)", "en": "Severity (1-10)"},
    "notes": {"ru": "Примечания", "en": "Notes"},
    "symptoms_tags": {
        "ru": "Симптомы (вводите и нажимайте Enter)",
        "en": "Symptoms (type and press Enter)",
    },
    "symptoms_csv": {"ru": "Симптомы через запятую", "en": "Symptoms comma-separated"},
    "analyze": {"ru": "🔎 Проанализировать симптомы", "en": "🔎 Analyze symptoms"},
    "triage_results": {"ru": "Результаты триажа", "en": "Triage Results"},
    "risk_level": {"ru": "Уровень риска", "en": "Risk level"},
    "possible_conditions": {"ru": "Возможные причины", "en": "Possible conditions"},
    "self_care": {"ru": "Самопомощь", "en": "Self-care"},
    "doctor_questions": {"ru": "Вопросы врачу", "en": "Questions for doctor"},
    "ai_recommendations": {"ru": "Рекомендации ИИ", "en": "AI Recommendations"},
    "llm_offline": {
        "ru": "LLM не настроен (нет ключа/OpenAI или не запущен Ollama). Показаны только результаты триажа.",
        "en": "LLM is not configured (no OpenAI key or Ollama not running). Showing triage only.",
    },
    "future": {"ru": "Планы на будущее", "en": "Future plans"},
    "future_items": {
        "ru": "- Визуализация температуры/давления/пульса (линейные и столбчатые графики)\n- История наблюдений пациента и экспорт в PDF",
        "en": "- Visualization of temperature/blood pressure/pulse (line and bar charts)\n- Patient history and PDF export",
    },
    "language": {"ru": "Язык интерфейса", "en": "Interface language"},
    "language_help": {"ru": "Выберите язык приложения", "en": "Select application language"},
    "settings_help": {"ru": "Параметры генерации ответов ИИ", "en": "Parameters for AI response generation"},
    "provider_help": {"ru": "Выберите поставщика ИИ: OpenAI (облако) или Ollama (локально)", "en": "Select AI provider: OpenAI (cloud) or Ollama (local)"},
    "openai_model_help": {"ru": "Название модели OpenAI (напр. gpt-4o-mini)", "en": "OpenAI model name (e.g., gpt-4o-mini)"},
    "ollama_model_help": {"ru": "Название локальной модели Ollama (напр. llama3:8b-instruct)", "en": "Ollama local model name (e.g., llama3:8b-instruct)"},
    "temperature_help": {"ru": "Креативность модели: выше — более вариативные ответы", "en": "Model creativity: higher = more diverse answers"},
    "faq_desc": {"ru": "Частые вопросы по заболеваниям и препаратам", "en": "Frequently asked questions on diseases and medicines"},
    "faq_search_help": {"ru": "Введите запрос для поиска по FAQ", "en": "Enter a query to search the FAQ"},
    "symptoms_desc": {"ru": "Опишите ваши симптомы — ассистент оценит риски и возможные причины", "en": "Describe your symptoms — the assistant will assess risks and possible causes"},
    "symptoms_help": {"ru": "Перечислите симптомы по одному (или через запятую)", "en": "List symptoms one by one (or comma-separated)"},
    "age_help": {"ru": "Возраст пациента в годах", "en": "Patient age in years"},
    "sex_help": {"ru": "Пол пациента", "en": "Patient biological sex"},
    "duration_help": {"ru": "Сколько дней продолжаются симптомы", "en": "How many days symptoms have persisted"},
    "severity_help": {"ru": "Субъективная тяжесть симптомов (1 — минимально, 10 — максимально)", "en": "Subjective symptom severity (1 minimal, 10 maximal)"},
    "notes_help": {"ru": "Дополнительные сведения: приём лекарств, сопутствующие болезни и т. д.", "en": "Additional info: medications, comorbidities, etc."},
    "analyze_help": {"ru": "Запустить анализ и сгенерировать рекомендации", "en": "Run analysis and generate recommendations"},
    "triage_desc": {"ru": "Эвристический триаж: предварительная оценка по правилам", "en": "Heuristic triage: preliminary rule-based assessment"},
    "ai_reco_desc": {"ru": "Пояснения и советы, сформированные языковой моделью", "en": "Explanations and advice generated by the language model"},
}

# Placeholders
UI_TEXT.update({
    "faq_placeholder": {
        "ru": "Например: грипп, кашель, парацетамол",
        "en": "E.g.: flu, cough, paracetamol",
    },
    "symptoms_placeholder": {
        "ru": "Например: температура, кашель",
        "en": "E.g.: fever, cough",
    },
    "notes_placeholder": {
        "ru": "Например: принимаю парацетамол, аллергия на пенициллин",
        "en": "E.g.: taking paracetamol, penicillin allergy",
    },
    "openai_model_ph": {
        "ru": "например: gpt-4o-mini",
        "en": "e.g.: gpt-4o-mini",
    },
    "ollama_model_ph": {
        "ru": "например: llama3:8b-instruct",
        "en": "e.g.: llama3:8b-instruct",
    },
})


SYMPTOM_SUGGESTIONS = {
    "ru": [
        "температура",
        "кашель",
        "головная боль",
        "боль в горле",
        "одышка",
        "боль в груди",
        "боль в животе",
        "сыпь",
        "диарея",
        "тошнота",
    ],
    "en": [
        "fever",
        "cough",
        "headache",
        "sore throat",
        "shortness of breath",
        "chest pain",
        "abdominal pain",
        "rash",
        "diarrhea",
        "nausea",
    ],
}


RISK_MAP = {
    "ru": {
        "low": "низкий",
        "moderate": "умеренный",
        "high": "высокий",
        "emergency": "экстренный",
    },
    "en": {
        "low": "low",
        "moderate": "moderate",
        "high": "high",
        "emergency": "emergency",
    },
}


CONDITION_RU_EN = {
    "Вирусная инфекция": "Viral infection",
    "Бактериальная инфекция": "Bacterial infection",
    "Грипп": "Influenza (flu)",
    "COVID-19": "COVID-19",
    "Простуда": "Common cold",
    "Пневмония": "Pneumonia",
    "Бронхит": "Bronchitis",
    "Фарингит": "Pharyngitis",
    "Ангина (стрептококк)": "Strep throat (tonsillitis)",
    "ОРВИ": "ARI (acute respiratory infection)",
    "Мигрень": "Migraine",
    "Напряжённая головная боль": "Tension headache",
    "Синусит": "Sinusitis",
    "Стенокардия": "Angina",
    "Инфаркт миокарда": "Myocardial infarction",
    "Мышечно-скелетная боль": "Musculoskeletal pain",
    "Тревожное расстройство": "Anxiety disorder",
    "Астма": "Asthma",
    "ТЭЛА": "Pulmonary embolism",
    "Сердечная недостаточность": "Heart failure",
    "Гастроэнтерит": "Gastroenteritis",
    "Аппендицит": "Appendicitis",
    "ЖКБ/колика": "Biliary colic (gallstones)",
    "Аллергический дерматит": "Allergic dermatitis",
    "Вирусная экзантема": "Viral exanthem",
    "Пищевая токсикоинфекция": "Foodborne illness",
    "Синдром раздражённого кишечника": "Irritable bowel syndrome",
    "Гастрит": "Gastritis",
    "Беременность": "Pregnancy",
    "Неспецифические симптомы": "Nonspecific symptoms",
}


PHRASE_RU_EN = {
    # Advice
    "Пейте больше жидкости": "Drink more fluids",
    "Жаропонижающее (парацетамол/ибупрофен) при необходимости": "Antipyretics (paracetamol/ibuprofen) if needed",
    "Отдых и контроль температуры": "Rest and monitor temperature",
    "Тёплое питьё": "Warm drinks",
    "Покой": "Rest",
    "При влажном кашле — муколитики по показаниям": "If productive cough — mucolytics as indicated",
    "Полоскания": "Gargling",
    "Топические антисептики": "Topical antiseptics",
    "Гидратация": "Hydration",
    "НПВС по необходимости": "NSAIDs if needed",
    "Немедленно оценить риски": "Immediate risk assessment",
    "Ограничить нагрузку": "Reduce physical activity",
    "Срочная оценка состояния": "Urgent evaluation",
    "Дробное питьё": "Small frequent sips",
    "Лёгкая диета": "Light diet",
    "Избегать раздражителей": "Avoid irritants",
    "Антигистаминные при необходимости": "Antihistamines if needed",
    "Оральная регидратация": "Oral rehydration",
    "Диета BRAT": "BRAT diet",
    "Избегать жирной пищи": "Avoid fatty foods",
    # Questions
    "Какая максимальная температура?": "What is the highest temperature?",
    "Сколько дней держится температура?": "How many days does fever persist?",
    "Есть ли озноб?": "Any chills?",
    "Сухой или влажный кашель?": "Dry or productive cough?",
    "Есть ли одышка?": "Any shortness of breath?",
    "Есть ли кровь в мокроте?": "Any blood in sputum?",
    "Есть ли налёт на миндалинах?": "Any tonsillar exudate?",
    "Есть ли высокая температура?": "High fever present?",
    "Боль пульсирующая?": "Is the pain pulsating?",
    "Тошнота/светобоязнь?": "Nausea/photophobia?",
    "Связь с нагрузкой?": "Relation to exertion?",
    "Иррадиация в руку/челюсть?": "Radiation to arm/jaw?",
    "Потливость/тошнота?": "Sweating/nausea?",
    "Свистящее дыхание?": "Wheezing?",
    "Отёки?": "Edema?",
    "Боль в груди?": "Chest pain?",
    "Локализация боли?": "Pain location?",
    "Связь с приёмом пищи?": "Relation to meals?",
    "Тошнота/рвота/диарея?": "Nausea/vomiting/diarrhea?",
    "Зуд?": "Itching?",
    "Новые лекарства/косметика?": "New meds/cosmetics?",
    "Кровь в стуле?": "Blood in stool?",
    "Температура?": "Fever?",
    "Недавние поездки?": "Recent travel?",
    "Связь с едой?": "Relation to food?",
    "Беременность возможна?": "Possible pregnancy?",
    # Red flags
    "Температура > 39°C более 3 дней": ">39°C for more than 3 days",
    "Сильная головная боль и ригидность шеи": "Severe headache and neck stiffness",
    "Одышка": "Shortness of breath",
    "Кровохаркание": "Hemoptysis",
    "Боль в груди": "Chest pain",
    "Затруднение дыхания": "Breathing difficulty",
    "Сильное затруднение глотания": "Severe swallowing difficulty",
    "Внезапная сильнейшая боль": "Sudden worst-ever pain",
    "Очаговый неврологический дефицит": "Focal neurological deficit",
    "Давящая боль в груди": "Pressing chest pain",
    "Холодный пот": "Cold sweat",
    "Обморок": "Syncope",
    "Одышка в покое": "Dyspnea at rest",
    "Сатурация низкая (если известна)": "Low oxygen saturation (if known)",
    "Живот напряжён": "Rigid abdomen",
    "Кровь в стуле/рвоте": "Blood in stool/vomit",
    "Высокая температура": "High fever",
    "Отёк лица/языка": "Facial/tongue swelling",
}


def t(key: str, lang: str) -> str:
    return UI_TEXT.get(key, {}).get(lang, UI_TEXT.get(key, {}).get("en", key))


def translate_condition(name: str, lang: str) -> str:
    if lang == "ru":
        return name
    return CONDITION_RU_EN.get(name, name)


def translate_list(items: List[str], lang: str) -> List[str]:
    if lang == "ru":
        return items
    return [PHRASE_RU_EN.get(x, x) for x in items]


def localize_triage(tr: TriageResult, lang: str) -> Dict:
    return {
        "risk_level": RISK_MAP.get(lang, RISK_MAP["en"]).get(tr.risk_level, tr.risk_level),
        "possible_conditions": [
            {
                "condition": translate_condition(h.condition, lang),
                "confidence": h.confidence,
            }
            for h in tr.possible_conditions
        ],
        "self_care_advice": translate_list(tr.self_care_advice, lang),
        "doctor_questions": translate_list(tr.doctor_questions, lang),
    }


