from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import json

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.ai_service import AIService
from app.services.chat_session_service import ChatSessionService

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

    # Generate embedding for user's question
    question_vector = EmbeddingService.get_embedding(
        request.question
    )

    vector_service = VectorService()

    # Search only inside the selected document
    results = vector_service.search_document(
        vector=question_vector,
        document_id=request.document_id,
    )

    context_parts = []
    sources = []

    for point in results:
        payload = point.payload

        context_parts.append(
            f"""
========================
Document : {payload["filename"]}
Page : {payload["page"]}
Chunk : {payload["chunk_number"]}
========================

{payload["text"]}
"""
        )

        sources.append(
            {
                "filename": payload["filename"],
                "page": payload["page"],
                "chunk_number": payload["chunk_number"],
                "score": round(point.score, 4),
            }
        )

    context = "\n\n".join(context_parts)

    async def generate():

        # Save user's message
        ChatSessionService.save_message(
            session_id=request.session_id,
            role="user",
            content=request.question,
        )

        full_answer = ""

        # Stream Gemini response
        for chunk in AIService.stream_answer(
            context=context,
            question=request.question,
        ):
            full_answer += chunk

            yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"

        # Save AI response
        ChatSessionService.save_message(
            session_id=request.session_id,
            role="assistant",
            content=full_answer,
            sources=sources,
        )

        # Send sources to frontend
        yield f"data: {json.dumps({'type': 'sources', 'content': sources})}\n\n"

        # Notify frontend that streaming is complete
        yield "data: {\"type\":\"done\"}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )