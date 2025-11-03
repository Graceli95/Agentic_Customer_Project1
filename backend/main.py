"""
Advanced Customer Service AI - FastAPI Backend

This is the main entry point for the FastAPI application.
It provides REST API endpoints for the multi-agent customer service system.

LangChain Version: v1.0+
Last Updated: November 2, 2025
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator, ValidationError
from dotenv import load_dotenv
import os
import logging
import re

# Import LangChain agent
from backend.agents import get_agent

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Import OpenAI for error handling
try:
    from openai import (
        APIError,
        APIConnectionError,
        RateLimitError,
        AuthenticationError,
        APITimeoutError,
    )
    OPENAI_AVAILABLE = True
except ImportError:
    # If OpenAI is not installed, disable specific error handling
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not found - using generic error handling")

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
# Chat Endpoint - LangChain Agent Integration
# ============================================================================


@app.post("/chat", response_model=ChatResponse, responses={
    400: {"model": ErrorResponse, "description": "Bad Request - Invalid input"},
    500: {"model": ErrorResponse, "description": "Internal Server Error"},
})
async def chat_endpoint(request: ChatRequest):
    """
    Process user messages through the LangChain customer service agent.
    
    This endpoint:
    - Validates the incoming message and session ID
    - Invokes the LangChain agent with conversation memory
    - Maintains conversation history per session (thread_id)
    - Returns the AI assistant's response
    
    Args:
        request: ChatRequest containing message and session_id
        
    Returns:
        ChatResponse: AI assistant's response with session confirmation
        
    Raises:
        HTTPException 400: Invalid session ID format
        HTTPException 500: Agent initialization error or LLM API error
        
    Example:
        Request:
        ```json
        {
            "message": "Hello, I need help with my account",
            "session_id": "550e8400-e29b-41d4-a716-446655440000"
        }
        ```
        
        Response:
        ```json
        {
            "response": "I'd be happy to help you with your account...",
            "session_id": "550e8400-e29b-41d4-a716-446655440000"
        }
        ```
    """
    try:
        logger.info(f"Received chat request for session: {request.session_id}")
        logger.debug(f"Message: {request.message[:50]}...")  # Log first 50 chars
        
        # Get the LangChain agent
        # This may raise RuntimeError if agent isn't initialized (missing API key)
        try:
            agent = get_agent()
        except RuntimeError as e:
            logger.error(f"Agent not initialized: {e}")
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Service configuration error",
                    "detail": str(e),
                    "session_id": request.session_id
                }
            )
        
        # Create configuration with thread_id for conversation memory
        # This enables the agent to maintain context across multiple messages
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Invoke the LangChain agent
        # The agent will:
        # 1. Load conversation history for this thread_id
        # 2. Process the new message with full context
        # 3. Generate a response using GPT-4o-mini
        # 4. Save the updated conversation to memory
        logger.info(f"Invoking agent for session: {request.session_id}")
        
        result = agent.invoke(
            {"messages": [{"role": "user", "content": request.message}]},
            config
        )
        
        # Extract the agent's response from the result
        # The last message in the conversation is the agent's response
        response_text = result["messages"][-1].content
        
        logger.info(f"Agent response generated for session: {request.session_id}")
        logger.debug(f"Response: {response_text[:50]}...")  # Log first 50 chars
        
        # Return the response with session confirmation
        return ChatResponse(
            response=response_text,
            session_id=request.session_id
        )
        
    except HTTPException:
        # Re-raise HTTPExceptions (validation errors, agent init errors)
        raise
    
    except ValidationError as e:
        # Handle Pydantic validation errors
        logger.warning(f"Validation error for session {request.session_id}: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid request format",
                "detail": str(e),
                "session_id": request.session_id
            }
        )
        
    except Exception as e:
        # OpenAI-specific error handling
        # Check error type and handle accordingly
        
        if OPENAI_AVAILABLE:
            if isinstance(e, AuthenticationError):
                # Invalid API key
                logger.error(f"OpenAI authentication error: {e}")
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "Service configuration error",
                        "detail": "API authentication failed. Please contact support.",
                        "session_id": request.session_id
                    }
                )
            
            elif isinstance(e, RateLimitError):
                # Rate limit exceeded
                logger.warning(f"OpenAI rate limit exceeded for session {request.session_id}: {e}")
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Service temporarily unavailable",
                        "detail": "Too many requests. Please wait a moment and try again.",
                        "session_id": request.session_id
                    }
                )
            
            elif isinstance(e, APIConnectionError):
                # Network connection issues
                logger.error(f"OpenAI API connection error: {e}")
                raise HTTPException(
                    status_code=503,
                    detail={
                        "error": "Service temporarily unavailable",
                        "detail": "Unable to connect to AI service. Please try again in a moment.",
                        "session_id": request.session_id
                    }
                )
            
            elif isinstance(e, APITimeoutError):
                # Request timeout
                logger.warning(f"OpenAI API timeout for session {request.session_id}: {e}")
                raise HTTPException(
                    status_code=504,
                    detail={
                        "error": "Request timeout",
                        "detail": "The request took too long to process. Please try again.",
                        "session_id": request.session_id
                    }
                )
            
            elif isinstance(e, APIError):
                # General OpenAI API errors
                logger.error(f"OpenAI API error: {e}", exc_info=True)
                raise HTTPException(
                    status_code=500,
                    detail={
                        "error": "AI service error",
                        "detail": "An error occurred while processing your request. Please try again.",
                        "session_id": request.session_id
                    }
                )
        # Catch any other unexpected errors
        logger.error(f"Unexpected error in chat endpoint: {str(e)}", exc_info=True)
        
        # Return a user-friendly error without exposing internal details
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to process your message",
                "detail": "An unexpected error occurred. Please try again in a moment.",
                "session_id": request.session_id
            }
        )


# ============================================================================
# Application Startup/Shutdown Events
# ============================================================================


@app.on_event("startup")
async def startup_event():
    """
    Execute tasks on application startup.
    
    Validates required configuration and initializes the LangChain agent.
    The application will fail to start if critical configuration is missing.
    """
    logger.info("=" * 70)
    logger.info("Starting Advanced Customer Service AI backend...")
    logger.info("=" * 70)
    
    # Log environment information
    environment = os.getenv('ENVIRONMENT', 'development')
    logger.info(f"Environment: {environment}")
    logger.info(f"CORS origins: {cors_origins}")
    logger.info(f"Log level: {os.getenv('LOG_LEVEL', 'INFO')}")
    
    # ========================================================================
    # Phase 2: Validate Required Configuration
    # ========================================================================
    logger.info("")
    logger.info("Validating configuration...")
    
    # Check for required environment variables
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for LLM integration"
    }
    
    missing_vars = []
    for var_name, description in required_vars.items():
        if not os.getenv(var_name):
            missing_vars.append(f"  - {var_name}: {description}")
            logger.error(f"❌ Missing required environment variable: {var_name}")
        else:
            # Mask the API key in logs (show only first/last 4 chars)
            value = os.getenv(var_name)
            if len(value) > 12:
                masked_value = f"{value[:4]}...{value[-4:]}"
            else:
                masked_value = "****"
            logger.info(f"✅ {var_name}: {masked_value}")
    
    # Check for optional but recommended environment variables
    optional_vars = {
        "LANGSMITH_API_KEY": "LangSmith tracing (recommended for debugging)",
        "LANGSMITH_TRACING": "Enable LangSmith tracing",
        "LANGSMITH_PROJECT": "LangSmith project name",
    }
    
    logger.info("")
    logger.info("Optional configuration:")
    for var_name, description in optional_vars.items():
        if os.getenv(var_name):
            if "API_KEY" in var_name:
                value = os.getenv(var_name)
                masked_value = f"{value[:4]}...{value[-4:]}" if len(value) > 12 else "****"
                logger.info(f"✅ {var_name}: {masked_value}")
            else:
                logger.info(f"✅ {var_name}: {os.getenv(var_name)}")
        else:
            logger.info(f"ℹ️  {var_name}: Not set ({description})")
    
    # If any required variables are missing, fail startup
    if missing_vars:
        logger.error("")
        logger.error("=" * 70)
        logger.error("STARTUP FAILED: Missing required configuration")
        logger.error("=" * 70)
        logger.error("The following environment variables are required:")
        for var in missing_vars:
            logger.error(var)
        logger.error("")
        logger.error("Please:")
        logger.error("1. Copy backend/.env.example to backend/.env")
        logger.error("2. Add your OPENAI_API_KEY to backend/.env")
        logger.error("3. Restart the application")
        logger.error("=" * 70)
        raise RuntimeError(
            "Missing required environment variables. "
            "See logs above for details."
        )
    
    # ========================================================================
    # Phase 2: Initialize LangChain Agent
    # ========================================================================
    logger.info("")
    logger.info("Initializing LangChain agent...")
    
    try:
        # Attempt to get the agent (this validates the configuration)
        test_agent = get_agent()
        logger.info("✅ LangChain agent initialized successfully")
        logger.info(f"   Agent name: {test_agent.name}")
        logger.info("   Model: GPT-4o-mini (OpenAI)")
        logger.info("   Memory: InMemorySaver (conversation history)")
    except RuntimeError as e:
        logger.error("")
        logger.error("=" * 70)
        logger.error("STARTUP FAILED: Agent initialization error")
        logger.error("=" * 70)
        logger.error(f"Error: {e}")
        logger.error("")
        logger.error("This usually means:")
        logger.error("1. OPENAI_API_KEY is set but invalid")
        logger.error("2. There's a problem with the agent configuration")
        logger.error("")
        logger.error("Please check your API key and try again.")
        logger.error("=" * 70)
        raise
    except Exception as e:
        logger.error("")
        logger.error("=" * 70)
        logger.error("STARTUP FAILED: Unexpected error during agent initialization")
        logger.error("=" * 70)
        logger.error(f"Error: {e}")
        logger.error("=" * 70)
        raise
    
    # ========================================================================
    # Startup Complete
    # ========================================================================
    logger.info("")
    logger.info("=" * 70)
    logger.info("✅ Advanced Customer Service AI backend started successfully!")
    logger.info("=" * 70)
    logger.info(f"API Documentation: http://localhost:{os.getenv('PORT', 8000)}/docs")
    logger.info(f"Health Check: http://localhost:{os.getenv('PORT', 8000)}/health")
    logger.info(f"Chat Endpoint: POST http://localhost:{os.getenv('PORT', 8000)}/chat")
    logger.info("=" * 70)
    logger.info("")


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
