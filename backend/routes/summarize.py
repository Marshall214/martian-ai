from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from utils.summarizer import summarize_text
from utils.audio_tools import transcribe_audio
from utils.document_processor import process_uploaded_document, validate_text_length
import tempfile
import os
from typing import Optional

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str
    mode: str = "short"  # "short", "detailed", or "keypoints"

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """Upload and extract text from document files (PDF, DOCX, TXT)"""
    try:
        # Read file content
        file_content = await file.read()
        
        # Process document and extract text
        extracted_text, word_count = process_uploaded_document(file_content, file.filename or "")
        
        # Validate text length
        is_valid, word_count, status_message = validate_text_length(extracted_text)
        
        return {
            "text": extracted_text,
            "word_count": word_count,
            "filename": file.filename,
            "is_valid": is_valid,
            "status_message": status_message,
            "file_type": file.content_type
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Document upload error: {str(e)}")  # Backend logging
        raise HTTPException(status_code=500, detail="Failed to process document")

@router.post("/summarize")
async def summarize(request: SummarizeRequest):
    try:
        # Validate mode
        valid_modes = ["short", "detailed", "keypoints"]
        if request.mode not in valid_modes:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid mode. Must be one of: {', '.join(valid_modes)}"
            )
        
        # Validate text length
        if not request.text or len(request.text.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail="Text must be at least 50 characters long"
            )
        
        word_count = len(request.text.split())
        if word_count > 5000:
            raise HTTPException(
                status_code=400,
                detail="Text must be under 5000 words. Current count: " + str(word_count)
            )
        
        # Generate summary
        summarized_result = summarize_text(request.text, request.mode)
        
        return {
            "summary_text": summarized_result,
            "mode": request.mode,
            "original_word_count": word_count,
            "summary_word_count": len(summarized_result.split())
        }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Summarization error: {str(e)}")  # Backend logging
        raise HTTPException(status_code=500, detail="Internal server error during summarization")

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Transcribe audio file to text using Whisper."""
    try:
        # Save to a proper temp file with cleanup
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename or ".wav")[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            transcribed_text = transcribe_audio(tmp_path)
            return {"transcribed_text": transcribed_text}
        finally:
            # Always clean up the temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
