'use client';

import { useState, useEffect } from 'react';
import { getOrCreateSessionId, clearSession } from '@/lib/sessionManager';
import ChatInterface from '@/components/ChatInterface';

export default function Home() {
  // Initialize session ID only on client side to prevent hydration mismatch
  const [sessionId, setSessionId] = useState<string>('');
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    // This ensures we only run on client side after hydration
    setIsClient(true);
    setSessionId(getOrCreateSessionId());
  }, []);

  // Handle clearing the session
  const handleClearSession = () => {
    const newId = clearSession();
    setSessionId(newId);
  };

  // Show loading state during SSR or if session isn't ready
  if (!isClient || !sessionId) {
    return (
      <div className="flex h-screen items-center justify-center bg-slate-950">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-500 border-t-transparent"></div>
          </div>
          <p className="text-sm text-slate-400">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <main style={{ height: '100vh', width: '100vw', overflow: 'hidden', backgroundColor: '#020617', color: 'white' }}>
      <ChatInterface sessionId={sessionId} onClearSession={handleClearSession} />
    </main>
  );
}

