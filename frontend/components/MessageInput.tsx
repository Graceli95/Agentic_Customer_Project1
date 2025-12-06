/**
 * MessageInput Component
 * 
 * Provides a text input field and submit button for users to send messages.
 * Handles form submission, input validation, and disabled states during processing.
 * 
 * Related to Task 4.2 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

import { useState, type FormEvent, type KeyboardEvent } from 'react';

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
    <form onSubmit={handleSubmit} className="flex gap-3">
      {/* Text input */}
      <div className="relative flex-1">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder={placeholder}
          rows={1}
          maxLength={MAX_LENGTH + 100}
          className={`w-full resize-none rounded-xl border bg-slate-800 px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:opacity-50 ${
            isOverLimit ? 'border-red-500' : 'border-slate-700'
          }`}
          style={{ minHeight: '48px', maxHeight: '120px' }}
          aria-label="Message input"
        />
        {isNearLimit && (
          <span className={`absolute bottom-2 right-3 text-xs ${isOverLimit ? 'text-red-400' : 'text-slate-500'}`}>
            {remainingChars}
          </span>
        )}
      </div>

      {/* Send button */}
      <button
        type="submit"
        disabled={disabled || !message.trim() || isOverLimit}
        className="flex h-12 items-center gap-2 rounded-xl bg-blue-600 px-5 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        {disabled ? (
          <>
            <svg className="h-4 w-4 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            Sending...
          </>
        ) : (
          <>
            Send
            <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </>
        )}
      </button>
    </form>
  );
}

