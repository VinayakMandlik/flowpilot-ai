from fastapi import APIRouter, UploadFile, File
import os
from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService

router = APIRouter(prefix="/api/v1", tags=["Upload"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    text = PDFService.extract_text(file_path)

    chunks = ChunkService.chunk_text(text)

    vector_service = VectorService()

    first_vector = EmbeddingService.get_embedding(chunks[0])
    vector_service.create_collection(len(first_vector))

    for chunk in chunks[:2]:
        vector = EmbeddingService.get_embedding(chunk)
        vector_service.store_chunk(vector, chunk)

    return {
        "filename": file.filename,
        "chunks": len(chunks),
        "message": "Stored successfully in Qdrant"
    }