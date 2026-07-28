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
        "pages",
        "section",
        "chapter",
        "uploaded",
        "upload",
        "file",
        "table",
        "figure",
        "paragraph",
        "line",
        "context",
        "chunk",
        "according",
        "mentioned",
        "this",
        "that",
        "these",
        "those",
        "it",
        "its",
        "above",
        "below",
        "previous",
        "same",
        "again",
    }

    GENERAL_PATTERNS = (
        "who is",
        "when did",
        "where is",
        "tell me about",
    )

    @staticmethod
    def detect(
        question: str,
        has_document: bool,
    ) -> Intent:

        question = question.strip()
        question_lower = question.lower()

        if not has_document:
            return Intent.GENERAL

        words = set(question_lower.replace("?", "").split())

        if words & IntentRouter.DOCUMENT_KEYWORDS:
            return Intent.RAG

        if len(words) <= 5:
            return Intent.RAG

        if any(question_lower.startswith(pattern) for pattern in IntentRouter.GENERAL_PATTERNS):
            return Intent.GENERAL

        # If a document is open and the question does not explicitly
        # target the document or general knowledge, let the Hybrid
        # pipeline decide.
        return Intent.HYBRID