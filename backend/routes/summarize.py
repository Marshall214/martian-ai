from fastapi import APIRouter, HTTPException, UploadFile, File
from pydantic import BaseModel
from utils.summarizer import summarize_text
from utils.audio_tools import transcribe_audio
from utils.document_processor import process_uploaded_document
import tempfile
import os
from utils.document_processor import process_uploaded_document, validate_text_length
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
    try:
        # Save the uploaded file temporarily (or process directly)
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        transcribed_text = transcribe_audio(file_location)
        
        # Clean up the temporary file
        import os
        os.remove(file_location)
        
        return {"transcribed_text": transcribed_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-document")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process document files (PDF, DOCX, TXT) for summarization
    """
    try:
        # Validate file type
        allowed_extensions = ['.pdf', '.docx', '.txt']
        file_extension = os.path.splitext(file.filename)[1].lower()
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Process the document
            result = process_uploaded_document(temp_path)
            
            if not result["success"]:
                raise HTTPException(status_code=500, detail=result["error"])
            
            return {
                "text": result["text"],
                "word_count": result["word_count"],
                "is_valid": result["is_valid"],
                "status_message": result["status_message"],
                "filename": file.filename
            }
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")
