from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from..services.llm_service import LLMService
from..core.config import get_llm_service

# Define Pydantic models for request and response
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Create an API router
router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def handle_chat(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Handles a chat request by invoking the LLM service.
    """
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    try:
        reply = llm_service.invoke(request.message)
        return ChatResponse(reply=reply)
    except Exception as e:
        # Log the exception details in a real application
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")