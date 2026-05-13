from datetime import datetime, timezone
from typing import Optional

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


def serialize_datetime(value: Optional[datetime]) -> Optional[str]:
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
