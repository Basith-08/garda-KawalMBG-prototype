from typing import Any, Dict

from risk_assessment import normalize_distribution_record

import models
from services.history import record_audit_event, record_risk_snapshot
from services.serialization import is_platform_operator, serialize_private_data_for_user


def save_runtime_data(
    db: Any,
    data: Dict[str, Any],
    current_user: models.User,
    distribution_fields: set[str],
) -> Dict[str, Any]:
    is_regulator = is_platform_operator(current_user)
    vendor_id = current_user.vendorId

    if is_regulator and "vendors" in data:
        for vendor_data in data["vendors"]:
            db.merge(models.Vendor(**vendor_data))

    if is_regulator and "schools" in data:
        for school_data in data["schools"]:
            db.merge(models.School(**school_data))

    if "distributions" in data:
        for distribution_data in data["distributions"]:
            normalized_distribution = normalize_distribution_record(distribution_data)
            if not is_regulator and normalized_distribution.get("vendorId") != vendor_id:
                continue

            persisted_distribution = {
                key: normalized_distribution[key]
                for key in distribution_fields
                if key in normalized_distribution
            }
            merged_distribution = db.merge(models.Distribution(**persisted_distribution))
            record_risk_snapshot(
                db,
                merged_distribution.id,
                merged_distribution.vendorId,
                normalized_distribution["assessment"],
            )
            record_audit_event(
                db,
                action="distribution.upsert",
                entity_type="distribution",
                entity_id=merged_distribution.id,
                actor_user_id=current_user.id,
                details={
                    "vendorId": merged_distribution.vendorId,
                    "riskStatus": normalized_distribution["assessment"]["riskStatus"],
                    "finalRiskScore": normalized_distribution["assessment"]["finalRiskScore"],
                },
            )

    if is_regulator and "alerts" in data:
        for alert_data in data["alerts"]:
            if "vendorId" not in alert_data and alert_data.get("vendorName"):
                vendor = db.query(models.Vendor).filter(models.Vendor.name == alert_data["vendorName"]).first()
                if vendor:
                    alert_data = {**alert_data, "vendorId": vendor.id}
            db.merge(models.Alert(**alert_data))

    if "documents" in data:
        for document_data in data["documents"]:
            if not is_regulator and document_data.get("vendorId") != vendor_id:
                continue
            db.merge(models.Document(**document_data))

    db.commit()
    return serialize_private_data_for_user(db, current_user)
