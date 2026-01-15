from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tempfile
import os
from pathlib import Path
from utils.audio_tools import process_audio_file, process_text_for_audio

router = APIRouter()

class NotesRequest(BaseModel):
    text: str

class TextToAudioRequest(BaseModel):
    text: str

@router.post("/notes")
async def create_notes(request: NotesRequest):
    try:
        # Placeholder for smart notes generation logic
        # In a real scenario, you'd integrate with a notes AI utility
        generated_notes = f"Smart notes for: {request.text[:50]}..."
        return {"notes": generated_notes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio-to-text")
async def convert_audio_to_text(audio: UploadFile = File(...)):
    """
    Convert uploaded audio file to detailed text summary
    """
    try:
        # Validate file type
        allowed_types = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/m4a', 'audio/ogg']
        if audio.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio.filename).suffix) as temp_file:
            content = await audio.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Process the audio file
            result = process_audio_file(temp_path)
            
            if result["status"] == "error":
                raise HTTPException(status_code=500, detail=result["detailed_summary"])
            
            return {
                "transcribed_text": result["transcribed_text"],
                "detailed_summary": result["detailed_summary"],
                "word_count": result["word_count"],
                "filename": audio.filename
            }
        
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process audio: {str(e)}")

@router.post("/text-to-audio")
async def convert_text_to_audio(request: TextToAudioRequest):
    """
    Convert text to enhanced audio summary with actual audio generation
    """
    try:
        # Validate input
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content is required")
        
        word_count = len(request.text.split())
        if word_count < 10:
            raise HTTPException(status_code=400, detail="Text must be at least 10 words long")
        if word_count > 5000:
            raise HTTPException(status_code=400, detail="Text must be less than 5000 words")
        
        # Process the text and generate actual audio
        result = process_text_for_audio(request.text)
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["enhanced_text"])
        
        # Get the actual audio file path and convert to URL
        audio_file_path = result["audio_path"]
        if audio_file_path and os.path.exists(audio_file_path):
            # Convert absolute path to relative URL path
            audio_url = f"/static/audio/{os.path.basename(audio_file_path)}"
        else:
            # Fallback if file generation failed
            audio_url = None
        
        return {
            "original_text": result["original_text"],
            "enhanced_text": result["enhanced_text"],
            "audio_url": audio_url,
            "audio_file_path": audio_file_path,
            "word_count": result["word_count"],
            "duration_estimate": f"{max(1, result['word_count'] // 3)} minutes"  # Rough estimate
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {str(e)}")

@router.get("/download-audio/{filename}")
async def download_audio(filename: str):
    """
    Download generated audio file
    """
    try:
        audio_path = os.path.join("static", "audio", filename)
        
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail="Audio file not found")
        
        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=filename,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {str(e)}")
