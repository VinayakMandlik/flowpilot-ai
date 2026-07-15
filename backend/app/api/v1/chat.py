from fastapi import APIRouter
from pydantic import BaseModel

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.ai_service import AIService

router = APIRouter(prefix="/api/v1", tags=["Chat"])


class ChatRequest(BaseModel):
    question: str


@router.post("/chat")
async def chat(request: ChatRequest):

    # Step 1: Convert question into embedding
    question_vector = EmbeddingService.get_embedding(request.question)

    # Step 2: Search Qdrant
    vector_service = VectorService()
    results = vector_service.search(question_vector)

    # Step 3: Build context
    context_parts = []
    sources = []

    for point in results:

        payload = point.payload

        context_parts.append(
            f"""
========================
Document : {payload['filename']}
Chunk : {payload['chunk_number']}
========================

{payload['text']}
"""
        )

        sources.append({
            "filename": payload["filename"],
            "chunk_number": payload["chunk_number"],
            "score": round(point.score, 4)
        })

    context = "\n\n".join(context_parts)

    # Step 4: Ask Gemini
    answer = AIService.generate_answer(
        context=context,
        question=request.question
    )

    return {
        "answer": answer,
        "sources": sources,
        # "context": context   # Uncomment only while debugging
    }