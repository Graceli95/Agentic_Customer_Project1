# Lib Directory

This directory contains utility functions, API clients, and shared logic for the Customer Service AI frontend.

## Current Structure

```
lib/
├── api.ts             # Backend API client (standard + SSE streaming)
├── sessionManager.ts  # Session ID management with localStorage
├── utils/             # Utility functions
│   └── cn.ts         # Tailwind class name utility
└── README.md          # This file
```

## Files

### `api.ts` - API Client

The main API client for communicating with the FastAPI backend.

**Features:**
- Standard chat endpoint (`sendChatMessage`)
- SSE streaming endpoint (`sendChatMessageStream`)
- Health check (`checkBackendHealth`)
- Comprehensive error handling with `ApiError` class
- User-friendly error messages with `formatErrorMessage`

**Key Exports:**

```typescript
// Standard chat (non-streaming)
export async function sendChatMessage(
  message: string,
  sessionId: string
): Promise<ChatResponse>

// Streaming chat (SSE)
export async function sendChatMessageStream(
  message: string,
  sessionId: string,
  onEvent: StreamCallback,
  onComplete?: () => void,
  onError?: (error: ApiError) => void
): Promise<void>

// Health check
export async function checkBackendHealth(): Promise<boolean>

// Error formatting
export function formatErrorMessage(error: unknown): string
```

**Types:**
- `ChatRequest` - Request payload for chat endpoint
- `ChatResponse` - Response from chat endpoint
- `ChatStreamEvent` - Union type for SSE events
- `ApiError` - Custom error class with status codes

**Usage Example:**

```typescript
import { sendChatMessage, formatErrorMessage } from '@/lib/api';

try {
  const response = await sendChatMessage("Hello!", sessionId);
  console.log(response.response);
  console.log(response.agent); // "Technical Support" | "Billing Support" | etc.
} catch (error) {
  const userMessage = formatErrorMessage(error);
  showError(userMessage);
}
```

---

### `sessionManager.ts` - Session Management

Manages user session IDs for conversation tracking with localStorage persistence.

**Features:**
- UUID v4 generation with `crypto.randomUUID()` fallback
- localStorage persistence across page refreshes
- SSR-safe (handles server-side rendering)
- Session validation

**Key Exports:**

```typescript
// Get or create session ID
export function getOrCreateSessionId(): string

// Clear session and generate new one
export function clearSession(): string

// Validate UUID format
export function isValidUUID(uuid: string): boolean

// Ensure valid session ID
export function ensureValidSessionId(): string
```

**Usage Example:**

```typescript
import { getOrCreateSessionId, clearSession } from '@/lib/sessionManager';

// On page load
const sessionId = getOrCreateSessionId();

// When user clicks "Clear Conversation"
const newSessionId = clearSession();
```

---

### `utils/cn.ts` - Class Name Utility

A utility function for conditionally joining Tailwind CSS class names.

**Features:**
- Merges Tailwind classes intelligently
- Handles conditional classes
- Resolves conflicts (e.g., `px-2` vs `px-4`)

**Usage Example:**

```typescript
import { cn } from '@/lib/utils/cn';

<div className={cn(
  "base-classes px-4 py-2",
  isActive && "bg-blue-500",
  isError && "bg-red-500",
  className
)} />
```

---

## Best Practices

1. **Use TypeScript** - All files are fully typed
2. **Handle errors gracefully** - Always use try/catch with ApiError
3. **SSR Safety** - Check for browser environment before using localStorage
4. **Import via aliases** - Use `@/lib/...` for cleaner imports

```typescript
// Preferred import style
import { sendChatMessage, ApiError } from '@/lib/api';
import { getOrCreateSessionId } from '@/lib/sessionManager';
import { cn } from '@/lib/utils/cn';
```

---

## Resources

- [Next.js API Routes](https://nextjs.org/docs/app/building-your-application/routing/route-handlers)
- [Server-Sent Events (SSE)](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
- [Web Crypto API](https://developer.mozilla.org/en-US/docs/Web/API/Crypto/randomUUID)

---

**Last Updated**: December 9, 2025
