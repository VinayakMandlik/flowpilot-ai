import json

from app.services.ai_service import AIService
from app.services.chat_session_service import ChatSessionService
from app.services.retrieval_service import RetrievalService


class HybridPipeline:

    MIN_CONFIDENCE = 0.45

    @staticmethod
    async def execute(request, history):

        retrieval = RetrievalService.retrieve(
            question=request.question,
            history=history,
            document_id=request.document_id,
        )

        context = retrieval["context"]
        sources = retrieval["sources"]
        confidence = retrieval["confidence"]

        async def generate():

            ChatSessionService.save_message(
                session_id=request.session_id,
                role="user",
                content=request.question,
            )

            full_answer = ""

            if (
                context.strip()
                and confidence >= HybridPipeline.MIN_CONFIDENCE
            ):

                stream = AIService.stream_rag_answer(
                    context=context,
                    question=request.question,
                    history=history,
                )

            else:

                stream = AIService.stream_general_answer(
                    question=request.question,
                    history=history,
                )

            for chunk in stream:

                full_answer += chunk

                yield (
                    f"data: {json.dumps({'type':'token','content':chunk})}\n\n"
                )

            ChatSessionService.save_message(
                session_id=request.session_id,
                role="assistant",
                content=full_answer,
                sources=sources,
            )

            yield (
                f"data: {json.dumps({'type':'confidence','content':confidence})}\n\n"
            )

            yield (
                f"data: {json.dumps({'type':'sources','content':sources})}\n\n"
            )

            yield 'data: {"type":"done"}\n\n'

        return generate()