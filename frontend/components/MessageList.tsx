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
  /** Callback when an example query is clicked */
  onExampleClick?: (query: string) => void;
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
export default function MessageList({ messages, isLoading = false, onExampleClick }: MessageListProps) {
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
    <div style={{ height: '100%', width: '100%', overflowY: 'auto' }}>
      {/* Container with proper width */}
      <div style={{ margin: '0 auto', width: '100%', maxWidth: '900px', padding: '32px 16px' }}>
        {/* Empty state - no messages yet */}
        {messages.length === 0 && !isLoading && (
          <div 
            style={{ 
              display: 'flex', 
              minHeight: '50vh', 
              alignItems: 'center', 
              justifyContent: 'center',
              width: '100%'
            }}
          >
            <div style={{ width: '100%', maxWidth: '500px', textAlign: 'center' }}>
              {/* Icon */}
              <div 
                style={{ 
                  width: '56px', 
                  height: '56px', 
                  margin: '0 auto 20px auto',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '16px',
                  background: 'linear-gradient(to bottom right, #3b82f6, #4f46e5)',
                  color: 'white',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
                }}
              >
                <svg style={{ width: '28px', height: '28px' }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              
              {/* Heading */}
              <h3 style={{ 
                marginBottom: '8px', 
                fontSize: '20px', 
                fontWeight: 600, 
                color: 'white',
                whiteSpace: 'nowrap'
              }}>
                How can I help you today?
              </h3>
              <p style={{ 
                marginBottom: '32px', 
                fontSize: '14px', 
                color: '#cbd5e1'
              }}>
                Choose a topic below or type your question
              </p>

              {/* Quick action buttons */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <button
                  onClick={() => onExampleClick?.("I'm getting Error 500")}
                  style={{
                    display: 'flex',
                    width: '100%',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.05)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    color: 'white'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>🔧</span>
                  <div>
                    <span style={{ display: 'block', fontSize: '12px', fontWeight: 500, color: '#94a3b8' }}>Technical</span>
                    <span style={{ display: 'block', marginTop: '4px', fontSize: '14px', color: 'white' }}>I&apos;m getting Error 500</span>
                  </div>
                </button>

                <button
                  onClick={() => onExampleClick?.("What are your pricing plans?")}
                  style={{
                    display: 'flex',
                    width: '100%',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.05)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    color: 'white'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>💰</span>
                  <div>
                    <span style={{ display: 'block', fontSize: '12px', fontWeight: 500, color: '#94a3b8' }}>Billing</span>
                    <span style={{ display: 'block', marginTop: '4px', fontSize: '14px', color: 'white' }}>What are your pricing plans?</span>
                  </div>
                </button>

                <button
                  onClick={() => onExampleClick?.("What services do you offer?")}
                  style={{
                    display: 'flex',
                    width: '100%',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.05)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    color: 'white'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>ℹ️</span>
                  <div>
                    <span style={{ display: 'block', fontSize: '12px', fontWeight: 500, color: '#94a3b8' }}>General</span>
                    <span style={{ display: 'block', marginTop: '4px', fontSize: '14px', color: 'white' }}>What services do you offer?</span>
                  </div>
                </button>

                <button
                  onClick={() => onExampleClick?.("What's your data retention policy?")}
                  style={{
                    display: 'flex',
                    width: '100%',
                    alignItems: 'center',
                    gap: '16px',
                    padding: '16px',
                    borderRadius: '12px',
                    border: '1px solid rgba(255,255,255,0.1)',
                    background: 'rgba(255,255,255,0.05)',
                    textAlign: 'left',
                    cursor: 'pointer',
                    color: 'white'
                  }}
                >
                  <span style={{ fontSize: '24px' }}>🔒</span>
                  <div>
                    <span style={{ display: 'block', fontSize: '12px', fontWeight: 500, color: '#94a3b8' }}>Compliance</span>
                    <span style={{ display: 'block', marginTop: '4px', fontSize: '14px', color: 'white' }}>What&apos;s your data retention policy?</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Messages list */}
        {messages.length > 0 && (
          <div className="space-y-10">
            {messages.map((message) => (
              <div key={message.id} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse max-w-[50%]' : 'flex-row max-w-[70%]'}`}>
                  {/* Avatar */}
                  <div
                    className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full text-xs font-bold ${
                      message.role === 'user'
                        ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white'
                        : message.role === 'error'
                        ? 'bg-red-500 text-white'
                        : 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
                    }`}
                  >
                    {message.role === 'user' ? 'U' : message.role === 'error' ? '!' : 'AI'}
                  </div>

                  {/* Message content */}
                  <div className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
                    {/* Header */}
                    <div className="mb-1.5 flex items-center gap-2 text-xs">
                      <span className="font-medium text-slate-300">
                        {message.role === 'user' ? 'You' : message.role === 'error' ? 'Error' : 'AI Assistant'}
                      </span>
                      {message.role === 'assistant' && message.agent && (
                        <span className="rounded bg-blue-500/20 px-2 py-0.5 text-[10px] font-semibold uppercase text-blue-300">
                          {message.agent}
                        </span>
                      )}
                      <span className="text-slate-500">{formatTime(message.timestamp)}</span>
                    </div>

                    {/* Bubble */}
                    <div
                      className={`rounded-2xl py-5 ${
                        message.role === 'user'
                          ? 'bg-blue-600 text-white px-6'
                          : message.role === 'error'
                          ? 'border border-red-500/30 bg-red-500/10 text-red-200 px-6'
                          : 'border border-white/10 bg-slate-800/80 text-slate-100 pl-8 pr-8'
                      }`}
                    >
                      {message.role === 'user' ? (
                        <p className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</p>
                      ) : message.role === 'assistant' && message.content === '' && isLoading ? (
                        /* Show "Thinking..." animation inside empty assistant message during streaming */
                        <div className="flex items-center gap-2">
                          <div className="flex space-x-1">
                            <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                            <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                            <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
                          </div>
                          <span className="text-xs text-slate-400">Thinking...</span>
                        </div>
                      ) : (
                        <div className="prose prose-sm prose-invert max-w-none">
                          <ReactMarkdown
                            remarkPlugins={[remarkGfm]}
                            components={{
                              code: ({node, inline, className, children, ...props}: any) => {
                                return inline ? (
                                  <code className="rounded bg-slate-700 px-1.5 py-0.5 text-xs font-mono text-slate-200" {...props}>{children}</code>
                                ) : (
                                  <code className="my-2 block overflow-x-auto rounded-lg bg-slate-900 p-3 text-xs font-mono text-slate-200" {...props}>{children}</code>
                                );
                              },
                              pre: ({node, ...props}: any) => <pre className="!bg-transparent !p-0 !m-0" {...props} />,
                              ul: ({node, ...props}: any) => <ul className="my-3 pl-6 list-disc list-inside space-y-2 [&_p]:inline [&_p]:m-0" {...props} />,
                              ol: ({node, ...props}: any) => <ol className="my-3 pl-6 list-decimal list-inside space-y-2 [&_p]:inline [&_p]:m-0" {...props} />,
                              li: ({node, ...props}: any) => <li className="text-sm leading-relaxed" {...props} />,
                              p: ({node, ...props}: any) => <p className="my-2 text-sm leading-relaxed" {...props} />,
                              h1: ({node, ...props}: any) => <h1 className="mb-2 mt-4 text-base font-bold" {...props} />,
                              h2: ({node, ...props}: any) => <h2 className="mb-2 mt-3 text-sm font-bold" {...props} />,
                              h3: ({node, ...props}: any) => <h3 className="mb-1 mt-2 text-sm font-semibold" {...props} />,
                              blockquote: ({node, ...props}: any) => <blockquote className="my-2 border-l-2 border-blue-500 pl-3 italic text-slate-300" {...props} />,
                              table: ({node, ...props}: any) => (
                                <div className="my-3 overflow-x-auto">
                                  <table className="min-w-full border-collapse text-sm" {...props} />
                                </div>
                              ),
                              thead: ({node, ...props}: any) => <thead className="border-b border-slate-600" {...props} />,
                              tbody: ({node, ...props}: any) => <tbody className="divide-y divide-slate-700" {...props} />,
                              tr: ({node, ...props}: any) => <tr className="border-b border-slate-700" {...props} />,
                              th: ({node, ...props}: any) => <th className="px-3 py-2 text-left font-semibold text-slate-200" {...props} />,
                              td: ({node, ...props}: any) => <td className="px-3 py-2 text-slate-300" {...props} />,
                            }}
                          >
                            {message.content}
                          </ReactMarkdown>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Loading indicator - only show if there's no empty assistant message already (streaming uses placeholder) */}
            {isLoading && !messages.some(m => m.role === 'assistant' && m.content === '') && (
              <div className="flex justify-start">
                <div className="flex max-w-[85%] gap-3">
                  <div className="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-emerald-500 to-teal-600 text-xs font-bold text-white">
                    AI
                  </div>
                  <div className="flex flex-col items-start">
                    <div className="mb-1.5 text-xs font-medium text-slate-300">AI Assistant</div>
                    <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-slate-800/80 px-4 py-3">
                      <div className="flex space-x-1">
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.3s]" />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400 [animation-delay:-0.15s]" />
                        <div className="h-2 w-2 animate-bounce rounded-full bg-slate-400" />
                      </div>
                      <span className="text-xs text-slate-400">Thinking...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>
    </div>
  );
}

