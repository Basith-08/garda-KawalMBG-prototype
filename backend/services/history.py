from datetime import datetime, timezone
from uuid import uuid4
from typing import Any, Dict, Optional

import models


def record_risk_snapshot(
    db: Any,
    distribution_id: str,
    vendor_id: str,
    assessment: Dict[str, Any],
) -> None:
    db.add(
        models.RiskScoreHistory(
            id=f"risk-{uuid4().hex}",
            distributionId=distribution_id,
            vendorId=vendor_id,
            finalRiskScore=float(assessment["finalRiskScore"]),
            riskStatus=str(assessment["riskStatus"]),
            componentScores=assessment.get("componentScores"),
            summary=assessment.get("operationalSummary"),
            assessedAt=datetime.now(timezone.utc),
        )
    )


def record_audit_event(
    db: Any,
    action: str,
    entity_type: str,
    entity_id: str,
    actor_user_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> None:
    db.add(
        models.AuditLog(
            id=f"audit-{uuid4().hex}",
            actorUserId=actor_user_id,
            action=action,
            entityType=entity_type,
            entityId=entity_id,
            details=details or None,
            createdAt=datetime.now(timezone.utc),
        )
    )
