from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any, Dict, Iterable, Optional


HIGH_PROTEIN_KEYWORDS = (
    "ayam",
    "ikan",
    "daging",
    "rendang",
    "opor",
    "bakso",
    "sarden",
    "kambing",
    "telur",
    "geprek",
    "teri",
)

HIGH_MOISTURE_KEYWORDS = (
    "soto",
    "rawon",
    "gulai",
    "kuah",
    "sayur",
    "opor",
    "tim",
    "gudeg",
    "asem",
    "bening",
    "sambal",
)

ANOMALY_KEYWORDS = ("fraud", "anomali", "selisih", "tidak sesuai", "hilang", "duplikasi")
DELAY_KEYWORDS = ("terlambat", "delay", "lambat", "pending", "melebihi", "telat")
ISSUE_KEYWORDS = (
    "bau",
    "tidak layak",
    "kemasan rusak",
    "rusak",
    "jumlah kurang",
    "porsi kurang",
    "tidak sesuai",
    "penyok",
    "masalah",
)
OK_KEYWORDS = ("diterima baik", "konfirmasi positif", "received ok", "ok", "lancar", "no issues", "safe")
GENERIC_STATUS_TEXT = {"safe", "medium", "high risk", "pending review"}


def _to_text(*values: Any) -> str:
    return " ".join(str(value).strip().lower() for value in values if value is not None)


def _has_keyword(text: str, keywords: Iterable[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def _append_unique(items: list[str], value: str) -> None:
    if value not in items:
        items.append(value)


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _parse_time(value: Any) -> Optional[datetime]:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    text = str(value).strip()
    for fmt in ("%H:%M", "%H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    return None


def _minutes_between(start: Optional[datetime], end: Optional[datetime]) -> Optional[int]:
    if start is None or end is None:
        return None
    if end < start:
        end += timedelta(days=1)
    return max(0, round((end - start).total_seconds() / 60))


def _duration_minutes(distribution: Dict[str, Any]) -> int:
    cooked_at = _parse_time(distribution.get("cooked_at") or distribution.get("cookedAt"))
    delivered_at = _parse_time(distribution.get("delivered_at") or distribution.get("deliveredAt"))
    timeline_duration = _minutes_between(cooked_at, delivered_at)
    if timeline_duration is not None:
        return timeline_duration
    return int(distribution.get("durasi") or distribution.get("durationMinutes") or 0)


def _time_risk(duration: int, has_timeline: bool) -> tuple[int, str]:
    if duration <= 0:
        return 100, "Time risk: production-to-arrival timeline is incomplete."
    if has_timeline:
        if duration <= 240:
            return 0, f"Time risk: cook-to-arrival exposure stayed within 4 hours ({duration} minutes)."
        if duration <= 300:
            return 40, f"Time risk: cook-to-arrival exposure reached 4-5 hours ({duration} minutes)."
        return 80, f"Time risk: cook-to-arrival exposure exceeded 5 hours ({duration} minutes)."
    if duration <= 45:
        return 10, f"Time risk: route duration stayed within the 45-minute dispatch target ({duration} minutes)."
    if duration <= 60:
        return 40, f"Time risk: route duration exceeded the 45-minute dispatch target ({duration} minutes)."
    if duration <= 120:
        return 70, f"Time risk: route duration created extended distribution exposure ({duration} minutes)."
    return 90, f"Time risk: route duration exceeded 2 hours ({duration} minutes)."


def _sop_risk(distribution: Dict[str, Any], combined_text: str) -> tuple[int, str]:
    evidence_fields = (
        "qcPhotoUploaded",
        "productionPhotoUploaded",
        "packagingPhotoUploaded",
        "vehiclePhotoUploaded",
        "evidenceUploaded",
    )
    present_fields = [field for field in evidence_fields if field in distribution]
    uploaded_count = sum(1 for field in present_fields if bool(distribution.get(field)))

    if present_fields:
        missing = len(present_fields) - uploaded_count
        if missing == 0:
            return 0, "SOP risk: required QC and dispatch evidence is complete."
        if missing == 1:
            return 40, "SOP risk: one required evidence item is missing."
        if missing == 2:
            return 70, "SOP risk: multiple evidence items are missing."
        return 100, "SOP risk: required operational evidence was not uploaded."

    if _has_keyword(combined_text, ANOMALY_KEYWORDS):
        return 85, "SOP risk: discrepancy or anomaly signal was detected in the operational log."
    if _has_keyword(combined_text, DELAY_KEYWORDS):
        return 60, "SOP risk: delay signal was detected in the operational log."
    return 40, "SOP risk: evidence completeness is not available in the current distribution record."


def _menu_risk(combined_text: str) -> tuple[int, str]:
    high_protein = _has_keyword(combined_text, HIGH_PROTEIN_KEYWORDS)
    high_moisture = _has_keyword(combined_text, HIGH_MOISTURE_KEYWORDS)
    if high_protein and high_moisture:
        return 70, "Menu risk: high-protein and high-moisture components increase food sensitivity."
    if high_protein:
        return 50, "Menu risk: high-protein menu composition requires tighter exposure control."
    if high_moisture:
        return 50, "Menu risk: high-moisture menu components require tighter exposure control."
    return 20, "Menu risk: menu composition is relatively stable for distribution."


def _arrival_risk(distribution: Dict[str, Any], combined_text: str) -> tuple[int, str]:
    raw_status = str(
        distribution.get("arrivalVerification")
        or distribution.get("arrivalStatus")
        or distribution.get("schoolVerificationStatus")
        or ""
    ).strip().lower()
    raw_issue_type = str(distribution.get("receiptIssueType") or distribution.get("arrivalIssueType") or "").strip().lower()
    if raw_status in {"ok", "received_ok", "received-good", "received_good", "diterima_baik"}:
        return 0, "Arrival verification risk: school confirmed receipt without issue."
    if raw_status in {"not_confirmed", "unconfirmed", "belum_dikonfirmasi"}:
        return 50, "Arrival verification risk: school receipt is not yet confirmed."
    if raw_status in {"not_received", "belum_diterima"}:
        return 100, "Arrival verification risk: school reported that the distribution was not received."
    if raw_status in {"issue", "received_with_issue", "problem", "ada_masalah"}:
        if raw_issue_type in {"unsafe_smell_or_quality", "not_received"}:
            return 100, "Arrival verification risk: school reported a severe receipt issue."
        return 70, "Arrival verification risk: school reported an issue on receipt."
    if raw_status in {"major_issue", "rejected", "heavy_issue"}:
        return 100, "Arrival verification risk: school reported a severe receipt issue."

    if _has_keyword(combined_text, ISSUE_KEYWORDS):
        return 70, "Arrival verification risk: field note indicates a receipt or quality issue."
    if _has_keyword(combined_text, OK_KEYWORDS):
        return 0, "Arrival verification risk: field note indicates normal receipt."
    return 50, "Arrival verification risk: school receipt is not yet confirmed."


def _vendor_history_risk(distribution: Dict[str, Any], combined_text: str) -> tuple[int, str]:
    trust_score = distribution.get("vendorTrustScore")
    if trust_score is not None:
        trust = float(trust_score)
        if trust >= 85:
            return 0, f"Vendor history risk: vendor trust score is strong ({trust:.0f})."
        if trust >= 70:
            return 30, f"Vendor history risk: vendor trust score needs monitoring ({trust:.0f})."
        if trust >= 50:
            return 70, f"Vendor history risk: vendor trust score is weak ({trust:.0f})."
        return 100, f"Vendor history risk: vendor trust score is critical ({trust:.0f})."

    if _has_keyword(combined_text, ("investigasi", "critical", "fraud", "high risk incident")):
        return 100, "Vendor history risk: active investigation or critical history signal detected."
    if _has_keyword(combined_text, ("sering", "laporan buruk", "high-risk")):
        return 70, "Vendor history risk: repeated negative history signal detected."
    if _has_keyword(combined_text, DELAY_KEYWORDS):
        return 30, "Vendor history risk: prior delay signal detected."
    return 0, "Vendor history risk: no negative history signal was available."


def _weather_risk(temperature: float) -> tuple[int, str]:
    if temperature >= 35:
        return 80, f"Weather risk: ambient temperature reached {temperature:.0f}°C."
    if temperature >= 32:
        return 60, f"Weather risk: ambient temperature remained elevated at {temperature:.0f}°C."
    if temperature >= 28:
        return 35, f"Weather risk: ambient temperature of {temperature:.0f}°C adds moderate context."
    return 10, f"Weather risk: ambient temperature of {temperature:.0f}°C adds limited context."


def _estimate_danger_zone_minutes(duration: int, temperature: float) -> int:
    if duration <= 0:
        return 0
    if temperature >= 32:
        return duration
    if temperature >= 28:
        return max(10, round(duration * 0.8))
    if temperature >= 24:
        return max(5, round(duration * 0.55))
    return max(0, round(duration * 0.25))


def _risk_status(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"


def _status_from_risk(risk_status: str) -> str:
    return {
        "LOW": "safe",
        "MEDIUM": "medium",
        "HIGH": "high-risk",
    }[risk_status]


def _status_text_from_risk(risk_status: str, current_status_text: str, anomaly_detected: bool) -> str:
    if anomaly_detected:
        return "Operational Anomaly"

    lowered = current_status_text.strip().lower()
    if lowered and lowered not in GENERIC_STATUS_TEXT:
        return current_status_text

    return {
        "LOW": "Within SOP Window",
        "MEDIUM": "Exposure Monitor",
        "HIGH": "High Exposure",
    }[risk_status]


def build_distribution_assessment(distribution: Dict[str, Any]) -> Dict[str, Any]:
    menu_name = str(distribution.get("menuName") or "Unknown Menu")
    menu_detail = str(distribution.get("menuUtama") or "")
    school_name = str(distribution.get("schoolName") or "Unknown Destination")
    duration = _duration_minutes(distribution)
    has_timeline = bool(
        (distribution.get("cooked_at") or distribution.get("cookedAt"))
        and (distribution.get("delivered_at") or distribution.get("deliveredAt"))
    )
    temperature = float(distribution.get("suhu") or distribution.get("ambient_temperature") or 0)
    status_text = str(distribution.get("statusText") or "")
    notes = str(distribution.get("catatan") or "")
    combined_text = _to_text(
        menu_name,
        menu_detail,
        status_text,
        notes,
        distribution.get("status"),
        distribution.get("vendorStatusText"),
        distribution.get("arrivalVerification"),
        distribution.get("arrivalStatus"),
        distribution.get("receiptIssueType"),
        distribution.get("receiptNote"),
    )

    risk_factors: list[str] = []
    sop_violations: list[str] = []

    time_risk, time_reason = _time_risk(duration, has_timeline)
    sop_risk, sop_reason = _sop_risk(distribution, combined_text)
    menu_risk, menu_reason = _menu_risk(combined_text)
    arrival_risk, arrival_reason = _arrival_risk(distribution, combined_text)
    vendor_history_risk, vendor_history_reason = _vendor_history_risk(distribution, combined_text)
    weather_risk, weather_reason = _weather_risk(temperature)

    component_scores = {
        "timeRisk": time_risk,
        "sopRisk": sop_risk,
        "menuRisk": menu_risk,
        "arrivalVerificationRisk": arrival_risk,
        "vendorHistoryRisk": vendor_history_risk,
        "weatherRisk": weather_risk,
    }
    score = (
        time_risk * 0.25
        + sop_risk * 0.25
        + menu_risk * 0.15
        + arrival_risk * 0.20
        + vendor_history_risk * 0.10
        + weather_risk * 0.05
    )

    for reason in (time_reason, sop_reason, menu_reason, arrival_reason, vendor_history_reason, weather_reason):
        _append_unique(risk_factors, reason)

    if duration > 45:
        _append_unique(sop_violations, "Route duration exceeded the 45-minute operational delivery threshold.")

    if sop_risk >= 70:
        _append_unique(sop_violations, sop_reason)

    if arrival_risk >= 70:
        _append_unique(sop_violations, arrival_reason)

    anomaly_detected = _has_keyword(combined_text, ANOMALY_KEYWORDS)
    if anomaly_detected:
        _append_unique(sop_violations, "Operational anomaly signal detected in the field log.")

    delay_detected = _has_keyword(combined_text, DELAY_KEYWORDS)
    if delay_detected:
        _append_unique(sop_violations, "Delay-related signal detected in the operational note.")

    score = int(round(_clamp(score, 5, 98)))
    risk_status = _risk_status(score)
    danger_zone_minutes = _estimate_danger_zone_minutes(duration, temperature)

    if not sop_violations:
        sop_violations.append("No major SOP violation was detected from the available delivery log.")

    operational_summary = (
        f"{menu_name} for {school_name} shows {risk_status.lower()} operational exposure "
        f"driven by {duration} minutes of distribution time and ambient temperature of {temperature:.0f}°C."
    )

    recommended_action = {
        "LOW": "Allow normal distribution and keep the operational log for audit.",
        "MEDIUM": "Allow distribution with QC evidence requirement and mandatory school receipt monitoring.",
        "HIGH": "Apply soft block pending supervisor approval, require additional evidence, and alert the regulator dashboard.",
    }[risk_status]

    return {
        "operationalSummary": operational_summary,
        "exposureAnalysis": [
            f"Total exposure duration: {duration} minutes",
            f"Estimated danger-zone exposure: {danger_zone_minutes} minutes",
            f"Ambient temperature: {temperature:.0f}°C",
            "Holding condition: no refrigerated evidence in the current delivery log",
        ],
        "sopViolations": sop_violations,
        "riskFactors": risk_factors,
        "componentScores": component_scores,
        "finalRiskScore": score,
        "riskStatus": risk_status,
        "recommendedAction": recommended_action,
    }


def normalize_distribution_record(distribution: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(distribution)
    assessment = build_distribution_assessment(normalized)
    normalized["assessment"] = assessment
    normalized["riskScore"] = assessment["finalRiskScore"]
    normalized["levelRisiko"] = f"{assessment['riskStatus']} RISK"
    normalized["status"] = _status_from_risk(assessment["riskStatus"])
    normalized["statusText"] = _status_text_from_risk(
        assessment["riskStatus"],
        str(normalized.get("statusText") or ""),
        _has_keyword(_to_text(normalized.get("statusText"), normalized.get("catatan")), ANOMALY_KEYWORDS),
    )
    normalized["catatan"] = str(normalized.get("catatan") or assessment["operationalSummary"])
    return normalized
