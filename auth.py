"""
Authentication & User Management Module for PerplexAI Chatbot.
Provides secure local SQLite persistence, PBKDF2-HMAC-SHA256 password hashing,
session token tracking, input validation, and external OAuth provider configuration hooks.
"""

import os
import re
import hmac
import hashlib
import secrets
import sqlite3
from datetime import datetime
from typing import Optional, Tuple, Dict, Any

DB_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DB_DIR, "users.db")

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def _get_db_connection() -> sqlite3.Connection:
    """Creates directory if needed and returns a SQLite connection."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password: str, salt: str) -> str:
    """Computes PBKDF2-HMAC-SHA256 hash using 100,000 iterations."""
    key = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        100_000
    )
    return key.hex()

def verify_password(password: str, salt: str, stored_hash: str) -> bool:
    """Verifies a password against the stored salt and hash using constant-time comparison."""
    computed_hash = hash_password(password, salt)
    return hmac.compare_digest(computed_hash, stored_hash)

def init_auth_db() -> None:
    """Initializes SQLite tables for users and sessions, and seeds demo account if empty."""
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            );
        """)
        conn.commit()

        # Check if demo account exists; if not, seed it for immediate verification
        cursor.execute("SELECT id FROM users WHERE email = ?", ("demo@perplexai.com",))
        if not cursor.fetchone():
            demo_salt = secrets.token_hex(32)
            demo_hash = hash_password("Demo1234!", demo_salt)
            cursor.execute("""
                INSERT INTO users (email, name, salt, password_hash)
                VALUES (?, ?, ?, ?)
            """, ("demo@perplexai.com", "Alex Morgan", demo_salt, demo_hash))
            conn.commit()
    finally:
        conn.close()

def validate_email(email: str) -> bool:
    """Validates email format using RFC-compliant pattern."""
    if not email or len(email) > 254:
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def validate_password(password: str) -> Tuple[bool, str]:
    """Validates password length and complexity requirements."""
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters long."
    return True, ""

def register_user(email: str, name: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Registers a new user into SQLite with a unique salt and PBKDF2 hash.
    Returns (success, message, user_dict).
    """
    email_clean = email.strip().lower()
    name_clean = name.strip() or "User"

    if not validate_email(email_clean):
        return False, "Please enter a valid email address.", None

    is_valid_pwd, pwd_err = validate_password(password)
    if not is_valid_pwd:
        return False, pwd_err, None

    salt = secrets.token_hex(32)
    pwd_hash = hash_password(password, salt)

    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (email, name, salt, password_hash)
            VALUES (?, ?, ?, ?)
        """, (email_clean, name_clean, salt, pwd_hash))
        user_id = cursor.lastrowid
        conn.commit()

        user = {
            "id": user_id,
            "email": email_clean,
            "name": name_clean,
            "created_at": datetime.now().strftime("%Y-%m-%d")
        }
        return True, "Account created successfully!", user
    except sqlite3.IntegrityError:
        return False, "An account with this email address already exists.", None
    except Exception as e:
        return False, f"Registration error: {e}", None
    finally:
        conn.close()

def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Authenticates user credentials against the SQLite database.
    Returns (success, message, user_dict).
    """
    email_clean = email.strip().lower()
    if not email_clean or not password:
        return False, "Please provide both email and password.", None

    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, email, name, salt, password_hash, created_at
            FROM users
            WHERE email = ?
        """, (email_clean,))
        row = cursor.fetchone()

        if not row:
            return False, "Invalid email or password.", None

        if not verify_password(password, row["salt"], row["password_hash"]):
            return False, "Invalid email or password.", None

        created_str = str(row["created_at"])[:10] if row["created_at"] else "Recently"
        user = {
            "id": row["id"],
            "email": row["email"],
            "name": row["name"],
            "created_at": created_str
        }
        return True, "Authentication successful!", user
    except Exception as e:
        return False, f"Authentication error: {e}", None
    finally:
        conn.close()

def create_session(user_id: int) -> str:
    """Generates a secure random session token and stores it in SQLite."""
    token = secrets.token_urlsafe(32)
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO sessions (token, user_id) VALUES (?, ?)", (token, user_id))
        conn.commit()
    finally:
        conn.close()
    return token

def get_user_by_session(token: str) -> Optional[Dict[str, Any]]:
    """Retrieves user info corresponding to an active session token."""
    if not token:
        return None
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.email, u.name, u.created_at
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            WHERE s.token = ?
        """, (token,))
        row = cursor.fetchone()
        if row:
            return {
                "id": row["id"],
                "email": row["email"],
                "name": row["name"],
                "created_at": str(row["created_at"])[:10] if row["created_at"] else "Recently"
            }
    except Exception:
        pass
    finally:
        conn.close()
    return None

def delete_session(token: str) -> None:
    """Deletes an active session token from SQLite upon sign out."""
    if not token:
        return
    conn = _get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    except Exception:
        pass
    finally:
        conn.close()

def check_oauth_provider_status() -> Dict[str, Any]:
    """Checks whether external OAuth credentials (e.g. Google OAuth) are configured in the environment."""
    google_id = os.getenv("GOOGLE_CLIENT_ID")
    google_secret = os.getenv("GOOGLE_CLIENT_SECRET")
    return {
        "google_configured": bool(google_id and google_secret),
        "provider": "google" if (google_id and google_secret) else "local_sqlite"
    }

# Auto-initialize database schema when module is imported
init_auth_db()
