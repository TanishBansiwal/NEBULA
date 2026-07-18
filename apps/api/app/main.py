from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth
from app.routers import users
from app.routers import conversations
from app.routers import messages
from app.routers import chat
from app.routers import documents

app = FastAPI(
    title="Nebula API",
    version="0.1.0",
    description="Backend API for the Nebula 3D Platform",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173/",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include_router
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(users.router)

app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(chat.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Nebula API 🚀"
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "Nebula API",
        "version": "0.1.0"
    }