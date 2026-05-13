import os
import unittest

from settings import get_settings, validate_runtime_settings


class SettingsRuntimeTest(unittest.TestCase):
    def setUp(self):
        self._original_env = os.environ.copy()
        get_settings.cache_clear()

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self._original_env)
        get_settings.cache_clear()

    def test_auto_seed_flag_defaults_to_disabled(self):
        os.environ.pop("AUTO_SEED_ON_STARTUP", None)
        os.environ["APP_ENV"] = "local"
        get_settings.cache_clear()

        settings = get_settings()

        self.assertFalse(settings.auto_seed_on_startup)

    def test_auto_seed_flag_accepts_truthy_values(self):
        os.environ["AUTO_SEED_ON_STARTUP"] = "true"
        get_settings.cache_clear()

        settings = get_settings()

        self.assertTrue(settings.auto_seed_on_startup)

    def test_production_cannot_enable_auto_seed(self):
        os.environ["APP_ENV"] = "production"
        os.environ["AUTH_TOKEN_SECRET"] = "override-production-secret"
        os.environ["AUTO_SEED_ON_STARTUP"] = "true"
        get_settings.cache_clear()

        with self.assertRaises(RuntimeError) as exc:
            validate_runtime_settings()

        self.assertIn("AUTO_SEED_ON_STARTUP", str(exc.exception))


if __name__ == "__main__":
    unittest.main()
