from google import genai

from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)


class AIService:

    @staticmethod
    def generate_answer(context: str, question: str):

        prompt = f"""
You are FlowPilot AI, an enterprise document assistant.

Your task is to answer the user's question using ONLY the information provided in the context.

Instructions:

- Read every retrieved document carefully.
- If the answer exists, explain it clearly.
- You may infer explanations from SQL code examples.
- Never make up facts.
- If the answer is not present anywhere in the context, reply exactly:

"I couldn't find this information in the uploaded documents."

======================== CONTEXT ========================

{context}

======================== QUESTION ========================

{question}

======================== ANSWER ==========================
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        return response.text

    @staticmethod
    def stream_answer(context: str, question: str):

        prompt = f"""
You are FlowPilot AI, an enterprise document assistant.

Your task is to answer the user's question using ONLY the information provided in the context.

Instructions:

- Read every retrieved document carefully.
- If the answer exists, explain it clearly.
- You may infer explanations from SQL code examples.
- Never make up facts.
- If the answer is not present anywhere in the context, reply exactly:

"I couldn't find this information in the uploaded documents."

======================== CONTEXT ========================

{context}

======================== QUESTION ========================

{question}

======================== ANSWER ==========================
"""

        response = client.models.generate_content_stream(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text