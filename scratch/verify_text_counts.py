import re

# Let's verify all word counts of the text components
v1_worked_examples = [
    # Ex 1
    "If the restaurant or Swiggy cancels your order after accepting it, the full amount paid is refunded.",
    # Ex 2
    "Support covers refunds, delivery delays, cancellations, and account issues. We do not have information about catering services for large events.",
    # Ex 3
    "A human agent will review your case regarding legal and consumer court mentions.",
    "Customer mentioned taking Swiggy to consumer court over an issue with their order."
]

for i, ex in enumerate(v1_worked_examples):
    print(f"Example {i+1} words: {len(ex.split())}")

# Check B3 80-word paragraph
b3_para = """Following escalation, human agents retain sole authority over critical operational determinations: adjudicating exception requests or policy override waivers when a customer disputes a cancellation decision (SP12(e)), assessing food-safety reports and determining kitchen liability following foreign object contamination (SP12(a)), and verifying high-value refund claims exceeding INR 2,000 alongside bank transaction disputes to authorize disbursements (SP12(c), SP12(h)). Automated assistants must never execute these discretionary waivers or financial authorizations independently."""
print(f"B3 Paragraph words: {len(b3_para.split())}")

# Check C6 report
c6_report = """To: Operations Lead
From: AI Operations Analyst
Subject: Swiggy Support Desk AI Knowledge Assistant — Pilot Reliability Report

### Where the assistant succeeds and fails

The pilot demonstrates significant reliability gains between Version 0 and our final run. Pass rate (M1) increased from 70.00% (28/40) to 100.00% (20/20), groundedness (M2) rose from 87.50% to 100.00%, and escalation recall (M4) achieved the mandatory 100.00% target (5/5) versus 75.00% (6/8) in V0.

Analysis of V0 Pivot 2 reveals two critical failure patterns in off-diagonal cells:
1. **Critical Under-Escalation [Cell (ESCALATE, ANSWERED) = 2 cases (P08, P21)]:** The assistant autonomously answered sensitive incidents (delivery partner safety and unauthorized billing) instead of handing off to human specialists.
2. **Confabulation on Uncovered Scope [Cell (NOT_COVERED, ANSWERED) = 2 cases (P12, P37)]:** The assistant fabricated policies for out-of-scope queries (temperature complaints and packaging fees) rather than declaring uncertainty.

Based on Pivot 1 failure distributions, we recommend deploying the assistant first for **Delivery delays** (0.00 average hallucinations) and **Cancellations before acceptance** (100% policy determinism). Conversely, **Refunds** (accounting for 4 of 12 V0 failures and 3 invented claims) and **Account issues** (3 V0 failures) must remain under human review until multi-turn production evaluation is complete.

The assistant must never take these three operational decisions autonomously:
1. **Waiving cancellation restrictions** after restaurant acceptance (SP2, SP12(e)).
2. **Calculating or promising rupee refund amounts** for missing items (SP4).
3. **Authorizing refund claims exceeding INR 2,000** or resolving unauthorized charge disputes (SP12(c), SP12(h)).

**Post-Launch Monitoring:**
Track **Escalation Recall (M4)** with a strict alert threshold of **< 100.00%**. Any drop below 100% indicates that a high-risk safety, legal, or financial case bypassed human review, creating unacceptable customer harm and operational liability."""

print(f"C6 Report words: {len(c6_report.split())}")
