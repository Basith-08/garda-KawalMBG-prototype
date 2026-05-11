from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from database import engine, get_db
import models
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from auth_utils import verify_password
from migrations import run_migrations
from risk_assessment import normalize_distribution_record
from seed import seed_database
from settings import get_settings, validate_runtime_settings
from token_utils import create_access_token, decode_access_token

# Create tables in the local PostgreSQL database
models.Base.metadata.create_all(bind=engine)
settings = get_settings()
validate_runtime_settings()

app = FastAPI(title="KawalMBG API with Local Supabase")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer(auto_error=False)

class LoginRequest(BaseModel):
    email: str
    password: str


class AdminUserUpdateRequest(BaseModel):
    role: Optional[str] = None
    vendorId: Optional[str] = None
    isActive: Optional[bool] = None


DISTRIBUTION_FIELDS = {
    "id",
    "vendorId",
    "schoolName",
    "porsi",
    "status",
    "statusText",
    "time",
    "riskScore",
    "menuName",
    "menuUtama",
    "suhu",
    "durasi",
    "levelRisiko",
    "catatan",
}


MONTH_MAP = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "mei": 5,
    "jun": 6,
    "jul": 7,
    "agu": 8,
    "sep": 9,
    "okt": 10,
    "nov": 11,
    "des": 12,
}


def serialize_datetime(value: Optional[datetime]):
    return value.isoformat() if value else None


def parse_indonesian_date(raw: str) -> Optional[datetime]:
    if not raw or raw == "-":
        return None
    parts = raw.strip().split()
    if len(parts) != 3:
        return None
    try:
        day = int(parts[0])
        month = MONTH_MAP.get(parts[1].lower()[:3])
        year = int(parts[2])
        if month is None:
            return None
        return datetime(year, month, day, tzinfo=timezone.utc)
    except ValueError:
        return None


def get_vendor_school_index(db: Session):
    vendor_schools: Dict[str, list[str]] = {}
    for school in db.query(models.School).all():
        vendor_schools.setdefault(school.vendorId, []).append(school.name)
    return vendor_schools


def is_platform_operator(user: models.User):
    return user.role in {"regulator", "super-admin"}


def serialize_user(user: models.User):
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "vendorId": user.vendorId,
        "isActive": user.isActive,
        "createdAt": serialize_datetime(user.createdAt),
        "lastLoginAt": serialize_datetime(user.lastLoginAt),
        "avatar": user.avatar,
    }


def serialize_vendor(vendor: models.Vendor, school_names: Optional[list[str]] = None):
    return {
        "id": vendor.id,
        "name": vendor.name,
        "status": vendor.status,
        "statusText": vendor.statusText,
        "trustScore": vendor.trustScore,
        "trend": vendor.trend,
        "trendDir": vendor.trendDir,
        "address": vendor.address,
        "joinDate": vendor.joinDate,
        "schools": school_names if school_names is not None else (vendor.schools or []),
    }


def serialize_school(school: models.School):
    return {
        "id": school.id,
        "name": school.name,
        "npsn": school.npsn,
        "address": school.address,
        "vendorId": school.vendorId,
        "vendorName": school.vendorName,
        "trustScore": school.trustScore,
        "status": school.status,
        "statusText": school.statusText,
    }


def serialize_distribution(distribution: models.Distribution):
    return normalize_distribution_record(
        {
            "id": distribution.id,
            "vendorId": distribution.vendorId,
            "schoolName": distribution.schoolName,
            "porsi": distribution.porsi,
            "status": distribution.status,
            "statusText": distribution.statusText,
            "time": distribution.time,
            "riskScore": distribution.riskScore,
            "menuName": distribution.menuName,
            "menuUtama": distribution.menuUtama,
            "suhu": distribution.suhu,
            "durasi": distribution.durasi,
            "levelRisiko": distribution.levelRisiko,
            "catatan": distribution.catatan,
        }
    )


def serialize_private_data(db: Session):
    vendor_school_index = get_vendor_school_index(db)
    return {
        "vendors": [
            serialize_vendor(v, vendor_school_index.get(v.id, v.schools or []))
            for v in db.query(models.Vendor).all()
        ],
        "schools": [serialize_school(s) for s in db.query(models.School).all()],
        "distributions": [serialize_distribution(d) for d in db.query(models.Distribution).all()],
        "alerts": [
            {
                "id": a.id,
                "type": a.type,
                "vendorId": a.vendorId,
                "vendorName": a.vendorName,
                "description": a.description,
                "time": a.time,
                "statusTag": a.statusTag,
            }
            for a in db.query(models.Alert).all()
        ],
        "documents": [
            {
                "id": d.id,
                "vendorId": d.vendorId,
                "name": d.name,
                "expiry": d.expiry,
                "status": d.status,
            }
            for d in db.query(models.Document).all()
        ],
    }


def serialize_private_data_for_user(db: Session, user: models.User):
    if is_platform_operator(user):
        return serialize_private_data(db)

    vendor_id = user.vendorId
    if not vendor_id:
        return {
            "vendors": [],
            "schools": [],
            "distributions": [],
            "alerts": [],
            "documents": [],
        }

    vendor = db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()

    return {
        "vendors": [serialize_vendor(vendor, get_vendor_school_index(db).get(vendor_id, vendor.schools or []))] if vendor else [],
        "schools": [
            serialize_school(s)
            for s in db.query(models.School).filter(models.School.vendorId == vendor_id).all()
        ],
        "distributions": [
            serialize_distribution(d)
            for d in db.query(models.Distribution).filter(models.Distribution.vendorId == vendor_id).all()
        ],
        "alerts": [
            {
                "id": a.id,
                "type": a.type,
                "vendorId": a.vendorId,
                "vendorName": a.vendorName,
                "description": a.description,
                "time": a.time,
                "statusTag": a.statusTag,
            }
            for a in (
                db.query(models.Alert).filter(models.Alert.vendorId == vendor_id).all()
                if vendor_id
                else []
            )
        ],
        "documents": [
            {
                "id": d.id,
                "vendorId": d.vendorId,
                "name": d.name,
                "expiry": d.expiry,
                "status": d.status,
            }
            for d in db.query(models.Document).filter(models.Document.vendorId == vendor_id).all()
        ],
    }


def serialize_public_data(db: Session):
    vendor_school_index = get_vendor_school_index(db)
    return {
        "vendors": [
            serialize_vendor(v, vendor_school_index.get(v.id, v.schools or []))
            for v in db.query(models.Vendor).all()
        ],
        "schools": [serialize_school(s) for s in db.query(models.School).all()],
        "distributions": [],
        "alerts": [],
        "documents": [],
    }


def require_role(user: models.User, *roles: str):
    if user.role not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")


def build_admin_overview(db: Session):
    vendors = db.query(models.Vendor).all()
    schools = db.query(models.School).all()
    distributions = db.query(models.Distribution).all()
    alerts = db.query(models.Alert).all()
    documents = db.query(models.Document).all()
    users = db.query(models.User).all()

    vendor_school_index = get_vendor_school_index(db)
    vendor_ids = {vendor.id for vendor in vendors}
    now = datetime.now(timezone.utc)

    expiring_documents = []
    for document in documents:
        expiry_date = parse_indonesian_date(document.expiry)
        days_left = None if expiry_date is None else (expiry_date - now).days
        if expiry_date and days_left <= 30:
            expiring_documents.append(
                {
                    "id": document.id,
                    "vendorId": document.vendorId,
                    "name": document.name,
                    "expiry": document.expiry,
                    "status": document.status,
                    "daysLeft": days_left,
                }
            )

    vendor_alert_counts: Dict[str, int] = {}
    for alert in alerts:
        if alert.vendorId:
            vendor_alert_counts[alert.vendorId] = vendor_alert_counts.get(alert.vendorId, 0) + 1

    vendor_document_counts: Dict[str, int] = {}
    for document in expiring_documents:
        vendor_document_counts[document["vendorId"]] = vendor_document_counts.get(document["vendorId"], 0) + 1

    vendor_distribution_counts: Dict[str, int] = {}
    for distribution in distributions:
        vendor_distribution_counts[distribution.vendorId] = vendor_distribution_counts.get(distribution.vendorId, 0) + 1

    vendor_attention = sorted(
        [
            {
                "id": vendor.id,
                "name": vendor.name,
                "status": vendor.status,
                "trustScore": vendor.trustScore,
                "schoolCount": len(vendor_school_index.get(vendor.id, [])),
                "distributionCount": vendor_distribution_counts.get(vendor.id, 0),
                "alertCount": vendor_alert_counts.get(vendor.id, 0),
                "expiringDocumentCount": vendor_document_counts.get(vendor.id, 0),
            }
            for vendor in vendors
        ],
        key=lambda item: (
            0 if item["status"] == "high-risk" else 1 if item["status"] == "medium" else 2,
            item["trustScore"],
        ),
    )[:8]

    data_quality = [
        {
            "code": "vendor_users_without_vendor_link",
            "severity": "high",
            "count": len([user for user in users if user.role == "vendor" and not user.vendorId]),
            "description": "Akun vendor tanpa relasi vendorId eksplisit.",
        },
        {
            "code": "schools_without_matching_vendor",
            "severity": "medium",
            "count": len([school for school in schools if school.vendorId not in vendor_ids]),
            "description": "Sekolah terhubung ke vendorId yang tidak ada di tabel vendors.",
        },
        {
            "code": "vendor_school_legacy_mismatch",
            "severity": "low",
            "count": len(
                [
                    vendor
                    for vendor in vendors
                    if sorted(vendor.schools or []) != sorted(vendor_school_index.get(vendor.id, []))
                ]
            ),
            "description": "Field legacy vendors.schools berbeda dari relasi schools yang dinormalisasi.",
        },
    ]

    user_rows = []
    vendor_lookup = {vendor.id: vendor.name for vendor in vendors}
    for user in sorted(users, key=lambda item: ((item.role != "super-admin"), item.name)):
        user_rows.append(
            {
                **serialize_user(user),
                "vendorName": vendor_lookup.get(user.vendorId) if user.vendorId else None,
            }
        )

    return {
        "platformMetrics": {
            "totalUsers": len(users),
            "activeUsers": len([user for user in users if user.isActive]),
            "superAdmins": len([user for user in users if user.role == "super-admin"]),
            "regulators": len([user for user in users if user.role == "regulator"]),
            "vendors": len(vendors),
            "schools": len(schools),
            "distributions": len(distributions),
            "highRiskDistributions": len([item for item in distributions if item.status == "high-risk"]),
            "alerts": len(alerts),
            "criticalAlerts": len([item for item in alerts if item.type == "CRITICAL"]),
            "expiringDocuments30d": len(expiring_documents),
        },
        "dataQuality": data_quality,
        "userAccess": user_rows,
        "availableVendors": [
            {
                "id": vendor.id,
                "name": vendor.name,
            }
            for vendor in sorted(vendors, key=lambda item: item.name)
        ],
        "vendorAttention": vendor_attention,
        "expiringDocuments": sorted(expiring_documents, key=lambda item: item["daysLeft"])[:8],
    }


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")

    try:
        payload = decode_access_token(credentials.credentials)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User session not found")

    return user


@app.on_event("startup")
def bootstrap_data():
    models.Base.metadata.create_all(bind=engine)
    run_migrations()
    seed_database(only_if_empty=True)


@app.get("/api/health")
def health_check(db: Session = Depends(get_db)):
    counts = {
        "vendors": db.query(models.Vendor).count(),
        "schools": db.query(models.School).count(),
        "distributions": db.query(models.Distribution).count(),
        "alerts": db.query(models.Alert).count(),
        "documents": db.query(models.Document).count(),
        "users": db.query(models.User).count(),
    }
    return {
        "status": "ok",
        "database": "connected",
        "seeded": counts["users"] > 0,
        "counts": counts,
    }

@app.get("/api/public-data")
def get_public_data(db: Session = Depends(get_db)):
    return serialize_public_data(db)


@app.get("/api/data")
def get_data(_current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return serialize_private_data_for_user(db, _current_user)

@app.post("/api/data")
def save_data(
    data: Dict[str, Any],
    _current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        is_regulator = is_platform_operator(_current_user)
        vendor_id = _current_user.vendorId

        if is_regulator and "vendors" in data:
            for v_data in data["vendors"]:
                db.merge(models.Vendor(**v_data))
        if is_regulator and "schools" in data:
            for s_data in data["schools"]:
                db.merge(models.School(**s_data))
        if "distributions" in data:
            for d_data in data["distributions"]:
                normalized_distribution = normalize_distribution_record(d_data)
                if not is_regulator and normalized_distribution.get("vendorId") != vendor_id:
                    continue
                persisted_distribution = {
                    key: normalized_distribution[key]
                    for key in DISTRIBUTION_FIELDS
                    if key in normalized_distribution
                }
                db.merge(models.Distribution(**persisted_distribution))
        if is_regulator and "alerts" in data:
            for a_data in data["alerts"]:
                if "vendorId" not in a_data and a_data.get("vendorName"):
                    vendor = db.query(models.Vendor).filter(models.Vendor.name == a_data["vendorName"]).first()
                    if vendor:
                        a_data = {**a_data, "vendorId": vendor.id}
                db.merge(models.Alert(**a_data))
        if "documents" in data:
            for doc_data in data["documents"]:
                if not is_regulator and doc_data.get("vendorId") != vendor_id:
                    continue
                db.merge(models.Document(**doc_data))
        db.commit()
        return serialize_private_data_for_user(db, _current_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/admin/overview")
def get_admin_overview(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    require_role(current_user, "super-admin")
    return build_admin_overview(db)


@app.patch("/api/admin/users/{user_id}")
def update_admin_user(
    user_id: str,
    payload: AdminUserUpdateRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_role(current_user, "super-admin")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    next_role = payload.role or user.role
    if next_role not in {"super-admin", "regulator", "vendor"}:
        raise HTTPException(status_code=400, detail="Invalid role")

    if user.id == current_user.id and payload.isActive is False:
        raise HTTPException(status_code=400, detail="Super admin tidak dapat menonaktifkan akun sendiri")

    if user.id == current_user.id and payload.role and payload.role != "super-admin":
        raise HTTPException(status_code=400, detail="Super admin tidak dapat menurunkan role akun sendiri")

    desired_vendor_id = payload.vendorId if payload.role is not None or payload.vendorId is not None else user.vendorId
    if next_role == "vendor":
        if not desired_vendor_id:
            raise HTTPException(status_code=400, detail="Vendor user harus terhubung ke vendor")
        vendor = db.query(models.Vendor).filter(models.Vendor.id == desired_vendor_id).first()
        if not vendor:
            raise HTTPException(status_code=400, detail="Vendor link tidak valid")
        user.vendorId = desired_vendor_id
    else:
        user.vendorId = None

    user.role = next_role
    if payload.isActive is not None:
        user.isActive = payload.isActive

    db.add(user)
    db.commit()
    db.refresh(user)
    return serialize_user(user)


@app.post("/api/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    if not verify_password(req.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    if not user.isActive:
        raise HTTPException(status_code=403, detail="User inactive")

    user.lastLoginAt = datetime.now(timezone.utc)
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token({"sub": user.id, "role": user.role, "email": user.email, "vendorId": user.vendorId})

    return {
        "token": token,
        "user": serialize_user(user),
    }


@app.get("/api/auth/session")
def auth_session(current_user: models.User = Depends(get_current_user)):
    return serialize_user(current_user)
