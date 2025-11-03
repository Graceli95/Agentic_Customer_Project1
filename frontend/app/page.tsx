'use client';

import { useEffect, useState } from 'react';
import { getOrCreateSessionId, clearSession } from '@/lib/sessionManager';
import ChatInterface from '@/components/ChatInterface';

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

  // Show loading state until client-side hydration is complete
  if (!isClient) {
    return (
      <div className="flex h-screen items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <div className="h-12 w-12 animate-spin rounded-full border-4 border-blue-600 border-t-transparent"></div>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-gray-50 dark:bg-gray-950">
      {/* Chat Interface */}
      <ChatInterface sessionId={sessionId} onClearSession={handleClearSession} />
    </div>
  );
}

