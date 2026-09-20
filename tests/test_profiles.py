import unittest
from app.profiles import recommend_profile, get_profile

class TestProfiles(unittest.TestCase):
    def test_eco(self):
        self.assertEqual(
            recommend_profile({"memory_total_gb": 4, "cpu_threads": 4}),
            "Eco"
        )

    def test_balanced(self):
        self.assertEqual(
            recommend_profile({"memory_total_gb": 8, "cpu_threads": 4}),
            "Balanced"
        )

    def test_competitive(self):
        self.assertEqual(
            recommend_profile({"memory_total_gb": 16, "cpu_threads": 8}),
            "Competitive"
        )

    def test_fallback(self):
        self.assertEqual(get_profile("Unknown"), get_profile("Balanced"))

if __name__ == "__main__":
    unittest.main()
