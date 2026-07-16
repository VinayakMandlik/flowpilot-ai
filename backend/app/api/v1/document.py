from fastapi import APIRouter

from app.services.document_service import DocumentService

router = APIRouter(
    prefix="/api/v1/documents",
    tags=["Documents"]
)


@router.get("")
def get_documents():

    return DocumentService.get_all_documents()
@router.delete("/{document_id}")
def delete_document(document_id: str):

    return DocumentService.delete_document(document_id)