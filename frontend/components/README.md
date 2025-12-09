# Components Directory

This directory contains reusable React components for the Customer Service AI frontend.

## Current Structure

```
components/
├── ChatInterface.tsx   # Main chat container with streaming toggle
├── MessageList.tsx     # Message display with agent badges
├── MessageInput.tsx    # Text input with validation
├── ui/                 # UI primitives (future shadcn/ui)
│   └── .gitkeep
└── README.md           # This file
```

## Components

### `ChatInterface.tsx` - Main Chat Container

The main container component that orchestrates the complete chat experience.

**Features:**
- Combines MessageList and MessageInput components
- Manages conversation state and API communication
- Streaming toggle (SSE vs standard mode)
- Loading states and error handling
- Export conversation to text file
- Clear conversation button

**Props:**

```typescript
interface ChatInterfaceProps {
  sessionId: string;        // Session ID for conversation continuity
  onClearSession?: () => void;  // Callback when session should be cleared
}
```

**Usage Example:**

```tsx
<ChatInterface 
  sessionId={currentSessionId}
  onClearSession={() => {
    const newId = clearSession();
    setSessionId(newId);
  }}
/>
```

**Key Features:**
- 🔄 **Streaming Toggle**: Switch between real-time SSE streaming and standard responses
- 📤 **Export**: Download conversation as text file
- 🗑️ **Clear**: Start fresh with new session
- ⏳ **Loading States**: Visual indicators during API calls
- ❌ **Error Handling**: Graceful error display and recovery

---

### `MessageList.tsx` - Message Display

Displays the conversation history with styling for different message types.

**Features:**
- User and assistant message styling
- Agent attribution badges (Technical Support, Billing, etc.)
- Markdown rendering with react-markdown
- Error message styling
- Auto-scroll to latest message
- Empty state with example queries

**Props:**

```typescript
interface MessageListProps {
  messages: Message[];      // Array of messages to display
  isLoading?: boolean;      // Shows loading indicator
  onExampleClick?: (text: string) => void;  // Callback for example queries
}

interface Message {
  id: string;
  content: string;
  role: 'user' | 'assistant' | 'error';
  timestamp: Date;
  agent?: string;  // "Technical Support" | "Billing Support" | etc.
}
```

**Usage Example:**

```tsx
<MessageList 
  messages={messages} 
  isLoading={isLoading}
  onExampleClick={(text) => handleSendMessage(text)}
/>
```

**Key Features:**
- 💬 **Message Bubbles**: Different styling for user vs assistant
- 🏷️ **Agent Badges**: Shows which specialized agent handled the response
- 📝 **Markdown Support**: Tables, code blocks, lists, headers
- 🎯 **Example Queries**: Clickable examples when conversation is empty
- 📜 **Auto-scroll**: Automatically scrolls to new messages

---

### `MessageInput.tsx` - Text Input

Handles user text input with validation and submit functionality.

**Features:**
- Character count with 2000 character limit
- Disabled state during loading
- Enter key submission (Shift+Enter for newline)
- Focus management
- Placeholder text

**Props:**

```typescript
interface MessageInputProps {
  onSendMessage: (message: string) => void;  // Called when message is submitted
  disabled?: boolean;       // Disable input during loading
  placeholder?: string;     // Placeholder text
}
```

**Usage Example:**

```tsx
<MessageInput
  onSendMessage={handleSendMessage}
  disabled={isLoading}
  placeholder="Type your question..."
/>
```

**Key Features:**
- ✅ **Validation**: Enforces 1-2000 character limit
- ⌨️ **Keyboard Support**: Enter to send, Shift+Enter for newline
- 🔢 **Character Counter**: Shows current/max characters
- 🎨 **Styling**: Consistent with dark theme

---

## Naming Conventions

- **PascalCase** for component files: `ChatInterface.tsx`
- **Interface names** match component names: `ChatInterfaceProps`
- **TypeScript types** included in same file

## Component Patterns

### Client Components

All chat components use `'use client'` directive for client-side interactivity:

```tsx
'use client';

import { useState } from 'react';

export default function MyComponent() {
  const [state, setState] = useState(initialValue);
  // ...
}
```

### Props with Default Values

```tsx
interface Props {
  required: string;
  optional?: boolean;  // Optional props use ?
}

export default function Component({ 
  required, 
  optional = false  // Provide default values
}: Props) {
  // ...
}
```

### Event Handlers

```tsx
const handleClick = (e: React.MouseEvent) => {
  e.preventDefault();
  // Handle click
};

const handleSubmit = (content: string) => {
  // Handle submit
};
```

---

## Best Practices

1. **Keep components focused** - Each component does one thing well
2. **Use TypeScript** - Define proper prop types for all components
3. **Prefer composition** - Build complex components from simpler ones
4. **Use Tailwind classes** - Leverage utility-first CSS for styling
5. **Handle loading states** - Show feedback during async operations
6. **Handle errors gracefully** - Display user-friendly error messages
7. **Accessibility** - Include proper ARIA attributes

---

## Resources

- [React Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [Client Components](https://nextjs.org/docs/app/building-your-application/rendering/client-components)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [react-markdown](https://github.com/remarkjs/react-markdown)

---

**Last Updated**: December 9, 2025
