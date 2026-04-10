# schemas.py
# Schemas are Pydantic models — they define the SHAPE of data coming IN and going OUT of your API.
# Think of them as a strict form: if the data doesn't match, the request is rejected immediately
# before it even touches your database.

from pydantic import BaseModel, EmailStr, field_validator


# Schema for registering a new user.
# This is what the client must send in the request body for /signUp.
class UserCreate(BaseModel):
    email: EmailStr       # Pydantic validates this is a real email format (e.g. has @, domain, etc.)
    password: str
    username: str

    # FIX ADDED: Enforce a minimum password length.
    # Without this, someone could register with an empty string "" as their password.
    @field_validator("password")
    @classmethod
    def password_must_be_strong(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        if len(v.encode("utf-8")) > 72:      # ← bytes, not characters
            raise ValueError("Password must be under 72 bytes")
        return v


# Schema for logging in.
# Only email + password needed — no username required at login.
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema for the /profile response — what we send BACK to the client.
# Notice: password is NOT included here. Never expose the hashed password in API responses.
class UserProfile(BaseModel):
    email: EmailStr
    username: str

    # from_attributes = True allows Pydantic to read data from SQLAlchemy model objects
    # (which are not plain dicts). Without this, returning a User DB object would fail.
    class Config:
        from_attributes = True


# Schema for the token response returned after login.
class Token(BaseModel):
    access_token: str
    token_type: str   # will always be "bearer"