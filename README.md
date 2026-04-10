# 🔐 FastAPI Auth System

A step-by-step backend authentication system built using FastAPI.
This project is part of my journey to deeply understand how authentication works in real-world applications.

---

## 🚀 Tech Stack

* **FastAPI** — web framework for building APIs
* **Python** — core language
* **Uvicorn** — ASGI server to run FastAPI
* **SQLAlchemy** — ORM (maps Python classes to DB tables)
* **SQLite** — lightweight database (file-based, no setup needed)
* **Pydantic** — data validation (schemas)
* **bcrypt** — password hashing (direct, no passlib)
* **python-jose** — JWT token creation and verification

---

## 📌 Features

* [x] Project setup with FastAPI
* [x] Basic routing
* [x] Database setup (SQLite + SQLAlchemy)
* [x] User model with `email`, `username`, `password`, `is_verified`
* [x] User signup with duplicate email + username checks
* [x] Password hashing with bcrypt (never stored in plain text)
* [x] User login with JWT access token
* [x] Protected routes via token validation
* [x] Input validation with Pydantic schemas (min 8, max 72 bytes)
* [x] Full end-to-end auth flow tested and working
* [ ] Token storage on frontend (localStorage / HttpOnly cookie)
* [ ] Logout + token blocklist
* [ ] Email verification flow
* [ ] Refresh tokens
* [ ] Role-based access control (admin vs user)

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

### Day 3
* Implemented user signup with input validation
* Added password hashing using bcrypt
* Added duplicate email and username checks
* Created Pydantic schemas for request/response shape

### Day 4
* Implemented user login endpoint
* Integrated JWT token generation (access token, 15 min expiry)
* Added `get_current_user` dependency for protected routes
* Built `/profile` endpoint as first protected route
* Moved secret key to environment variable
* Fixed multiple bugs (duplicate function, wrong status codes, deprecated datetime usage)

### Day 5
* Dropped passlib entirely — it's abandoned and broken with bcrypt 4.x+
* Rewrote `hashing.py` to use bcrypt directly (no third-party wrapper)
* Fixed `ImportError` caused by relative imports (files were in `backend/` not `app/`)
* Fixed `OperationalError` — deleted stale `test.db` missing the `is_verified` column
* Added password byte-length validation (bcrypt hard limit is 72 bytes)
* Successfully tested full flow end-to-end: signup → login → JWT → protected profile

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

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy pydantic[email] bcrypt python-jose[cryptography]

# Set your secret key (important — don't skip this)
# Windows
set SECRET_KEY=your-long-random-secret-key
# Mac/Linux
export SECRET_KEY=your-long-random-secret-key

# Run server
uvicorn main:app --reload
```

---

## 📍 API Endpoints

### GET /
Health check — confirms the server is running.

**Response:**
```json
{ "message": "Server is running!" }
```

---

### POST /signUp
Register a new user. Returns 201 on success.

**Request Body:**
```json
{
  "email": "prashant@example.com",
  "password": "securepass123",
  "username": "prashant"
}
```

**Response:**
```json
{ "message": "User created successfully!" }
```

**Possible errors:**
- `400` — Email already registered
- `400` — Username already taken
- `422` — Validation error (e.g. password too short, invalid email)

---

### POST /login
Log in and receive a JWT access token.

> ⚠️ This endpoint expects **form data** (not JSON) because it uses the OAuth2 standard.
> Use the `/docs` UI or send `Content-Type: application/x-www-form-urlencoded`.

**Form Fields:**
```
username = prashant@example.com
password = securepass123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Possible errors:**
- `401` — Invalid email or password

---

### GET /profile 🔒 Protected
Returns the profile of the currently logged-in user.

**Headers:**
```
Authorization: Bearer <your_access_token>
```

**Response:**
```json
{
  "email": "prashant@example.com",
  "username": "prashant"
}
```

**Possible errors:**
- `401` — Token missing, invalid, or expired

---

## 📍 API Docs

Once the server is running, FastAPI auto-generates interactive docs:

* **Swagger UI:** http://127.0.0.1:8000/docs
* **ReDoc:** http://127.0.0.1:8000/redoc

To test protected routes in Swagger UI:
1. Call `POST /login` and copy the `access_token` from the response
2. Click the **Authorize 🔒** button at the top of the page
3. Enter your email as username and password, then click Authorize
4. All protected endpoints will now include your token automatically

---

## 🗂️ Project Structure

```
backend/
├── main.py        # API routes (entry point)
├── models.py      # Database table definitions (SQLAlchemy)
├── schemas.py     # Request/response shape validation (Pydantic)
├── crud.py        # Database operations (create, read, etc.)
├── auth.py        # JWT token creation and validation
├── hashing.py     # Password hashing and verification (bcrypt direct)
├── database.py    # DB connection and session setup
├── __init__.py    # Makes backend a Python package
└── test.db        # Auto-generated SQLite database file
```

---

## 🔒 Security Notes

* Passwords are **never stored in plain text** — bcrypt hashes them before saving
* bcrypt is used directly (no passlib wrapper) — passlib is abandoned and broken with bcrypt 4.x+
* Password length is validated to 8–72 bytes — bcrypt has a hard 72-byte limit
* JWT tokens expire after **15 minutes**
* The secret key is loaded from an **environment variable**, not hardcoded
* Login errors return the same message whether the email or password is wrong — prevents attackers from enumerating registered emails
* All inputs are validated by Pydantic before touching the database

---

## 💡 Lessons Learned

* `passlib` is abandoned — use `bcrypt` directly in new projects
* Relative imports (`from . import`) require the folder to be a proper Python package with `__init__.py`
* `Base.metadata.create_all()` only creates missing tables — it won't update existing ones if you add columns (delete `test.db` in dev, use Alembic migrations in production)
* bcrypt counts **bytes** not characters — a password with special characters can exceed 72 bytes even under 72 characters
* JWT tokens can't be invalidated before expiry without a server-side blocklist — keep expiry short (15 min)
* Swagger's "Logout" button only clears the token from the browser — it doesn't invalidate the token on the server

---

## 🎯 Goal

To build a production-ready authentication system while understanding:

* How authentication works internally
* Security best practices (hashing, JWT, input validation)
* Clean backend architecture (separation of concerns)

---

## 🧠 Learning Approach

Built step-by-step (day by day) instead of copying tutorials — focusing on real understanding, reading docs, and hands-on debugging.

---

## ✍️ Author

**Prashant Maurya**