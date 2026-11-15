"""
Unit Tests for GuardrailValidator.
"""

import unittest
from src.policy_engine import PolicyEngine
from src.guardrails import GuardrailValidator

class TestGuardrails(unittest.TestCase):
    def setUp(self):
        self.policy = PolicyEngine()
        self.validator = GuardrailValidator(self.policy)

    def test_valid_answered_reply(self):
        msg = "The restaurant has not accepted my order yet. Can I cancel it?"
        reply = (
            "STATUS: ANSWERED\n"
            "CLAUSES: SP1\n"
            "You may cancel your order in the app until the restaurant accepts it. A cancellation before acceptance is refunded in full."
        )
        res = self.validator.validate_reply(msg, reply, expected_status="ANSWERED")
        self.assertTrue(res["valid"])
        self.assertEqual(res["verdict"], "PASS")
        self.assertLessEqual(res["body_word_count"], 80)

    def test_body_word_limit_exceeded(self):
        msg = "Can I cancel?"
        long_body = "word " * 85
        reply = f"STATUS: ANSWERED\nCLAUSES: SP1\n{long_body}"
        res = self.validator.validate_reply(msg, reply)
        self.assertFalse(res["valid"])
        self.assertEqual(res["verdict"], "FAIL")
        self.assertIn("exceeds 80 words", res["errors"][0])

    def test_rupee_calculation_prohibited(self):
        msg = "Missing item from my order. How many rupees do I get back?"
        reply = (
            "STATUS: ANSWERED\n"
            "CLAUSES: SP4\n"
            "You will receive a refund of INR 210 for your missing items computed in the app."
        )
        res = self.validator.validate_reply(msg, reply)
        self.assertEqual(res["invented_claims"], 1)
        self.assertEqual(res["verdict"], "FAIL")

    def test_escalate_requires_handoff_line(self):
        msg = "Found plastic in my food"
        reply = (
            "STATUS: ESCALATE\n"
            "CLAUSES: SP12\n"
            "A human agent will review your case."
        )
        res = self.validator.validate_reply(msg, reply, expected_status="ESCALATE")
        self.assertFalse(res["valid"])
        self.assertIn("requires a final HANDOFF line", str(res["errors"]))

    def test_forced_escalation_enforced(self):
        msg = "Someone charged twice for my INR 380 order"
        reply = (
            "STATUS: ANSWERED\n"
            "CLAUSES: SP7\n"
            "Refunds take 2 business days."
        )
        res = self.validator.validate_reply(msg, reply)
        self.assertFalse(res["valid"])
        self.assertIn("triggers mandatory SP12", str(res["errors"]))

if __name__ == "__main__":
    unittest.main()
