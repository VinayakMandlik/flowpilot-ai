from fastapi import APIRouter
from pydantic import BaseModel

from app.services.chat_session_service import ChatSessionService

router = APIRouter(
    prefix="/api/v1",
    tags=["Chat Sessions"]
)


class CreateSessionRequest(BaseModel):
    title: str
    document_id: str


@router.post("/chat/session")
async def create_session(request: CreateSessionRequest):

    session = ChatSessionService.create_session(
        title=request.title,
        document_id=request.document_id,
    )

    return session


@router.get("/chat/session")
async def get_sessions():

    return ChatSessionService.get_sessions()


@router.get("/chat/session/{session_id}")
async def get_session_messages(session_id: str):

    return ChatSessionService.get_messages(session_id)


@router.delete("/chat/session/{session_id}")
async def delete_session(session_id: str):

    return ChatSessionService.delete_session(session_id)