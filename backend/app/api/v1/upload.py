from fastapi import APIRouter, UploadFile, File
from app.core.supabase import supabase

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.pdf_service import PDFService
from app.services.chunk_service import ChunkService
from app.services.document_service import DocumentService

router = APIRouter(prefix="/api/v1", tags=["Upload"])


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    file_bytes = await file.read()

    # Upload PDF to Supabase Storage
    supabase.storage.from_("documents").upload(
        path=file.filename,
        file=file_bytes,
        file_options={
            "content-type": "application/pdf",
            "upsert": "true",
        },
    )

    # Extract pages
    pages = PDFService.extract_pages(file_bytes)

    chunks = []

    for page in pages:

        page_chunks = ChunkService.chunk_text(page["text"])

        for chunk in page_chunks:

            chunks.append(
                {
                    "text": chunk,
                    "page": page["page"],
                }
            )

    document = DocumentService.create_document(
        filename=file.filename,
        total_chunks=len(chunks),
    )

    vector_service = VectorService()

    first_vector = EmbeddingService.get_embedding(
        chunks[0]["text"]
    )

    vector_service.create_collection(len(first_vector))

    stored_count = 0

    for index, chunk in enumerate(chunks):

        try:

            vector = EmbeddingService.get_embedding(
                chunk["text"]
            )

            vector_service.store_chunk(
                vector=vector,
                text=chunk["text"],
                filename=file.filename,
                chunk_number=index,
                page=chunk["page"],
                document_id=document["id"],
            )

            stored_count += 1

        except Exception as e:
            print(e)

    return {
        "document_id": document["id"],
        "filename": file.filename,
        "total_chunks": len(chunks),
        "stored_chunks": stored_count,
    }