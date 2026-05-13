from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import HTTPException

import models
from auth_utils import verify_password
from services.history import record_audit_event
from services.serialization import serialize_user
from token_utils import create_access_token


def login_user(db: Any, email: str, password: str) -> Dict[str, Any]:
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    if not user.isActive:
        raise HTTPException(status_code=403, detail="User inactive")

    user.lastLoginAt = datetime.now(timezone.utc)
    db.add(user)
    record_audit_event(
        db,
        action="auth.login.success",
        entity_type="user",
        entity_id=user.id,
        actor_user_id=user.id,
        details={"role": user.role, "vendorId": user.vendorId},
    )
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email, "vendorId": user.vendorId})
    return {
        "token": token,
        "user": serialize_user(user),
    }
