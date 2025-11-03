'use client';

import { useEffect, useState } from 'react';
import { getOrCreateSessionId, clearSession } from '@/lib/sessionManager';

export default function Home() {
  const [sessionId, setSessionId] = useState<string>('');
  const [isClient, setIsClient] = useState(false);

  // Initialize session on component mount
  useEffect(() => {
    setIsClient(true);
    const id = getOrCreateSessionId();
    setSessionId(id);
  }, []);

  // Handle clearing the session
  const handleClearSession = () => {
    const newId = clearSession();
    setSessionId(newId);
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-8">
      {/* Hero Section */}
      <main className="flex w-full max-w-5xl flex-col items-center text-center">
        {/* Icon/Logo Placeholder */}
        <div className="mb-8 flex h-24 w-24 items-center justify-center rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 shadow-lg">
          <svg
            className="h-12 w-12 text-white"
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

        {/* Title */}
        <h1 className="mb-4 text-5xl font-bold tracking-tight text-gray-900 dark:text-gray-50 sm:text-6xl md:text-7xl">
          Customer Service AI
        </h1>

        {/* Subtitle */}
        <p className="mb-8 max-w-2xl text-xl text-gray-600 dark:text-gray-400 sm:text-2xl">
          Advanced Multi-Agent AI System for Intelligent Customer Support
        </p>

        {/* Description */}
        <div className="mb-12 max-w-3xl space-y-4 text-lg text-gray-700 dark:text-gray-300">
          <p>
            Powered by <span className="font-semibold text-blue-600 dark:text-blue-400">LangChain v1.0+</span> and{' '}
            <span className="font-semibold text-purple-600 dark:text-purple-400">LangGraph</span>,
            our intelligent system handles:
          </p>
          <ul className="mx-auto max-w-md space-y-2 text-left">
            <li className="flex items-start">
              <span className="mr-2 text-green-500">✓</span>
              <span>Technical support inquiries</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2 text-green-500">✓</span>
              <span>Billing and payment questions</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2 text-green-500">✓</span>
              <span>Compliance and policy information</span>
            </li>
            <li className="flex items-start">
              <span className="mr-2 text-green-500">✓</span>
              <span>General customer service requests</span>
            </li>
          </ul>
        </div>

        {/* Session Status - Demo for Phase 2 Task 3.3 */}
        {isClient && (
          <div className="mb-8 w-full max-w-2xl rounded-lg border border-blue-200 bg-blue-50 p-6 dark:border-blue-800 dark:bg-blue-950">
            <h3 className="mb-3 text-lg font-semibold text-blue-900 dark:text-blue-100">
              Session Initialized ✓
            </h3>
            <p className="mb-2 text-sm text-blue-700 dark:text-blue-300">
              Your conversation session is active and ready. This session persists across page refreshes.
            </p>
            <div className="mb-4 rounded bg-white p-3 font-mono text-xs text-gray-700 dark:bg-gray-900 dark:text-gray-300">
              Session ID: {sessionId}
            </div>
            <button
              onClick={handleClearSession}
              className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:bg-blue-500 dark:hover:bg-blue-600"
            >
              Clear Session (Generate New ID)
            </button>
            <p className="mt-3 text-xs text-blue-600 dark:text-blue-400">
              💡 Try refreshing the page - your session ID will remain the same!
            </p>
          </div>
        )}

        {/* Status Badge */}
        <div className="mb-8 inline-flex items-center gap-2 rounded-full bg-green-100 px-4 py-2 text-sm font-medium text-green-800 dark:bg-green-900 dark:text-green-200">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-green-400 opacity-75"></span>
            <span className="relative inline-flex h-2 w-2 rounded-full bg-green-500"></span>
          </span>
          In Development - Phase 2: Session Management Active
        </div>

        {/* Feature Cards */}
        <div className="grid w-full max-w-4xl grid-cols-1 gap-6 md:grid-cols-3">
          {/* Card 1 */}
          <div className="card">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900">
              <svg
                className="h-6 w-6 text-blue-600 dark:text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M13 10V3L4 14h7v7l9-11h-7z"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-gray-50">
              Lightning Fast
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Real-time responses powered by advanced AI agents
            </p>
          </div>

          {/* Card 2 */}
          <div className="card">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900">
              <svg
                className="h-6 w-6 text-purple-600 dark:text-purple-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-gray-50">
              Secure & Compliant
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Enterprise-grade security with RAG-powered knowledge base
            </p>
          </div>

          {/* Card 3 */}
          <div className="card">
            <div className="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-cyan-100 dark:bg-cyan-900">
              <svg
                className="h-6 w-6 text-cyan-600 dark:text-cyan-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
            </div>
            <h3 className="mb-2 text-lg font-semibold text-gray-900 dark:text-gray-50">
              Multi-Agent System
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Specialized agents for technical, billing, and compliance
            </p>
          </div>
        </div>

        {/* Footer Note */}
        <div className="mt-16 text-sm text-gray-500 dark:text-gray-500">
          <p>Built with Next.js 16, TypeScript, Tailwind CSS, FastAPI, and LangChain v1.0+</p>
        </div>
      </main>
    </div>
  );
}

