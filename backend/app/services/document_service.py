from app.core.supabase import supabase
from app.services.vector_service import VectorService


class DocumentService:

    @staticmethod
    def create_document(filename: str, total_chunks: int):

        response = (
            supabase.table("documents")
            .insert(
                {
                    "filename": filename,
                    "storage_path": filename,
                    "total_chunks": total_chunks,
                }
            )
            .execute()
        )

        return response.data[0]

    @staticmethod
    def get_all_documents():

        response = (
            supabase.table("documents")
            .select("*")
            .order("uploaded_at", desc=True)
            .execute()
        )

        return response.data

    @staticmethod
    def delete_document(document_id: str):

        response = (
            supabase.table("documents")
            .select("*")
            .eq("id", document_id)
            .single()
            .execute()
        )

        document = response.data

        if not document:
            return {
                "message": "Document not found"
            }

        # Delete file from Supabase Storage
        supabase.storage.from_("documents").remove(
            [document["storage_path"]]
        )

        # Delete vectors from Qdrant
        vector_service = VectorService()
        vector_service.delete_document_chunks(document_id)

        # Delete document metadata
        (
            supabase.table("documents")
            .delete()
            .eq("id", document_id)
            .execute()
        )

        return {
            "message": "Document deleted successfully"
        }