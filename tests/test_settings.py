import unittest
from app.settings import DEFAULT_SETTINGS

class TestSettings(unittest.TestCase):
    def test_default_profile(self):
        self.assertIn(
            DEFAULT_SETTINGS["profile"],
            {"Eco", "Balanced", "Competitive"}
        )

    def test_restore_is_boolean(self):
        self.assertIsInstance(DEFAULT_SETTINGS["auto_restore_power"], bool)

if __name__ == "__main__":
    unittest.main()
