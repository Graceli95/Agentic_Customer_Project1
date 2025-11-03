/**
 * API Client
 * 
 * Provides functions for communicating with the FastAPI backend.
 * Handles request/response formatting, error handling, and session management.
 * 
 * Related to Task 3.2 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

/**
 * Configuration for API endpoints
 */
const API_CONFIG = {
  baseUrl: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  endpoints: {
    chat: '/chat',
    health: '/health',
  },
} as const;

/**
 * Request payload for chat endpoint
 */
export interface ChatRequest {
  message: string;
  session_id: string;
}

/**
 * Successful response from chat endpoint
 */
export interface ChatResponse {
  response: string;
  session_id: string;
}

/**
 * Error response from backend
 */
export interface ErrorResponse {
  error: string;
  detail: string;
  session_id?: string;
}

/**
 * Custom error class for API errors
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public detail: string,
    public sessionId?: string
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

/**
 * Sends a chat message to the backend agent
 * 
 * @param message - The user's message (1-2000 characters)
 * @param sessionId - The UUID v4 session identifier
 * @returns Promise resolving to the agent's response
 * @throws {ApiError} If the request fails or returns an error
 * 
 * @example
 * ```typescript
 * try {
 *   const response = await sendChatMessage("Hello!", sessionId);
 *   console.log(response.response); // Agent's reply
 * } catch (error) {
 *   if (error instanceof ApiError) {
 *     console.error(error.message);
 *   }
 * }
 * ```
 */
export async function sendChatMessage(
  message: string,
  sessionId: string
): Promise<ChatResponse> {
  // Validate inputs
  if (!message || message.trim().length === 0) {
    throw new ApiError(
      'Message cannot be empty',
      400,
      'Message must contain at least 1 character'
    );
  }

  if (message.length > 2000) {
    throw new ApiError(
      'Message is too long',
      400,
      'Message must be 2000 characters or less'
    );
  }

  if (!sessionId) {
    throw new ApiError(
      'Session ID is required',
      400,
      'session_id must be provided'
    );
  }

  const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.chat}`;
  const requestBody: ChatRequest = {
    message: message.trim(),
    session_id: sessionId,
  };

  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    // Parse response body
    const data = await response.json();

    // Handle non-OK responses
    if (!response.ok) {
      const errorData = data as ErrorResponse;
      throw new ApiError(
        errorData.error || 'Request failed',
        response.status,
        errorData.detail || 'Unknown error occurred',
        errorData.session_id
      );
    }

    // Return successful response
    return data as ChatResponse;
  } catch (error) {
    // Re-throw ApiError as-is
    if (error instanceof ApiError) {
      throw error;
    }

    // Handle network errors
    if (error instanceof TypeError) {
      throw new ApiError(
        'Unable to connect to server',
        0,
        'Network error - please check your connection and ensure the backend is running',
        sessionId
      );
    }

    // Handle JSON parsing errors
    if (error instanceof SyntaxError) {
      throw new ApiError(
        'Invalid response from server',
        0,
        'Failed to parse server response',
        sessionId
      );
    }

    // Handle unknown errors
    throw new ApiError(
      'An unexpected error occurred',
      0,
      error instanceof Error ? error.message : 'Unknown error',
      sessionId
    );
  }
}

/**
 * Checks if the backend server is healthy and reachable
 * 
 * @returns Promise resolving to true if healthy, false otherwise
 * 
 * @example
 * ```typescript
 * const isHealthy = await checkBackendHealth();
 * if (!isHealthy) {
 *   console.error("Backend is not responding");
 * }
 * ```
 */
export async function checkBackendHealth(): Promise<boolean> {
  const url = `${API_CONFIG.baseUrl}${API_CONFIG.endpoints.health}`;

  try {
    const response = await fetch(url, {
      method: 'GET',
      // Short timeout for health checks
      signal: AbortSignal.timeout(5000),
    });

    return response.ok;
  } catch (error) {
    console.error('Backend health check failed:', error);
    return false;
  }
}

/**
 * Gets the configured API base URL
 * Useful for debugging or displaying connection status
 * 
 * @returns The base URL for API requests
 */
export function getApiBaseUrl(): string {
  return API_CONFIG.baseUrl;
}

/**
 * Formats an error for display to the user
 * Converts technical errors into user-friendly messages
 * 
 * @param error - The error to format
 * @returns User-friendly error message
 * 
 * @example
 * ```typescript
 * try {
 *   await sendChatMessage(msg, sessionId);
 * } catch (error) {
 *   const userMessage = formatErrorMessage(error);
 *   showErrorToUser(userMessage);
 * }
 * ```
 */
export function formatErrorMessage(error: unknown): string {
  if (error instanceof ApiError) {
    // Map common errors to user-friendly messages
    switch (error.statusCode) {
      case 400:
        return error.message; // Validation errors are already user-friendly
      case 401:
        return 'Authentication failed. Please refresh the page.';
      case 429:
        return 'Too many requests. Please wait a moment and try again.';
      case 500:
        return 'The server encountered an error. Please try again.';
      case 503:
        return 'The service is temporarily unavailable. Please try again later.';
      case 0:
        return error.message; // Network errors already have good messages
      default:
        return 'Something went wrong. Please try again.';
    }
  }

  // Fallback for non-ApiError errors
  if (error instanceof Error) {
    return error.message;
  }

  return 'An unexpected error occurred. Please try again.';
}

