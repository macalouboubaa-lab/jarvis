from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers import chat, memory, jobs, voice, agents

app = FastAPI(title="Jarvis API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(memory.router)
app.include_router(jobs.router)
app.include_router(voice.router)
app.include_router(agents.router)

@app.get("/health", tags=["Santé"])
async def health_check():
    return {"status": "healthy", "service": "Jarvis Souverain"}
