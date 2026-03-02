import os, json, logging, urllib.request, urllib.error
from app.models.schemas import AnalysisResponse

logger = logging.getLogger(__name__)

PROMPT = '''You are a contract risk analyst. Analyze the contract text below and return ONLY valid JSON.
No markdown, no explanation outside the JSON.

Return this exact structure:
{
  "overall_score": <integer 1-10>,
  "contract_type": "<type of contract>",
  "summary": "<2-3 sentence plain English summary of the main risks>",
  "findings": [
    {
      "category": "<Liability|Payment Terms|Termination|IP Ownership|Confidentiality|Other>",
      "severity": "<High|Medium|Low>",
      "clause": "<the problematic clause in plain English>",
      "explanation": "<why this is risky>",
      "recommendation": "<what to do about it>"
    }
  ],
  "missing_clauses": ["<clause name>", ...]
}

Contract text:
{contract_text}'''

class AIService:
    def __init__(self):
        self.api_key = os.getenv('GROQ_API_KEY')

    async def analyze(self, contract_text: str) -> AnalysisResponse:
        prompt = PROMPT.replace('{contract_text}', contract_text)

        url = 'https://api.groq.com/openai/v1/chat/completions'
        body = json.dumps({
            'model': 'llama-3.3-70b-versatile',
            'messages': [{'role': 'user', 'content': prompt}],
            'temperature': 0.1
        }).encode('utf-8')

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.api_key}'
            },
            method='POST'
        )

        try:
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                text = data['choices'][0]['message']['content']
                text = text.replace('```json', '').replace('```', '').strip()
                result = json.loads(text)
                return AnalysisResponse(**result)
        except urllib.error.HTTPError as e:
            body = e.read().decode('utf-8')
            logger.error(f'Groq HTTP Error {e.code}: {body}')
            raise Exception(f'Groq API error {e.code}: {body}')
        except Exception as e:
            logger.error(f'Unexpected error: {e}')
            raise

ai_service = AIService()
