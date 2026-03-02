from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_service import extract_text
from app.services.ai_service import ai_service
from app.models.schemas import AnalysisResponse

router = APIRouter()

@router.post('/analyze', response_model=AnalysisResponse)
async def analyze_contract(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail='Only PDF files are supported.')
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail='File size must be under 10MB.')
    try:
        file_bytes = await file.read()
        contract_text = extract_text(file_bytes)
        result = await ai_service.analyze(contract_text)
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail='Analysis failed. Please try again.')
