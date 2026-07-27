from typing import List


class QueryProcessor:

    FOLLOW_UP_KEYWORDS = {
        "it",
        "this",
        "that",
        "these",
        "those",
        "continue",
        "again",
        "previous",
        "above",
        "same",
        "example",
        "sql",
        "query",
        "optimize",
        "rewrite",
        "simplify",
        "why",
        "how",
        "explain",
    }

    @staticmethod
    def is_follow_up(question: str) -> bool:

        question = question.lower()

        words = set(question.replace("?", "").split())

        return bool(words & QueryProcessor.FOLLOW_UP_KEYWORDS)

    @staticmethod
    def build_search_query(question: str, history: List[dict]) -> str:

        if not history:
            return question

        if not QueryProcessor.is_follow_up(question):
            return question

        recent_messages = history[-4:]

        previous_context = []

        for msg in recent_messages:

            if msg["role"] == "user":
                previous_context.append(msg["content"])

        previous_context = "\n".join(previous_context)

        return f"""
Conversation Context:

{previous_context}

Current User Question:

{question}
"""