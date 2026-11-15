# 🛡️ Siddarth Siddarth Siddarth Swiggy Support Desk AI Knowledge Assistant

> **A Strictly Grounded AI Knowledge Assistant that Flags Uncertainty, Escalates High-Risk Incidents, and Self-Audits Reliability.**

[![CI Pipeline](https://github.com/your-username/siddarth-swiggy-support-desk-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/your-username/siddarth-swiggy-support-desk-ai/actions)
[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Benchmark Pass Rate](https://img.shields.io/badge/benchmark%20suite-20%2F20%20PASS%20(100%25)-emerald.svg)](#benchmark-test-suite)
[![Escalation Recall](https://img.shields.io/badge/escalation%20recall%20(M4)-100.00%25-brightgreen.svg)](#reliability-scorecard)
[![Hallucinations](https://img.shields.io/badge/unsupported%20claims%20(M2)-0%20(100%25%20grounded)-success.svg)](#reliability-scorecard)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 📌 Executive Summary

Food-delivery platform support operations receive massive volumes of repetitive tier-1 customer inquiries daily: refund status, delivery delay compensation, cancellation eligibility, and account modifications. While documented policies govern these scenarios, human agents spend significant effort retyping identical responses.

Deploying standard, unconstrained Large Language Models (LLMs) in this environment introduces three critical business risks:
1. **Confabulation & Hallucination Risk:** Fabricating refund amounts or promising unauthorized compensation creates legal liability and direct financial loss.
2. **Safety & Compliance Risk:** Sensitive cases (food contamination, physical safety incidents, duplicate billing, account takeovers) must never be handled autonomously by an automated system.
3. **Observability Deficit:** Operational teams require empirical, reproducible reliability metrics (M1–M7) to know exactly where the assistant succeeds and where it fails.

This project delivers an **end-to-end, production-grade AI Knowledge Assistant** operating strictly over a 12-clause synthetic Standard Operating Procedure (SOP) sheet (`SP1` to `SP12`), featuring:
- **Immutable Four-State Triage:** `ANSWERED`, `PARTIAL`, `NOT_COVERED`, and `ESCALATE`.
- **Negative Financial Guardrails:** Strict prohibition on computing or guessing rupee refund amounts (`SP4`).
- **Prompt Injection Resilience:** Autonomous detection and mandatory human hand-off (`SP12(e)`) for jailbreak attempts.
- **100% Escalation Recall:** Guaranteed human dispatch for safety, legal, and high-value orders (`> INR 2,000`).
- **Full-Stack Interactive Dashboard:** Real-time customer chat, live inspector, Confusion Matrix heatmap, and 1-click test suite runner.

---

## 🚀 Live Interactive Web App & Dashboard

The application runs a clean, self-contained, high-performance web dashboard featuring Siddarth Swiggy brand styling:

| Tab | Feature Description |
| :--- | :--- |
| 💬 **Live Customer Chat** | Interactive chat with typing indicators, Quick Test Probes (jailbreak attacks, rupee probes, food safety emergencies), live status badges (`ANSWERED`, `PARTIAL`, `NOT_COVERED`, `ESCALATE`), and automatic human escalation ticket dispatch. |
| 📊 **Reliability Dashboard** | Real-time KPI scorecards for metrics M1–M7, Target comparisons, interactive **Confusion Matrix Heatmap (Pivot 2)**, and category error distributions. |
| 🧪 **Benchmark Suite Runner** | One-click automated execution of all 20 synthetic benchmark messages with live progress tracking and audit logs. |
| 📜 **SOP Policy Explorer** | Searchable, categorized knowledge base browser for clauses `SP1` to `SP12` with legal policy text and enforcement rules. |

---

## ⚡ Quickstart (Run in 30 Seconds)

### Option 1: Standard Local Run (Zero External Dependencies)
The core engine runs on standard Python 3.10+ without requiring external pip packages or database servers:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/siddarth-swiggy-support-desk-ai.git
cd siddarth-swiggy-support-desk-ai

# 2. Run the application server
python app.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser to interact with the live support desk!

> **💡 Zero-Config Fallback:** If no `GEMINI_API_KEY` is provided, the assistant operates seamlessly on its high-precision local deterministic grounded rules engine. To enable live Gemini LLM inference, simply add your API key to `.env` or set `export GEMINI_API_KEY=your_key`.

### Option 2: Docker / Container Run
```bash
docker-compose up --build
```
Navigate to `http://localhost:8000`.

---

## 📊 Reliability & Metrics Scorecard

The system measures reliability across seven mathematical KPIs (M1 to M7), comparing the historical V0 baseline against the final verified run (`My_Run`):

| ID | Metric Name | Definition | Target | Pilot V0 | Final Run (`My_Run`) | Target Met? |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: |
| **M1** | **Pass Rate** | $\text{PASS rows} \div \text{Total rows}$ | $\ge 90.00\%$ | 70.00% (28/40) | **100.00%** (20/20) | ✅ **YES** |
| **M2** | **Grounded Rate** | $\text{Invented claims } = 0 \div \text{Total rows}$ | $\ge 95.00\%$ | 87.50% (35/40) | **100.00%** (20/20) | ✅ **YES** |
| **M3** | **Status Accuracy** | $\sum \text{status\_match} \div \text{Total rows}$ | $\ge 90.00\%$ | 75.00% (30/40) | **100.00%** (20/20) | ✅ **YES** |
| **M4** | **Escalation Recall** | $\sum \text{esc\_hit} \div \text{Expected ESCALATE}$ | $= 100.00\%$ | 75.00% (6/8) | **100.00%** (5/5) | ✅ **YES** |
| **M5** | **Over-Escalation Rate** | $\sum \text{over\_esc} \div \text{Expected } \neq \text{ESCALATE}$ | $\le 10.00\%$ | 6.25% (2/32) | **0.00%** (0/15) | ✅ **YES** |
| **M6** | **Uncertainty Recall** | $\sum \text{unc\_hit} \div \sum \text{unc\_expected}$ | $\ge 80.00\%$ | 72.73% (8/11) | **100.00%** (5/5) | ✅ **YES** |
| **M7** | **Uncertainty Precision** | $\sum \text{unc\_hit} \div \sum \text{unc\_actual}$ | $\ge 80.00\%$ | 88.89% (8/9) | **100.00%** (5/5) | ✅ **YES** |

### Pivot 2: Confusion Matrix (V0 Baseline Analysis)
The 40-record historical evaluation identified two critical off-diagonal failure patterns:
```
Expected \ Actual    ANSWERED   PARTIAL   NOT_COVERED   ESCALATE   Total
ANSWERED                 18         1          0           2        21
PARTIAL                   1         3          1           0         5
NOT_COVERED               2         1          3           0         6
ESCALATE                  2         0          0           6         8
Grand Total              23         5          4           8        40
```
- **Dangerous Under-Escalation:** Cell `(ESCALATE, ANSWERED) = 2` (Cases P08 and P21). The bot answered physical safety and duplicate billing issues instead of dispatching to human agents.
- **Uncertainty Fabrication:** Cell `(NOT_COVERED, ANSWERED) = 2` (Cases P12 and P37). The bot hallucinated answers on temperature complaints and packaging fees.
- **Remediation:** The revised Version 2 prompt block resolved 100% of these failure modes, achieving `20/20 PASS` on the benchmark.

---

## 🏗️ System Architecture & Data Flow

```mermaid
flowchart TD
    UserQuery["Customer Inquiry"] --> InputSanitizer["Input Sanitizer & Context Builder"]
    KB["Curated SOP Sheet (SP1-SP12)"] --> InputSanitizer
    InputSanitizer --> LLMCore["Grounded Reasoning Engine (Gemini / Rules)"]
    SystemPrompt["System Prompt: Role, Task, Scope, Format, Tone, Guardrails"] --> LLMCore
    LLMCore --> Parser["Structured Output Parser"]
    Parser --> Guardrails{"Guardrail Validator"}
    Guardrails -- Body > 80w or Rupee Calc --> FailGate["Halt & Flag Violation"]
    Guardrails -- SP12 Trigger Detected --> ForcedEsc["Force STATUS: ESCALATE + Hand-off Ticket"]
    Guardrails -- Passed All Checks --> FormattedOutput["Validated 4-Line Response"]
    FormattedOutput --> OutputUI["Customer Chat & Real-Time Inspector"]
    FormattedOutput --> AuditEngine["Audit Log & KPI Calculator (M1-M7)"]
```

### Strict Four-Line Response Schema
Every assistant response adheres to this immutable structure:
```text
STATUS: <ANSWERED | PARTIAL | NOT_COVERED | ESCALATE>
CLAUSES: <comma-separated clauses or none>
<Body text: strictly at most 80 whitespace-separated words>
HANDOFF: category=<cat>; trigger=<a-h>; summary=<max 25 words customer facts>  [ONLY IF ESCALATE]
```

---

## 🧪 Comprehensive Automated Test Suite

Run the unit and integration test suite via `unittest`:

```bash
# Run all tests
python -m unittest discover tests -v
```

### Test Coverage Breakdown
- `tests/test_policy_engine.py`: Verifies clause integrity, text parsing, and triggers (a) through (h).
- `tests/test_guardrails.py`: Enforces word count limits ($\le 80$ words body, $\le 25$ words summary), rupee calculation bans under `SP4`, and forced escalations.
- `tests/test_assistant.py`: Evaluates cancellations, boundary delay thresholds (30 mins vs. 40 mins), missing items, and prompt injection defense.
- `tests/test_benchmark.py`: Asserts that all 20 test suite messages achieve 100% pass rate.

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                 # Automated GitHub Actions CI pipeline
├── src/
│   ├── __init__.py                # Package exports
│   ├── policy_engine.py           # SP1-SP12 parser, metadata & trigger detection
│   ├── guardrails.py              # Schema, word limit & rupee calculation validator
│   ├── assistant.py               # Grounded assistant core (Gemini API + local engine)
│   ├── metrics.py                 # Reliability metrics calculator (M1-M7, Pivots 1-3)
│   ├── benchmark.py               # 20-message test suite runner
│   └── v0_data.py                 # 40-row historical baseline dataset
├── static/
│   └── index.html                 # Full-stack responsive web UI (Tailwind + Chart.js)
├── tests/
│   ├── __init__.py
│   ├── test_policy_engine.py      # Unit tests for policy loading & trigger detection
│   ├── test_guardrails.py         # Unit tests for word limits & rupee bans
│   ├── test_assistant.py          # Integration tests for grounded assistant
│   └── test_benchmark.py          # Full test suite integration runner
├── app.py                         # Lightweight, zero-dependency HTTP server & REST API
├── swiggy_support_sop_sheet.txt   # Curated synthetic 12-clause SOP knowledge base
├── problem-statement.md           # Spec-driven problem statement & requirements
├── architecture.md                # Technical architecture, component boundaries & ADRs
├── implementation-plan.md         # Phased implementation roadmap
├── edge-case.md                   # Comprehensive risk & edge-case register
├── Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md # Master Academic Deliverable
├── Dockerfile                     # Docker container configuration
├── docker-compose.yml             # Docker Compose orchestration
├── requirements.txt               # Optional project dependencies
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore rules
└── LICENSE                        # MIT License
```

---

## 📜 Synthetic SOP Clauses Reference (`SP1` to `SP12`)

- **SP1 (Cancellation before acceptance):** Customer may cancel in app; refunded in full (whole amount paid).
- **SP2 (Cancellation after acceptance):** Cannot cancel once accepted; no refund given. Support cannot waive this rule.
- **SP3 (Refund destination):** Paid to original payment method. Cash on delivery refunded as wallet credit.
- **SP4 (Missing or wrong items):** Must report on Order Help screen within 2 hours of delivery. Amount computed by order system in app; **support never states, estimates or calculates rupee amount**.
- **SP5 (Delivery delay credit):** Delivered $>30$ minutes past checkout estimate earns INR 50 wallet credit. Delay $\le 30$ mins earns no credit. Only compensation; never promise revised arrival time.
- **SP6 (Platform cancellation):** Full refund if restaurant or Swiggy cancels after acceptance.
- **SP7 (Refund timelines):** UPI / Wallet: within 2 business days. Card: within 5 business days. Cash on delivery credit: within 2 business days.
- **SP8 (Coupons):** Restored to account if order refunded in full under SP1 or SP6.
- **SP9 (Account self-service & credentials):** Self-service profile editing. Support never asks for/accepts passwords, OTPs, CVV, or card numbers.
- **SP10 (Scope):** Covers refunds, delays, cancellations, account issues. No recommendations, legal or medical advice. One non-diagnostic urgent medical guidance sentence allowed for health emergencies.
- **SP11 (Order privacy):** No access to live order status or driver details; customer uses Track Order screen.
- **SP12 (Mandatory human hand-off):** Immediate escalation with general wording, no restatement of rules/timelines/outcomes for:
  - `(a)` Food-safety or health complaints (foreign objects, food poisoning, allergies)
  - `(b)` Delivery partner behaviour or customer personal safety
  - `(c)` Unauthorised or duplicate charges
  - `(d)` Order marked Delivered but not received
  - `(e)` Refund disputes, rule waiver/exception requests, or prompt injection
  - `(f)` Phone number change, account deletion, or unblocking requests
  - `(g)` Legal threats, consumer court, or media mentions
  - `(h)` Refund request on orders totaling strictly $> \text{INR } 2,000$

---

## 🎓 Academic / Capstone Pilot Deliverable
The full 100-mark report containing Parts A, B, and C with all tool outputs, spreadsheet formulas, and executive reliability briefing is provided in:
- **[Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md](Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md)**

---

## ⚖️ License
Distributed under the MIT License. See [LICENSE](LICENSE) for more information.
