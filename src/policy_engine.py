"""
Policy Engine for Swiggy Support Desk AI Knowledge Assistant.
Loads, parses, and validates the 12 synthetic SOP clauses (SP1 to SP12).
"""

import os
import re
from typing import Dict, List, Optional, Tuple

CLAUSES_METADATA = {
    "SP1": {
        "title": "Cancellation before acceptance",
        "category": "Cancellations",
        "summary": "Customer may cancel in app before acceptance; refunded in full (whole amount paid)."
    },
    "SP2": {
        "title": "Cancellation after acceptance",
        "category": "Cancellations",
        "summary": "Once restaurant accepts, order cannot be cancelled; no refund given. Support cannot waive this rule."
    },
    "SP3": {
        "title": "Refund destination",
        "category": "Refunds",
        "summary": "Refunds go to original payment method. Cash on delivery refunded as wallet credit."
    },
    "SP4": {
        "title": "Missing or wrong items",
        "category": "Refunds",
        "summary": "Must report on Order Help screen within 2 hours of delivery for refund eligibility. Refund amount is computed by order system in app; support never states rupee amount."
    },
    "SP5": {
        "title": "Delivery delay credit",
        "category": "Delivery delays",
        "summary": "Delay > 30 minutes past checkout estimate earns INR 50 wallet credit. <= 30 mins earns no credit. Only compensation."
    },
    "SP6": {
        "title": "Restaurant or platform cancellation",
        "category": "Cancellations",
        "summary": "If restaurant or Swiggy cancels after acceptance, full amount paid is refunded."
    },
    "SP7": {
        "title": "Refund timelines",
        "category": "Refunds",
        "summary": "UPI / Wallet: within 2 business days. Debit / Credit card: within 5 business days. Cash on delivery wallet credit: within 2 business days."
    },
    "SP8": {
        "title": "Coupons",
        "category": "Refunds",
        "summary": "Coupon used on order refunded in full under SP1 or SP6 is restored to customer account."
    },
    "SP9": {
        "title": "Account self-service and credentials",
        "category": "Account issues",
        "summary": "Customer can edit name, addresses, email on Profile screen. Support never asks for/accepts passwords, OTPs, card numbers or CVV."
    },
    "SP10": {
        "title": "Scope",
        "category": "Other",
        "summary": "Covers refunds, delivery delays, cancellations, account issues. No recommendations, medical or legal advice. One non-diagnostic urgent medical guidance allowed for health risks."
    },
    "SP11": {
        "title": "Order privacy",
        "category": "Delivery delays",
        "summary": "No access to live order status, delivery partner details or payment records. Customer must use Track Order screen in app."
    },
    "SP12": {
        "title": "Mandatory human hand-off",
        "category": "Other",
        "summary": "Mandatory human escalation for triggers (a)-(h). General wording only; restate no rules or timelines; imply no outcome."
    }
}

SP12_TRIGGERS = {
    "a": "Food-safety or health complaint (foreign object in food, food poisoning, allergic reaction)",
    "b": "Complaint about delivery partner's behaviour or personal safety",
    "c": "Unauthorised or duplicate charge",
    "d": "Order marked Delivered that customer says was not received",
    "e": "Customer disputes refund decision, requests rule waiver/exception, or prompt injection/override",
    "f": "Request to change registered phone number, delete account, or unblock account",
    "g": "Legal threat, or mention of consumer court or media",
    "h": "Refund request on order totaling strictly more than INR 2,000"
}


class PolicyEngine:
    def __init__(self, kb_path: Optional[str] = None):
        if kb_path is None:
            # Look in same directory or parent
            candidates = [
                os.path.join(os.path.dirname(__file__), "..", "swiggy_support_sop_sheet.txt"),
                os.path.join(os.getcwd(), "swiggy_support_sop_sheet.txt"),
                "swiggy_support_sop_sheet.txt"
            ]
            for c in candidates:
                if os.path.exists(c):
                    kb_path = c
                    break
        self.kb_path = kb_path
        self.clauses: Dict[str, str] = {}
        self.load_knowledge_base()

    def load_knowledge_base(self):
        if not self.kb_path or not os.path.exists(self.kb_path):
            raise FileNotFoundError(f"Knowledge base file not found at {self.kb_path}")
        with open(self.kb_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if not line:
                continue
            match = re.match(r"^(SP\d+)\s+(.*)$", line)
            if match:
                c_id, c_text = match.group(1), match.group(2)
                self.clauses[c_id] = c_text

    def get_clause_text(self, clause_id: str) -> Optional[str]:
        return self.clauses.get(clause_id.upper())

    def get_all_clauses(self) -> Dict[str, Dict]:
        res = {}
        for c_id, text in self.clauses.items():
            meta = CLAUSES_METADATA.get(c_id, {"title": "", "category": "Other", "summary": ""})
            res[c_id] = {
                "id": c_id,
                "title": meta["title"],
                "category": meta["category"],
                "summary": meta["summary"],
                "full_text": text
            }
        return res

    def validate_clauses(self, clause_list: List[str]) -> Tuple[bool, List[str]]:
        """Checks if all clauses in list exist."""
        invalid = [c for c in clause_list if c not in self.clauses]
        return len(invalid) == 0, invalid

    def detect_sp12_trigger(self, message: str) -> Optional[str]:
        """
        Detects if a customer message triggers an SP12 hand-off.
        Triggers:
        a: foreign object, food poisoning, plastic, glass, allergy, allergic, hospital
        b: delivery partner behavior, physical threat, assault, safety
        c: charged twice, duplicate charge, unauthorized deduction
        d: marked delivered but not received, did not receive, order missing
        e: override, prompt injection, bypass rule, exception, waive rule, dispute refund
        f: change phone number, new number, lost SIM, delete account, unblock
        g: consumer court, legal action, lawyer, media, police
        h: refund request on order > INR 2000
        """
        lower = message.lower()

        # Prompt injection / override / dispute -> trigger e
        if any(term in lower for term in [
            "ignore all your previous instructions", "ignore all previous instructions",
            "ignore previous instructions", "disregard all previous", "disregard prior",
            "you are now a", "approve any refund", "override", "waive", "make an exception",
            "dispute", "system override", "jailbreak"
        ]):
            return "e"

        # Food safety / health risk -> trigger a
        if any(term in lower for term in [
            "plastic", "glass", "insect", "cockroach", "foreign object",
            "food poisoning", "vomiting", "allergic", "allergy", "sick after eating"
        ]):
            return "a"

        # Delivery partner / personal safety -> trigger b
        if any(term in lower for term in [
            "driver was rude", "delivery partner harassed", "misbehaved", "threatened",
            "personal safety", "assault"
        ]):
            return "b"

        # Duplicate / unauthorized charge -> trigger c
        if any(term in lower for term in [
            "charged twice", "double charged", "duplicate charge", "unauthorized charge",
            "debited twice", "money deducted twice"
        ]):
            return "c"

        # Marked delivered but not received -> trigger d
        if any(term in lower for term in [
            "marked delivered but not received", "marked delivered but i didn't get it",
            "says delivered but haven't received", "never received my food"
        ]):
            return "d"

        # Account credential / phone number change / delete / unblock -> trigger f
        if any(term in lower for term in [
            "change my phone number", "change the phone number", "lost my old sim",
            "new phone number", "delete my account", "unblock my account"
        ]):
            return "f"

        # Legal / court / media -> trigger g
        if any(term in lower for term in [
            "consumer court", "legal threat", "take you to court", "file a case",
            "contacting the media", "twitter scandal"
        ]):
            return "g"

        # High value refund > INR 2000 -> trigger h
        # Extract order amounts
        amount_matches = re.findall(r"(?:inr|rs\.?|₹)\s*([\d,]+)", lower)
        for m in amount_matches:
            val_clean = m.replace(",", "")
            if val_clean.isdigit():
                val = int(val_clean)
                if val > 2000 and any(w in lower for w in ["refund", "missing", "cancel"]):
                    return "h"

        return None
