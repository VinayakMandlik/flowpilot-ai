from uuid import uuid4

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue,
    PayloadSchemaType,
)

from app.core.config import settings


class VectorService:

    COLLECTION = "flowpilot"

    DEFAULT_LIMIT = 12

    def __init__(self):

        self.client = QdrantClient(
            url=settings.QDRANT_URL,
            api_key=settings.QDRANT_API_KEY,
        )

    def create_collection(self, vector_size):

        collections = self.client.get_collections().collections
        names = [c.name for c in collections]

        if self.COLLECTION not in names:

            self.client.create_collection(
                collection_name=self.COLLECTION,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE,
                ),
            )

        try:
            self.client.create_payload_index(
                collection_name=self.COLLECTION,
                field_name="document_id",
                field_schema=PayloadSchemaType.KEYWORD,
            )
        except Exception:
            pass

    def store_chunk(
        self,
        vector,
        text,
        filename,
        chunk_number,
        page,
        document_id,
    ):

        self.client.upsert(
            collection_name=self.COLLECTION,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "document_id": document_id,
                        "text": text,
                        "filename": filename,
                        "chunk_number": chunk_number,
                        "page": page,
                    },
                )
            ],
        )

    def search(
        self,
        vector,
        limit=None,
        score_threshold=0.35,
    ):

        if limit is None:
            limit = self.DEFAULT_LIMIT

        results = self.client.query_points(
            collection_name=self.COLLECTION,
            query=vector,
            limit=limit,
            score_threshold=score_threshold,
        )

        return sorted(
            results.points,
            key=lambda x: x.score,
            reverse=True,
        )

    def search_document(
        self,
        vector,
        document_id,
        limit=None,
        score_threshold=0.35,
    ):

        if limit is None:
            limit = self.DEFAULT_LIMIT

        results = self.client.query_points(
            collection_name=self.COLLECTION,
            query=vector,
            query_filter=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
            limit=limit,
            score_threshold=score_threshold,
        )

        ranked = sorted(
            results.points,
            key=lambda x: x.score,
            reverse=True,
        )

        unique = []
        seen = set()

        for point in ranked:

            payload = point.payload

            key = (
                payload["page"],
                payload["chunk_number"],
            )

            if key in seen:
                continue

            seen.add(key)
            unique.append(point)

        return unique

    def delete_document_chunks(self, document_id):

        self.client.delete(
            collection_name=self.COLLECTION,
            points_selector=Filter(
                must=[
                    FieldCondition(
                        key="document_id",
                        match=MatchValue(value=document_id),
                    )
                ]
            ),
        )