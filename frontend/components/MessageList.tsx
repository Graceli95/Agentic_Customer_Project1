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
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

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
  /** Which specialist agent handled the query (for assistant messages) */
  agent?: string;
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
        <div className="flex h-full items-center justify-center p-6">
          <div className="w-full max-w-3xl">
            <div className="mb-6 text-center">
              <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
                <svg
                  className="h-8 w-8 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
                  />
                </svg>
              </div>
              <h3 className="mb-2 text-xl font-bold text-gray-900 dark:text-gray-50">
                Welcome to AI Customer Service
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Multi-agent AI system for technical, billing, general, and compliance support
              </p>
            </div>
            
            <div className="mt-6">
              <p className="mb-3 text-center text-xs font-semibold uppercase tracking-wide text-gray-500 dark:text-gray-400">
                Try these examples:
              </p>
              <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                <div className="group cursor-pointer rounded-lg border-2 border-gray-200 bg-white p-3 text-left transition-all hover:border-blue-500 hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
                  <div className="mb-1 flex items-center gap-2">
                    <span className="text-lg">🔧</span>
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Technical</span>
                  </div>
                  <p className="text-sm text-gray-900 dark:text-gray-50">
                    "I'm getting Error 500"
                  </p>
                </div>
                
                <div className="group cursor-pointer rounded-lg border-2 border-gray-200 bg-white p-3 text-left transition-all hover:border-purple-500 hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
                  <div className="mb-1 flex items-center gap-2">
                    <span className="text-lg">💰</span>
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Billing</span>
                  </div>
                  <p className="text-sm text-gray-900 dark:text-gray-50">
                    "What are your pricing plans?"
                  </p>
                </div>
                
                <div className="group cursor-pointer rounded-lg border-2 border-gray-200 bg-white p-3 text-left transition-all hover:border-green-500 hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
                  <div className="mb-1 flex items-center gap-2">
                    <span className="text-lg">ℹ️</span>
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">General</span>
                  </div>
                  <p className="text-sm text-gray-900 dark:text-gray-50">
                    "What services do you offer?"
                  </p>
                </div>
                
                <div className="group cursor-pointer rounded-lg border-2 border-gray-200 bg-white p-3 text-left transition-all hover:border-red-500 hover:shadow-md dark:border-gray-700 dark:bg-gray-800">
                  <div className="mb-1 flex items-center gap-2">
                    <span className="text-lg">🔒</span>
                    <span className="text-xs font-medium text-gray-500 dark:text-gray-400">Compliance</span>
                  </div>
                  <p className="text-sm text-gray-900 dark:text-gray-50">
                    "What's your data retention policy?"
                  </p>
                </div>
              </div>
            </div>
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
                
                {/* Agent specialist badge */}
                {message.role === 'assistant' && message.agent && (
                  <span className="rounded-full bg-gradient-to-r from-blue-500 to-purple-500 px-2 py-0.5 text-xs font-medium text-white">
                    {message.agent}
                  </span>
                )}
                
                <span className="text-xs text-gray-500 dark:text-gray-500">
                  {formatTime(message.timestamp)}
                </span>
              </div>

              {/* Message bubble */}
              <div
                className={`rounded-2xl px-5 py-4 ${
                  message.role === 'user'
                    ? 'bg-blue-600 text-white dark:bg-blue-500'
                    : message.role === 'error'
                    ? 'border border-red-300 bg-red-50 text-red-900 dark:border-red-700 dark:bg-red-950 dark:text-red-100'
                    : 'bg-gray-100 text-gray-900 dark:bg-gray-800 dark:text-gray-100'
                }`}
              >
                {message.role === 'user' ? (
                  // User messages - simple text
                  <p className="whitespace-pre-wrap break-words text-sm leading-relaxed">
                    {message.content}
                  </p>
                ) : (
                  // AI/Error messages - rendered markdown with better formatting
                  <div className="prose prose-sm prose-slate dark:prose-invert max-w-none">
                    <ReactMarkdown
                      remarkPlugins={[remarkGfm]}
                      components={{
                        // Custom styling for inline code
                        code: ({node, inline, className, children, ...props}: any) => {
                          return inline ? (
                            <code className="bg-gray-200 dark:bg-gray-700 px-1.5 py-0.5 rounded text-xs font-mono text-gray-900 dark:text-gray-100" {...props}>
                              {children}
                            </code>
                          ) : (
                            <code className="block bg-gray-800 dark:bg-gray-950 text-gray-100 p-4 rounded-lg text-xs font-mono overflow-x-auto my-3" {...props}>
                              {children}
                            </code>
                          );
                        },
                        // Better pre (code block container) styling
                        pre: ({node, ...props}: any) => (
                          <pre className="!bg-transparent !p-0 !m-0" {...props} />
                        ),
                        // Better table styling
                        table: ({node, ...props}: any) => (
                          <div className="overflow-x-auto my-4 -mx-1">
                            <table className="min-w-full border-collapse text-sm" {...props} />
                          </div>
                        ),
                        thead: ({node, ...props}: any) => (
                          <thead className="bg-gray-200 dark:bg-gray-700" {...props} />
                        ),
                        th: ({node, ...props}: any) => (
                          <th className="border border-gray-300 dark:border-gray-600 px-3 py-2 text-left font-semibold text-xs" {...props} />
                        ),
                        td: ({node, ...props}: any) => (
                          <td className="border border-gray-300 dark:border-gray-600 px-3 py-2 text-xs" {...props} />
                        ),
                        // Better list styling
                        ul: ({node, ...props}: any) => (
                          <ul className="!list-disc !list-outside !ml-5 space-y-1 my-2" {...props} />
                        ),
                        ol: ({node, ...props}: any) => (
                          <ol className="!list-decimal !list-outside !ml-5 space-y-1 my-2" {...props} />
                        ),
                        li: ({node, ...props}: any) => (
                          <li className="text-sm leading-relaxed" {...props} />
                        ),
                        // Better heading styles
                        h1: ({node, ...props}: any) => (
                          <h1 className="text-lg font-bold mt-4 mb-2 text-gray-900 dark:text-gray-100" {...props} />
                        ),
                        h2: ({node, ...props}: any) => (
                          <h2 className="text-base font-bold mt-3 mb-2 text-gray-900 dark:text-gray-100" {...props} />
                        ),
                        h3: ({node, ...props}: any) => (
                          <h3 className="text-sm font-semibold mt-2 mb-1 text-gray-900 dark:text-gray-100" {...props} />
                        ),
                        // Paragraph styling
                        p: ({node, ...props}: any) => (
                          <p className="text-sm leading-relaxed my-2 text-gray-900 dark:text-gray-100" {...props} />
                        ),
                        // Blockquote styling
                        blockquote: ({node, ...props}: any) => (
                          <blockquote className="border-l-4 border-blue-500 pl-4 italic my-3 text-gray-700 dark:text-gray-300" {...props} />
                        ),
                        // Horizontal rule
                        hr: ({node, ...props}: any) => (
                          <hr className="my-4 border-gray-300 dark:border-gray-600" {...props} />
                        ),
                      }}
                    >
                      {message.content}
                    </ReactMarkdown>
                  </div>
                )}
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

