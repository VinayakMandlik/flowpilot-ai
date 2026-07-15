from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from uuid import uuid4

from app.core.config import settings


class VectorService:

    COLLECTION = "flowpilot"

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

    def store_chunk(self, vector, text, filename, chunk_number):

        self.client.upsert(
            collection_name=self.COLLECTION,
            points=[
                PointStruct(
                    id=str(uuid4()),
                    vector=vector,
                    payload={
                        "text": text,
                        "filename": filename,
                        "chunk_number": chunk_number,
                    },
                )
            ],
        )

    def search(self, vector, limit=8):

        results = self.client.query_points(
            collection_name=self.COLLECTION,
            query=vector,
            limit=limit,
        )

        return results.points