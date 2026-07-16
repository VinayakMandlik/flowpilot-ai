from app.core.supabase import supabase
from app.services.vector_service import VectorService

class DocumentService:

    @staticmethod
    def create_document(filename: str, total_chunks: int):

        response = (
            supabase.table("documents")
            .insert({
                "filename": filename,
                "total_chunks": total_chunks,
            })
            .execute()
        )

        return response.data[0]
    @staticmethod
    def get_all_documents():

        response = (
            supabase
            .table("documents")
            .select("*")
            .order("uploaded_at", desc=True)
            .execute()
        )

        return response.data
    @staticmethod
    def delete_document(document_id: str):

        vector_service = VectorService()

        # Delete vectors
        vector_service.delete_document_chunks(document_id)

        # Delete metadata
        supabase.table("documents") \
            .delete() \
            .eq("id", document_id) \
            .execute()

        return {
            "message": "Document deleted successfully"
        }