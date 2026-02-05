import json

from cryptography.fernet import Fernet

from app.core.config import settings


def get_fernet() -> Fernet:
    return Fernet(settings.ENCRYPTION_KEY.encode())


def encrypt_credentials(credentials: dict) -> str:
    """Encrypt credentials dict to a string for storage."""
    fernet = get_fernet()
    json_bytes = json.dumps(credentials).encode()
    return fernet.encrypt(json_bytes).decode()


def decrypt_credentials(encrypted: str) -> dict:
    """Decrypt credentials string back to a dict."""
    fernet = get_fernet()
    decrypted_bytes = fernet.decrypt(encrypted.encode())
    return json.loads(decrypted_bytes.decode())
