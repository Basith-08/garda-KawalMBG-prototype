from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from pydantic import BaseModel
from typing import Dict, Any, List

# Create tables in the Neon Database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="KawalMBG API with Neon DB")

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/api/data")
def get_data(db: Session = Depends(get_db)):
    vendors = [{"id": v.id, "name": v.name, "status": v.status, "statusText": v.statusText, "trustScore": v.trustScore, "trend": v.trend, "trendDir": v.trendDir, "address": v.address, "joinDate": v.joinDate, "schools": v.schools} for v in db.query(models.Vendor).all()]
    schools = [{"id": s.id, "name": s.name, "npsn": s.npsn, "address": s.address, "vendorId": s.vendorId, "vendorName": s.vendorName, "trustScore": s.trustScore, "status": s.status, "statusText": s.statusText} for s in db.query(models.School).all()]
    distributions = [{"id": d.id, "vendorId": d.vendorId, "schoolName": d.schoolName, "porsi": d.porsi, "status": d.status, "statusText": d.statusText, "time": d.time, "riskScore": d.riskScore, "menuName": d.menuName, "menuUtama": d.menuUtama, "suhu": d.suhu, "durasi": d.durasi, "levelRisiko": d.levelRisiko, "catatan": d.catatan} for d in db.query(models.Distribution).all()]
    alerts = [{"id": a.id, "type": a.type, "vendorName": a.vendorName, "description": a.description, "time": a.time, "statusTag": a.statusTag} for a in db.query(models.Alert).all()]
    documents = [{"id": d.id, "vendorId": d.vendorId, "name": d.name, "expiry": d.expiry, "status": d.status} for d in db.query(models.Document).all()]
    
    return {
        "vendors": vendors,
        "schools": schools,
        "distributions": distributions,
        "alerts": alerts,
        "documents": documents
    }

@app.post("/api/data")
def save_data(data: Dict[str, Any], db: Session = Depends(get_db)):
    try:
        if "vendors" in data:
            for v_data in data["vendors"]:
                db.merge(models.Vendor(**v_data))
        if "schools" in data:
            for s_data in data["schools"]:
                db.merge(models.School(**s_data))
        if "distributions" in data:
            for d_data in data["distributions"]:
                db.merge(models.Distribution(**d_data))
        if "alerts" in data:
            for a_data in data["alerts"]:
                db.merge(models.Alert(**a_data))
        if "documents" in data:
            for doc_data in data["documents"]:
                db.merge(models.Document(**doc_data))
        db.commit()
        return {"status": "success"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

from auth_utils import verify_password

@app.post("/api/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
        
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "avatar": user.avatar,
    }
