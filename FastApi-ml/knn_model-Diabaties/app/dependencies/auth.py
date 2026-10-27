import hashlib
import hmac
import os
import secrets
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from fastapi import HTTPException, Request, status


SESSION_COOKIE_NAME = "luminar_session"
SESSION_TTL_SECONDS = 8 * 60 * 60
PASSWORD_HASH_ITERATIONS = 310_000
AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "false").lower() == "true"
AUTH_DB_PATH = Path(
    os.getenv(
        "AUTH_DB_PATH",
        str(Path(__file__).resolve().parents[2] / "data" / "auth.sqlite3"),
    )
)


def _connect() -> sqlite3.Connection:
    AUTH_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(AUTH_DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY COLLATE NOCASE,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS sessions (
            token_hash TEXT PRIMARY KEY,
            username TEXT NOT NULL REFERENCES users(username) ON DELETE CASCADE,
            expires_at INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS sessions_expiry_idx ON sessions(expires_at);
        """
    )
    return connection


@contextmanager
def _database() -> Iterator[sqlite3.Connection]:
    connection = _connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialize_auth_store() -> None:
    with _database() as connection:
        connection.execute("DELETE FROM sessions WHERE expires_at <= ?", (int(time.time()),))


def _hash_password(password: str, salt: bytes) -> str:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        PASSWORD_HASH_ITERATIONS,
    ).hex()


def create_user(username: str, password: str) -> None:
    canonical_username = username.strip().lower()
    salt = secrets.token_bytes(16)
    password_hash = _hash_password(password, salt)
    try:
        with _database() as connection:
            connection.execute(
                "INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)",
                (canonical_username, password_hash, salt.hex()),
            )
    except sqlite3.IntegrityError as exc:
        raise ValueError("Username is already registered") from exc


def verify_credentials(username: str, password: str) -> str | None:
    canonical_username = username.strip().lower()
    with _database() as connection:
        user = connection.execute(
            "SELECT username, password_hash, password_salt FROM users WHERE username = ?",
            (canonical_username,),
        ).fetchone()

    salt = bytes.fromhex(user["password_salt"]) if user else bytes(16)
    expected_hash = user["password_hash"] if user else "0" * 64
    password_matches = hmac.compare_digest(_hash_password(password, salt), expected_hash)
    if user is None or not password_matches:
        return None
    return user["username"]


def create_session(username: str) -> str:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    expires_at = int(time.time()) + SESSION_TTL_SECONDS
    with _database() as connection:
        connection.execute(
            "INSERT INTO sessions (token_hash, username, expires_at) VALUES (?, ?, ?)",
            (token_hash, username, expires_at),
        )
    return token


def revoke_session(token: str) -> None:
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with _database() as connection:
        connection.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))


def get_current_user(request: Request) -> str:
    token = request.cookies.get(SESSION_COOKIE_NAME)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with _database() as connection:
        session = connection.execute(
            """
            SELECT users.username
            FROM sessions
            JOIN users ON users.username = sessions.username
            WHERE sessions.token_hash = ? AND sessions.expires_at > ?
            """,
            (token_hash, int(time.time())),
        ).fetchone()
        connection.execute(
            "DELETE FROM sessions WHERE token_hash = ? AND expires_at <= ?",
            (token_hash, int(time.time())),
        )

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        )
    return session["username"]
