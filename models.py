from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class SymptomInput(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    sex: Optional[Literal["male", "female", "other"]] = None
    symptoms: List[str] = Field(default_factory=list)
    duration_days: Optional[int] = Field(None, ge=0)
    severity_1to10: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = None


class ConditionHypothesis(BaseModel):
    condition: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    rationale: str
    red_flags: List[str] = Field(default_factory=list)
    recommended_actions: List[str] = Field(default_factory=list)


class TriageResult(BaseModel):
    risk_level: Literal["low", "moderate", "high", "emergency"]
    possible_conditions: List[ConditionHypothesis] = Field(default_factory=list)
    self_care_advice: List[str] = Field(default_factory=list)
    doctor_questions: List[str] = Field(default_factory=list)


class FAQItem(BaseModel):
    question: str
    answer: str
    tags: List[str] = Field(default_factory=list)


