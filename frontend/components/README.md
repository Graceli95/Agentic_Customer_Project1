# Components Directory

This directory contains reusable React components for the Customer Service AI application.

## Structure

```
components/
├── ui/              # UI primitives (buttons, inputs, cards, etc.)
├── chat/            # Chat-specific components
├── layout/          # Layout components (header, footer, sidebar)
└── shared/          # Shared/common components
```

## Naming Conventions

- Use PascalCase for component files: `ChatMessage.tsx`
- Use kebab-case for utility/style files: `chat-message.module.css`
- Include TypeScript types in the same file or adjacent `.types.ts` file

## Component Structure

```tsx
// components/chat/ChatMessage.tsx
import { FC } from 'react';

interface ChatMessageProps {
  content: string;
  role: 'user' | 'assistant';
  timestamp?: Date;
}

export const ChatMessage: FC<ChatMessageProps> = ({ content, role, timestamp }) => {
  return (
    <div className={`chat-message chat-message-${role}`}>
      <p>{content}</p>
      {timestamp && <span className="text-xs text-gray-500">{timestamp.toLocaleTimeString()}</span>}
    </div>
  );
};
```

## Best Practices

1. **Keep components small and focused** - Each component should do one thing well
2. **Use TypeScript** - Define proper prop types for all components
3. **Prefer composition** - Build complex components from simpler ones
4. **Export named components** - Use named exports for better refactoring
5. **Document props** - Add JSDoc comments for complex props
6. **Use Tailwind classes** - Leverage utility-first CSS for styling
7. **Make components accessible** - Include proper ARIA attributes
8. **Test your components** - Write unit tests for important logic

## Example Components

### UI Components
- `Button.tsx` - Reusable button with variants
- `Input.tsx` - Form input with validation
- `Card.tsx` - Container component
- `Badge.tsx` - Status badges
- `Modal.tsx` - Dialog/modal component

### Chat Components
- `ChatMessage.tsx` - Individual chat message
- `ChatInput.tsx` - Message input field
- `ChatContainer.tsx` - Chat messages list
- `TypingIndicator.tsx` - Loading indicator

### Layout Components
- `Header.tsx` - Application header
- `Sidebar.tsx` - Navigation sidebar
- `Footer.tsx` - Application footer

## Resources

- [Next.js Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
- [React Component Patterns](https://react.dev/learn/thinking-in-react)
- [Tailwind Components](https://tailwindcss.com/docs/reusing-styles)

