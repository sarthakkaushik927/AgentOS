from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
from app.db.models.user import User
from app.api.v1.deps import get_current_user

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatEvent(BaseModel):
    event_type: str
    content: str | dict

async def run_agent_reasoning_loop(request: ChatRequest, user: User) -> AsyncGenerator[str, None]:
    yield "LangGraph agent integration pending\n"

@router.post("", response_class=StreamingResponse)
async def chat_endpoint(request: ChatRequest, current_user: User = Depends(get_current_user)):
    return StreamingResponse(run_agent_reasoning_loop(request, current_user), media_type="text/event-stream")
