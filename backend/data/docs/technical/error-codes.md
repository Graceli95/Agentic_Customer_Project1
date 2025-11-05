# Error Code Reference Guide

## HTTP Error Codes

### 2xx Success Codes
- **200 OK**: Request succeeded
- **201 Created**: Resource created successfully
- **204 No Content**: Success but no content to return

### 4xx Client Error Codes

#### 400 Bad Request
**Meaning**: Server cannot process request due to client error
**Common Causes**:
- Malformed JSON syntax
- Missing required fields
- Invalid data types
- Failed validation rules

**Example Response**:
```json
{
  "error": "Bad Request",
  "message": "Missing required field: email",
  "field": "email"
}
```

**Fix**: Check request format and include all required fields

#### 401 Unauthorized
**Meaning**: Authentication required or failed
**Common Causes**:
- Missing API key or token
- Expired authentication token
- Invalid credentials
- Token not included in header

**Fix**:
```bash
# Include Authorization header
curl -H "Authorization: Bearer YOUR_TOKEN" https://api.example.com/endpoint
```

#### 403 Forbidden
**Meaning**: Server understood but refuses to authorize
**Common Causes**:
- Insufficient permissions
- Account suspended
- Resource access restricted
- IP address blocked

**Difference from 401**: You are authenticated but not authorized

#### 404 Not Found
**Meaning**: Requested resource doesn't exist
**Common Causes**:
- Incorrect URL or endpoint
- Resource was deleted
- Typo in path
- Resource ID doesn't exist

**Fix**: Verify URL spelling and resource existence

#### 429 Too Many Requests
**Meaning**: Rate limit exceeded
**Common Causes**:
- Too many requests in short time
- Exceeded API quota
- Missing rate limit handling

**Fix**:
```python
import time

# Implement retry with exponential backoff
def retry_request(url, max_retries=3):
    for i in range(max_retries):
        response = requests.get(url)
        if response.status_code == 429:
            wait_time = 2 ** i
            time.sleep(wait_time)
            continue
        return response
```

### 5xx Server Error Codes

#### 500 Internal Server Error
**Meaning**: Generic server error
**Common Causes**:
- Unhandled exception in code
- Database connection failure
- Configuration error
- Resource exhaustion

**User Action**: Contact support with request details

#### 502 Bad Gateway
**Meaning**: Invalid response from upstream server
**Common Causes**:
- Load balancer cannot reach backend
- Backend server down
- Timeout from backend
- Network connectivity issues

**User Action**: Try again later or contact support

#### 503 Service Unavailable
**Meaning**: Server temporarily unable to handle request
**Common Causes**:
- Server maintenance
- Server overloaded
- Dependency service down

**User Action**: Retry after some time

#### 504 Gateway Timeout
**Meaning**: Upstream server didn't respond in time
**Common Causes**:
- Slow database query
- Long-running operation
- Network latency
- Backend not responding

**User Action**: Retry or optimize request

## Application-Specific Error Codes

### AUTH-001: Invalid API Key
**Description**: Provided API key is not valid
**Resolution**:
1. Verify API key is correct
2. Check key hasn't expired
3. Ensure key is for correct environment (dev/prod)
4. Generate new key if needed

### AUTH-002: Token Expired
**Description**: Authentication token has expired
**Resolution**:
```javascript
// Refresh token before expiry
if (tokenExpiryTime < Date.now()) {
  const newToken = await refreshAuthToken();
  updateToken(newToken);
}
```

### DB-001: Connection Failed
**Description**: Cannot connect to database
**Resolution**:
1. Check database server is running
2. Verify connection string
3. Check firewall rules
4. Verify credentials

### DB-002: Query Timeout
**Description**: Database query took too long
**Resolution**:
1. Optimize query with indexes
2. Reduce result set size
3. Increase timeout setting
4. Check database performance

### VALID-001: Required Field Missing
**Description**: Required field not provided
**Resolution**: Include all required fields in request

**Example**:
```json
{
  "error_code": "VALID-001",
  "message": "Required field missing",
  "field": "email",
  "required_fields": ["name", "email", "password"]
}
```

### VALID-002: Invalid Format
**Description**: Field value doesn't match expected format
**Resolution**: Check format requirements

**Common Format Rules**:
- Email: must contain @ and valid domain
- Phone: must match pattern (e.g., +1-555-555-5555)
- Date: ISO 8601 format (YYYY-MM-DD)
- UUID: Valid UUID v4 format

### RATE-001: Rate Limit Exceeded
**Description**: Too many requests in time window
**Response Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1635789600
```

**Resolution**:
1. Wait until reset time
2. Implement request throttling
3. Upgrade to higher tier plan
4. Use batch endpoints if available

## Error Response Format

All API errors follow consistent format:

```json
{
  "error": "Error Type",
  "message": "Human-readable description",
  "error_code": "APP-CODE",
  "details": {
    "field": "problematic_field",
    "value": "invalid_value",
    "expected": "format description"
  },
  "timestamp": "2025-11-04T10:30:00Z",
  "request_id": "req_abc123",
  "documentation": "https://docs.example.com/errors/APP-CODE"
}
```

## Best Practices for Error Handling

### In Your Application

**1. Always Check Status Codes**
```python
response = requests.post(url, json=data)
if response.status_code != 200:
    handle_error(response)
```

**2. Log Errors with Context**
```python
logger.error(f"API call failed: {response.status_code}", 
             extra={
                 "url": url,
                 "request_id": response.headers.get("X-Request-ID"),
                 "error_code": error.get("error_code")
             })
```

**3. Implement Retry Logic**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def api_call_with_retry(url):
    response = requests.get(url)
    response.raise_for_status()
    return response
```

**4. Provide User-Friendly Messages**
```python
error_messages = {
    "AUTH-001": "Your session has expired. Please log in again.",
    "RATE-001": "Too many requests. Please try again in a few minutes.",
    "DB-001": "We're experiencing technical difficulties. Please try again later."
}

user_message = error_messages.get(error_code, "An error occurred. Please contact support.")
```

### When Reporting Errors to Support

Include:
1. Full error response (JSON)
2. Request details (URL, method, headers - remove auth tokens)
3. Timestamp
4. Request ID from response headers
5. Steps to reproduce
6. Application version and environment

## Quick Reference

| Code | Name | Retry? | User Action |
|------|------|--------|-------------|
| 400 | Bad Request | No | Fix request format |
| 401 | Unauthorized | No | Check authentication |
| 403 | Forbidden | No | Check permissions |
| 404 | Not Found | No | Verify URL/resource |
| 429 | Too Many Requests | Yes | Wait and retry |
| 500 | Internal Server | Maybe | Contact support |
| 502 | Bad Gateway | Yes | Retry after delay |
| 503 | Service Unavailable | Yes | Wait and retry |
| 504 | Gateway Timeout | Maybe | Retry or optimize |

