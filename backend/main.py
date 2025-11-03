"""
Advanced Customer Service AI - FastAPI Backend

This is the main entry point for the FastAPI application.
It provides REST API endpoints for the multi-agent customer service system.

LangChain Version: v1.0+
Last Updated: November 2, 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from dotenv import load_dotenv
import os
import logging
import re

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Advanced Customer Service AI",
    description="Multi-agent AI system for customer service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
# Pydantic Models for Request/Response Validation
# ============================================================================


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint.
    
    Validates incoming chat requests with message content and session management.
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User's message to the AI assistant",
        examples=["Hello, I need help with my account"]
    )
    session_id: str = Field(
        ...,
        description="UUID v4 session identifier for conversation continuity",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    
    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, v: str) -> str:
        """
        Validate that session_id is a valid UUID v4 format.
        
        Args:
            v: The session_id string to validate
            
        Returns:
            str: The validated session_id
            
        Raises:
            ValueError: If session_id is not a valid UUID v4
        """
        # UUID v4 pattern: 8-4-4-4-12 hexadecimal characters
        uuid_pattern = r'^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$'
        
        if not re.match(uuid_pattern, v.lower()):
            raise ValueError(
                "session_id must be a valid UUID v4 format "
                "(e.g., '550e8400-e29b-41d4-a716-446655440000')"
            )
        
        return v.lower()  # Normalize to lowercase
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Hello, I need help with my account",
                    "session_id": "550e8400-e29b-41d4-a716-446655440000"
                },
                {
                    "message": "What are your pricing plans?",
                    "session_id": "123e4567-e89b-12d3-a456-426614174000"
                }
            ]
        }
    }


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint.
    
    Returns the AI assistant's response along with metadata.
    """
    response: str = Field(
        ...,
        description="AI assistant's response to the user's message",
        examples=["I'd be happy to help you with your account. What specific issue are you experiencing?"]
    )
    session_id: str = Field(
        ...,
        description="Echo back the session_id for confirmation",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "response": "I'd be happy to help you with your account. What specific issue are you experiencing?",
                    "session_id": "550e8400-e29b-41d4-a716-446655440000"
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """
    Error response model for consistent error handling.
    
    Used when requests fail validation or processing.
    """
    error: str = Field(
        ...,
        description="User-friendly error message",
        examples=["Invalid session ID format"]
    )
    detail: str = Field(
        ...,
        description="Technical details about the error",
        examples=["session_id must be a valid UUID v4 format"]
    )
    session_id: str | None = Field(
        None,
        description="Session ID if available",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "Invalid request",
                    "detail": "session_id must be a valid UUID v4 format",
                    "session_id": None
                }
            ]
        }
    }


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
        "environment": os.getenv("ENVIRONMENT", "development"),
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
        "version": "1.0.0",
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
        log_level=os.getenv("LOG_LEVEL", "info").lower(),
    )
