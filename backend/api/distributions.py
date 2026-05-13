from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from constants import DISTRIBUTION_FIELDS
from database import get_db
import models
from schemas.requests import ReceiptVerificationRequest
from services.history import record_audit_event, record_risk_snapshot
from services.receipts import (
    apply_receipt_verification,
    build_receipt_alert_description,
    build_receipt_response,
    validate_receipt_verification_payload,
)
from services.serialization import persist_normalized_distribution, serialize_distribution


router = APIRouter()


@router.get("/api/distributions/{distribution_id}/receipt")
def get_distribution_receipt(distribution_id: str, db: Session = Depends(get_db)):
    distribution = db.query(models.Distribution).filter(models.Distribution.id == distribution_id).first()
    if not distribution:
        raise HTTPException(status_code=404, detail="Distribution not found")
    vendor = db.query(models.Vendor).filter(models.Vendor.id == distribution.vendorId).first()
    data = serialize_distribution(distribution, vendor)
    return build_receipt_response(data)


@router.post("/api/distributions/{distribution_id}/receipt")
def verify_distribution_receipt(
    distribution_id: str,
    payload: ReceiptVerificationRequest,
    db: Session = Depends(get_db),
):
    validate_receipt_verification_payload(payload)

    distribution = db.query(models.Distribution).filter(models.Distribution.id == distribution_id).first()
    if not distribution:
        raise HTTPException(status_code=404, detail="Distribution not found")

    vendor = db.query(models.Vendor).filter(models.Vendor.id == distribution.vendorId).first()
    apply_receipt_verification(distribution, payload)

    normalized = persist_normalized_distribution(db, distribution, DISTRIBUTION_FIELDS, vendor)
    record_risk_snapshot(db, distribution.id, distribution.vendorId, normalized["assessment"])
    record_audit_event(
        db,
        action="distribution.receipt.verify",
        entity_type="distribution",
        entity_id=distribution.id,
        details={
            "arrivalStatus": payload.arrivalStatus,
            "issueType": payload.issueType,
            "receiptEvidenceUploaded": bool(payload.evidenceUploaded),
        },
    )

    if payload.arrivalStatus in {"received_with_issue", "not_received"}:
        alert_id = f"receipt-{distribution.id}-{int(datetime.now(timezone.utc).timestamp())}"
        db.merge(
            models.Alert(
                id=alert_id,
                type="CRITICAL",
                vendorId=distribution.vendorId,
                vendorName=vendor.name if vendor else distribution.vendorId,
                description=build_receipt_alert_description(distribution.schoolName, payload),
                time="baru saja",
                statusTag="School Receipt",
            )
        )

    db.commit()
    db.refresh(distribution)
    return serialize_distribution(distribution, vendor)
