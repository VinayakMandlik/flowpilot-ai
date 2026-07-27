from enum import Enum


class Intent(str, Enum):
    RAG = "rag"
    GENERAL = "general"
    HYBRID = "hybrid"


class IntentRouter:

    DOCUMENT_KEYWORDS = {
        "document",
        "pdf",
        "page",
        "section",
        "chapter",
        "uploaded",
        "question",
        "table",
        "figure",
        "paragraph",
        "line",
        "this",
        "that",
        "it",
        "above",
        "below",
        "previous",
    }

    GENERAL_PATTERNS = (
        "what is",
        "who is",
        "when did",
        "where is",
        "why is",
        "how does",
        "define",
        "explain",
        "difference between",
        "advantages of",
        "disadvantages of",
    )

    @staticmethod
    def detect(
        question: str,
        has_document: bool,
    ) -> Intent:

        question_lower = question.lower()

        if not has_document:
            return Intent.GENERAL

        words = set(question_lower.split())

        # Explicit document reference
        if words & IntentRouter.DOCUMENT_KEYWORDS:
            return Intent.RAG

        # Pure general knowledge question
        if any(
            question_lower.startswith(pattern)
            for pattern in IntentRouter.GENERAL_PATTERNS
        ):
            return Intent.GENERAL

        # Default to RAG when a document is selected
        return Intent.RAG