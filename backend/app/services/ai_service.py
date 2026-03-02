import os, json, logging, urllib.request
from app.models.schemas import AnalysisResponse, RiskFinding

logger = logging.getLogger(__name__)

MOCK_RESPONSE = {
    "overall_risk": "HIGH",
    "summary": "This contract contains several high-risk clauses that heavily favor the other party. Key concerns include unlimited liability exposure, overly broad IP assignment, and a unilateral termination clause with no notice period.",
    "findings": [
        {
            "title": "Unlimited Liability Clause",
            "category": "Liability",
            "severity": "high",
            "explanation": "Section 8.2 exposes you to unlimited financial liability with no cap, meaning you could be held responsible for damages far exceeding the contract value.",
            "suggestion": "Negotiate a liability cap equal to the total contract value or 12 months of fees."
        },
        {
            "title": "Broad IP Assignment",
            "category": "IP Ownership",
            "severity": "high",
            "explanation": "Section 12 assigns all intellectual property created during the engagement to the client, including pre-existing work and tools you bring to the project.",
            "suggestion": "Carve out pre-existing IP and background IP. Only assign IP specifically created for this client."
        },
        {
            "title": "Unilateral Termination",
            "category": "Termination",
            "severity": "medium",
            "explanation": "The client can terminate this agreement at any time with no notice period, leaving you with no guaranteed income or transition time.",
            "suggestion": "Request a minimum 30-day notice period and a kill fee for work completed."
        },
        {
            "title": "Auto-Renewal Clause",
            "category": "Payment Terms",
            "severity": "medium",
            "explanation": "Section 4.3 automatically renews the contract for 12-month terms unless cancelled 90 days in advance, which is an unusually long notice window.",
            "suggestion": "Reduce the cancellation notice period to 30 days and add a reminder mechanism."
        },
        {
            "title": "Non-Compete Scope",
            "category": "Other",
            "severity": "low",
            "explanation": "The non-compete clause restricts you from working in the same industry for 2 years, which may be overly broad depending on your jurisdiction.",
            "suggestion": "Limit the non-compete to direct competitors only and reduce the duration to 6-12 months."
        }
    ]
}

PROMPT = """You are a contract risk analyst. Analyze the contract text below and return ONLY valid JSON.
No markdown, no explanation outside the JSON.

Return this exact structure:
{
  "overall_risk": "LOW|MEDIUM|HIGH|CRITICAL",
  "summary": "<2-3 sentence plain English summary of the main risks>",
  "findings": [
    {
      "title": "<short title for this risk>",
      "category": "<Liability|Payment Terms|Termination|IP Ownership|Confidentiality|Other>",
      "severity": "high|medium|low",
      "explanation": "<why this is risky in plain English>",
      "suggestion": "<what to do about it>"
    }
  ]
}

Contract text:
{contract_text}
"""

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.debug_mode = os.getenv('ENVIRONMENT') == 'development'

    async def analyze(self, contract_text: str) -> AnalysisResponse:
        if self.debug_mode or not self.api_key:
            logger.info("Using mock response (debug mode or no API key)")
            return AnalysisResponse(**MOCK_RESPONSE)

        prompt = PROMPT.replace('{contract_text}', contract_text)
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key={self.api_key}'
        body = json.dumps({'contents': [{'parts': [{'text': prompt}]}]}).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'application/json'}, method='POST')
        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                text = data['candidates'][0]['content']['parts'][0]['text']
                text = text.replace('```json', '').replace('```', '').strip()
                result = json.loads(text)
                for f in result.get('findings', []):
                    f['severity'] = f.get('severity', 'low').lower()
                    if 'title' not in f:
                        f['title'] = f.get('category', 'Risk')
                return AnalysisResponse(**result)
        except Exception as e:
            logger.error(f"AI service error: {e}")
            raise ValueError(f"Analysis failed: {str(e)}")

ai_service = AIService()
