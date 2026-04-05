# 🔐 FastAPI Auth System

A step-by-step backend authentication system built using FastAPI.
This project is part of my journey to deeply understand how authentication works in real-world applications.

---

## 🚀 Tech Stack

* FastAPI
* Python
* Uvicorn
* SQLAlchemy (ORM)
* SQLite (Database)

---

## 📌 Features (Planned & Completed)

* [x] Project setup with FastAPI
* [x] Basic routing
* [x] Database setup (SQLite)
* [x] User model (SQLAlchemy ORM)
* [ ] User signup (registration API)
* [ ] User login
* [ ] Password hashing
* [ ] JWT authentication
* [ ] Protected routes
* [ ] Refresh tokens (advanced)

---

## 📅 Progress Log

### Day 1

* Setup FastAPI project
* Created basic routes
* Ran server successfully

### Day 2

* Setup SQLite database
* Created database connection
* Defined User model using SQLAlchemy
* Successfully created database tables

---

## ⚙️ How to Run

```bash
# Clone the repo
git clone <your-repo-url>

# Navigate to project
cd auth-system-fastapi/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic

# Run server
uvicorn main:app --reload
```

---

## 📍 API Endpoints

### POST /signup

Register a new user

**Request Body:**

```json
{
  "email": "test@example.com",
  "password": "123456"
}
```

**Response:**

```json
{
  "message": "User created successfully"
}
```

---

## 📍 API Docs

Once server is running:

* Swagger UI: http://127.0.0.1:8000/docs

---

## ⚠️ Current Limitation

* Passwords are stored in plain text (will be fixed in upcoming steps with hashing)

---

## 🎯 Goal

To build a production-ready authentication system while understanding:

* How authentication works internally
* Security best practices
* Backend architecture

---

## 🧠 Learning Approach

This project is built step-by-step (day by day) instead of copying tutorials, focusing on real understanding and hands-on debugging.

---

## ✍️ Author

Prashant Maurya
