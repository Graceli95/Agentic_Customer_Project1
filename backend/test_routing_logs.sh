#!/bin/bash
# Test script to demonstrate routing logging in Phase 3
# Run this after starting the backend with: uvicorn main:app --reload

echo "================================================"
echo "PHASE 3: ROUTING LOGGING TEST"
echo "================================================"
echo ""
echo "Watch the backend logs to see routing decisions!"
echo ""

# Test 1: Technical query - should route to worker
echo "Test 1: Technical Query (Should route to worker)"
echo "------------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Error 500 when logging in",
    "session_id": "test-route-1-550e8400-e29b-41d4-a716-446655440000"
  }' | jq .

echo ""
echo "👆 Check logs for: 🔀 ROUTING: Query routed to worker agent"
echo ""
sleep 2

# Test 2: General query - should handle directly
echo "Test 2: General Query (Should handle directly)"
echo "------------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Hello! How are you?",
    "session_id": "test-route-2-a1b2c3d4-e5f6-4789-a012-3456789abcde"
  }' | jq .

echo ""
echo "👆 Check logs for: ✋ DIRECT: Supervisor handled query directly"
echo ""
sleep 2

# Test 3: Another technical query
echo "Test 3: Technical Query (Should route to worker)"
echo "------------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "My app keeps crashing",
    "session_id": "test-route-3-b2c3d4e5-f6a7-4890-b123-456789abcdef"
  }' | jq .

echo ""
echo "👆 Check logs for: 🔀 ROUTING: Query routed to worker agent"
echo ""
sleep 2

# Test 4: Another general query
echo "Test 4: General Query (Should handle directly)"
echo "------------------------------------------------"
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Thank you for your help!",
    "session_id": "test-route-4-c3d4e5f6-a7b8-4901-c234-567890abcdef"
  }' | jq .

echo ""
echo "👆 Check logs for: ✋ DIRECT: Supervisor handled query directly"
echo ""

echo "================================================"
echo "TEST COMPLETE"
echo "================================================"
echo ""
echo "Summary:"
echo "- Tests 1 & 3 should show: 🔀 ROUTING (routed to worker)"
echo "- Tests 2 & 4 should show: ✋ DIRECT (handled by supervisor)"
echo "- Each log shows execution time in seconds"
echo ""

