from pydantic import BaseModel
from typing import List

class RiskFinding(BaseModel):
    category: str
    severity: str
    clause: str
    explanation: str
    recommendation: str

class AnalysisResponse(BaseModel):
    overall_score: int
    contract_type: str
    summary: str
    findings: List[RiskFinding]
    missing_clauses: List[str]
