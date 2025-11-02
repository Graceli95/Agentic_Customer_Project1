# Lib Directory

This directory contains utility functions, API clients, constants, and shared logic for the Customer Service AI application.

## Structure

```
lib/
├── api/             # API client and backend communication
├── utils/           # Utility functions and helpers
├── hooks/           # Custom React hooks
├── constants/       # Application constants
├── types/           # Shared TypeScript types
└── validators/      # Input validation functions
```

## What Goes Here

### API Layer (`lib/api/`)
- API client configuration
- Backend communication functions
- Request/response interceptors
- Error handling utilities

### Utils (`lib/utils/`)
- Pure utility functions
- String formatters
- Date/time helpers
- Data transformations

### Hooks (`lib/hooks/`)
- Custom React hooks
- Reusable stateful logic
- Side effect management

### Constants (`lib/constants/`)
- Configuration values
- Enum-like objects
- Fixed data structures

### Types (`lib/types/`)
- Shared TypeScript interfaces
- Type definitions
- API response types

### Validators (`lib/validators/`)
- Form validation functions
- Input sanitization
- Data validation schemas

## Example Files

### API Client (`lib/api/client.ts`)
```typescript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
  timeout: parseInt(process.env.NEXT_PUBLIC_API_TIMEOUT || '30000'),
  headers: {
    'Content-Type': 'application/json',
  },
});

export default apiClient;
```

### Utility Function (`lib/utils/format.ts`)
```typescript
export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(date);
}

export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}
```

### Custom Hook (`lib/hooks/useChat.ts`)
```typescript
import { useState, useCallback } from 'react';
import { sendMessage } from '@/lib/api/chat';

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const send = useCallback(async (content: string) => {
    setIsLoading(true);
    try {
      const response = await sendMessage(content);
      setMessages(prev => [...prev, response]);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { messages, isLoading, send };
}
```

### Constants (`lib/constants/config.ts`)
```typescript
export const APP_CONFIG = {
  name: process.env.NEXT_PUBLIC_APP_NAME || 'Customer Service AI',
  version: process.env.NEXT_PUBLIC_APP_VERSION || '0.1.0',
  maxMessageLength: parseInt(process.env.NEXT_PUBLIC_MAX_MESSAGE_LENGTH || '2000'),
  chatHistoryLimit: parseInt(process.env.NEXT_PUBLIC_CHAT_HISTORY_LIMIT || '50'),
} as const;

export const MESSAGE_ROLES = {
  USER: 'user',
  ASSISTANT: 'assistant',
  SYSTEM: 'system',
} as const;
```

### Type Definitions (`lib/types/chat.ts`)
```typescript
export interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'system';
  timestamp: Date;
}

export interface ChatSession {
  id: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
```

## Best Practices

1. **Keep functions pure** - Avoid side effects in utility functions
2. **Use TypeScript** - Properly type all functions and exports
3. **Document complex logic** - Add JSDoc comments for clarity
4. **Test utilities** - Write unit tests for critical functions
5. **Avoid circular dependencies** - Keep imports clean and unidirectional
6. **Export named functions** - Use named exports for better tree-shaking
7. **Handle errors gracefully** - Always handle potential failures
8. **Use environment variables** - Leverage Next.js env vars for configuration

## Path Aliases

Use Next.js path aliases for cleaner imports:

```typescript
// Instead of: import { formatDate } from '../../../lib/utils/format';
import { formatDate } from '@/lib/utils/format';

// Instead of: import apiClient from '../../lib/api/client';
import apiClient from '@/lib/api/client';
```

The `@/` alias points to the `frontend/` root directory (configured in `tsconfig.json`).

## Resources

- [Next.js App Directory](https://nextjs.org/docs/app)
- [TypeScript Best Practices](https://typescript-eslint.io/rules/)
- [React Hooks](https://react.dev/reference/react)

