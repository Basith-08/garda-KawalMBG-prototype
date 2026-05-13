from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_current_user
from constants import DISTRIBUTION_FIELDS
from database import get_db
import models
from services.runtime_data import save_runtime_data
from services.serialization import serialize_private_data_for_user


router = APIRouter()


@router.get("/api/data")
def get_data(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return serialize_private_data_for_user(db, current_user)


@router.post("/api/data")
def save_data(
    data: Dict[str, Any],
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return save_runtime_data(db, data, current_user, DISTRIBUTION_FIELDS)
    except Exception as exc:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(exc))
