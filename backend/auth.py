# auth.py
# This file handles JWT token creation and validation.
# JWT = JSON Web Token — a compact, signed string that proves who the user is.
# Structure: header.payload.signature  (e.g. "eyJ...abc.eyJ...xyz.SflK...")

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import os

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────

# FIX: Secret key should come from an environment variable, NOT be hardcoded.
# A hardcoded key in source code is a critical security vulnerability —
# anyone with access to your repo can forge tokens.
# Set this in your environment: export SECRET_KEY="some-long-random-string"
# In production, generate with: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production")

# The algorithm used to sign the JWT.
# HS256 = HMAC + SHA-256 (symmetric — same key signs and verifies).
# For distributed systems, prefer RS256 (asymmetric), but HS256 is fine for single-server apps.
ALGORITHM = "HS256"

# How long the access token is valid.
# Keep this short (15–30 min) — if a token is stolen, it expires quickly.
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # FIX: reduced from 30 to 15 for better security

# This tells FastAPI where clients send their token (the /login endpoint).
# FastAPI uses this to auto-generate the "Authorize" button in the /docs UI.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ─────────────────────────────────────────────
# TOKEN CREATION
# ─────────────────────────────────────────────

def create_access_token(data: dict) -> str:
    """
    Creates a signed JWT token.
    
    'data' is the payload — info you want to embed in the token (like the user's email).
    We add an expiry time (exp) so the token stops working after ACCESS_TOKEN_EXPIRE_MINUTES.
    
    The token is signed with SECRET_KEY — any tampering with the payload invalidates the signature.
    """
    to_encode = data.copy()  # never mutate the original dict

    # FIX: Use timezone-aware UTC (datetime.utcnow() is deprecated in Python 3.12+)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # add expiry to the payload

    # jwt.encode() creates the final signed token string
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# ─────────────────────────────────────────────
# TOKEN VALIDATION (used to protect routes)
# ─────────────────────────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),  # extracts Bearer token from the Authorization header
    db: Session = Depends(get_db)         # gives us a DB session to look up the user
):
    """
    Decodes and validates the JWT, then returns the logged-in user object.
    
    Used as a dependency on protected routes:
        @app.get("/profile")
        def profile(current_user = Depends(get_current_user)):
            ...
    
    Flow:
      1. Extract the token from the "Authorization: Bearer <token>" header
      2. Decode and verify the signature using SECRET_KEY
      3. Extract the email ("sub") from the payload
      4. Look up the user in the database
      5. Return the user — or raise 401 if anything is wrong
    """
    try:
        # Decode the token — this also automatically checks if it's expired
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # "sub" (subject) is the standard JWT field for identifying the user
        email: str = payload.get("sub")

        if email is None:
            # Token is valid but has no "sub" — something is wrong
            raise HTTPException(status_code=401, detail="Invalid token")

        # Look up the actual user in the DB to make sure they still exist
        user = crud.get_user_by_email(db, email=email)

        if user is None:
            # Token was valid but the user account was deleted
            raise HTTPException(status_code=401, detail="Invalid token")

        return user  # this gets injected into the route as current_user

    except JWTError:
        # Covers: bad signature, expired token, malformed token
        raise HTTPException(status_code=401, detail="Invalid token")