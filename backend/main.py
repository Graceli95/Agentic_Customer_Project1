"""
Advanced Customer Service AI - FastAPI Backend

This is the main entry point for the FastAPI application.
It provides REST API endpoints for the multi-agent customer service system.

LangChain Version: v1.0+
Last Updated: November 2, 2025
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent AI system for customer service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        dict: Status information about the service
    """
    return {
        "status": "healthy",
        "service": "customer-service-ai",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        dict: Welcome message and API details
    """
    return {
        "message": "Welcome to Advanced Customer Service AI",
        "docs": "/docs",
        "health": "/health",
        "version": "1.0.0"
    }

# ============================================================================
# Application Startup/Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Execute tasks on application startup."""
    logger.info("Starting Advanced Customer Service AI backend...")
    logger.info(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    logger.info(f"CORS origins: {cors_origins}")

@app.on_event("shutdown")
async def shutdown_event():
    """Execute cleanup tasks on application shutdown."""
    logger.info("Shutting down Advanced Customer Service AI backend...")

# ============================================================================
# Run Application
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,  # Enable auto-reload during development
        log_level=os.getenv("LOG_LEVEL", "info").lower()
    )
