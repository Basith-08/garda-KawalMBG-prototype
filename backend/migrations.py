from typing import Callable, List, Tuple

from sqlalchemy import text

from auth_utils import get_password_hash
from database import engine
import models


Migration = Tuple[str, Callable[[], None]]


def _create_migrations_table() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR PRIMARY KEY,
                    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                )
                """
            )
        )


def _migration_add_users_vendor_id() -> None:
    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS "vendorId" VARCHAR'))
        conn.execute(
            text(
                """
                UPDATE users
                SET "vendorId" = '2'
                WHERE role = 'vendor'
                  AND email = 'vendor@garda.id'
                  AND ("vendorId" IS NULL OR "vendorId" = '')
                """
            )
        )


def _migration_add_user_governance_fields() -> None:
    super_admin_password = get_password_hash("password123")

    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS "isActive" BOOLEAN NOT NULL DEFAULT TRUE'))
        conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS "createdAt" TIMESTAMPTZ NULL'))
        conn.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS "lastLoginAt" TIMESTAMPTZ NULL'))
        conn.execute(text('UPDATE users SET "isActive" = TRUE WHERE "isActive" IS NULL'))
        conn.execute(text('UPDATE users SET "createdAt" = NOW() WHERE "createdAt" IS NULL'))
        conn.execute(
            text(
                """
                INSERT INTO users ("id", "name", "email", "hashed_password", "role", "vendorId", "isActive", "createdAt", "lastLoginAt", "avatar")
                SELECT
                    '100',
                    'Sari Super Admin',
                    'superadmin@garda.id',
                    :hashed_password,
                    'super-admin',
                    NULL,
                    TRUE,
                    NOW(),
                    NULL,
                    'https://i.pravatar.cc/80?u=super-admin'
                WHERE NOT EXISTS (
                    SELECT 1 FROM users WHERE email = 'superadmin@garda.id'
                )
                """
            ),
            {"hashed_password": super_admin_password},
        )


def _migration_normalize_vendor_foreign_keys() -> None:
    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE alerts ADD COLUMN IF NOT EXISTS "vendorId" VARCHAR'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_alerts_vendorId ON alerts ("vendorId")'))
        conn.execute(
            text(
                """
                UPDATE alerts
                SET "vendorId" = vendors.id
                FROM vendors
                WHERE alerts."vendorId" IS NULL
                  AND alerts."vendorName" = vendors.name
                """
            )
        )
        conn.execute(
            text(
                """
                DO $$
                BEGIN
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_schools_vendor_id') THEN
                        ALTER TABLE schools
                        ADD CONSTRAINT fk_schools_vendor_id
                        FOREIGN KEY ("vendorId") REFERENCES vendors(id);
                    END IF;
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_distributions_vendor_id') THEN
                        ALTER TABLE distributions
                        ADD CONSTRAINT fk_distributions_vendor_id
                        FOREIGN KEY ("vendorId") REFERENCES vendors(id);
                    END IF;
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_documents_vendor_id') THEN
                        ALTER TABLE documents
                        ADD CONSTRAINT fk_documents_vendor_id
                        FOREIGN KEY ("vendorId") REFERENCES vendors(id);
                    END IF;
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_users_vendor_id') THEN
                        ALTER TABLE users
                        ADD CONSTRAINT fk_users_vendor_id
                        FOREIGN KEY ("vendorId") REFERENCES vendors(id);
                    END IF;
                    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'fk_alerts_vendor_id') THEN
                        ALTER TABLE alerts
                        ADD CONSTRAINT fk_alerts_vendor_id
                        FOREIGN KEY ("vendorId") REFERENCES vendors(id);
                    END IF;
                END
                $$;
                """
            )
        )


def _migration_add_distribution_operational_fields() -> None:
    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "cookedAt" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "packagedAt" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "pickupAt" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "deliveredAt" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "arrivalStatus" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "qcPhotoUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "productionPhotoUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "packagingPhotoUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "vehiclePhotoUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "evidenceUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))

def _migration_add_distribution_receipt_fields() -> None:
    with engine.begin() as conn:
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "receiptIssueType" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "receiptEvidenceUploaded" BOOLEAN NOT NULL DEFAULT FALSE'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "receiptNote" VARCHAR'))
        conn.execute(text('ALTER TABLE distributions ADD COLUMN IF NOT EXISTS "receiptVerifiedAt" TIMESTAMPTZ NULL'))


def _migration_create_history_tables() -> None:
    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS risk_scores (
                    id VARCHAR PRIMARY KEY,
                    "distributionId" VARCHAR NOT NULL REFERENCES distributions(id),
                    "vendorId" VARCHAR NOT NULL REFERENCES vendors(id),
                    "finalRiskScore" DOUBLE PRECISION NOT NULL,
                    "riskStatus" VARCHAR NOT NULL,
                    "componentScores" JSONB NULL,
                    "summary" VARCHAR NULL,
                    "assessedAt" TIMESTAMPTZ NOT NULL
                )
                """
            )
        )
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_risk_scores_distribution_id ON risk_scores ("distributionId")'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_risk_scores_vendor_id ON risk_scores ("vendorId")'))
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id VARCHAR PRIMARY KEY,
                    "actorUserId" VARCHAR NULL REFERENCES users(id),
                    "action" VARCHAR NOT NULL,
                    "entityType" VARCHAR NOT NULL,
                    "entityId" VARCHAR NOT NULL,
                    "details" JSONB NULL,
                    "createdAt" TIMESTAMPTZ NOT NULL
                )
                """
            )
        )
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_audit_logs_actor_user_id ON audit_logs ("actorUserId")'))
        conn.execute(text('CREATE INDEX IF NOT EXISTS ix_audit_logs_entity_id ON audit_logs ("entityId")'))


MIGRATIONS: List[Migration] = [
    ("20260510_001_add_users_vendor_id", _migration_add_users_vendor_id),
    ("20260510_002_add_user_governance_fields", _migration_add_user_governance_fields),
    ("20260510_003_normalize_vendor_foreign_keys", _migration_normalize_vendor_foreign_keys),
    ("20260514_004_add_distribution_operational_fields", _migration_add_distribution_operational_fields),
    ("20260514_005_add_distribution_receipt_fields", _migration_add_distribution_receipt_fields),
    ("20260514_006_create_history_tables", _migration_create_history_tables),
]


def run_migrations() -> List[str]:
    models.Base.metadata.create_all(bind=engine)
    _create_migrations_table()

    with engine.begin() as conn:
        applied = {
            row[0]
            for row in conn.execute(text("SELECT version FROM schema_migrations"))
        }

    newly_applied: List[str] = []
    for version, migration in MIGRATIONS:
        if version in applied:
            continue
        migration()
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": version},
            )
        newly_applied.append(version)

    return newly_applied


if __name__ == "__main__":
    applied = run_migrations()
    if applied:
        print("Applied migrations:", ", ".join(applied))
    else:
        print("No pending migrations.")
