# 📝 Notes App Backend API

A backend REST API service for a multi-user notes application built using FastAPI, SQLite, SQLAlchemy, and JWT authentication.

This project was developed as part of an Engineering Internship Assignment.

---

# 🚀 Live Deployment

Base URL:

https://kartik-notes-app.onrender.com

Swagger API Docs:

https://kartik-notes-app.onrender.com/docs

OpenAPI JSON:

https://kartik-notes-app.onrender.com/openapi.json

---

# ⚙️ Tech Stack

- Python
- FastAPI
- SQLite
- SQLAlchemy
- JWT Authentication
- Passlib + Bcrypt
- Uvicorn
- Render (Deployment)

---

# ✨ Features

## Authentication
- User Registration
- User Login
- JWT Token Authentication
- Protected Routes

## Notes Management
- Create Notes
- Get All Notes
- Get Note By ID
- Update Notes
- Delete Notes

## Sharing System
- Share notes with another registered user
- View notes shared with authenticated user
- Ownership validation for security

## Additional Endpoints
- `/about`
- `/openapi.json`

---

# 📌 API Endpoints

## Register User

POST /register

Payload:

```json
{
  "email": "string",
  "password": "string"
}