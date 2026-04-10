# crud.py
# CRUD = Create, Read, Update, Delete
# This file contains all the database operations.
# Routes call these functions — keeping DB logic here and route logic in main.py keeps code clean.

from sqlalchemy.orm import Session
import models, schemas
from hashing import hash_password, verify_password


def get_user_by_email(db: Session, email: str):
    """
    Looks up a user by their email address.
    Returns the User object if found, or None if no user has that email.
    """
    return db.query(models.User).filter(models.User.email == email).first()


# FIX ADDED: Also check for duplicate usernames.
# Your original code only checked for duplicate emails in main.py,
# but the username column is also unique — trying to insert a duplicate
# username would crash with an unhandled DB integrity error.
def get_user_by_username(db: Session, username: str):
    """
    Looks up a user by their username.
    Returns the User object if found, or None if username is available.
    """
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user record in the database.
    Steps:
      1. Hash the plain text password
      2. Build a User model object
      3. Add it to the session (staged, not saved yet)
      4. Commit (save to DB)
      5. Refresh (reload the object from DB to get the auto-generated ID)
      6. Return the saved user
    """
    hashed_pwd = hash_password(user.password)  # NEVER store plain text

    db_user = models.User(
        email=user.email,
        password=hashed_pwd,
        username=user.username,
        # is_verified defaults to False — user must verify their email
    )

    db.add(db_user)      # stage the new user (not saved yet)
    db.commit()          # write to database
    db.refresh(db_user)  # reload from DB so db_user.id is populated
    return db_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Verifies a user's credentials during login.
    Returns the User object if email exists AND password matches.
    Returns None if either check fails.

    IMPORTANT: We return the same None for both "email not found" and "wrong password".
    This is intentional — never tell an attacker which one failed (it leaks info).
    """
    user = get_user_by_email(db, email)

    if not user:
        return None  # email not found — but we don't say that to the client
    
    if len(password.encode("utf-8")) > 72:
        return None

    if not verify_password(password, user.password):
        return None  # password wrong — same generic response

    return user  # both checks passed — login successful