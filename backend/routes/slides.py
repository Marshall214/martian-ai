from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from utils.slidegen_advanced import generate_slides as generate_slides_util
from utils.document_processor import process_uploaded_document
import tempfile
import os
from typing import Optional

router = APIRouter()

class SlidesFromTextRequest(BaseModel):
    text: str
    title: str = "Presentation"
    prompt: Optional[str] = None
    template: Optional[str] = None  # academic, business, creative, research, default
    export_format: str = "pptx"  # pptx, pdf, both

class SlidesFromPromptRequest(BaseModel):
    prompt: str
    title: str = "Presentation"
    template: Optional[str] = None
    export_format: str = "pptx"

@router.post("/generate-slides-from-text")
async def generate_slides_from_text(request: SlidesFromTextRequest):
    """
    Generate slides from text content
    - Accepts up to 1MB of text
    - Intelligently chunks content into slides
    - Supports multiple templates and export formats
    """
    try:
        # Validate input
        if not request.text or len(request.text.strip()) == 0:
            raise ValueError("Text content is required")
        
        # Check text size (rough estimate: ~5 bytes per character)
        if len(request.text.encode('utf-8')) > 1024 * 1024:
            raise ValueError("Text exceeds 1MB limit")
        
        # Generate slides
        result = generate_slides_util(
            content=request.text,
            title=request.title,
            prompt=request.prompt,
            template=request.template,
            export_format=request.export_format
        )
        
        # Determine file name
        safe_title = "".join(c for c in request.title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:30] or "presentation"
        
        # Return appropriate format
        if request.export_format == "pptx":
            return StreamingResponse(
                result['pptx'],
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                headers={"Content-Disposition": f"attachment; filename={safe_title}.pptx"}
            )
        elif request.export_format == "pdf":
            if result['pdf']:
                return StreamingResponse(
                    result['pdf'],
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={safe_title}.pdf"}
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="PDF export is not available. Please use PPTX format or ensure LibreOffice is installed."
                )
        elif request.export_format == "both":
            # Return metadata with both files available
            return {
                "status": "success",
                "message": "Use separate requests for PPTX and PDF",
                "metadata": result['metadata'],
                "available_formats": ["pptx", "pdf"] if result['pdf'] else ["pptx"]
            }
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Slide generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate slides: {str(e)}")

@router.post("/generate-slides-from-document")
async def generate_slides_from_document(
    file: UploadFile = File(...),
    title: Optional[str] = None,
    prompt: Optional[str] = None,
    template: Optional[str] = None,
    export_format: str = "pptx"
):
    """
    Generate slides from uploaded document (PDF, DOCX, TXT)
    - File size limit: 1MB
    - Extracts text and generates slides
    - Supports multiple templates and export formats
    """
    try:
        # Validate file type
        allowed_types = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                        'text/plain']
        if file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: PDF, DOCX, TXT"
            )
        
        # Read file content
        file_content = await file.read()
        
        # Check file size (1MB limit)
        if len(file_content) > 1024 * 1024:
            raise HTTPException(status_code=400, detail="File exceeds 1MB limit")
        
        # Extract text from document
        extracted_text, word_count = process_uploaded_document(file_content, file.filename or "")
        
        if not extracted_text or len(extracted_text.strip()) == 0:
            raise ValueError("No text content found in document")
        
        # Use filename or provided title
        presentation_title = title or (file.filename or "Presentation").split('.')[0]
        
        # Generate slides
        result = generate_slides_util(
            content=extracted_text,
            title=presentation_title,
            prompt=prompt,
            template=template,
            export_format=export_format
        )
        
        # Determine file name
        safe_title = "".join(c for c in presentation_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title[:30] or "presentation"
        
        # Return appropriate format
        if export_format == "pptx":
            return StreamingResponse(
                result['pptx'],
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                headers={"Content-Disposition": f"attachment; filename={safe_title}.pptx"}
            )
        elif export_format == "pdf":
            if result['pdf']:
                return StreamingResponse(
                    result['pdf'],
                    media_type="application/pdf",
                    headers={"Content-Disposition": f"attachment; filename={safe_title}.pdf"}
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="PDF export is not available. Please use PPTX format or ensure LibreOffice is installed."
                )
        elif export_format == "both":
            return {
                "status": "success",
                "message": "Use separate requests for PPTX and PDF",
                "metadata": result['metadata'],
                "available_formats": ["pptx", "pdf"] if result['pdf'] else ["pptx"]
            }
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Document slide generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process document: {str(e)}")

@router.post("/slides")
async def generate_slides_legacy(request: SlidesFromPromptRequest):
    """
    Legacy endpoint - generates slides from prompt alone
    For backward compatibility
    """
    try:
        # Use prompt as both content and title if no clear structure
        result = generate_slides_util(
            content=request.prompt,
            title=request.title,
            prompt=None,
            template=request.template,
            export_format=request.export_format
        )
        
        if request.export_format == "pptx":
            return StreamingResponse(
                result['pptx'],
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                headers={"Content-Disposition": f"attachment; filename={request.title}.pptx"}
            )
        else:
            return result['metadata']
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
