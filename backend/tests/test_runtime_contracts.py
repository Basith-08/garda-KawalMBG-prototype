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
                    }
                ]
            },
            user,
            self.db,
        )
        after = self.db.query(models.Distribution).count()
        self.assertEqual(before, after)
        self.assertEqual({item["vendorId"] for item in result["distributions"]}, {"2"})

    def test_regulator_cannot_open_super_admin_overview(self):
        payload = self._login("regulator@garda.id", "password123")
        user = self._current_user(payload["token"])
        with self.assertRaises(main.HTTPException) as exc:
            main.get_admin_overview(user, self.db)
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
