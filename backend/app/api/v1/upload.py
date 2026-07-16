from fastapi import APIRouter, UploadFile, File
import os

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService

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

    # Create document record in Supabase
    document = DocumentService.create_document(
        filename=file.filename,
        total_chunks=len(chunks)
    )

    vector_service = VectorService()

    first_vector = EmbeddingService.get_embedding(chunks[0])
    vector_service.create_collection(len(first_vector))

    stored_count = 0

    for index, chunk in enumerate(chunks):

        try:

            vector = EmbeddingService.get_embedding(chunk)

            vector_service.store_chunk(
                vector=vector,
                text=chunk,
                filename=file.filename,
                chunk_number=index,
                document_id=document["id"],
            )

            stored_count += 1
            print(f"Stored {stored_count}/{len(chunks)}")

        except Exception as e:
            print(f"Failed chunk {index + 1}: {e}")

    return {
        "document_id": document["id"],
        "filename": file.filename,
        "total_chunks": len(chunks),
        "stored_chunks": stored_count,
    }