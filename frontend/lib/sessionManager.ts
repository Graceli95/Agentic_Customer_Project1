/**
 * Session Manager
 * 
 * Manages user session IDs for conversation tracking.
 * Session IDs are stored in localStorage and persist across page refreshes.
 * Each session represents a separate conversation with the AI agent.
 * 
 * Related to Task 3.1 in PRD-0002 (Phase 2: Simple Agent Foundation)
 */

const SESSION_STORAGE_KEY = 'session_id';

/**
 * Checks if code is running in browser environment
 * (prevents errors during SSR in Next.js)
 */
function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
}

/**
 * Generates a new UUID v4 session identifier
 * 
 * @returns A UUID v4 string (e.g., "550e8400-e29b-41d4-a716-446655440000")
 */
function generateSessionId(): string {
  if (isBrowser() && window.crypto && window.crypto.randomUUID) {
    return window.crypto.randomUUID();
  }
  
  // Fallback for older browsers (should rarely be needed)
  // This creates a UUID v4 compliant string
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = Math.random() * 16 | 0;
    const v = c === 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * Retrieves the current session ID from localStorage
 * 
 * @returns The stored session ID, or null if none exists
 */
function getSessionId(): string | null {
  if (!isBrowser()) {
    return null;
  }
  
  try {
    return localStorage.getItem(SESSION_STORAGE_KEY);
  } catch (error) {
    console.error('Failed to read session ID from localStorage:', error);
    return null;
  }
}

/**
 * Stores a session ID in localStorage
 * 
 * @param sessionId - The session ID to store
 */
function setSessionId(sessionId: string): void {
  if (!isBrowser()) {
    return;
  }
  
  try {
    localStorage.setItem(SESSION_STORAGE_KEY, sessionId);
  } catch (error) {
    console.error('Failed to save session ID to localStorage:', error);
  }
}

/**
 * Gets the current session ID or creates a new one if none exists
 * This is the primary function for initializing sessions on page load.
 * 
 * @returns The current or newly created session ID
 */
export function getOrCreateSessionId(): string {
  let sessionId = getSessionId();
  
  if (!sessionId) {
    sessionId = generateSessionId();
    setSessionId(sessionId);
  }
  
  return sessionId;
}

/**
 * Clears the current session and generates a new session ID
 * Use this when the user wants to start a fresh conversation.
 * 
 * @returns The newly generated session ID
 */
export function clearSession(): string {
  const newSessionId = generateSessionId();
  setSessionId(newSessionId);
  return newSessionId;
}

/**
 * Validates that a string is a valid UUID v4 format
 * 
 * @param uuid - The string to validate
 * @returns True if the string is a valid UUID v4
 */
export function isValidUUID(uuid: string): boolean {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
  return uuidRegex.test(uuid);
}

/**
 * Validates the current session ID format
 * If invalid, generates a new one
 * 
 * @returns A valid session ID
 */
export function ensureValidSessionId(): string {
  const sessionId = getSessionId();
  
  if (sessionId && isValidUUID(sessionId)) {
    return sessionId;
  }
  
  // Invalid or missing session ID - create new one
  const newSessionId = generateSessionId();
  setSessionId(newSessionId);
  return newSessionId;
}

