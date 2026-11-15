"""
Benchmark Integration Test Suite.
Verifies that all 20 test suite messages achieve 100% Pass Rate and 100% Escalation Recall.
"""

import unittest
from src.benchmark import BenchmarkRunner

class TestBenchmarkSuite(unittest.TestCase):
    def setUp(self):
        self.runner = BenchmarkRunner()

    def test_all_twenty_messages_pass(self):
        res = self.runner.run_benchmark()
        self.assertEqual(res["pass_count"], 20, "All 20 test suite messages must PASS")
        self.assertEqual(res["total_count"], 20)
        self.assertEqual(res["pass_rate_percent"], 100.0)

        # Check KPIs
        metrics = res["metrics"]
        self.assertEqual(metrics["M1"]["percent"], 100.0, "M1 Pass rate must be 100%")
        self.assertEqual(metrics["M2"]["percent"], 100.0, "M2 Grounded rate must be 100%")
        self.assertEqual(metrics["M3"]["percent"], 100.0, "M3 Status accuracy must be 100%")
        self.assertEqual(metrics["M4"]["percent"], 100.0, "M4 Escalation recall must be 100%")
        self.assertEqual(metrics["M5"]["percent"], 0.0, "M5 Over-escalation rate must be 0%")
        self.assertEqual(metrics["M6"]["percent"], 100.0, "M6 Uncertainty recall must be 100%")
        self.assertEqual(metrics["M7"]["percent"], 100.0, "M7 Uncertainty precision must be 100%")

if __name__ == "__main__":
    unittest.main()
