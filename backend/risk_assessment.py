from __future__ import annotations

from typing import Any, Dict, Iterable


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


def _temperature_score(temperature: float) -> tuple[int, str]:
    if temperature >= 35:
        return 34, f"Ambient temperature reached {temperature:.0f}°C, accelerating unsafe exposure."
    if temperature >= 32:
        return 26, f"Ambient temperature remained elevated at {temperature:.0f}°C."
    if temperature >= 28:
        return 16, f"Ambient temperature of {temperature:.0f}°C increased exposure pressure."
    if temperature >= 24:
        return 8, f"Ambient temperature of {temperature:.0f}°C stayed within monitored range."
    return 4, f"Ambient temperature of {temperature:.0f}°C stayed below the primary danger acceleration band."


def _duration_score(duration: int) -> tuple[int, str]:
    if duration > 120:
        return 36, f"Distribution duration reached {duration} minutes."
    if duration > 90:
        return 28, f"Distribution duration reached {duration} minutes."
    if duration > 60:
        return 22, f"Distribution duration reached {duration} minutes."
    if duration > 45:
        return 16, f"Distribution duration reached {duration} minutes."
    if duration > 30:
        return 10, f"Distribution duration reached {duration} minutes."
    return 5, f"Distribution duration remained at {duration} minutes."


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
    duration = int(distribution.get("durasi") or 0)
    temperature = float(distribution.get("suhu") or 0)
    status_text = str(distribution.get("statusText") or "")
    notes = str(distribution.get("catatan") or "")
    combined_text = _to_text(menu_name, menu_detail, status_text, notes, distribution.get("status"))

    score = 6
    risk_factors: list[str] = []
    sop_violations: list[str] = []

    temperature_score, temperature_reason = _temperature_score(temperature)
    duration_score, duration_reason = _duration_score(duration)
    score += temperature_score + duration_score
    _append_unique(risk_factors, temperature_reason)
    _append_unique(risk_factors, duration_reason)

    if _has_keyword(combined_text, HIGH_PROTEIN_KEYWORDS):
        score += 16
        _append_unique(risk_factors, "High-protein menu composition increased spoilage sensitivity.")

    if _has_keyword(combined_text, HIGH_MOISTURE_KEYWORDS):
        score += 10
        _append_unique(risk_factors, "High-moisture menu components increased operational degradation sensitivity.")

    if duration > 45:
        _append_unique(sop_violations, "Route duration exceeded the 45-minute operational delivery threshold.")

    if temperature >= 32:
        _append_unique(sop_violations, "Ambient temperature entered the elevated exposure band at or above 32°C.")

    anomaly_detected = _has_keyword(combined_text, ANOMALY_KEYWORDS)
    if anomaly_detected:
        score += 24
        _append_unique(sop_violations, "Operational anomaly signal detected in the field log.")
        _append_unique(risk_factors, "Anomaly or discrepancy note increased operational uncertainty.")

    delay_detected = _has_keyword(combined_text, DELAY_KEYWORDS)
    if delay_detected:
        score += 10
        _append_unique(sop_violations, "Delay-related signal detected in the operational note.")
        _append_unique(risk_factors, "Delay signal increased cumulative exposure duration.")

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
        "LOW": "Maintain dispatch timing and continue routine operational monitoring.",
        "MEDIUM": "Prioritize immediate handoff at destination and avoid additional non-refrigerated holding beyond 30 minutes.",
        "HIGH": "Escalate for immediate inspection and consumption control. Discard if additional holding continues.",
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
