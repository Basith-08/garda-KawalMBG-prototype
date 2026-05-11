import base64
import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional
from settings import get_settings


def _b64encode(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _b64decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding)


def create_access_token(payload: Dict[str, Any], expires_in: Optional[int] = None) -> str:
    settings = get_settings()
    token_payload = dict(payload)
    token_payload["exp"] = int(time.time()) + (expires_in or settings.auth_token_ttl_seconds)
    message = _b64encode(json.dumps(token_payload, separators=(",", ":"), sort_keys=True).encode("utf-8"))
    signature = _b64encode(
        hmac.new(settings.auth_token_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    )
    return f"{message}.{signature}"


def decode_access_token(token: str) -> Dict[str, Any]:
    settings = get_settings()
    try:
        message, signature = token.split(".", 1)
    except ValueError as exc:
        raise ValueError("Malformed token") from exc

    expected_signature = _b64encode(
        hmac.new(settings.auth_token_secret.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
    )
    if not hmac.compare_digest(signature, expected_signature):
        raise ValueError("Invalid token signature")

    try:
        payload = json.loads(_b64decode(message).decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Invalid token payload") from exc

    if int(payload.get("exp", 0)) <= int(time.time()):
        raise ValueError("Token expired")

    return payload
