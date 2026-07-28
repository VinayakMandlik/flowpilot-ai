from app.providers.provider_factory import ProviderFactory
from app.services.prompt_builder import PromptBuilder


class AIService:

    @staticmethod
    def _build_history(history):

        if not history:
            return "No previous conversation."

        formatted = []

        for message in history:

            role = (
                "User"
                if message["role"] == "user"
                else "Assistant"
            )

            formatted.append(
                f"{role}: {message['content']}"
            )

        return "\n\n".join(formatted)

    @staticmethod
    def _stream(prompt: str):

        provider = ProviderFactory.get_provider()

        yield from provider.stream(prompt)

    @staticmethod
    def stream_rag_answer(
        context: str,
        question: str,
        history=None,
    ):

        history_text = AIService._build_history(history)
        # print("\n" + "=" * 100)
        # print("CONTEXT LENGTH:", len(context))
        # print("=" * 100)
        # print(context[:3000])  # Print first 3000 characters
        # print("=" * 100)

        prompt = PromptBuilder.build_rag_prompt(
            context=context,
            question=question,
            history_text=history_text,
        )
        # print("\n" + "=" * 100)
        # print("PROMPT SENT TO GEMINI")
        # print("=" * 100)
        # print(prompt)
        # print("=" * 100)

        yield from AIService._stream(prompt)

    @staticmethod
    def stream_general_answer(
        question: str,
        history=None,
    ):

        history_text = AIService._build_history(history)

        prompt = PromptBuilder.build_general_prompt(
            question=question,
            history_text=history_text,
        )

        yield from AIService._stream(prompt)