from fastapi import FastAPI

app = FastAPI(
    title="Nebula API",
    version="0.1.0",
    description="Backend API for the Nebula 3D Platform"
)


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