from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import HTTPException

import models
from services.history import record_audit_event
from services.serialization import get_vendor_school_index, serialize_user
from utils.dates import parse_indonesian_date


def build_admin_overview(db: Any) -> Dict[str, Any]:
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


def update_admin_user_access(
    db: Any,
    current_user: models.User,
    user_id: str,
    payload: Any,
) -> Dict[str, Any]:
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
    record_audit_event(
        db,
        action="admin.user_access.update",
        entity_type="user",
        entity_id=user.id,
        actor_user_id=current_user.id,
        details={
            "role": user.role,
            "vendorId": user.vendorId,
            "isActive": user.isActive,
        },
    )
    db.commit()
    db.refresh(user)
    return serialize_user(user)
