from pydantic import BaseModel
from typing import List, Optional

class RiskFinding(BaseModel):
    title: str
    category: str
    severity: str
    explanation: str
    suggestion: Optional[str] = None

class AnalysisResponse(BaseModel):
    overall_risk: str
    summary: str
    findings: List[RiskFinding]
