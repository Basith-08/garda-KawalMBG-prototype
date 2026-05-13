from typing import Any, Dict

import models


def build_regulator_overview(db: Any) -> Dict[str, Any]:
    vendors = db.query(models.Vendor).all()
    distributions = db.query(models.Distribution).all()
    alerts = db.query(models.Alert).all()
    schools = db.query(models.School).all()

    vendor_lookup = {vendor.id: vendor for vendor in vendors}
    delayed_distributions = [distribution for distribution in distributions if (distribution.durasi or 0) > 45]
    high_risk_distributions = [distribution for distribution in distributions if distribution.status == "high-risk"]
    receipt_issue_distributions = [
        distribution
        for distribution in distributions
        if distribution.arrivalStatus in {"received_with_issue", "not_received"}
    ]

    on_time_rate = 0
    if distributions:
        on_time_rate = round(((len(distributions) - len(delayed_distributions)) / len(distributions)) * 100)

    top_vendors = sorted(
        [
            {
                "id": vendor.id,
                "name": vendor.name,
                "trustScore": round(vendor.trustScore or 0),
                "status": vendor.status,
                "statusText": vendor.statusText,
            }
            for vendor in vendors
        ],
        key=lambda item: item["trustScore"],
        reverse=True,
    )[:5]

    recent_high_risk = sorted(
        [
            {
                "id": distribution.id,
                "vendorId": distribution.vendorId,
                "vendorName": vendor_lookup.get(distribution.vendorId).name if vendor_lookup.get(distribution.vendorId) else distribution.vendorId,
                "schoolName": distribution.schoolName,
                "riskScore": round(distribution.riskScore or 0),
                "statusText": distribution.statusText,
                "time": distribution.time,
            }
            for distribution in high_risk_distributions
        ],
        key=lambda item: item["riskScore"],
        reverse=True,
    )[:6]

    return {
        "platformMetrics": {
            "vendors": len(vendors),
            "schools": len(schools),
            "distributions": len(distributions),
            "highRiskDistributions": len(high_risk_distributions),
            "activeAlerts": len(alerts),
            "delayedDistributions": len(delayed_distributions),
            "receiptIssues": len(receipt_issue_distributions),
            "onTimeRate": on_time_rate,
        },
        "topVendors": top_vendors,
        "recentHighRisk": recent_high_risk,
    }
