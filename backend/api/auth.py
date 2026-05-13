from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_current_user
from database import get_db
import models
from schemas.requests import LoginRequest
from services.auth import login_user
from services.serialization import serialize_user


router = APIRouter()


@router.post("/api/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, req.email, req.password)


@router.get("/api/auth/session")
def auth_session(current_user: models.User = Depends(get_current_user)):
    return serialize_user(current_user)
