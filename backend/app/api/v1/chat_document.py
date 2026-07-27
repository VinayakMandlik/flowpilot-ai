from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import logging

from app.services.intent_router import IntentRouter
from app.services.chat_session_service import ChatSessionService
from app.pipelines.pipeline_factory import PipelineFactory

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"]
)


class ChatDocumentRequest(BaseModel):
    question: str
    document_id: str
    session_id: str


@router.post("/chat/document")
async def chat_document(request: ChatDocumentRequest):

    # ------------------------------------------------------------------
    # Load recent conversation history
    # ------------------------------------------------------------------
    history = ChatSessionService.get_recent_history(
        request.session_id,
        limit=6,
    )

    # ------------------------------------------------------------------
    # Detect intent
    # ------------------------------------------------------------------
    intent = IntentRouter.detect(
        question=request.question,
        has_document=True,
    )

    logger.info("=" * 80)
    logger.info("Question: %s", request.question)
    logger.info("Intent: %s", intent.value)
    logger.info("=" * 80)

    # ------------------------------------------------------------------
    # Route request
    # ------------------------------------------------------------------
    pipeline = PipelineFactory.get(intent)

    generator = await pipeline.execute(
        request=request,
        history=history,
    )

    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )