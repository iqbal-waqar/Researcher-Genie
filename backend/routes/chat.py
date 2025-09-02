from fastapi import APIRouter, HTTPException
from backend.schemas.chat import ChatMessage, ChatResponse
from backend.interactors.chat import ChatInteractor

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_with_agent(chat_message: ChatMessage) -> ChatResponse:
    try:
        chat_interactor = ChatInteractor()
        return chat_interactor.process_chat(chat_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")