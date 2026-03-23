"""
Encryption service for storing sensitive credentials (API keys, passwords).
Uses Fernet symmetric encryption.
"""

from cryptography.fernet import Fernet

from app.config import settings


def _get_fernet() -> Fernet:
    """Get Fernet instance from secret key. Pads/hashes to 32 bytes."""
    import hashlib
    import base64
    key = hashlib.sha256(settings.secret_key.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def encrypt(plaintext: str) -> str:
    """Encrypt a string and return the encrypted token."""
    if not plaintext:
        return ""
    f = _get_fernet()
    return f.encrypt(plaintext.encode()).decode()


def decrypt(token: str) -> str:
    """Decrypt an encrypted token back to plaintext."""
    if not token:
        return ""
    f = _get_fernet()
    return f.decrypt(token.encode()).decode()
