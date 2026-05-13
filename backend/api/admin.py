from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_role
from database import get_db
import models
from schemas.requests import AdminUserUpdateRequest
from services.admin import build_admin_overview, update_admin_user_access


router = APIRouter()


@router.get("/api/admin/overview")
def get_admin_overview(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_role(current_user, "super-admin")
    return build_admin_overview(db)


@router.patch("/api/admin/users/{user_id}")
def update_admin_user(
    user_id: str,
    payload: AdminUserUpdateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_role(current_user, "super-admin")
    return update_admin_user_access(db, current_user, user_id, payload)
