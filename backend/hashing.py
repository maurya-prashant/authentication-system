# hashing.py
import bcrypt

def hash_password(password: str) -> str:
    """
    Takes a plain text password and returns a secure hash.
    Example: "mypassword123" → "$2b$12$eImiTXuWVxfM37uY4JANj..."
    The hash is different every time (bcrypt adds a random salt internally).
    """
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")  # store as string in DB


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Checks whether a plain text password matches a stored hash.
    Returns True if they match, False otherwise.
    """
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8")
    )