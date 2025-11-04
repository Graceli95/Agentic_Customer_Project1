/**
 * ChatInterface Component
 * 
 * Main container that orchestrates the chat experience by combining
 * MessageList and MessageInput components with API communication.
 * Manages conversation state, loading states, and error handling.
 * 
 * Related to Task 4.4 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

'use client';

import { useState } from 'react';
import MessageList, { type Message } from './MessageList';
import MessageInput from './MessageInput';
import { 
  sendChatMessage, 
  sendChatMessageStream, 
  formatErrorMessage,
  type ChatStreamEvent 
} from '@/lib/api';

interface ChatInterfaceProps {
  /** Session ID for conversation continuity */
  sessionId: string;
  /** Callback when session should be cleared */
  onClearSession?: () => void;
}

/**
 * ChatInterface component provides the complete chat experience.
 * 
 * Features:
 * - Displays conversation history
 * - Handles user message input
 * - Communicates with backend API
 * - Manages loading states
 * - Displays errors gracefully
 * - Auto-generates message IDs
 * 
 * @example
 * ```tsx
 * <ChatInterface 
 *   sessionId={currentSessionId}
 *   onClearSession={() => handleClear()}
 * />
 * ```
 */
export default function ChatInterface({ sessionId, onClearSession }: ChatInterfaceProps) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [useStreaming, setUseStreaming] = useState(true); // Enable streaming by default

  /**
   * Generates a unique message ID
   */
  const generateMessageId = (): string => {
    return `msg-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  };

  /**
   * Handles sending a message to the AI assistant
   */
  const handleSendMessage = async (content: string) => {
    // Create user message
    const userMessage: Message = {
      id: generateMessageId(),
      content,
      role: 'user',
      timestamp: new Date(),
    };

    // Add user message to conversation
    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      if (useStreaming) {
        // Use streaming mode (SSE)
        const assistantMessageId = generateMessageId();
        let streamedContent = '';

        // Create placeholder assistant message
        const assistantMessage: Message = {
          id: assistantMessageId,
          content: '',
          role: 'assistant',
          timestamp: new Date(),
        };
        setMessages((prev) => [...prev, assistantMessage]);

        // Stream the response
        await sendChatMessageStream(
          content,
          sessionId,
          (event: ChatStreamEvent) => {
            if (event.type === 'token' && 'content' in event) {
              // Type guard: ensure event has content property
              // Append token to streamed content
              streamedContent += event.content;
              
              // Update the assistant message with accumulated content
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? { ...msg, content: streamedContent }
                    : msg
                )
              );
            }
          },
          () => {
            // Stream complete
            console.log('Streaming complete');
          },
          (error) => {
            // Stream error
            console.error('Streaming error:', error);
            
            // Update message to show error
            setMessages((prev) =>
              prev.map((msg) =>
                msg.id === assistantMessageId
                  ? {
                      ...msg,
                      content: formatErrorMessage(error),
                      role: 'error' as const,
                    }
                  : msg
              )
            );
          }
        );
      } else {
        // Use non-streaming mode (traditional)
        const response = await sendChatMessage(content, sessionId);

        // Create assistant message from response
        const assistantMessage: Message = {
          id: generateMessageId(),
          content: response.response,
          role: 'assistant',
          timestamp: new Date(),
        };

        // Add assistant response to conversation
        setMessages((prev) => [...prev, assistantMessage]);
      }
    } catch (error) {
      // Handle errors gracefully
      console.error('Failed to send message:', error);

      // Create error message for display
      const errorMessage: Message = {
        id: generateMessageId(),
        content: formatErrorMessage(error),
        role: 'error',
        timestamp: new Date(),
      };

      // Add error message to conversation
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handles clearing the conversation
   */
  const handleClearConversation = () => {
    // Clear messages
    setMessages([]);
    
    // Notify parent to generate new session
    if (onClearSession) {
      onClearSession();
    }
  };

  return (
    <div className="flex h-full flex-col">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 bg-white px-6 py-4 dark:border-gray-700 dark:bg-gray-900">
        <div className="flex items-center gap-3">
          {/* Chat icon */}
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-blue-500 to-purple-600">
            <svg
              className="h-5 w-5 text-white"
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
          
          <div>
            <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-50">
              AI Assistant
            </h2>
            <p className="text-xs text-gray-600 dark:text-gray-400">
              {messages.length === 0 ? 'Ready to help' : `${messages.filter(m => m.role !== 'error').length} messages`}
            </p>
          </div>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          {/* Streaming toggle */}
          <button
            onClick={() => setUseStreaming(!useStreaming)}
            disabled={isLoading}
            className={`rounded-lg border px-4 py-2 text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 ${
              useStreaming
                ? 'border-blue-500 bg-blue-50 text-blue-700 hover:bg-blue-100 dark:border-blue-400 dark:bg-blue-900/30 dark:text-blue-300 dark:hover:bg-blue-900/50'
                : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700'
            } dark:focus:ring-offset-gray-900`}
            aria-label={useStreaming ? 'Disable streaming' : 'Enable streaming'}
            title={useStreaming ? 'Streaming enabled (real-time)' : 'Streaming disabled'}
          >
            <div className="flex items-center gap-2">
              <svg
                className="h-4 w-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                {useStreaming ? (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 10V3L4 14h7v7l9-11h-7z"
                  />
                ) : (
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                )}
              </svg>
              <span className="hidden sm:inline">{useStreaming ? 'Streaming' : 'Standard'}</span>
            </div>
          </button>

          {/* Clear conversation button */}
          {messages.length > 0 && (
            <button
              onClick={handleClearConversation}
              disabled={isLoading}
              className="rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-300 dark:hover:bg-gray-700 dark:focus:ring-offset-gray-900"
              aria-label="Clear conversation"
            >
              <div className="flex items-center gap-2">
                <svg
                  className="h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                  />
                </svg>
                <span className="hidden sm:inline">Clear</span>
              </div>
            </button>
          )}
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-hidden bg-gray-50 dark:bg-gray-950">
        <MessageList messages={messages} isLoading={isLoading} />
      </div>

      {/* Input area */}
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={isLoading}
        placeholder="Ask me anything..."
      />
    </div>
  );
}

