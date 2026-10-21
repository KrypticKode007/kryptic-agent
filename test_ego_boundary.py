#!/usr/bin/env python3
"""Unit tests for the IM-FIN homeostasis and recovery invariants."""

import unittest
from kryptic_integration_core import IMFINInterceptNode

class TestIMFINHomeostasis(unittest.TestCase):
    def setUp(self):
        self.node = IMFINInterceptNode()

    def test_operational_load_preserves_stamina_bounds(self):
        metrics = self.node.evaluate_homeostasis(operational_load=35.0)

        self.assertEqual(metrics["stamina"], 50.0)
        self.assertEqual(metrics["status"], "STABLE")

    def test_critical_load_recovers_without_exceeding_bounds(self):
        for _ in range(4):
            metrics = self.node.evaluate_homeostasis(operational_load=99.9)
            self.assertGreaterEqual(metrics["stamina"], 0.0)
            self.assertLessEqual(metrics["stamina"], 50.0)

        self.assertEqual(metrics["stamina"], 25.0)
        self.assertEqual(metrics["entropy_cycles"], 1)

if __name__ == "__main__":
    unittest.main()
        # Step 2: Inject a massive, un-predicted sensory burst

