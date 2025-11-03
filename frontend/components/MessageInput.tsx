/**
 * MessageInput Component
 * 
 * Provides a text input field and submit button for users to send messages.
 * Handles form submission, input validation, and disabled states during processing.
 * 
 * Related to Task 4.2 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

import { useState, FormEvent, KeyboardEvent } from 'react';

interface MessageInputProps {
  /** Callback function when user submits a message */
  onSendMessage: (message: string) => void;
  /** Whether the system is currently processing a message */
  disabled?: boolean;
  /** Placeholder text for the input field */
  placeholder?: string;
}

/**
 * MessageInput component provides a user interface for sending messages.
 * 
 * Features:
 * - Text input with character limit (2000 chars per backend API)
 * - Submit button with loading state
 * - Keyboard shortcuts (Enter to send, Shift+Enter for new line)
 * - Input validation and trimming
 * - Disabled state while processing
 * - Character count indicator
 * - Responsive design
 * 
 * @example
 * ```tsx
 * <MessageInput 
 *   onSendMessage={(msg) => handleSend(msg)}
 *   disabled={isLoading}
 *   placeholder="Type your message..."
 * />
 * ```
 */
export default function MessageInput({
  onSendMessage,
  disabled = false,
  placeholder = 'Type your message...',
}: MessageInputProps) {
  const [message, setMessage] = useState('');
  const MAX_LENGTH = 2000; // Match backend validation

  // Handle form submission
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    sendMessage();
  };

  // Send message if valid
  const sendMessage = () => {
    const trimmedMessage = message.trim();
    
    // Don't send empty messages
    if (!trimmedMessage) {
      return;
    }

    // Don't send if disabled (processing)
    if (disabled) {
      return;
    }

    // Don't send if exceeds max length
    if (trimmedMessage.length > MAX_LENGTH) {
      return;
    }

    // Send the message
    onSendMessage(trimmedMessage);
    
    // Clear the input
    setMessage('');
  };

  // Handle Enter key (send) vs Shift+Enter (new line)
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  // Calculate remaining characters
  const remainingChars = MAX_LENGTH - message.length;
  const isNearLimit = remainingChars < 100;
  const isOverLimit = remainingChars < 0;

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-4 dark:border-gray-700 dark:bg-gray-900">
      <form onSubmit={handleSubmit} className="flex flex-col gap-2">
        <div className="flex gap-2">
          {/* Text input */}
          <div className="relative flex-1">
            <textarea
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={disabled}
              placeholder={placeholder}
              rows={1}
              maxLength={MAX_LENGTH + 100} // Allow typing slightly over to show error
              className={`w-full resize-none rounded-lg border px-4 py-3 pr-16 text-sm focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50 ${
                isOverLimit
                  ? 'border-red-300 bg-red-50 focus:border-red-500 focus:ring-red-500 dark:border-red-700 dark:bg-red-950 dark:focus:border-red-500'
                  : 'border-gray-300 bg-white focus:border-blue-500 focus:ring-blue-500 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-100 dark:focus:border-blue-500'
              }`}
              style={{
                minHeight: '44px',
                maxHeight: '120px',
                height: 'auto',
              }}
              aria-label="Message input"
              aria-invalid={isOverLimit}
              aria-describedby={isNearLimit ? 'char-count' : undefined}
            />
            
            {/* Character count - shown when near or over limit */}
            {isNearLimit && (
              <div
                id="char-count"
                className={`absolute bottom-2 right-2 text-xs font-medium ${
                  isOverLimit
                    ? 'text-red-600 dark:text-red-400'
                    : 'text-gray-500 dark:text-gray-400'
                }`}
              >
                {remainingChars}
              </div>
            )}
          </div>

          {/* Send button */}
          <button
            type="submit"
            disabled={disabled || !message.trim() || isOverLimit}
            className="flex h-[44px] items-center justify-center rounded-lg bg-blue-600 px-6 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:bg-blue-600 dark:bg-blue-500 dark:hover:bg-blue-600 dark:focus:ring-offset-gray-900"
            aria-label="Send message"
          >
            {disabled ? (
              <>
                {/* Loading spinner */}
                <svg
                  className="mr-2 h-4 w-4 animate-spin"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Sending...
              </>
            ) : (
              <>
                Send
                {/* Send icon */}
                <svg
                  className="ml-2 h-4 w-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"
                  />
                </svg>
              </>
            )}
          </button>
        </div>

        {/* Helper text */}
        <div className="flex items-center justify-between px-1">
          <p className="text-xs text-gray-500 dark:text-gray-500">
            Press <kbd className="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-xs dark:bg-gray-800">Enter</kbd> to send,{' '}
            <kbd className="rounded bg-gray-100 px-1.5 py-0.5 font-mono text-xs dark:bg-gray-800">Shift+Enter</kbd> for new line
          </p>
          
          {/* Error message when over limit */}
          {isOverLimit && (
            <p className="text-xs font-medium text-red-600 dark:text-red-400">
              Message too long ({Math.abs(remainingChars)} over limit)
            </p>
          )}
        </div>
      </form>
    </div>
  );
}

