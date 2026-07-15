from fastapi import FastAPI
from app.services.vector_service import VectorService
from app.api.v1.upload import router as upload_router
from app.services.ai_service import AIService
from app.services.embedding_service import EmbeddingService
app = FastAPI(
    title="FlowPilot AI"
)

app.include_router(upload_router)


@app.get("/")
def home():
    return {
        "message": "FlowPilot AI Running"
    }
@app.get("/test-ai")
def test_ai():

    answer = AIService.ask(
        "In one sentence, explain what FlowPilot AI is."
    )

    return {
        "answer": answer
    }
@app.get("/test-qdrant")
def test_qdrant():

    service = VectorService()

    return {
        "message": service.create_collection()
    }
@app.get("/test-embedding")
def test_embedding():

    vector = EmbeddingService.get_embedding(
        "FlowPilot AI is an enterprise document assistant."
    )

    return {
        "dimensions": len(vector),
        "first_10_values": vector[:10]
    }