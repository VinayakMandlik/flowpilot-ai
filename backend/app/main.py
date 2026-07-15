from fastapi import FastAPI

from app.api.v1.upload import router as upload_router
from app.api.v1.chat import router as chat_router

app = FastAPI(
    title="FlowPilot AI"
)

app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def home():
    return {
        "message": "FlowPilot AI Running"
    }