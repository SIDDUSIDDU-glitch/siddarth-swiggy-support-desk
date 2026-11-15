# Swiggy Support Desk AI Knowledge Assistant — Phased Implementation Plan

## Overview
This implementation plan organizes the development, testing, tuning, and auditing of the Swiggy Support Desk AI Knowledge Assistant into five structured, dependency-ordered phases. Each phase delivers a vertical slice of verified functionality.

---

## Phase 1: Knowledge Base and Initial System Prompt Design (Part A)
- **Objective:** Establish the curated synthetic SOP source of truth, construct the 6-part system instruction block with embedded worked examples, and conduct baseline grounding comparative experiments.
- **User-Visible Outcome:** A complete, reproducible AI Studio prompt setup and an empirical 3-way comparative evaluation demonstrating the risks of ungrounded generation.
- **Requirements Covered:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06.
- **Implementation Slices:**
  - *Slice 1.1:* Author `swiggy_support_sop_sheet.txt` containing clauses `SP1`–`SP12` strictly.
  - *Slice 1.2:* Construct initial 6-part System Prompt in `prompt_v1.txt` (Role, Task, Scope, Format, Tone, Guardrails, with 3 distinct non-test-suite worked examples).
  - *Slice 1.3:* Run comparative questions Qa, Qb, Qc across Ungrounded, NotebookLM, and Configured setups.
  - *Slice 1.4:* Execute Specific Safety Check, Leading Question Check, and Cross-Verification Check, and draft comparative synthesis.
- **Verification & Tests:**
  - Automated clause count verification (must equal exactly 12 clauses).
  - Word count verification on worked examples ($\le 80$ words body, $\le 25$ words summary).
- **Completion Criteria:** A1, A2, and A3 fully satisfied and verified.

---

## Phase 2: Test Suite Execution & Diagnostic Prompt Tuning (Part B)
- **Objective:** Execute the fixed 20-message synthetic test suite against the initial assistant, log detailed observations, diagnose failure modes, refine instructions into Version 2, and achieve 100% test pass rate.
- **User-Visible Outcome:** 20-row B1 audit log, detailed failure taxonomy and diagnosis, revised instruction block, and final 20/20 PASS evaluation table.
- **Requirements Covered:** FR-01, FR-02, FR-03, FR-04, FR-05, FR-06.
- **Implementation Slices:**
  - *Slice 2.1:* Run initial 20 test messages, capturing verbatim responses, cited clauses, word counts, and evaluation columns.
  - *Slice 2.2:* Diagnose any failure modes (status mismatches, clause omissions, word count overflow, trigger ambiguities).
  - *Slice 2.3:* Formulate Revised Prompt (`prompt_v2.txt`) with explicit clause pairing and edge-case strengthening.
  - *Slice 2.4:* Re-run all 20 test messages; capture final-run log; verify messages 16–20 verbatim replies.
  - *Slice 2.5:* Evaluate hand-off quality table for messages 16–20 (4 checks per message + 80-word human agent boundary paragraph).
  - *Slice 2.6:* Perform B4 figure audit across messages 1–12 (extract $\ge 8$ figures, verify clauses, prove 0 computed rupee refund figures).
- **Verification & Tests:**
  - Python test runner validating word counts, format lines, and forbidden rupee refund calculations.
  - 100% pass rate achieved on final run ($20/20$).
- **Completion Criteria:** B1, B2, B3, and B4 fully satisfied.

---

## Phase 3: Historical V0 Log Analysis & Spreadsheet Engine (Part C1–C3)
- **Objective:** Process the 40-row synthetic `Pilot_Log` (V0), implement helper columns H–N using robust Excel formulas, compute operational metrics M1–M7, generate Pivot Tables 1–3, and design the Dashboard.
- **User-Visible Outcome:** Deterministic calculation tables, verified formula text, pivot table cross-tabulations, and color-scale analysis.
- **Requirements Covered:** FR-07.
- **Implementation Slices:**
  - *Slice 3.1:* Build `scratch/check_v0_metrics.py` to calculate helper columns, totals, metrics M1–M7, and SUMIF/SUMIFS.
  - *Slice 3.2:* Generate 40-row helper table and verify exact totals against manual / Python baselines.
  - *Slice 3.3:* Generate Pivot 1 (Category $\times$ Verdict), Pivot 2 (Expected $\times$ Actual), and Pivot 3 (Average Hallucinations by Category).
  - *Slice 3.4:* Document color-scale inversion analysis for Pivot 3 and draft Dashboard specification (KPI tiles and chart rationale).
- **Verification & Tests:**
  - Reconcile grand totals (Pivot 1 = 40, Pivot 2 = 40).
  - Verify SUMIF category sums equal total invented claims ($3 + 0 + 1 + 0 + 2 = 6$).
- **Completion Criteria:** C1, C2, and C3 fully satisfied.

---

## Phase 4: Final Run Auditing, Verification & Operations Report (Part C4–C6)
- **Objective:** Calculate metrics M1–M7 on the final run (`My_Run`), execute independent verification checks, prompt an external LLM for formula validation, and author the executive reliability report.
- **User-Visible Outcome:** Side-by-side KPI comparison table against target thresholds, independent verification log, and $\le 300$-word executive briefing to the Operations Lead.
- **Requirements Covered:** FR-07.
- **Implementation Slices:**
  - *Slice 4.1:* Calculate M1–M7 on `My_Run` (20 rows) and populate comparative target table.
  - *Slice 4.2:* Conduct independent recounts for M1, M4, and M6 via filtering logic.
  - *Slice 4.3:* Run specific AI formula generation prompt and document cross-verification results.
  - *Slice 4.4:* Author the concise, evidence-backed executive report ($\le 300$ words) fulfilling all five mandate requirements.
- **Verification & Tests:**
  - Verify word count of C6 report is strictly $\le 300$ words.
  - Verify exact denominator and percentage figures match throughout.
- **Completion Criteria:** C4, C5, and C6 fully satisfied.

---

## Phase 5: Master Deliverable Assembly & Quality Gate
- **Objective:** Compile the complete, unified pilot report document (`Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md`) adhering strictly to the required heading sequence and submission guidelines.
- **User-Visible Outcome:** A single, self-contained, publication-ready document ready for immediate review or Google Docs conversion.
- **Completion Checklist:**
  - [x] Text-only deliverable, no external unauthorized links.
  - [x] Headings ordered: Part A, Part B, Part C with task labels A1–C6.
  - [x] Every table rendered as a real markdown table.
  - [x] Zero placeholders, zero truncated fields.
  - [x] All synthetic safety guidelines strictly observed.
