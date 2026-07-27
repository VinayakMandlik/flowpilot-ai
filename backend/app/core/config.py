from dotenv import load_dotenv
import os

load_dotenv()


class Settings:

    # =========================
    # LLM Configuration
    # =========================

    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")
    LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OLLAMA_URL = os.getenv(
        "OLLAMA_URL",
        "http://host.docker.internal:11434",
    )

    # =========================
    # Vector Database
    # =========================

    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # =========================
    # Database
    # =========================

    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")


settings = Settings()