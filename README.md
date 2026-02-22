# FastAPI Microblog API

A production oriented REST API built with FastAPI that demonstrates:

- Secure user authentication (Basic Auth)
- Clean architecture separation
- Input validation with Pydantic
- Relational modeling with SQLAlchemy
- Paginated resource retrieval
- Secure password hashing (bcrypt)
- Production-aware design decisions

This project was built as a take-home assessment to showcase backend engineering fundamentals, clean code structure, and architectural clarity.

---

# Run This:

```bash
git clone https://github.com/DavidLivingstoneHini/fastapi-microblog-api
cd posts-service

python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Then open:

Swagger UI:
http://localhost:8000/docs

ReDoc:
http://localhost:8000/redoc

You can test all endpoints directly from Swagger.

---

# Table of Contents

- Project Overview
- Architecture Overview
- Tech Stack
- Features
- Database Schema
- API Endpoints
- Testing the API
- Design Decisions
- Assumptions
- Production Improvements
- Troubleshooting

---

# Project Overview

This service provides:

- User registration
- Basic authentication
- Post creation
- Post listing with pagination
- Proper validation and error handling

The implementation emphasizes:

- Separation of concerns
- Explicit validation
- Secure password storage
- Clean and maintainable structure

---

# Architecture Overview

The project follows a layered architecture:

### 1. API Layer
- FastAPI routers
- Request/response handling
- Dependency injection

### 2. Schema Layer
- Pydantic models
- Input validation
- Response serialization

### 3. Service / Business Logic Layer
- Authentication handling
- Data validation rules
- Business logic orchestration

### 4. Data Layer
- SQLAlchemy ORM models
- Database session management

This separation ensures:

- Maintainability
- Testability
- Clear dependency boundaries
- Clean scaling path

---

# Features

## Core Requirements

- User Registration
- Basic Authentication
- Create Text Posts
- List Posts (Paginated)
- Input Validation
- Proper HTTP Status Codes

## Additional Enhancements

- Password hashing with bcrypt
- Unique constraints (email, username)
- Relationship loading (post includes author)
- Environment-configurable database
- CORS enabled
- Type hints throughout

---

# Database Schema

## Users

- id (Primary Key)
- email (Unique)
- username (Unique)
- hashed_password
- created_at

## Posts

- id (Primary Key)
- title
- content
- author_id (Foreign Key → users.id)
- created_at

Relationship:

One User → Many Posts

---

# API Endpoints

## User Endpoints

### Register User

POST /users/register

```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123"
}
```

Returns 201 Created

---

### Get Current User

GET /users/me

Requires Basic Authentication

---

## Post Endpoints

### Create Post

POST /posts

Requires Basic Authentication

```json
{
  "title": "My First Post",
  "content": "This is the content"
}
```

Returns 201 Created

---

### List Posts (Paginated)

GET /posts?page=1&page_size=10

Query Parameters:

- page (default: 1)
- page_size (default: 10, max: 50)

Response:

```json
{
  "items": ["..."],
  "total": 50,
  "page": 1,
  "page_size": 10,
  "pages": 5
}
```

---

### Get Single Post

GET /posts/{post_id}

Includes author details in response.

---

# Testing the API

## Using Swagger

Visit:
http://localhost:8000/docs

Register a user first, then use the "Authorize" button for Basic Auth.

---

## Using curl

### Register User

```bash
curl -X POST http://localhost:8000/users/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'
```

### Create Post (macOS/Linux)

```bash
curl -X POST http://localhost:8000/posts \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'testuser:password123' | base64)" \
  -d '{"title":"Hello","content":"My first post"}'
```

### Create Post (PowerShell)

```powershell
$cred = [Convert]::ToBase64String([Text.Encoding]::ASCII.GetBytes("testuser:password123"))
curl -X POST http://localhost:8000/posts `
  -H "Content-Type: application/json" `
  -H "Authorization: Basic $cred" `
  -d '{"title":"Hello","content":"My first post"}'
```

---

# Key Design Decisions

## Why Basic Authentication?

The assignment explicitly requested Basic Auth.  
In production, I would've replaced it with JWT or OAuth2.

## Why SQLite?

SQLite keeps setup simple and portable.  
The project is database-agnostic and can easily switch to PostgreSQL via configuration.

## Pagination Strategy

Offset based pagination (page + page_size) was chosen for clarity and simplicity.

For large scale production systems, cursor based pagination would be the preferred choice for me.

## Password Security

Passwords are hashed using bcrypt via passlib.  
Plain text passwords are never stored.

---

# Assumptions

- Posts are publicly readable.
- No editing or deletion required.
- No role-based access control required.
- Basic Auth sufficient for this assignment.
- No file uploads required.

---

# Production Improvements

If extended beyond an assignment, I would:

- Replace Basic Auth with JWT + refresh tokens
- Add unit and integration tests
- Add Docker containerization
- Use PostgreSQL in production
- Add structured logging
- Add rate limiting
- Add request/response tracing
- Add soft deletes
- Implement cursor based pagination
- Add CI/CD pipeline
- Add database migrations

---

# Troubleshooting

## Virtual Environment Not Activating (Windows)

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then activate:

```powershell
.\venv\Scripts\Activate
```

---

## Port Already in Use

Windows:

```powershell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Or run on a different port:

```bash
uvicorn app.main:app --reload --port 8001
```

---

# Author

Livingstone David Hini