from time import perf_counter

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.reranker_service import RerankerService
from app.services.confidence_service import ConfidenceService
from app.services.citation_service import CitationService
from app.services.query_processor import QueryProcessor


class RetrievalService:

    @staticmethod
    def retrieve(
        question: str,
        history,
        document_id: str,
    ):

        started = perf_counter()

        retrieval_query = QueryProcessor.build_search_query(
            question,
            history,
        )
        # print("=" * 80)
        # print("ORIGINAL QUESTION:")
        # print(question)
        # print()

        # print("RETRIEVAL QUERY:")
        # print(retrieval_query)
        # print("=" * 80)

        embedding_started = perf_counter()

        question_vector = EmbeddingService.get_embedding(
            retrieval_query
        )

        embedding_time = round(
            perf_counter() - embedding_started,
            3,
        )

        vector_service = VectorService()

        search_started = perf_counter()

        results = vector_service.search_document(
            vector=question_vector,
            document_id=document_id,
        )

        search_time = round(
            perf_counter() - search_started,
            3,
        )

        rerank_started = perf_counter()

        ranked_results = RerankerService.rerank(
            query=retrieval_query,
            results=results,
        )

        rerank_time = round(
            perf_counter() - rerank_started,
            3,
        )

        confidence = ConfidenceService.calculate(
            ranked_results
        )

        context = CitationService.build_context(
            ranked_results
        )

        sources = CitationService.build_sources(
            ranked_results
        )

        total_time = round(
            perf_counter() - started,
            3,
        )

        # print("\n" + "=" * 80)
        # print("RETRIEVAL REPORT")
        # print("=" * 80)
        # print(f"Question      : {question}")
        # print(f"Embedding     : {embedding_time}s")
        # print(f"Vector Search : {search_time}s")
        # print(f"Rerank        : {rerank_time}s")
        # print(f"Confidence    : {confidence:.2f}")
        # print(f"Chunks        : {len(ranked_results)}")
        # print(f"Total Time    : {total_time}s")
        # print("-" * 80)

        # for index, point in enumerate(ranked_results, start=1):

        #     payload = point.payload

        #     print(
        #         f"[{index}] "
        #         f"{payload['filename']} | "
        #         f"Page {payload['page']} | "
        #         f"Chunk {payload['chunk_number']} | "
        #         f"Score {point.score:.4f}"
        #     )

        # print("=" * 80 + "\n")

        return {
            "context": context,
            "sources": sources,
            "confidence": confidence,
            "results": ranked_results,
        }