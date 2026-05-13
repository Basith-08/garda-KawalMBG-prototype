from typing import Any, Dict, Optional

import models
from risk_assessment import normalize_distribution_record
from utils.dates import serialize_datetime


def get_vendor_school_index(db: Any) -> Dict[str, list[str]]:
    vendor_schools: Dict[str, list[str]] = {}
    for school in db.query(models.School).all():
        vendor_schools.setdefault(school.vendorId, []).append(school.name)
    return vendor_schools


def is_platform_operator(user: models.User) -> bool:
    return user.role in {"regulator", "super-admin"}


def serialize_user(user: models.User) -> Dict[str, Any]:
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


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _average(values: list[float], default: float) -> float:
    return sum(values) / len(values) if values else default


def build_vendor_trust_profile(
    vendor: models.Vendor,
    distributions: list[models.Distribution],
    alerts: list[models.Alert],
) -> Dict[str, Any]:
    if not distributions:
        base_score = int(round(vendor.trustScore or 0))
        return {
            "trustScore": base_score,
            "status": vendor.status,
            "statusText": vendor.statusText,
            "trustBreakdown": {
                "timeliness": base_score,
                "evidence": base_score,
                "schoolReceipt": base_score,
                "portionConsistency": base_score,
                "history": base_score,
            },
        }

    timeliness_values = [
        100
        if (distribution.durasi or 0) <= 45
        else 60
        if (distribution.durasi or 0) <= 60
        else 30
        for distribution in distributions
    ]

    evidence_values: list[float] = []
    receipt_values: list[float] = []
    portion_values: list[float] = []

    for distribution in distributions:
        has_operational_fields = bool(
            distribution.cookedAt
            or distribution.packagedAt
            or distribution.pickupAt
            or distribution.deliveredAt
            or distribution.arrivalStatus
            or distribution.evidenceUploaded
            or distribution.qcPhotoUploaded
            or distribution.productionPhotoUploaded
            or distribution.packagingPhotoUploaded
            or distribution.vehiclePhotoUploaded
        )

        if has_operational_fields:
            evidence_count = sum(
                bool(value)
                for value in (
                    distribution.qcPhotoUploaded,
                    distribution.productionPhotoUploaded,
                    distribution.packagingPhotoUploaded,
                    distribution.vehiclePhotoUploaded,
                )
            )
            evidence_values.append(evidence_count * 25)
        else:
            evidence_values.append(60)

        if distribution.arrivalStatus == "received_ok":
            receipt_values.append(100)
        elif distribution.arrivalStatus in {"received_with_issue", "not_received"}:
            receipt_values.append(0)
        elif distribution.arrivalStatus == "not_confirmed":
            receipt_values.append(50)
        else:
            receipt_values.append(60)

        portion_values.append(100 if (distribution.porsi or 0) > 0 else 0)

    critical_alerts = len([alert for alert in alerts if alert.type == "CRITICAL"])
    fraud_alerts = len([alert for alert in alerts if alert.type == "FRAUD"])
    history_score = _clamp(100 - critical_alerts * 12 - fraud_alerts * 18, 0, 100)

    breakdown = {
        "timeliness": round(_average(timeliness_values, 60)),
        "evidence": round(_average(evidence_values, 60)),
        "schoolReceipt": round(_average(receipt_values, 60)),
        "portionConsistency": round(_average(portion_values, 100)),
        "history": round(history_score),
    }
    trust_score = int(
        round(
            breakdown["timeliness"] * 0.30
            + breakdown["evidence"] * 0.25
            + breakdown["schoolReceipt"] * 0.25
            + breakdown["portionConsistency"] * 0.10
            + breakdown["history"] * 0.10
        )
    )
    status = "safe" if trust_score >= 80 else "medium" if trust_score >= 60 else "high-risk"
    status_text = {
        "safe": "Operational Trust Stable",
        "medium": "Operational Monitoring",
        "high-risk": "Intervention Priority",
    }[status]

    return {
        "trustScore": trust_score,
        "status": status,
        "statusText": status_text,
        "trustBreakdown": breakdown,
    }


def serialize_vendor(
    vendor: models.Vendor,
    school_names: Optional[list[str]] = None,
    trust_profile: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    profile = trust_profile or {
        "trustScore": vendor.trustScore,
        "status": vendor.status,
        "statusText": vendor.statusText,
        "trustBreakdown": None,
    }
    return {
        "id": vendor.id,
        "name": vendor.name,
        "status": profile["status"],
        "statusText": profile["statusText"],
        "trustScore": profile["trustScore"],
        "trustBreakdown": profile["trustBreakdown"],
        "trend": vendor.trend,
        "trendDir": vendor.trendDir,
        "address": vendor.address,
        "joinDate": vendor.joinDate,
        "schools": school_names if school_names is not None else (vendor.schools or []),
    }


def serialize_school(school: models.School) -> Dict[str, Any]:
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


def serialize_distribution(
    distribution: models.Distribution,
    vendor: Optional[models.Vendor] = None,
    trust_profile: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
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
            "cookedAt": distribution.cookedAt,
            "packagedAt": distribution.packagedAt,
            "pickupAt": distribution.pickupAt,
            "deliveredAt": distribution.deliveredAt,
            "arrivalStatus": distribution.arrivalStatus,
            "receiptIssueType": distribution.receiptIssueType,
            "receiptEvidenceUploaded": distribution.receiptEvidenceUploaded,
            "receiptNote": distribution.receiptNote,
            "receiptVerifiedAt": serialize_datetime(distribution.receiptVerifiedAt),
            "qcPhotoUploaded": distribution.qcPhotoUploaded,
            "productionPhotoUploaded": distribution.productionPhotoUploaded,
            "packagingPhotoUploaded": distribution.packagingPhotoUploaded,
            "vehiclePhotoUploaded": distribution.vehiclePhotoUploaded,
            "evidenceUploaded": distribution.evidenceUploaded,
            "vendorTrustScore": trust_profile["trustScore"] if trust_profile else (vendor.trustScore if vendor else None),
            "vendorStatusText": trust_profile["statusText"] if trust_profile else (vendor.statusText if vendor else None),
        }
    )


def persist_normalized_distribution(
    db: Any,
    distribution: models.Distribution,
    distribution_fields: set[str],
    vendor: Optional[models.Vendor] = None,
) -> Dict[str, Any]:
    normalized = serialize_distribution(distribution, vendor)
    for key in distribution_fields:
        if key in normalized and hasattr(distribution, key):
            setattr(distribution, key, normalized[key])
    db.add(distribution)
    return normalized


def _serialize_alert(alert: models.Alert) -> Dict[str, Any]:
    return {
        "id": alert.id,
        "type": alert.type,
        "vendorId": alert.vendorId,
        "vendorName": alert.vendorName,
        "description": alert.description,
        "time": alert.time,
        "statusTag": alert.statusTag,
    }


def _serialize_document(document: models.Document) -> Dict[str, Any]:
    return {
        "id": document.id,
        "vendorId": document.vendorId,
        "name": document.name,
        "expiry": document.expiry,
        "status": document.status,
    }


def serialize_private_data(db: Any) -> Dict[str, Any]:
    vendor_school_index = get_vendor_school_index(db)
    vendor_lookup = {vendor.id: vendor for vendor in db.query(models.Vendor).all()}
    distributions = db.query(models.Distribution).all()
    alerts = db.query(models.Alert).all()
    distributions_by_vendor: Dict[str, list[models.Distribution]] = {}
    alerts_by_vendor: Dict[str, list[models.Alert]] = {}
    for distribution in distributions:
        distributions_by_vendor.setdefault(distribution.vendorId, []).append(distribution)
    for alert in alerts:
        if alert.vendorId:
            alerts_by_vendor.setdefault(alert.vendorId, []).append(alert)
    trust_profiles = {
        vendor.id: build_vendor_trust_profile(
            vendor,
            distributions_by_vendor.get(vendor.id, []),
            alerts_by_vendor.get(vendor.id, []),
        )
        for vendor in vendor_lookup.values()
    }
    return {
        "vendors": [
            serialize_vendor(vendor, vendor_school_index.get(vendor.id, vendor.schools or []), trust_profiles.get(vendor.id))
            for vendor in vendor_lookup.values()
        ],
        "schools": [serialize_school(school) for school in db.query(models.School).all()],
        "distributions": [
            serialize_distribution(distribution, vendor_lookup.get(distribution.vendorId), trust_profiles.get(distribution.vendorId))
            for distribution in distributions
        ],
        "alerts": [_serialize_alert(alert) for alert in alerts],
        "documents": [_serialize_document(document) for document in db.query(models.Document).all()],
    }


def serialize_private_data_for_user(db: Any, user: models.User) -> Dict[str, Any]:
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
    distributions = db.query(models.Distribution).filter(models.Distribution.vendorId == vendor_id).all()
    alerts = db.query(models.Alert).filter(models.Alert.vendorId == vendor_id).all()
    trust_profile = build_vendor_trust_profile(vendor, distributions, alerts) if vendor else None
    vendor_school_index = get_vendor_school_index(db)

    return {
        "vendors": [
            serialize_vendor(vendor, vendor_school_index.get(vendor_id, vendor.schools or []), trust_profile)
        ]
        if vendor
        else [],
        "schools": [
            serialize_school(school)
            for school in db.query(models.School).filter(models.School.vendorId == vendor_id).all()
        ],
        "distributions": [serialize_distribution(distribution, vendor, trust_profile) for distribution in distributions],
        "alerts": [_serialize_alert(alert) for alert in alerts],
        "documents": [
            _serialize_document(document)
            for document in db.query(models.Document).filter(models.Document.vendorId == vendor_id).all()
        ],
    }


def serialize_public_data(db: Any) -> Dict[str, Any]:
    vendor_school_index = get_vendor_school_index(db)
    distributions = db.query(models.Distribution).all()
    alerts = db.query(models.Alert).all()
    distributions_by_vendor: Dict[str, list[models.Distribution]] = {}
    alerts_by_vendor: Dict[str, list[models.Alert]] = {}
    for distribution in distributions:
        distributions_by_vendor.setdefault(distribution.vendorId, []).append(distribution)
    for alert in alerts:
        if alert.vendorId:
            alerts_by_vendor.setdefault(alert.vendorId, []).append(alert)
    return {
        "vendors": [
            serialize_vendor(
                vendor,
                vendor_school_index.get(vendor.id, vendor.schools or []),
                build_vendor_trust_profile(
                    vendor,
                    distributions_by_vendor.get(vendor.id, []),
                    alerts_by_vendor.get(vendor.id, []),
                ),
            )
            for vendor in db.query(models.Vendor).all()
        ],
        "schools": [serialize_school(school) for school in db.query(models.School).all()],
        "distributions": [],
        "alerts": [],
        "documents": [],
    }
