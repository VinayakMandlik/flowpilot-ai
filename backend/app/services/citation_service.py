class CitationService:

    @staticmethod
    def build_context(results):

        context_parts = []

        for point in results:

            payload = point.payload

            context_parts.append(
                f"""
========================
Source {len(context_parts)+1}

Document : {payload["filename"]}
Page : {payload["page"]}
Chunk : {payload["chunk_number"]}
Similarity : {round(point.score,4)}
========================

{payload["text"]}
"""
            )

        return "\n\n".join(context_parts)

    @staticmethod
    def build_sources(results):

        sources = []

        for point in results:

            payload = point.payload

            sources.append(
                {
                    "id": len(sources) + 1,
                    "filename": payload["filename"],
                    "page": payload["page"],
                    "chunk_number": payload["chunk_number"],
                    "score": round(point.score, 4),
                    "text": payload["text"],
                }
            )

        return sources