from typing import List


class QueryProcessor:

    # Only words that genuinely indicate dependency
    # on previous conversation.
    FOLLOW_UP_KEYWORDS = {
        "it",
        "its",
        "this",
        "that",
        "these",
        "those",
        "they",
        "them",
        "again",
        "continue",
        "previous",
        "above",
        "same",
    }

    @staticmethod
    def is_follow_up(question: str) -> bool:

        question = question.lower().strip()

        words = set(
            question.replace("?", "")
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        return bool(words & QueryProcessor.FOLLOW_UP_KEYWORDS)

    @staticmethod
    def build_search_query(
        question: str,
        history: List[dict],
    ) -> str:

        question = question.strip()

        # No history → use question directly
        if not history:
            return question

        # Standalone question → use it directly
        if not QueryProcessor.is_follow_up(question):
            return question

        # Only use previous USER questions for follow-ups.
        previous_questions = []

        for message in history[-4:]:

            if message["role"] == "user":
                previous_questions.append(message["content"])

        if not previous_questions:
            return question

        return (
            "Previous Topic:\n"
            + "\n".join(previous_questions)
            + "\n\nCurrent Question:\n"
            + question
        )