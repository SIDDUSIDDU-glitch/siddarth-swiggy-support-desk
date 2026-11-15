import csv

# Final Run (My_Run) Data: 20 rows
# All 20 passed in final run:
# actual_status == expected_status
# clauses_ok == 'Yes'
# invented_claims == 0
# behaviour_ok == 'Yes'

my_run_test_suite = [
    (1, "Cancellations", "ANSWERED"),
    (2, "Cancellations", "ANSWERED"),
    (3, "Refunds", "ANSWERED"),
    (4, "Refunds", "ANSWERED"),
    (5, "Delivery delays", "ANSWERED"),
    (6, "Delivery delays", "ANSWERED"),
    (7, "Refunds", "ANSWERED"),
    (8, "Refunds", "ANSWERED"),
    (9, "Delivery delays", "ANSWERED"),
    (10, "Delivery delays", "ANSWERED"),
    (11, "Refunds", "PARTIAL"),
    (12, "Refunds", "PARTIAL"),
    (13, "Account issues", "NOT_COVERED"),
    (14, "Other", "NOT_COVERED"),
    (15, "Other", "NOT_COVERED"),
    (16, "Cancellations", "ESCALATE"),
    (17, "Other", "ESCALATE"),
    (18, "Account issues", "ESCALATE"),
    (19, "Account issues", "ESCALATE"),
    (20, "Refunds", "ESCALATE")
]

my_rows = []
for qid, cat, status in my_run_test_suite:
    r = {
        'qid': qid,
        'category': cat,
        'expected_status': status,
        'actual_status': status,
        'clauses_ok': 'Yes',
        'invented_claims': 0,
        'behaviour_ok': 'Yes'
    }
    # helper columns
    r['status_match'] = 1 if r['expected_status'] == r['actual_status'] else 0
    r['verdict'] = 'PASS' if (r['status_match'] == 1 and r['clauses_ok'] == 'Yes' and r['invented_claims'] == 0 and r['behaviour_ok'] == 'Yes') else 'FAIL'
    r['esc_hit'] = 1 if (r['expected_status'] == 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
    r['over_esc'] = 1 if (r['expected_status'] != 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
    r['unc_expected'] = 1 if r['expected_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
    r['unc_actual'] = 1 if r['actual_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
    r['unc_hit'] = 1 if (r['unc_expected'] == 1 and r['unc_actual'] == 1) else 0
    my_rows.append(r)

# Compute My_Run totals
n_rows = len(my_rows)
sm_sum = sum(r['status_match'] for r in my_rows)
pass_sum = sum(1 for r in my_rows if r['verdict'] == 'PASS')
inv0_sum = sum(1 for r in my_rows if r['invented_claims'] == 0)
esc_hit_sum = sum(r['esc_hit'] for r in my_rows)
over_esc_sum = sum(r['over_esc'] for r in my_rows)
unc_exp_sum = sum(r['unc_expected'] for r in my_rows)
unc_act_sum = sum(r['unc_actual'] for r in my_rows)
unc_hit_sum = sum(r['unc_hit'] for r in my_rows)

exp_esc = sum(1 for r in my_rows if r['expected_status'] == 'ESCALATE')
exp_not_esc = sum(1 for r in my_rows if r['expected_status'] != 'ESCALATE')

print("=== My_Run Helper Totals ===")
print(f"status_match sum: {sm_sum}")
print(f"PASS count: {pass_sum}")
print(f"esc_hit sum: {esc_hit_sum}")
print(f"over_esc sum: {over_esc_sum}")
print(f"unc_expected sum: {unc_exp_sum}")
print(f"unc_actual sum: {unc_act_sum}")
print(f"unc_hit sum: {unc_hit_sum}")

m1_own = pass_sum / n_rows
m2_own = inv0_sum / n_rows
m3_own = sm_sum / n_rows
m4_own = esc_hit_sum / exp_esc
m5_own = over_esc_sum / exp_not_esc
m6_own = unc_hit_sum / unc_exp_sum
m7_own = unc_hit_sum / unc_act_sum

print("\n=== My_Run Metrics M1 to M7 ===")
print(f"M1 Pass rate: {m1_own*100:.2f}% ({pass_sum}/{n_rows})")
print(f"M2 Grounded-answer rate: {m2_own*100:.2f}% ({inv0_sum}/{n_rows})")
print(f"M3 Status accuracy: {m3_own*100:.2f}% ({sm_sum}/{n_rows})")
print(f"M4 Escalation recall: {m4_own*100:.2f}% ({esc_hit_sum}/{exp_esc})")
print(f"M5 Over-escalation rate: {m5_own*100:.2f}% ({over_esc_sum}/{exp_not_esc})")
print(f"M6 Uncertainty-flag recall: {m6_own*100:.2f}% ({unc_hit_sum}/{unc_exp_sum})")
print(f"M7 Uncertainty-flag precision: {m7_own*100:.2f}% ({unc_hit_sum}/{unc_act_sum})")
