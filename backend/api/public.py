from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from services.serialization import serialize_public_data


router = APIRouter()


@router.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    counts = {
        "vendors": db.query(models.Vendor).count(),
        "schools": db.query(models.School).count(),
        "distributions": db.query(models.Distribution).count(),
        "riskScores": db.query(models.RiskScoreHistory).count(),
        "alerts": db.query(models.Alert).count(),
        "auditLogs": db.query(models.AuditLog).count(),
        "documents": db.query(models.Document).count(),
        "users": db.query(models.User).count(),
    }
    return {
        "status": "ok",
        "database": "connected",
        "seeded": counts["users"] > 0,
        "counts": counts,
    }


@router.get("/api/public-data")
def get_public_data(db: Session = Depends(get_db)):
    return serialize_public_data(db)
