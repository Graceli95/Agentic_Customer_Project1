/**
 * MessageList Component
 * 
 * Displays the conversation history between the user and AI assistant.
 * Messages are visually distinguished by role (user vs assistant) with
 * different styling, alignment, and colors.
 * 
 * Related to Task 4.1 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

import { useEffect, useRef } from 'react';

/**
 * Represents a single message in the conversation
 */
export interface Message {
  /** Unique identifier for the message */
  id: string;
  /** Message content/text */
  content: string;
  /** Who sent the message */
  role: 'user' | 'assistant' | 'error';
  /** When the message was created */
  timestamp: Date;
}

interface MessageListProps {
  /** Array of messages to display */
  messages: Message[];
  /** Whether the AI is currently processing a response */
  isLoading?: boolean;
}

/**
 * MessageList component displays conversation history with visual distinction
 * between user and AI messages.
 * 
 * Features:
 * - Auto-scrolls to latest message
 * - Visual distinction between user/AI/error messages
 * - Responsive design
 * - Accessibility support
 * 
 * @example
 * ```tsx
 * <MessageList 
 *   messages={conversationMessages}
 *   isLoading={waitingForResponse}
 * />
 * ```
 */
export default function MessageList({ messages, isLoading = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  // Format timestamp for display
  const formatTime = (date: Date): string => {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  };

  return (
    <div className="flex h-full flex-col overflow-y-auto px-4 py-6">
      {/* Empty state - no messages yet */}
      {messages.length === 0 && !isLoading && (
        <div className="flex h-full items-center justify-center">
          <div className="text-center">
            <div className="mb-4 flex justify-center">
              <div className="flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600">
                <svg
                  className="h-8 w-8 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-gray-50">
              Start a Conversation
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Send a message to begin chatting with the AI assistant
            </p>
          </div>
        </div>
      )}

      {/* Messages list */}
      <div className="space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            <div
              className={`flex max-w-[80%] flex-col ${
                message.role === 'user' ? 'items-end' : 'items-start'
              }`}
            >
              {/* Message header with role and timestamp */}
              <div className="mb-1 flex items-center gap-2 px-1">
                <span
                  className={`text-xs font-medium ${
                    message.role === 'user'
                      ? 'text-blue-600 dark:text-blue-400'
                      : message.role === 'error'
                      ? 'text-red-600 dark:text-red-400'
                      : 'text-purple-600 dark:text-purple-400'
                  }`}
                >
                  {message.role === 'user' ? 'You' : message.role === 'error' ? 'Error' : 'AI Assistant'}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-500">
                  {formatTime(message.timestamp)}
                </span>
              </div>

              {/* Message bubble */}
              <div
                className={`rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white dark:bg-blue-500'
                    : message.role === 'error'
                    ? 'border border-red-300 bg-red-50 text-red-900 dark:border-red-700 dark:bg-red-950 dark:text-red-100'
                    : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
                }`}
              >
                <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
                  {message.content}
                </p>
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator when AI is typing */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="flex max-w-[80%] flex-col items-start">
              <div className="mb-1 px-1">
                <span className="text-xs font-medium text-purple-600 dark:text-purple-400">
                  AI Assistant
                </span>
              </div>
              <div className="rounded-2xl bg-gray-100 px-4 py-3 dark:bg-gray-800">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500 dark:bg-gray-400 [animation-delay:-0.3s]"></div>
                    <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500 dark:bg-gray-400 [animation-delay:-0.15s]"></div>
                    <div className="h-2 w-2 animate-bounce rounded-full bg-gray-500 dark:bg-gray-400"></div>
                  </div>
                  <span className="text-xs text-gray-600 dark:text-gray-400">
                    AI is thinking...
                  </span>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}

