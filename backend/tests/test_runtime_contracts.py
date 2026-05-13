import time
import unittest
from types import SimpleNamespace

from sqlalchemy import text

import main
import models
from database import SessionLocal
from migrations import run_migrations
from seed import seed_database
from token_utils import create_access_token, decode_access_token


class RuntimeContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        run_migrations()
        seed_database(only_if_empty=True)

    def setUp(self):
        self.db = SessionLocal()

    def tearDown(self):
        self.db.close()

    def _login(self, email: str, password: str):
        return main.login(main.LoginRequest(email=email, password=password), self.db)

    def _current_user(self, token: str):
        return main.get_current_user(SimpleNamespace(credentials=token), self.db)

    def test_migration_record_exists(self):
        versions = [
            row[0]
            for row in self.db.execute(text("SELECT version FROM schema_migrations ORDER BY version")).fetchall()
        ]
        self.assertIn("20260510_001_add_users_vendor_id", versions)
        self.assertIn("20260510_002_add_user_governance_fields", versions)
        self.assertIn("20260510_003_normalize_vendor_foreign_keys", versions)
        self.assertIn("20260514_004_add_distribution_operational_fields", versions)
        self.assertIn("20260514_005_add_distribution_receipt_fields", versions)
        self.assertIn("20260514_006_create_history_tables", versions)

    def test_vendor_login_returns_explicit_vendor_id(self):
        payload = self._login("vendor@garda.id", "password123")
        self.assertEqual(payload["user"]["vendorId"], "2")
        decoded = decode_access_token(payload["token"])
        self.assertEqual(decoded["vendorId"], "2")

    def test_regulator_session_sees_full_private_dataset(self):
        payload = self._login("regulator@garda.id", "password123")
        user = self._current_user(payload["token"])
        dataset = main.get_data(user, self.db)
        self.assertEqual(user.role, "regulator")
        self.assertGreaterEqual(len(dataset["vendors"]), 15)
        self.assertIn("trustBreakdown", dataset["vendors"][0])

    def test_super_admin_login_and_overview(self):
        payload = self._login("superadmin@garda.id", "password123")
        self.assertEqual(payload["user"]["role"], "super-admin")
        user = self._current_user(payload["token"])
        overview = main.get_admin_overview(user, self.db)
        self.assertIn("platformMetrics", overview)
        self.assertGreaterEqual(overview["platformMetrics"]["totalUsers"], 3)
        self.assertTrue(any(item["role"] == "super-admin" for item in overview["userAccess"]))
        self.assertTrue(all("id" in item and "name" in item for item in overview["availableVendors"]))

    def test_vendor_session_is_scoped_to_own_records(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        dataset = main.get_data(user, self.db)
        self.assertEqual(user.vendorId, "2")
        self.assertEqual(len(dataset["vendors"]), 1)
        self.assertEqual(dataset["vendors"][0]["id"], "2")
        self.assertEqual({item["vendorId"] for item in dataset["documents"]}, {"2"})
        self.assertEqual({item["vendorId"] for item in dataset["distributions"]}, {"2"})
        self.assertEqual({item["vendorId"] for item in dataset["schools"]}, {"2"})
        self.assertTrue(all(item["vendorId"] == "2" for item in dataset["alerts"]))

    def test_vendor_cannot_write_foreign_distribution(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        before = self.db.query(models.Distribution).count()
        result = main.save_data(
            {
                "distributions": [
                    {
                        "id": f"foreign-{int(time.time())}",
                        "vendorId": "999",
                        "schoolName": "Sekolah Asing",
                        "porsi": 100,
                        "status": "medium",
                        "statusText": "Pending",
                        "time": "10 Mei 2026",
                        "riskScore": 55,
                        "menuName": "Menu Uji",
                        "menuUtama": "Menu Uji",
                        "suhu": 30,
                        "durasi": 40,
                        "levelRisiko": "MEDIUM",
                        "catatan": "should be ignored",
                        "arrivalStatus": "received_with_issue",
                        "qcPhotoUploaded": True,
                    }
                ]
            },
            user,
            self.db,
        )
        after = self.db.query(models.Distribution).count()
        self.assertEqual(before, after)
        self.assertEqual({item["vendorId"] for item in result["distributions"]}, {"2"})

    def test_vendor_distribution_operational_fields_are_persisted(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        distribution_id = f"ops-{int(time.time())}"
        before_risk_rows = self.db.query(models.RiskScoreHistory).count()
        before_audit_rows = self.db.query(models.AuditLog).count()

        result = main.save_data(
            {
                "distributions": [
                    {
                        "id": distribution_id,
                        "vendorId": "2",
                        "schoolName": "SDN 05 Barat",
                        "porsi": 100,
                        "status": "medium",
                        "statusText": "Pending",
                        "time": "14 Mei 2026",
                        "riskScore": 0,
                        "menuName": "Soto Ayam",
                        "menuUtama": "Soto ayam, nasi, perkedel",
                        "suhu": 32,
                        "durasi": 70,
                        "levelRisiko": "MEDIUM",
                        "catatan": "menunggu konfirmasi sekolah",
                        "cookedAt": "05:00",
                        "packagedAt": "05:40",
                        "pickupAt": "06:10",
                        "deliveredAt": "07:20",
                        "arrivalStatus": "not_confirmed",
                        "qcPhotoUploaded": True,
                        "productionPhotoUploaded": True,
                        "packagingPhotoUploaded": True,
                        "vehiclePhotoUploaded": True,
                        "evidenceUploaded": True,
                    }
                ]
            },
            user,
            self.db,
        )

        saved = next(item for item in result["distributions"] if item["id"] == distribution_id)
        self.assertEqual(saved["arrivalStatus"], "not_confirmed")
        self.assertTrue(saved["qcPhotoUploaded"])
        self.assertEqual(saved["assessment"]["componentScores"]["sopRisk"], 0)
        self.assertEqual(self.db.query(models.RiskScoreHistory).count(), before_risk_rows + 1)
        self.assertEqual(self.db.query(models.AuditLog).count(), before_audit_rows + 1)

    def test_school_receipt_updates_arrival_risk_and_creates_alert(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        distribution_id = f"receipt-{int(time.time())}"
        main.save_data(
            {
                "distributions": [
                    {
                        "id": distribution_id,
                        "vendorId": "2",
                        "schoolName": "SDN 05 Barat",
                        "porsi": 100,
                        "status": "medium",
                        "statusText": "Pending",
                        "time": "14 Mei 2026",
                        "riskScore": 0,
                        "menuName": "Soto Ayam",
                        "menuUtama": "Soto ayam, nasi, perkedel",
                        "suhu": 32,
                        "durasi": 70,
                        "levelRisiko": "MEDIUM",
                        "catatan": "menunggu konfirmasi sekolah",
                        "arrivalStatus": "not_confirmed",
                    }
                ]
            },
            user,
            self.db,
        )

        before_alerts = self.db.query(models.Alert).count()
        verified = main.verify_distribution_receipt(
            distribution_id,
            main.ReceiptVerificationRequest(
                arrivalStatus="received_with_issue",
                issueType="packaging_damaged",
                evidenceUploaded=True,
                note="kemasan rusak pada beberapa porsi",
            ),
            self.db,
        )
        after_alerts = self.db.query(models.Alert).count()

        self.assertEqual(verified["arrivalStatus"], "received_with_issue")
        self.assertEqual(verified["receiptIssueType"], "packaging_damaged")
        self.assertTrue(verified["receiptEvidenceUploaded"])
        self.assertIsNotNone(verified["receiptVerifiedAt"])
        self.assertEqual(verified["assessment"]["componentScores"]["arrivalVerificationRisk"], 70)
        self.assertEqual(after_alerts, before_alerts + 1)
        self.assertTrue(
            self.db.query(models.RiskScoreHistory)
            .filter(models.RiskScoreHistory.distributionId == distribution_id)
            .count()
            >= 2
        )

    def test_login_creates_audit_log(self):
        before = self.db.query(models.AuditLog).count()
        payload = self._login("regulator@garda.id", "password123")
        self.assertIn("token", payload)
        after = self.db.query(models.AuditLog).count()
        self.assertEqual(after, before + 1)

    def test_problematic_receipt_requires_issue_type_and_evidence(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        distribution_id = f"receipt-rule-{int(time.time())}"
        main.save_data(
            {
                "distributions": [
                    {
                        "id": distribution_id,
                        "vendorId": "2",
                        "schoolName": "SDN 05 Barat",
                        "porsi": 100,
                        "status": "medium",
                        "statusText": "Pending",
                        "time": "14 Mei 2026",
                        "riskScore": 0,
                        "menuName": "Soto Ayam",
                        "menuUtama": "Soto ayam, nasi, perkedel",
                        "suhu": 32,
                        "durasi": 70,
                        "levelRisiko": "MEDIUM",
                        "catatan": "menunggu konfirmasi sekolah",
                        "arrivalStatus": "not_confirmed",
                    }
                ]
            },
            user,
            self.db,
        )

        with self.assertRaises(main.HTTPException) as missing_issue:
            main.verify_distribution_receipt(
                distribution_id,
                main.ReceiptVerificationRequest(arrivalStatus="received_with_issue", evidenceUploaded=True),
                self.db,
            )
        self.assertEqual(missing_issue.exception.status_code, 400)

        with self.assertRaises(main.HTTPException) as missing_evidence:
            main.verify_distribution_receipt(
                distribution_id,
                main.ReceiptVerificationRequest(arrivalStatus="received_with_issue", issueType="menu_mismatch"),
                self.db,
            )
        self.assertEqual(missing_evidence.exception.status_code, 400)

    def test_vendor_trust_profile_is_operational_not_static_only(self):
        vendor = models.Vendor(
            id="trust-test",
            name="Vendor Trust Test",
            status="safe",
            statusText="No Issues",
            trustScore=95,
            trend=0,
            trendDir="up",
            address="-",
            joinDate="2026-05-14",
            schools=[],
        )
        distributions = [
            models.Distribution(
                id="trust-dist-1",
                vendorId="trust-test",
                schoolName="SDN Uji",
                porsi=100,
                durasi=90,
                arrivalStatus="received_with_issue",
                qcPhotoUploaded=False,
                productionPhotoUploaded=False,
                packagingPhotoUploaded=False,
                vehiclePhotoUploaded=False,
            )
        ]
        alerts = [models.Alert(id="trust-alert-1", type="CRITICAL", vendorId="trust-test")]
        profile = main.build_vendor_trust_profile(vendor, distributions, alerts)

        self.assertLess(profile["trustScore"], 60)
        self.assertEqual(profile["status"], "high-risk")
        self.assertEqual(profile["trustBreakdown"]["schoolReceipt"], 0)

    def test_regulator_cannot_open_super_admin_overview(self):
        payload = self._login("regulator@garda.id", "password123")
        user = self._current_user(payload["token"])
        with self.assertRaises(main.HTTPException) as exc:
            main.get_admin_overview(user, self.db)
        self.assertEqual(exc.exception.status_code, 403)

    def test_regulator_can_open_regulator_overview(self):
        payload = self._login("regulator@garda.id", "password123")
        user = self._current_user(payload["token"])
        overview = main.get_regulator_overview(user, self.db)

        self.assertIn("platformMetrics", overview)
        self.assertIn("topVendors", overview)
        self.assertIn("recentHighRisk", overview)
        self.assertIn("receiptIssues", overview["platformMetrics"])
        self.assertIn("onTimeRate", overview["platformMetrics"])

    def test_vendor_cannot_open_regulator_overview(self):
        payload = self._login("vendor@garda.id", "password123")
        user = self._current_user(payload["token"])
        with self.assertRaises(main.HTTPException) as exc:
            main.get_regulator_overview(user, self.db)
        self.assertEqual(exc.exception.status_code, 403)

    def test_super_admin_can_update_vendor_user_mapping(self):
        payload = self._login("superadmin@garda.id", "password123")
        admin = self._current_user(payload["token"])
        updated = main.update_admin_user(
            "2",
            main.AdminUserUpdateRequest(role="vendor", vendorId="9", isActive=True),
            admin,
            self.db,
        )
        self.assertEqual(updated["vendorId"], "9")
        self.assertEqual(updated["role"], "vendor")

        reverted = main.update_admin_user(
            "2",
            main.AdminUserUpdateRequest(role="vendor", vendorId="2", isActive=True),
            admin,
            self.db,
        )
        self.assertEqual(reverted["vendorId"], "2")

    def test_super_admin_cannot_disable_self(self):
        payload = self._login("superadmin@garda.id", "password123")
        admin = self._current_user(payload["token"])
        with self.assertRaises(main.HTTPException) as exc:
            main.update_admin_user(
                "100",
                main.AdminUserUpdateRequest(isActive=False),
                admin,
                self.db,
            )
        self.assertEqual(exc.exception.status_code, 400)

    def test_expired_token_is_rejected(self):
        token = create_access_token({"sub": "2", "role": "vendor", "vendorId": "2"}, expires_in=-1)
        with self.assertRaises(ValueError):
            decode_access_token(token)


if __name__ == "__main__":
    unittest.main()
