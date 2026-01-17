# API Documentation

## Overview

The AI Interior Design Platform provides RESTful APIs for design recommendations, leasing management, and user authentication.

## Base URL

```
http://localhost:3000/api
```

## Authentication

Most endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

## Endpoints

### Design Recommendations

#### POST /api/design/recommendations

Get AI-powered design recommendations.

**Request Body:**
```json
{
  "space_type": "living_room",
  "style_preference": "modern",
  "budget": 5000,
  "dimensions": {
    "length": 20,
    "width": 15,
    "height": 10
  }
}
```

**Response:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Modern Sofa",
      "category": "furniture",
      "style": "modern",
      "price": 150,
      "lease_term": "6 months"
    }
  ],
  "total_estimated_cost": 150
}
```

#### POST /api/design/visualize

Generate 3D visualization of the design.

**Request Body:**
```json
{
  "items": [1, 2, 3],
  "room_layout": "standard"
}
```

### Lease Management

#### POST /api/lease/create

Create a new lease agreement.

**Request Body:**
```json
{
  "items": [{"id": 1, "price": 150}],
  "start_date": "2026-02-01",
  "end_date": "2026-08-01",
  "total_cost": 900
}
```

#### GET /api/lease/status/:lease_id

Get the status of a lease agreement.

### User Management

#### POST /api/user/register

Register a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe"
}
```

#### POST /api/user/login

Authenticate and receive a JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

#### GET /api/user/profile

Get user profile information (requires authentication).

## Error Responses

All endpoints may return the following error responses:

- `400 Bad Request`: Invalid input parameters
- `401 Unauthorized`: Missing or invalid authentication token
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

**Error Response Format:**
```json
{
  "error": "Error message",
  "code": "ERROR_CODE"
}
```
