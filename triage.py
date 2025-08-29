from typing import Dict, List, Tuple
from collections import defaultdict
from models import SymptomInput, TriageResult, ConditionHypothesis


# Simplified, rule-based symptom-to-condition mapping.
# We purposefully avoid clinical claims; this is an educational demo, not medical advice.
SYMPTOM_RULES: Dict[str, Dict] = {
    "fever": {
        "conditions": {"Вирусная инфекция": 2, "Бактериальная инфекция": 1, "Грипп": 2, "COVID-19": 2},
        "questions": ["Какая максимальная температура?", "Сколько дней держится температура?", "Есть ли озноб?"],
        "actions": [
            "Пейте больше жидкости",
            "Жаропонижающее (парацетамол/ибупрофен) при необходимости",
            "Отдых и контроль температуры"
        ],
        "red_flags": ["Температура > 39°C более 3 дней", "Сильная головная боль и ригидность шеи"],
    },
    "cough": {
        "conditions": {"Простуда": 1, "Грипп": 2, "COVID-19": 2, "Пневмония": 2, "Бронхит": 1},
        "questions": ["Сухой или влажный кашель?", "Есть ли одышка?", "Есть ли кровь в мокроте?"],
        "actions": ["Тёплое питьё", "Покой", "При влажном кашле — муколитики по показаниям"],
        "red_flags": ["Одышка", "Кровохаркание", "Боль в груди"],
    },
    "sore throat": {
        "conditions": {"Фарингит": 2, "Ангина (стрептококк)": 2, "ОРВИ": 1},
        "questions": ["Есть ли налёт на миндалинах?", "Есть ли высокая температура?"],
        "actions": ["Полоскания", "Тёплое питьё", "Топические антисептики"],
        "red_flags": ["Затруднение дыхания", "Сильное затруднение глотания"],
    },
    "headache": {
        "conditions": {"Мигрень": 2, "Напряжённая головная боль": 2, "Синусит": 1},
        "questions": ["Боль пульсирующая?", "Тошнота/светобоязнь?", "Связь с нагрузкой?"],
        "actions": ["Покой", "Гидратация", "НПВС по необходимости"],
        "red_flags": ["Внезапная сильнейшая боль", "Очаговый неврологический дефицит"],
    },
    "chest pain": {
        "conditions": {"Стенокардия": 2, "Инфаркт миокарда": 3, "Мышечно-скелетная боль": 1, "Тревожное расстройство": 1},
        "questions": ["Иррадиация в руку/челюсть?", "Одышка?", "Потливость/тошнота?"],
        "actions": ["Немедленно оценить риски", "Ограничить нагрузку"],
        "red_flags": ["Давящая боль в груди", "Одышка", "Холодный пот", "Обморок"],
    },
    "shortness of breath": {
        "conditions": {"Пневмония": 2, "Астма": 2, "ТЭЛА": 3, "Сердечная недостаточность": 2},
        "questions": ["Свистящее дыхание?", "Отёки?", "Боль в груди?"],
        "actions": ["Срочная оценка состояния"],
        "red_flags": ["Одышка в покое", "Сатурация низкая (если известна)"],
    },
    "abdominal pain": {
        "conditions": {"Гастроэнтерит": 1, "Аппендицит": 3, "ЖКБ/колика": 2},
        "questions": ["Локализация боли?", "Связь с приёмом пищи?", "Тошнота/рвота/диарея?"],
        "actions": ["Дробное питьё", "Лёгкая диета"],
        "red_flags": ["Живот напряжён", "Кровь в стуле/рвоте", "Высокая температура"],
    },
    "rash": {
        "conditions": {"Аллергический дерматит": 2, "Вирусная экзантема": 1},
        "questions": ["Зуд?", "Новые лекарства/косметика?"],
        "actions": ["Избегать раздражителей", "Антигистаминные при необходимости"],
        "red_flags": ["Отёк лица/языка", "Затруднение дыхания"],
    },
    "diarrhea": {
        "conditions": {"Гастроэнтерит": 2, "Пищевая токсикоинфекция": 2, "Синдром раздражённого кишечника": 1},
        "questions": ["Кровь в стуле?", "Температура?", "Недавние поездки?"],
        "actions": ["Оральная регидратация", "Диета BRAT"],
        "red_flags": ["Признаки обезвоживания", "Кровь в стуле"],
    },
    "nausea": {
        "conditions": {"Гастрит": 1, "Гастроэнтерит": 1, "Беременность": 1},
        "questions": ["Связь с едой?", "Беременность возможна?"],
        "actions": ["Дробное питьё", "Избегать жирной пищи"],
        "red_flags": ["Неукротимая рвота", "Признаки обезвоживания"],
    },
}


EMERGENCY_KEYWORDS = {"chest pain", "shortness of breath"}


# RU -> EN канонизация симптомов для входа
SYMPTOM_SYNONYMS_RU_EN: Dict[str, str] = {
    "температура": "fever",
    "жар": "fever",
    "лихорадка": "fever",
    "кашель": "cough",
    "боль в горле": "sore throat",
    "горло": "sore throat",
    "головная боль": "headache",
    "боль в груди": "chest pain",
    "одышка": "shortness of breath",
    "тяжело дышать": "shortness of breath",
    "боль в животе": "abdominal pain",
    "живот": "abdominal pain",
    "сыпь": "rash",
    "диарея": "diarrhea",
    "понос": "diarrhea",
    "тошнота": "nausea",
    "рвота": "nausea",
}


def _normalize(symptoms: List[str]) -> List[str]:
    normalized: List[str] = []
    for raw in symptoms:
        if not raw:
            continue
        s = raw.strip().lower()
        if not s:
            continue
        # Точное соответствие RU синонимам
        if s in SYMPTOM_SYNONYMS_RU_EN:
            normalized.append(SYMPTOM_SYNONYMS_RU_EN[s])
            continue
        # Подстрочное соответствие RU фразам
        matched = False
        for ru, en in SYMPTOM_SYNONYMS_RU_EN.items():
            if ru in s:
                normalized.append(en)
                matched = True
        if matched:
            continue
        # Оставляем как есть (возможно уже EN)
        normalized.append(s)
    # Уникализируем, сохраняя порядок
    seen = set()
    uniq = []
    for x in normalized:
        if x not in seen:
            seen.add(x)
            uniq.append(x)
    return uniq


def triage_symptoms(data: SymptomInput) -> TriageResult:
    symptoms = _normalize(data.symptoms)

    condition_scores: Dict[str, int] = defaultdict(int)
    recommended_actions: List[str] = []
    doctor_questions: List[str] = []
    matched_red_flags: List[str] = []

    for keyword, spec in SYMPTOM_RULES.items():
        if any(keyword in s for s in symptoms):
            for cond, w in spec["conditions"].items():
                condition_scores[cond] += w
            recommended_actions.extend(spec.get("actions", []))
            doctor_questions.extend(spec.get("questions", []))
            matched_red_flags.extend(spec.get("red_flags", []))

    # Determine risk level
    risk_level = "low"
    if any(k in symptoms for k in EMERGENCY_KEYWORDS):
        risk_level = "emergency"
    elif data.severity_1to10 and data.severity_1to10 >= 8:
        risk_level = "high"
    elif (data.duration_days and data.duration_days >= 7) or (data.severity_1to10 and data.severity_1to10 >= 5):
        risk_level = "moderate"

    # Build hypotheses
    total = sum(max(1, s) for s in condition_scores.values()) or 1
    ranked: List[Tuple[str, int]] = sorted(condition_scores.items(), key=lambda kv: kv[1], reverse=True)
    hypotheses: List[ConditionHypothesis] = []
    for cond, score in ranked[:8]:
        hypotheses.append(
            ConditionHypothesis(
                condition=cond,
                confidence=min(1.0, score / float(total)),
                rationale="Совпадение ключевых симптомов по правилам",
                red_flags=matched_red_flags[:],
                recommended_actions=sorted(set(recommended_actions))[:6],
            )
        )

    if not hypotheses:
        hypotheses.append(
            ConditionHypothesis(
                condition="Неспецифические симптомы",
                confidence=0.2,
                rationale="Недостаточно совпадений по правилам",
                red_flags=[],
                recommended_actions=["Наблюдение", "Гидратация", "Консультация врача при ухудшении"],
            )
        )

    # Self-care advice baseline
    self_care = ["Это не является медицинским советом. Обратитесь к врачу при сомнениях."]
    if risk_level in ("high", "emergency"):
        self_care.append("При тяжёлых симптомах — вызов скорой помощи/неотложная помощь.")

    # Deduplicate and trim
    doctor_questions = sorted(set(doctor_questions))[:10]
    recommended_actions = sorted(set(recommended_actions))[:8]

    return TriageResult(
        risk_level=risk_level,
        possible_conditions=hypotheses,
        self_care_advice=self_care,
        doctor_questions=doctor_questions,
    )


