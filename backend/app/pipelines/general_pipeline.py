import json

from app.services.ai_service import AIService
from app.services.chat_session_service import ChatSessionService


class GeneralPipeline:

    @staticmethod
    async def execute(request, history):

        async def generate():

            # Save user message
            ChatSessionService.save_message(
                session_id=request.session_id,
                role="user",
                content=request.question,
            )

            full_answer = ""

            # Generate answer using LLM only
            for chunk in AIService.stream_general_answer(
                question=request.question,
                history=history,
            ):

                full_answer += chunk

                yield f"data: {json.dumps({'type': 'token', 'content': chunk})}\n\n"

            # Save AI response
            ChatSessionService.save_message(
                session_id=request.session_id,
                role="assistant",
                content=full_answer,
                sources=[],
            )

            yield f"data: {json.dumps({'type': 'sources', 'content': []})}\n\n"

            yield "data: {\"type\":\"done\"}\n\n"

        return generate()