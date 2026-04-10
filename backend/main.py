# main.py
# This is the entry point of your FastAPI application.
# It defines all the API routes (endpoints) and wires everything together.

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import models, schemas, crud
from database import Base, engine, get_db
from auth import create_access_token, get_current_user
app = FastAPI()

# Create all tables defined in models.py if they don't exist yet.
# This runs once at startup — safe to call every time (it skips existing tables).
Base.metadata.create_all(bind=engine)


# ─────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────

@app.get("/")
def home():
    """Simple health check — confirms the server is running."""
    return {"message": "Server is running!"}


# ─────────────────────────────────────────────
# REGISTER
# ─────────────────────────────────────────────

@app.post("/signUp", status_code=201)  # 201 = "Created" (more correct than default 200)
def sign_up(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    Steps:
      1. Check if email is already taken → 400 if yes
      2. Check if username is already taken → 400 if yes  (FIX: this was missing)
      3. Create and store the user with a hashed password
      4. Return success message
    """
    # Check if email is already registered
    if crud.get_user_by_email(db, email=user.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # FIX: Also check if username is taken.
    # Without this, a duplicate username would cause an unhandled DB crash (IntegrityError).
    if crud.get_user_by_username(db, username=user.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    crud.create_user(db, user)
    return {"message": "User created successfully!"}


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────

@app.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),  # reads username + password from form body
    db: Session = Depends(get_db)
):
    """
    Log in and receive an access token.
    
    OAuth2PasswordRequestForm expects:
      - username (we treat this as the email)
      - password
    sent as form data (not JSON).
    
    Returns a JWT access token on success.
    
    FIX: Changed status_code from 400 → 401 for failed login.
    401 = "Unauthorized" which is semantically correct for wrong credentials.
    400 = "Bad Request" which means malformed input — not the same thing.
    """
    # authenticate_user checks if email exists AND password matches
    db_user = crud.authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        # Same error message for both "email not found" and "wrong password"
        # — never reveal which one failed (it would help attackers enumerate accounts)
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Build the JWT payload — "sub" (subject) is a standard JWT field for the user identifier
    access_token = create_access_token(
        data={"sub": db_user.email, "username": db_user.username}
    )

    return {"access_token": access_token, "token_type": "bearer"}


# ─────────────────────────────────────────────
# PROFILE (protected route)
# ─────────────────────────────────────────────

@app.get("/profile", response_model=schemas.UserProfile)
def profile(current_user=Depends(get_current_user)):
    """
    Returns the profile of the currently logged-in user.
    
    Depends(get_current_user) automatically:
      1. Reads the "Authorization: Bearer <token>" header
      2. Validates the token
      3. Looks up the user in DB
      4. Injects the user object here as current_user
    
    If the token is missing or invalid, get_current_user raises 401 before this runs.
    
    FIX: Changed Security(get_current_user) → Depends(get_current_user).
    Security() is for OAuth scopes — Depends() is correct for simple token auth.
    """
    return current_user