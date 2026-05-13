from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user, require_role
from database import get_db
import models
from services.regulator import build_regulator_overview


router = APIRouter()


@router.get("/api/regulator/overview")
def get_regulator_overview(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_role(current_user, "regulator", "super-admin")
    return build_regulator_overview(db)
