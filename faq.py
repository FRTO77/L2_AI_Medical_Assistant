from typing import List
from pathlib import Path
import json
from models import FAQItem


DATA_PATH_RU = Path(__file__).resolve().parent / "faq_data.json"
DATA_PATH_EN = Path(__file__).resolve().parent / "faq_en.json"


def load_faq(lang: str = "ru") -> List[FAQItem]:
    path = DATA_PATH_RU if lang == "ru" else DATA_PATH_EN
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return [FAQItem(**x) for x in data]


def search_faq(query: str, limit: int = 10, lang: str = "ru") -> List[FAQItem]:
    items = load_faq(lang)
    if not query:
        return items[:limit]
    q = query.lower()
    scored = []
    for it in items:
        text = f"{it.question}\n{it.answer}\n{' '.join(it.tags)}".lower()
        # Naive score: count of query tokens present
        tokens = [t for t in q.split() if t]
        score = sum(1 for t in tokens if t in text)
        if score > 0:
            scored.append((score, it))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [it for _, it in scored[:limit]]


