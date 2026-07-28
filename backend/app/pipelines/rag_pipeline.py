import json

from app.services.ai_service import AIService
from app.services.chat_session_service import ChatSessionService
from app.services.retrieval_service import RetrievalService


class RagPipeline:

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

            if (
                not context.strip()
                or confidence < RagPipeline.MIN_CONFIDENCE
            ):

                answer = (
                    "The uploaded document does not contain enough "
                    "relevant information to answer this question."
                )

                ChatSessionService.save_message(
                    session_id=request.session_id,
                    role="assistant",
                    content=answer,
                    sources=[],
                )

                yield (
                    f"data: {json.dumps({'type':'token','content':answer})}\n\n"
                )

                yield (
                    f"data: {json.dumps({'type':'confidence','content':confidence})}\n\n"
                )

                yield (
                    f"data: {json.dumps({'type':'sources','content':[]})}\n\n"
                )

                yield 'data: {"type":"done"}\n\n'
                return

            full_answer = ""

            for chunk in AIService.stream_rag_answer(
                context=context,
                question=request.question,
                history=history,
            ):

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