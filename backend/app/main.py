from fastapi import FastAPI
from app.api.v1.document import router as document_router
from app.api.v1.upload import router as upload_router
from app.api.v1.chat import router as chat_router
from app.api.v1.chat_document import router as chat_document_router
app = FastAPI(
    title="FlowPilot AI"
)
# app.include_router(upload_router)
app.include_router(upload_router)
app.include_router(chat_router)
app.include_router(document_router)
app.include_router(chat_document_router)
@app.get("/")
def home():
    return {
        "message": "FlowPilot AI Running"
    }