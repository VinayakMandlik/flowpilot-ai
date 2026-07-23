from app.core.supabase import supabase


class ChatSessionService:

    @staticmethod
    def create_session(title: str, document_id: str):

        response = (
            supabase
            .table("chat_sessions")
            .insert({
                "title": title,
                "document_id": document_id
            })
            .execute()
        )

        return response.data[0]

    @staticmethod
    def get_sessions():

        response = (
            supabase
            .table("chat_sessions")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        return response.data

    @staticmethod
    def get_session(session_id: str):

        response = (
            supabase
            .table("chat_sessions")
            .select("*")
            .eq("id", session_id)
            .single()
            .execute()
        )

        return response.data

    @staticmethod
    def rename_session(session_id: str, title: str):

        response = (
            supabase
            .table("chat_sessions")
            .update({
                "title": title
            })
            .eq("id", session_id)
            .execute()
        )

        return response.data[0]


    @staticmethod
    def save_message(
        session_id: str,
        role: str,
        content: str,
        sources=None,
    ):

        supabase \
            .table("chat_messages") \
            .insert({
                "session_id": session_id,
                "role": role,
                "content": content,
                "sources": sources,
            }) \
            .execute()

    @staticmethod
    def get_messages(session_id: str):

        response = (
            supabase
            .table("chat_messages")
            .select("*")
            .eq("session_id", session_id)
            .order("created_at")
            .execute()
        )

        return response.data
    @staticmethod
    def delete_session(session_id: str):

        supabase.table("chat_messages") \
            .delete() \
            .eq("session_id", session_id) \
            .execute()

        supabase.table("chat_sessions") \
            .delete() \
            .eq("id", session_id) \
            .execute()

        return {"message": "Session deleted successfully"}