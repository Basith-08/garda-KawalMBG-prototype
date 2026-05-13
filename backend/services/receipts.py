from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import HTTPException

from schemas.requests import ReceiptVerificationRequest

RECEIPT_ALLOWED_STATUSES = {"received_ok", "received_with_issue", "not_received", "not_confirmed"}


def build_receipt_response(data: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": data["id"],
        "vendorId": data["vendorId"],
        "schoolName": data["schoolName"],
        "menuName": data["menuName"],
        "menuUtama": data["menuUtama"],
        "porsi": data["porsi"],
        "time": data["time"],
        "arrivalStatus": data.get("arrivalStatus"),
        "receiptIssueType": data.get("receiptIssueType"),
        "receiptEvidenceUploaded": data.get("receiptEvidenceUploaded"),
        "receiptNote": data.get("receiptNote"),
        "receiptVerifiedAt": data.get("receiptVerifiedAt"),
        "assessment": data["assessment"],
    }


def validate_receipt_verification_payload(payload: ReceiptVerificationRequest) -> None:
    if payload.arrivalStatus not in RECEIPT_ALLOWED_STATUSES:
        raise HTTPException(status_code=400, detail="Invalid arrival status")
    if payload.arrivalStatus == "received_with_issue" and not payload.issueType:
        raise HTTPException(status_code=400, detail="Issue type is required for problematic receipt")
    if payload.arrivalStatus == "received_with_issue" and not payload.evidenceUploaded:
        raise HTTPException(status_code=400, detail="Receipt evidence is required for problematic receipt")
    if payload.arrivalStatus == "not_received" and not (payload.note or "").strip():
        raise HTTPException(status_code=400, detail="Receipt note is required when distribution was not received")


def apply_receipt_verification(distribution: Any, payload: ReceiptVerificationRequest) -> None:
    distribution.arrivalStatus = payload.arrivalStatus
    distribution.receiptIssueType = (
        payload.issueType
        if payload.arrivalStatus == "received_with_issue"
        else ("not_received" if payload.arrivalStatus == "not_received" else None)
    )
    distribution.receiptEvidenceUploaded = bool(payload.evidenceUploaded) if payload.arrivalStatus == "received_with_issue" else False
    distribution.receiptNote = payload.note.strip() if payload.note else None
    distribution.receiptVerifiedAt = datetime.now(timezone.utc)
    if payload.note:
        distribution.catatan = f"{distribution.catatan or ''} School receipt: {payload.note.strip()}".strip()


def build_receipt_alert_description(school_name: str, payload: ReceiptVerificationRequest) -> str:
    return (
        f"Verifikasi sekolah untuk {school_name}: "
        f"{payload.arrivalStatus.replace('_', ' ')}"
        + (f" ({payload.issueType.replace('_', ' ')})" if payload.issueType else "")
        + (f" - {payload.note}" if payload.note else "")
    )
