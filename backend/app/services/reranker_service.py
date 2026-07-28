from typing import List


class RerankerService:

    MAX_RESULTS = 5

    @staticmethod
    def rerank(
        query: str,
        results: List,
        max_results: int = MAX_RESULTS,
    ) -> List:
        """
        Re-ranks vector search results.

        Current implementation:
        - Removes duplicate chunks
        - Sorts by similarity score
        - Returns the top N chunks

        This service is intentionally isolated so we can later
        replace the logic with a cross-encoder reranker without
        changing the pipelines.
        """

        if not results:
            return []

        ranked = sorted(
            results,
            key=lambda x: x.score,
            reverse=True,
        )

        unique = []
        seen = set()

        for point in ranked:

            payload = point.payload

            key = (
                payload.get("filename"),
                payload.get("page"),
                payload.get("chunk_number"),
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(point)

            if len(unique) >= max_results:
                break

        return unique