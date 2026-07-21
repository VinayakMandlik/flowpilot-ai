from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.document import router as document_router
from app.api.v1.upload import router as upload_router
from app.api.v1.chat import router as chat_router
from app.api.v1.chat_document import router as chat_document_router
from app.api.v1 import chat_session
app = FastAPI(
    title="FlowPilot AI"
)

# -----------------------------
# CORS Configuration
# -----------------------------
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Routes
# -----------------------------
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)
app.include_router(chat_document_router)
app.include_router(chat_session.router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "FlowPilot AI Running"
    }