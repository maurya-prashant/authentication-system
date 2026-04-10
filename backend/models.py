# models.py
# This file defines your database TABLES using Python classes.
# SQLAlchemy will convert these classes into actual SQL table definitions.

from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    # The actual table name in the database
    __tablename__ = "users"

    # INTEGER column, primary key (unique ID auto-incremented for each user),
    # index=True makes lookups by ID faster.
    id = Column(Integer, primary_key=True, index=True)

    # STRING column, must be unique (no two users share an email),
    # index=True speeds up queries like "find user by email".
    email = Column(String, unique=True, index=True, nullable=False)

    # Stores the HASHED password — never the plain text password.
    password = Column(String, nullable=False)

    # Username must also be unique across all users.
    username = Column(String, unique=True, index=True, nullable=False)

    # FIX ADDED: Track whether the user has verified their email.
    # Unverified users can be blocked from sensitive actions.
    # Default is False — user must click the verification link to become True.
    is_verified = Column(Boolean, default=False)