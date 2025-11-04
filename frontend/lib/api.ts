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

/**
 * Stream event types from the SSE endpoint
 */
export type StreamEventType = 'start' | 'token' | 'done' | 'error';

/**
 * Base event structure for streaming responses
 */
export interface StreamEvent {
  type: StreamEventType;
  session_id: string;
}

/**
 * Token event with content chunk
 */
export interface TokenEvent extends StreamEvent {
  type: 'token';
  content: string;
}

/**
 * Done event with metadata
 */
export interface DoneEvent extends StreamEvent {
  type: 'done';
  tokens?: number;
  time?: number;
}

/**
 * Error event with details
 */
export interface StreamErrorEvent extends StreamEvent {
  type: 'error';
  error: string;
  detail?: string;
}

/**
 * Union type for all stream events
 */
export type ChatStreamEvent = TokenEvent | DoneEvent | StreamErrorEvent | StreamEvent;

/**
 * Callback function for handling stream events
 */
export type StreamCallback = (event: ChatStreamEvent) => void;

/**
 * Sends a chat message with streaming response using Server-Sent Events (SSE).
 * 
 * This function establishes an EventSource connection to receive real-time
 * token-by-token responses from the AI assistant.
 * 
 * @param message - The user's message (1-2000 characters)
 * @param sessionId - The UUID v4 session identifier
 * @param onEvent - Callback function called for each stream event
 * @param onComplete - Optional callback called when streaming completes successfully
 * @param onError - Optional callback called when an error occurs
 * @returns Promise<void> resolves when streaming is complete
 * @throws {ApiError} If the request fails or stream encounters errors
 * 
 * @example
 * ```typescript
 * await sendChatMessageStream(
 *   "Hello!",
 *   sessionId,
 *   (event) => {
 *     if (event.type === 'token') {
 *       console.log(event.content); // Display token
 *     }
 *   },
 *   () => console.log('Complete'),
 *   (error) => console.error(error)
 * );
 * ```
 */
export async function sendChatMessageStream(
  message: string,
  sessionId: string,
  onEvent: StreamCallback,
  onComplete?: () => void,
  onError?: (error: ApiError) => void
): Promise<void> {
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

  const url = `${API_CONFIG.baseUrl}/chat/stream`;
  const requestBody: ChatRequest = {
    message: message.trim(),
    session_id: sessionId,
  };

  try {
    // Use fetch with stream reading for SSE
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      // Handle non-OK responses
      const errorData = await response.json().catch(() => ({})) as ErrorResponse;
      throw new ApiError(
        errorData.error || 'Request failed',
        response.status,
        errorData.detail || 'Unknown error occurred',
        errorData.session_id
      );
    }

    // Check if response body is available
    if (!response.body) {
      throw new ApiError(
        'Stream not available',
        0,
        'Response body is null',
        sessionId
      );
    }

    // Read the stream
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        break;
      }

      // Decode the chunk
      buffer += decoder.decode(value, { stream: true });

      // Process complete SSE messages
      const lines = buffer.split('\n');
      buffer = lines.pop() || ''; // Keep incomplete line in buffer

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6); // Remove 'data: ' prefix
          
          try {
            const event = JSON.parse(data) as ChatStreamEvent;
            onEvent(event);

            // Handle error events
            if (event.type === 'error') {
              const errorEvent = event as StreamErrorEvent;
              const error = new ApiError(
                errorEvent.error,
                500,
                errorEvent.detail || 'Stream error occurred',
                errorEvent.session_id
              );
              
              if (onError) {
                onError(error);
              }
              return; // Stop processing
            }

            // Handle done event
            if (event.type === 'done') {
              if (onComplete) {
                onComplete();
              }
            }
          } catch (parseError) {
            console.error('Failed to parse SSE event:', data, parseError);
          }
        }
      }
    }
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

    // Handle unknown errors
    throw new ApiError(
      'An unexpected error occurred',
      0,
      error instanceof Error ? error.message : 'Unknown error',
      sessionId
    );
  }
}

