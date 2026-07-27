import json

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.ai_service import AIService
from app.services.chat_session_service import ChatSessionService
from app.services.query_processor import QueryProcessor


class RagPipeline:

    @staticmethod
    async def execute(request, history):

        retrieval_query = QueryProcessor.build_search_query(
            request.question,
            history,
        )

        question_vector = EmbeddingService.get_embedding(
            retrieval_query
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
                    "text": payload["text"],
                }
            )

        context = "\n\n".join(context_parts)

        async def generate():

            ChatSessionService.save_message(
                session_id=request.session_id,
                role="user",
                content=request.question,
            )

            full_answer = ""

            for chunk in AIService.stream_rag_answer(
                context=context,
                question=request.question,
                history=history,
            ):

                full_answer += chunk

                yield f"data: {json.dumps({'type':'token','content':chunk})}\n\n"

            ChatSessionService.save_message(
                session_id=request.session_id,
                role="assistant",
                content=full_answer,
                sources=sources,
            )

            yield f"data: {json.dumps({'type':'sources','content':sources})}\n\n"

            yield "data: {\"type\":\"done\"}\n\n"

        return generate()