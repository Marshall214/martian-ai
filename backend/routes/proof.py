from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.proof_ai import proofread_text

router = APIRouter()

class ProofreadRequest(BaseModel):
    text: str

@router.post("/proofread")
async def proofread(request: ProofreadRequest):
    """
    Endpoint for AI-based proofreading and humanization.
    Accepts text input (50-1500 words) and returns:
    - Original text with word count
    - Humanized version with word count
    - AI detection scores before and after
    - Improvement metrics
    """
    try:
        result = proofread_text(request.text)
        return {
            "status": "success",
            "original_text": result["original_text"],
            "humanized_text": result["humanized_text"],
            "original_word_count": result["original_word_count"],
            "humanized_word_count": result["humanized_word_count"],
            "ai_score_before_humanizing": result["ai_score_before_humanizing"],
            "ai_score_after_humanizing": result["ai_score_after_humanizing"],
            "improvement_percentage": result["improvement_percentage"],
            "word_limit": {"min": 50, "max": 1500}
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")
