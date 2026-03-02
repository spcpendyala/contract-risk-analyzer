import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

def extract_text(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype='pdf')
        text = ''
        for page in doc:
            text += page.get_text()
        doc.close()
        if not text.strip():
            raise ValueError('No text could be extracted from this PDF.')
        return text[:15000]
    except Exception as e:
        logger.error(f'PDF extraction error: {e}')
        raise
