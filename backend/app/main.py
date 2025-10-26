from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="One Button Game API", version="0.1.0")

# CORS middleware for Telegram Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://web.telegram.org", "https://telegram.org"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint for container monitoring."""
    return {"status": "healthy"}


@app.get("/api/")
async def root():
    """API root endpoint."""
    return {
        "message": "One Button Game API",
        "version": "0.1.0",
        "docs": "/docs",
    }
