#!/usr/bin/env python3
"""
Main entry point for the Reward Personalization Agent.
"""
import uvicorn
from fastapi import FastAPI
from workspace.api.main import router as api_router
from workspace.settings import settings
from workspace.utils.logger import setup_logger

logger = setup_logger(__name__)

app = FastAPI(
    title="Reward Personalization Agent",
    description="AI-driven reward personalization and engagement optimization",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "0.1.0"}

if __name__ == "__main__":
    logger.info(f"Starting Reward Personalization Agent on port {settings.PORT}")
    uvicorn.run("workspace.app:app", host="0.0.0.0", port=settings.PORT, reload=settings.DEBUG)
