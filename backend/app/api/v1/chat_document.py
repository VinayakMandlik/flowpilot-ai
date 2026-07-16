from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.ai_service import AIService


router = APIRouter(
    prefix="/api/v1",
    tags=["Chat"]
)


class ChatDocumentRequest(BaseModel):
    question: str
    document_id: str


@router.post("/chat/document")
async def chat_document(request: ChatDocumentRequest):

    question_vector = EmbeddingService.get_embedding(
        request.question
    )

    vector_service = VectorService()

    results = vector_service.search_document(
        vector=question_vector,
        document_id=request.document_id,
    )

    context_parts = []
    sources = []

    for point in results:

        payload = point.payload

        context_parts.append(payload["text"])

        sources.append({
            "filename": payload["filename"],
            "chunk_number": payload["chunk_number"],
            "score": round(point.score, 4)
        })

    context = "\n\n".join(context_parts)

    answer = AIService.generate_answer(
        context=context,
        question=request.question
    )

    return {
        "answer": answer,
        "sources": sources
    }