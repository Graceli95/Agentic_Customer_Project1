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
  const [useStreaming, setUseStreaming] = useState(false); // Disable streaming by default (non-streaming works better with create_agent)

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
    console.log('🚀 handleSendMessage called with:', content);
    console.log('📡 useStreaming:', useStreaming);
    console.log('🔑 sessionId:', sessionId);
    
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
      console.log('✅ About to send request...');
      if (useStreaming) {
        // Use streaming mode (SSE)
        const assistantMessageId = generateMessageId();
        let streamedContent = '';
        let agentName: string | undefined;

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
            } else if (event.type === 'done' && 'agent' in event) {
              // Capture agent name from done event
              agentName = event.agent as string;
              
              // Update message with agent info
              setMessages((prev) =>
                prev.map((msg) =>
                  msg.id === assistantMessageId
                    ? { ...msg, agent: agentName }
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
        console.log('📞 Calling non-streaming API...');
        const response = await sendChatMessage(content, sessionId);
        console.log('📥 Received response:', response);

        // Create assistant message from response
        const assistantMessage: Message = {
          id: generateMessageId(),
          content: response.response,
          role: 'assistant',
          timestamp: new Date(),
          agent: response.agent,
        };
        
        console.log('💬 Creating assistant message:', assistantMessage);

        // Add assistant response to conversation
        setMessages((prev) => [...prev, assistantMessage]);
        console.log('✅ Message added to state');
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

  /**
   * Exports the conversation to a text file
   */
  const handleExportConversation = () => {
    if (messages.length === 0) {
      return;
    }

    // Format conversation as text
    const conversationText = messages
      .filter(m => m.role !== 'error')
      .map((msg) => {
        const timestamp = new Date(msg.timestamp).toLocaleString();
        const role = msg.role === 'user' ? 'You' : `AI Assistant${msg.agent ? ` (${msg.agent})` : ''}`;
        return `[${timestamp}] ${role}:\n${msg.content}\n`;
      })
      .join('\n');

    // Create blob and download
    const blob = new Blob([conversationText], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `conversation-${new Date().toISOString().slice(0, 10)}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div style={{ display: 'flex', height: '100%', width: '100%', flexDirection: 'column' }}>
      {/* Compact header */}
      <div className="border-b border-white/10 bg-slate-900/50 px-6 py-4">
        <div className="mx-auto flex max-w-4xl items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 text-white">
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h1 className="text-lg font-semibold text-white">AI Customer Service</h1>
              <p className="text-xs text-slate-400">Technical • Billing • Compliance • General</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Status indicator */}
            <div className="flex items-center gap-2 text-xs text-slate-400">
              <span className={`h-2 w-2 rounded-full ${isLoading ? 'animate-pulse bg-yellow-400' : 'bg-emerald-400'}`} />
              {isLoading ? 'Responding...' : `${messages.filter(m => m.role !== 'error').length} messages`}
            </div>

            {/* Action buttons */}
            <div className="flex items-center gap-1">
              <button
                onClick={() => setUseStreaming(!useStreaming)}
                disabled={isLoading}
                className={`rounded-lg px-3 py-1.5 text-xs font-medium transition ${
                  useStreaming
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                }`}
                title={useStreaming ? 'Streaming mode' : 'Standard mode'}
              >
                {useStreaming ? '⚡ Stream' : '+ Standard'}
              </button>

              {messages.length > 0 && (
                <>
                  <button
                    onClick={handleExportConversation}
                    disabled={isLoading}
                    className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:bg-slate-700 disabled:opacity-50"
                    title="Export chat"
                  >
                    ↓ Export
                  </button>
                  <button
                    onClick={handleClearConversation}
                    disabled={isLoading}
                    className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-300 transition hover:bg-red-900/50 hover:text-red-300 disabled:opacity-50"
                    title="Clear chat"
                  >
                    ✕ Clear
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Conversation area */}
      <div style={{ flex: 1, overflow: 'hidden', background: 'linear-gradient(to bottom, #0f172a, #020617)', width: '100%' }}>
        <MessageList 
          messages={messages} 
          isLoading={isLoading} 
          onExampleClick={handleSendMessage}
        />
      </div>

      {/* Input area */}
      <div style={{ 
        borderTop: '1px solid rgba(255,255,255,0.1)', 
        backgroundColor: 'rgba(15, 23, 42, 0.8)',
        padding: '16px',
        width: '100%'
      }}>
        <div style={{ margin: '0 auto', maxWidth: '500px', width: '100%' }}>
          <MessageInput
            onSendMessage={handleSendMessage}
            disabled={isLoading}
            placeholder="Type your question..."
          />
        </div>
      </div>
    </div>
  );
}

