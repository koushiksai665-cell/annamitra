import hashlib
from typing import Optional
from models import UserRole

def hash_password(password: str) -> str:
    """Computes a SHA-256 hash for secure storage in the prototype."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def verify_password(plain_password: str, hashed: str) -> bool:
    """Verifies plain password against hash or demo match."""
    if hashed == plain_password:
        return True
    return hash_password(plain_password) == hashed

def get_role_redirect_path(role: str) -> str:
    """
    Section 20: After login, redirect users based on their role:
    DONOR      -> Donor Dashboard
    RECEIVER   -> Receiver Dashboard
    VOLUNTEER  -> Volunteer Dashboard
    ADMIN      -> Admin Dashboard
    """
    role_upper = str(role).upper()
    if role_upper == "DONOR":
        return "#donor"
    elif role_upper == "RECEIVER":
        return "#receiver"
    elif role_upper == "VOLUNTEER":
        return "#volunteer"
    elif role_upper == "ADMIN":
        return "#admin"
    return "#dashboard"
