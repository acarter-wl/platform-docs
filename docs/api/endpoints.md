# API Documentation

## Base URL

```
Production: https://api.example.com/v1
Staging: https://api-staging.example.com/v1
Development: http://localhost:3000/v1
```

## Authentication

All API requests require authentication using JWT tokens in the Authorization header:

```http
Authorization: Bearer <your_jwt_token>
```

### Getting a Token

**POST** `/auth/login`

```json
{
  "email": "user@example.com",
  "password": "your_password"
}
```

**Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expiresIn": 3600,
  "user": {
    "id": "user-123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

## Common Response Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request succeeded |
| 201 | Created | Resource created successfully |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

## Rate Limiting

- **Default**: 100 requests per minute
- **Authenticated**: 1000 requests per minute
- **Headers**:
  - `X-RateLimit-Limit`: Maximum requests allowed
  - `X-RateLimit-Remaining`: Remaining requests
  - `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

---

## Users API

### List Users

**GET** `/users`

Query Parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 20, max: 100) |
| role | string | No | Filter by role (admin, user, guest) |
| search | string | No | Search by name or email |

**Example Request**:
```bash
curl -X GET "https://api.example.com/v1/users?page=1&limit=20&role=user" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
{
  "data": [
    {
      "id": "user-123",
      "email": "john@example.com",
      "name": "John Doe",
      "role": "user",
      "createdAt": "2025-01-15T10:30:00Z",
      "updatedAt": "2025-01-15T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

### Get User by ID

**GET** `/users/:id`

**Example Request**:
```bash
curl -X GET "https://api.example.com/v1/users/user-123" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
{
  "id": "user-123",
  "email": "john@example.com",
  "name": "John Doe",
  "role": "user",
  "profile": {
    "avatar": "https://cdn.example.com/avatars/user-123.jpg",
    "bio": "Software engineer",
    "location": "San Francisco, CA"
  },
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-01-15T10:30:00Z"
}
```

### Create User

**POST** `/users`

**Permissions**: Admin only

**Request Body**:
```json
{
  "email": "newuser@example.com",
  "name": "Jane Smith",
  "password": "SecureP@ssw0rd",
  "role": "user"
}
```

**Response** (201 Created):
```json
{
  "id": "user-456",
  "email": "newuser@example.com",
  "name": "Jane Smith",
  "role": "user",
  "createdAt": "2025-11-19T14:30:00Z"
}
```

### Update User

**PATCH** `/users/:id`

**Permissions**: Own profile or admin

**Request Body**:
```json
{
  "name": "Jane Doe",
  "profile": {
    "bio": "Senior Software Engineer"
  }
}
```

**Response**:
```json
{
  "id": "user-456",
  "email": "newuser@example.com",
  "name": "Jane Doe",
  "role": "user",
  "profile": {
    "bio": "Senior Software Engineer"
  },
  "updatedAt": "2025-11-19T15:00:00Z"
}
```

### Delete User

**DELETE** `/users/:id`

**Permissions**: Admin only

**Response** (204 No Content)

---

## Orders API

### List Orders

**GET** `/orders`

Query Parameters:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| status | string | No | Filter by status (pending, completed, failed) |
| userId | string | No | Filter by user ID |
| startDate | string | No | ISO 8601 date |
| endDate | string | No | ISO 8601 date |
| cursor | string | No | Pagination cursor |

**Example Request**:
```bash
curl -X GET "https://api.example.com/v1/orders?status=completed&cursor=eyJpZCI6MTIzfQ==" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
{
  "data": [
    {
      "id": "order-789",
      "userId": "user-123",
      "items": [
        {
          "productId": "prod-001",
          "name": "Premium Subscription",
          "quantity": 1,
          "price": 99.99
        }
      ],
      "subtotal": 99.99,
      "tax": 8.00,
      "total": 107.99,
      "status": "completed",
      "createdAt": "2025-11-18T10:00:00Z",
      "completedAt": "2025-11-18T10:05:00Z"
    }
  ],
  "pagination": {
    "cursor": "eyJpZCI6Nzg5fQ==",
    "hasMore": true
  }
}
```

### Get Order by ID

**GET** `/orders/:id`

**Example Request**:
```bash
curl -X GET "https://api.example.com/v1/orders/order-789" \
  -H "Authorization: Bearer <token>"
```

**Response**:
```json
{
  "id": "order-789",
  "userId": "user-123",
  "items": [
    {
      "productId": "prod-001",
      "name": "Premium Subscription",
      "quantity": 1,
      "price": 99.99
    }
  ],
  "subtotal": 99.99,
  "tax": 8.00,
  "total": 107.99,
  "status": "completed",
  "paymentMethod": {
    "type": "card",
    "last4": "4242"
  },
  "shippingAddress": {
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105",
    "country": "US"
  },
  "createdAt": "2025-11-18T10:00:00Z",
  "updatedAt": "2025-11-18T10:05:00Z",
  "completedAt": "2025-11-18T10:05:00Z"
}
```

### Create Order

**POST** `/orders`

**Request Body**:
```json
{
  "items": [
    {
      "productId": "prod-001",
      "quantity": 1
    }
  ],
  "paymentMethodId": "pm_card_visa",
  "shippingAddress": {
    "street": "123 Main St",
    "city": "San Francisco",
    "state": "CA",
    "zip": "94105",
    "country": "US"
  }
}
```

**Response** (201 Created):
```json
{
  "id": "order-890",
  "userId": "user-123",
  "items": [
    {
      "productId": "prod-001",
      "name": "Premium Subscription",
      "quantity": 1,
      "price": 99.99
    }
  ],
  "subtotal": 99.99,
  "tax": 8.00,
  "total": 107.99,
  "status": "pending",
  "createdAt": "2025-11-19T14:30:00Z"
}
```

### Cancel Order

**POST** `/orders/:id/cancel`

**Permissions**: Order owner or admin

**Request Body** (optional):
```json
{
  "reason": "Customer requested cancellation"
}
```

**Response**:
```json
{
  "id": "order-890",
  "status": "cancelled",
  "cancelledAt": "2025-11-19T15:00:00Z",
  "cancelReason": "Customer requested cancellation"
}
```

---

## Webhooks API

### List Webhooks

**GET** `/webhooks`

**Permissions**: Admin only

**Response**:
```json
{
  "data": [
    {
      "id": "webhook-123",
      "url": "https://example.com/webhook",
      "events": ["order.created", "order.completed"],
      "active": true,
      "createdAt": "2025-11-01T10:00:00Z"
    }
  ]
}
```

### Create Webhook

**POST** `/webhooks`

**Permissions**: Admin only

**Request Body**:
```json
{
  "url": "https://example.com/webhook",
  "events": ["order.created", "order.completed"],
  "secret": "whsec_your_secret_key"
}
```

**Response** (201 Created):
```json
{
  "id": "webhook-456",
  "url": "https://example.com/webhook",
  "events": ["order.created", "order.completed"],
  "active": true,
  "createdAt": "2025-11-19T14:30:00Z"
}
```

### Test Webhook

**POST** `/webhooks/:id/test`

**Permissions**: Admin only

Sends a test event to the webhook URL.

**Response**:
```json
{
  "success": true,
  "statusCode": 200,
  "response": "Webhook received",
  "latency": 145
}
```

---

## Webhook Events

Sample Service can send webhook notifications for various events.

### Event Structure

```json
{
  "id": "evt_123456",
  "type": "order.created",
  "createdAt": "2025-11-19T14:30:00Z",
  "data": {
    "object": {
      "id": "order-890",
      "userId": "user-123",
      "total": 107.99,
      "status": "pending"
    }
  }
}
```

### Event Types

| Event | Description |
|-------|-------------|
| `order.created` | New order created |
| `order.completed` | Order successfully completed |
| `order.failed` | Order processing failed |
| `order.cancelled` | Order cancelled by user |
| `user.created` | New user registered |
| `user.updated` | User profile updated |
| `payment.succeeded` | Payment processed successfully |
| `payment.failed` | Payment processing failed |

### Webhook Signature Verification

Verify webhook authenticity using the signature header:

```javascript
const crypto = require('crypto')

function verifyWebhook(payload, signature, secret) {
  const hash = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(hash)
  )
}
```

---

## Health & Status

### Health Check

**GET** `/health`

No authentication required.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-19T14:30:00Z",
  "services": {
    "database": "healthy",
    "cache": "healthy",
    "queue": "healthy"
  },
  "uptime": 86400
}
```

### API Version

**GET** `/version`

No authentication required.

**Response**:
```json
{
  "version": "1.2.3",
  "apiVersion": "v1",
  "buildDate": "2025-11-15T10:00:00Z",
  "commit": "abc123def456"
}
```

---

## SDK Examples

### JavaScript/TypeScript

```typescript
import { SampleServiceClient } from '@example/sample-service-sdk'

const client = new SampleServiceClient({
  apiKey: 'your_api_key',
  baseUrl: 'https://api.example.com/v1'
})

// Get user
const user = await client.users.get('user-123')

// Create order
const order = await client.orders.create({
  items: [{ productId: 'prod-001', quantity: 1 }],
  paymentMethodId: 'pm_card_visa'
})
```

### Python

```python
from sample_service import Client

client = Client(
    api_key='your_api_key',
    base_url='https://api.example.com/v1'
)

# Get user
user = client.users.get('user-123')

# Create order
order = client.orders.create(
    items=[{'productId': 'prod-001', 'quantity': 1}],
    payment_method_id='pm_card_visa'
)
```

### cURL

```bash
# Get user
curl -X GET "https://api.example.com/v1/users/user-123" \
  -H "Authorization: Bearer <token>"

# Create order
curl -X POST "https://api.example.com/v1/orders" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"productId": "prod-001", "quantity": 1}],
    "paymentMethodId": "pm_card_visa"
  }'
```

---

## Best Practices

### Idempotency

Use idempotency keys for safe retries on POST requests:

```http
POST /orders
Idempotency-Key: unique-key-123
```

If the same key is used within 24 hours, the original response is returned.

### Pagination

Always use pagination for list endpoints to avoid timeouts:

```
GET /orders?limit=50&cursor=eyJpZCI6MTIzfQ==
```

### Error Handling

Always handle errors gracefully:

```typescript
try {
  const order = await client.orders.create(orderData)
} catch (error) {
  if (error.code === 'RATE_LIMIT_EXCEEDED') {
    // Wait and retry
  } else if (error.code === 'VALIDATION_ERROR') {
    // Handle validation errors
  } else {
    // Log and alert
  }
}
```

### Caching

Implement caching for frequently accessed resources:

```http
Cache-Control: max-age=60
ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

Use ETags for conditional requests:

```http
If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
```

---

## Support

- **API Issues**: #api-support on Slack
- **Rate Limit Increases**: Contact platform team
- **Documentation Bugs**: Open issue on GitHub
- **Security Issues**: security@example.com
