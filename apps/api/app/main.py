from fastapi import FastAPI
from app.routers import auth
from app.routers import users
from app.routers import conversations
from app.routers import messages
from app.routers import chat



app = FastAPI(
    title="Nebula API",
    version="0.1.0",
    description="Backend API for the Nebula 3D Platform"
)

app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"],
)

app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(chat.router)

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