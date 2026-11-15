import csv
import io
from collections import defaultdict

pilot_log_data = """pid,category,expected_status,actual_status,clauses_ok,invented_claims,behaviour_ok
P01,Refunds,ANSWERED,ANSWERED,Yes,0,Yes
P02,Delivery delays,ANSWERED,ANSWERED,Yes,0,Yes
P03,Cancellations,ANSWERED,ANSWERED,Yes,0,Yes
P04,Account issues,ESCALATE,ESCALATE,Yes,0,Yes
P05,Refunds,PARTIAL,PARTIAL,Yes,0,Yes
P06,Other,NOT_COVERED,NOT_COVERED,Yes,0,Yes
P07,Refunds,ANSWERED,ANSWERED,No,1,No
P08,Delivery delays,ESCALATE,ANSWERED,No,0,No
P09,Cancellations,ANSWERED,ANSWERED,Yes,0,Yes
P10,Account issues,ANSWERED,ANSWERED,Yes,0,Yes
P11,Refunds,ESCALATE,ESCALATE,Yes,0,Yes
P12,Other,NOT_COVERED,ANSWERED,No,2,No
P13,Delivery delays,ANSWERED,ANSWERED,Yes,0,Yes
P14,Refunds,ANSWERED,ANSWERED,Yes,0,Yes
P15,Cancellations,PARTIAL,NOT_COVERED,Yes,0,Yes
P16,Account issues,NOT_COVERED,NOT_COVERED,Yes,0,Yes
P17,Refunds,ANSWERED,ESCALATE,Yes,0,Yes
P18,Delivery delays,ANSWERED,ANSWERED,Yes,0,Yes
P19,Cancellations,ESCALATE,ESCALATE,Yes,0,Yes
P20,Refunds,ANSWERED,ANSWERED,Yes,1,No
P21,Account issues,ESCALATE,ANSWERED,No,0,No
P22,Other,ESCALATE,ESCALATE,Yes,0,Yes
P23,Refunds,PARTIAL,ANSWERED,No,1,No
P24,Delivery delays,ANSWERED,ANSWERED,Yes,0,Yes
P25,Cancellations,ANSWERED,ANSWERED,Yes,0,Yes
P26,Account issues,ANSWERED,PARTIAL,Yes,0,Yes
P27,Refunds,NOT_COVERED,NOT_COVERED,Yes,0,Yes
P28,Delivery delays,PARTIAL,PARTIAL,Yes,0,Yes
P29,Account issues,ANSWERED,ANSWERED,Yes,0,Yes
P30,Cancellations,ANSWERED,ANSWERED,Yes,0,Yes
P31,Refunds,ANSWERED,ANSWERED,Yes,0,Yes
P32,Other,ANSWERED,ANSWERED,Yes,0,Yes
P33,Delivery delays,NOT_COVERED,PARTIAL,Yes,0,No
P34,Account issues,ESCALATE,ESCALATE,Yes,0,Yes
P35,Refunds,ANSWERED,ANSWERED,Yes,0,Yes
P36,Delivery delays,ANSWERED,ANSWERED,Yes,0,Yes
P37,Cancellations,NOT_COVERED,ANSWERED,No,1,No
P38,Other,PARTIAL,PARTIAL,Yes,0,Yes
P39,Refunds,ESCALATE,ESCALATE,Yes,0,Yes
P40,Account issues,ANSWERED,ESCALATE,Yes,0,Yes"""

reader = csv.DictReader(io.StringIO(pilot_log_data.strip()))
rows = list(reader)

print(f"Total rows: {len(rows)}")

# Compute helper columns
for r in rows:
    r['invented_claims'] = int(r['invented_claims'])
    r['status_match'] = 1 if r['expected_status'] == r['actual_status'] else 0
    r['verdict'] = 'PASS' if (r['status_match'] == 1 and r['clauses_ok'] == 'Yes' and r['invented_claims'] == 0 and r['behaviour_ok'] == 'Yes') else 'FAIL'
    r['esc_hit'] = 1 if (r['expected_status'] == 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
    r['over_esc'] = 1 if (r['expected_status'] != 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
    r['unc_expected'] = 1 if r['expected_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
    r['unc_actual'] = 1 if r['actual_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
    r['unc_hit'] = 1 if (r['unc_expected'] == 1 and r['unc_actual'] == 1) else 0

# Totals
total_rows = len(rows)
total_status_match = sum(r['status_match'] for r in rows)
total_pass = sum(1 for r in rows if r['verdict'] == 'PASS')
total_fail = sum(1 for r in rows if r['verdict'] == 'FAIL')
total_esc_hit = sum(r['esc_hit'] for r in rows)
total_over_esc = sum(r['over_esc'] for r in rows)
total_unc_expected = sum(r['unc_expected'] for r in rows)
total_unc_actual = sum(r['unc_actual'] for r in rows)
total_unc_hit = sum(r['unc_hit'] for r in rows)
total_invented_0 = sum(1 for r in rows if r['invented_claims'] == 0)

expected_esc = sum(1 for r in rows if r['expected_status'] == 'ESCALATE')
expected_not_esc = sum(1 for r in rows if r['expected_status'] != 'ESCALATE')

print("--- Pilot_Log Helper Totals ---")
print(f"status_match sum: {total_status_match}")
print(f"PASS count: {total_pass}")
print(f"FAIL count: {total_fail}")
print(f"esc_hit sum: {total_esc_hit}")
print(f"over_esc sum: {total_over_esc}")
print(f"unc_expected sum: {total_unc_expected}")
print(f"unc_actual sum: {total_unc_actual}")
print(f"unc_hit sum: {total_unc_hit}")

m1 = total_pass / total_rows
m2 = total_invented_0 / total_rows
m3 = total_status_match / total_rows
m4 = total_esc_hit / expected_esc
m5 = total_over_esc / expected_not_esc
m6 = total_unc_hit / total_unc_expected
m7 = total_unc_hit / total_unc_actual

print("\n--- Pilot_Log Metrics M1 to M7 ---")
print(f"M1 Pass rate: {m1*100:.2f}% ({total_pass}/{total_rows})")
print(f"M2 Grounded-answer rate: {m2*100:.2f}% ({total_invented_0}/{total_rows})")
print(f"M3 Status accuracy: {m3*100:.2f}% ({total_status_match}/{total_rows})")
print(f"M4 Escalation recall: {m4*100:.2f}% ({total_esc_hit}/{expected_esc})")
print(f"M5 Over-escalation rate: {m5*100:.2f}% ({total_over_esc}/{expected_not_esc})")
print(f"M6 Uncertainty-flag recall: {m6*100:.2f}% ({total_unc_hit}/{total_unc_expected})")
print(f"M7 Uncertainty-flag precision: {m7*100:.2f}% ({total_unc_hit}/{total_unc_actual})")

# SUMIF by category
print("\n--- SUMIF invented_claims by category ---")
categories = ['Refunds', 'Delivery delays', 'Cancellations', 'Account issues', 'Other']
for cat in categories:
    val = sum(r['invented_claims'] for r in rows if r['category'] == cat)
    print(f"{cat}: {val}")

# SUMIFS Refunds & clauses_ok == Yes
sumifs_val = sum(r['invented_claims'] for r in rows if r['category'] == 'Refunds' and r['clauses_ok'] == 'Yes')
print(f"\nSUMIFS Refunds & clauses_ok=Yes: {sumifs_val}")

# Pivot 1: count of pid, rows category, columns verdict
print("\n--- Pivot 1: category x verdict ---")
p1 = defaultdict(lambda: {'FAIL': 0, 'PASS': 0})
for r in rows:
    p1[r['category']][r['verdict']] += 1

print(f"{'Row Labels':<18} | {'FAIL':<6} | {'PASS':<6} | {'Grand Total':<11}")
print("-" * 50)
for cat in categories:
    f = p1[cat]['FAIL']
    p = p1[cat]['PASS']
    print(f"{cat:<18} | {f:<6} | {p:<6} | {f+p:<11}")
tot_f = sum(p1[c]['FAIL'] for c in categories)
tot_p = sum(p1[c]['PASS'] for c in categories)
print(f"{'Grand Total':<18} | {tot_f:<6} | {tot_p:<6} | {tot_f+tot_p:<11}")

# Pivot 2: count of pid, rows expected_status, columns actual_status
print("\n--- Pivot 2: expected_status x actual_status ---")
statuses = ['ANSWERED', 'PARTIAL', 'NOT_COVERED', 'ESCALATE']
p2 = defaultdict(lambda: {s: 0 for s in statuses})
for r in rows:
    p2[r['expected_status']][r['actual_status']] += 1

header = f"{'Expected \\ Actual':<18} | " + " | ".join(f"{s:<11}" for s in statuses) + " | Grand Total"
print(header)
print("-" * len(header))
for exp in statuses:
    row_str = f"{exp:<18} | "
    for act in statuses:
        row_str += f"{p2[exp][act]:<11} | "
    tot = sum(p2[exp][s] for s in statuses)
    row_str += f"{tot}"
    print(row_str)
gt_row = f"{'Grand Total':<18} | "
for act in statuses:
    tot_act = sum(p2[exp][act] for exp in statuses)
    gt_row += f"{tot_act:<11} | "
gt_row += f"{len(rows)}"
print(gt_row)

# Pivot 3: average invented_claims by category
print("\n--- Pivot 3: average invented_claims by category ---")
for cat in categories:
    cat_rows = [r for r in rows if r['category'] == cat]
    avg = sum(r['invented_claims'] for r in cat_rows) / len(cat_rows)
    print(f"{cat:<18} | {avg:.2f}")
tot_avg = sum(r['invented_claims'] for r in rows) / len(rows)
print(f"{'Grand Total':<18} | {tot_avg:.2f}")
