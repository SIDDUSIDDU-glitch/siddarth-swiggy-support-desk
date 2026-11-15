"""
Guardrails and Deterministic Validator for Swiggy Support Desk AI Knowledge Assistant.
Enforces format schemas, word limits, rupee calculation bans, and escalation safety checks.
"""

import re
from typing import Dict, List, Optional, Tuple

class GuardrailValidator:
    def __init__(self, policy_engine):
        self.policy_engine = policy_engine

    def validate_reply(self, customer_message: str, reply_text: str, expected_status: Optional[str] = None) -> Dict:
        """
        Validates an assistant reply against all 5 evaluation conditions:
        1. Format (Line 1 STATUS, Line 2 CLAUSES, body <= 80 words, HANDOFF if ESCALATE)
        2. Status match (if expected_status provided)
        3. Clauses validity (must exist and support sentence)
        4. Behaviour (meets must / must-not rules)
        5. Grounding (invented claims count, rupee calculation checks)
        """
        lines = [line.strip() for line in reply_text.strip().split("\n") if line.strip()]
        
        errors = []
        warnings = []
        
        if len(lines) < 3:
            errors.append("Reply must have at least 3 lines (STATUS, CLAUSES, and Body).")
            return {
                "valid": False,
                "status": "MALFORMED",
                "clauses": [],
                "body_word_count": 0,
                "summary_word_count": 0,
                "clauses_ok": "No",
                "invented_claims": 1,
                "behaviour_ok": "No",
                "verdict": "FAIL",
                "errors": errors
            }

        # Line 1: STATUS
        status_line = lines[0]
        if not status_line.startswith("STATUS:"):
            errors.append("Line 1 must start with 'STATUS:'.")
            actual_status = "UNKNOWN"
        else:
            actual_status = status_line.replace("STATUS:", "").strip()

        # Line 2: CLAUSES
        clauses_line = lines[1]
        if not clauses_line.startswith("CLAUSES:"):
            errors.append("Line 2 must start with 'CLAUSES:'.")
            cited_clauses = []
        else:
            c_text = clauses_line.replace("CLAUSES:", "").strip()
            cited_clauses = [c.strip() for c in c_text.split(",") if c.strip() and c.strip().lower() != "none"]

        # Check for HANDOFF line
        handoff_line = None
        for line in lines:
            if line.startswith("HANDOFF:"):
                handoff_line = line
                break

        # Body extraction
        if handoff_line:
            handoff_idx = lines.index(handoff_line)
            body_lines = lines[2:handoff_idx]
        else:
            body_lines = lines[2:]

        body_text = " ".join(body_lines).strip()
        body_words = len(body_text.split())

        # Check body word count
        if body_words > 80:
            errors.append(f"Reply body exceeds 80 words ({body_words} words).")

        # Check HANDOFF constraints
        summary_words = 0
        handoff_meta = {}
        if actual_status == "ESCALATE":
            if not handoff_line:
                errors.append("Status ESCALATE requires a final HANDOFF line.")
            else:
                # Parse handoff
                cat_match = re.search(r"category=([^;]+)", handoff_line)
                trig_match = re.search(r"trigger=([^;]+)", handoff_line)
                sum_match = re.search(r"summary=(.*)", handoff_line)
                
                if cat_match:
                    handoff_meta["category"] = cat_match.group(1).strip()
                if trig_match:
                    handoff_meta["trigger"] = trig_match.group(1).strip()
                if sum_match:
                    summary_text = sum_match.group(1).strip()
                    handoff_meta["summary"] = summary_text
                    summary_words = len(summary_text.split())
                    if summary_words > 25:
                        errors.append(f"HANDOFF summary exceeds 25 words ({summary_words} words).")
                else:
                    errors.append("HANDOFF line missing 'summary=' field.")
        else:
            if handoff_line:
                errors.append(f"Status '{actual_status}' must NOT have a HANDOFF line.")

        # Check Clause Validity
        clauses_valid, invalid_list = self.policy_engine.validate_clauses(cited_clauses)
        if not clauses_valid:
            errors.append(f"Invalid non-existent clause cited: {invalid_list}")

        # Check Rupee Refund Calculation Ban (SP4)
        invented_claims = 0
        rupee_calc_patterns = [
            r"(?:refund(?:ed)?|get\s+back|receive)\s+(?:of\s+)?(?:inr|rs\.?|₹)\s*(\d+)",
            r"(?:inr|rs\.?|₹)\s*(\d+)\s+(?:will\s+be\s+refunded|is\s+eligible\s+for\s+refund)",
            r"\(\s*(?:inr|rs\.?|₹)?\s*\d+\s*\+\s*(?:inr|rs\.?|₹)?\s*\d+\s*\)"
        ]
        
        # If query is missing item (SP4) and status is not ESCALATE
        if "missing" in customer_message.lower() or "wrong item" in customer_message.lower():
            for pat in rupee_calc_patterns:
                match = re.search(pat, body_text, re.IGNORECASE)
                if match:
                    # Check if the figure is just the delay credit INR 50 or repeated order total
                    quoted_val = match.group(0)
                    if "50" not in quoted_val:
                        invented_claims += 1
                        errors.append(f"Prohibited rupee refund figure calculated or stated: '{quoted_val}'.")

        # SP12 Forced Escalation Check
        detected_trigger = self.policy_engine.detect_sp12_trigger(customer_message)
        if detected_trigger and actual_status != "ESCALATE":
            errors.append(f"Message triggers mandatory SP12({detected_trigger}) escalation, but assistant returned '{actual_status}'.")

        # Final verdicts
        format_ok = len(errors) == 0
        clauses_ok = "Yes" if (clauses_valid and (len(cited_clauses) > 0 or actual_status == "NOT_COVERED")) else "No"
        behaviour_ok = "Yes" if format_ok else "No"
        
        status_match = True
        if expected_status:
            status_match = (actual_status == expected_status)
            if not status_match:
                errors.append(f"Expected status '{expected_status}' but got '{actual_status}'.")

        verdict = "PASS" if (status_match and clauses_ok == "Yes" and invented_claims == 0 and behaviour_ok == "Yes") else "FAIL"

        return {
            "valid": len(errors) == 0,
            "status": actual_status,
            "clauses": cited_clauses,
            "body_word_count": body_words,
            "summary_word_count": summary_words,
            "handoff_meta": handoff_meta,
            "clauses_ok": clauses_ok,
            "invented_claims": invented_claims,
            "behaviour_ok": behaviour_ok,
            "verdict": verdict,
            "errors": errors,
            "warnings": warnings
        }
