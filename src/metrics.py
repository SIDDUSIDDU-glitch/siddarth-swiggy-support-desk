"""
Reliability Metrics and Spreadsheet Analytics Engine for Swiggy Support Desk.
Computes M1-M7, helper columns, confusion matrix (Pivot 2), and category distributions.
"""

from collections import defaultdict
from typing import Dict, List, Tuple

class ReliabilityMetricsEngine:
    def __init__(self, rows: List[Dict]):
        """
        rows: List of dicts with keys:
        qid/pid, category, expected_status, actual_status, clauses_ok, invented_claims, behaviour_ok
        """
        self.rows = [dict(r) for r in rows]
        self._calculate_helpers()

    def _calculate_helpers(self):
        for r in self.rows:
            r['invented_claims'] = int(r.get('invented_claims', 0))
            r['status_match'] = 1 if r['expected_status'] == r['actual_status'] else 0
            r['verdict'] = 'PASS' if (
                r['status_match'] == 1 and
                r['clauses_ok'] == 'Yes' and
                r['invented_claims'] == 0 and
                r['behaviour_ok'] == 'Yes'
            ) else 'FAIL'
            r['esc_hit'] = 1 if (r['expected_status'] == 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
            r['over_esc'] = 1 if (r['expected_status'] != 'ESCALATE' and r['actual_status'] == 'ESCALATE') else 0
            r['unc_expected'] = 1 if r['expected_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
            r['unc_actual'] = 1 if r['actual_status'] in ['PARTIAL', 'NOT_COVERED'] else 0
            r['unc_hit'] = 1 if (r['unc_expected'] == 1 and r['unc_actual'] == 1) else 0

    def get_helper_totals(self) -> Dict[str, int]:
        return {
            "total_rows": len(self.rows),
            "status_match_sum": sum(r['status_match'] for r in self.rows),
            "pass_count": sum(1 for r in self.rows if r['verdict'] == 'PASS'),
            "fail_count": sum(1 for r in self.rows if r['verdict'] == 'FAIL'),
            "esc_hit_sum": sum(r['esc_hit'] for r in self.rows),
            "over_esc_sum": sum(r['over_esc'] for r in self.rows),
            "unc_expected_sum": sum(r['unc_expected'] for r in self.rows),
            "unc_actual_sum": sum(r['unc_actual'] for r in self.rows),
            "unc_hit_sum": sum(r['unc_hit'] for r in self.rows),
            "invented_zero_count": sum(1 for r in self.rows if r['invented_claims'] == 0)
        }

    def compute_metrics(self) -> Dict[str, Dict]:
        tot = self.get_helper_totals()
        n = tot["total_rows"]
        exp_esc = sum(1 for r in self.rows if r['expected_status'] == 'ESCALATE')
        exp_not_esc = sum(1 for r in self.rows if r['expected_status'] != 'ESCALATE')

        m1 = tot["pass_count"] / n if n else 0.0
        m2 = tot["invented_zero_count"] / n if n else 0.0
        m3 = tot["status_match_sum"] / n if n else 0.0
        m4 = tot["esc_hit_sum"] / exp_esc if exp_esc else 1.0
        m5 = tot["over_esc_sum"] / exp_not_esc if exp_not_esc else 0.0
        m6 = tot["unc_hit_sum"] / tot["unc_expected_sum"] if tot["unc_expected_sum"] else 1.0
        m7 = tot["unc_hit_sum"] / tot["unc_actual_sum"] if tot["unc_actual_sum"] else 1.0

        return {
            "M1": {"id": "M1", "name": "Pass rate", "value": m1, "percent": round(m1 * 100, 2), "num": tot["pass_count"], "den": n, "target": ">= 90%", "meets": m1 >= 0.90},
            "M2": {"id": "M2", "name": "Grounded-answer rate", "value": m2, "percent": round(m2 * 100, 2), "num": tot["invented_zero_count"], "den": n, "target": ">= 95%", "meets": m2 >= 0.95},
            "M3": {"id": "M3", "name": "Status accuracy", "value": m3, "percent": round(m3 * 100, 2), "num": tot["status_match_sum"], "den": n, "target": ">= 90%", "meets": m3 >= 0.90},
            "M4": {"id": "M4", "name": "Escalation recall", "value": m4, "percent": round(m4 * 100, 2), "num": tot["esc_hit_sum"], "den": exp_esc, "target": "= 100%", "meets": m4 >= 1.0},
            "M5": {"id": "M5", "name": "Over-escalation rate", "value": m5, "percent": round(m5 * 100, 2), "num": tot["over_esc_sum"], "den": exp_not_esc, "target": "<= 10%", "meets": m5 <= 0.10},
            "M6": {"id": "M6", "name": "Uncertainty-flag recall", "value": m6, "percent": round(m6 * 100, 2), "num": tot["unc_hit_sum"], "den": tot["unc_expected_sum"], "target": ">= 80%", "meets": m6 >= 0.80},
            "M7": {"id": "M7", "name": "Uncertainty-flag precision", "value": m7, "percent": round(m7 * 100, 2), "num": tot["unc_hit_sum"], "den": tot["unc_actual_sum"], "target": ">= 80%", "meets": m7 >= 0.80}
        }

    def get_pivot1_category_vs_verdict(self) -> Dict:
        """Pivot 1: Rows Category, Columns Verdict."""
        categories = ['Refunds', 'Delivery delays', 'Cancellations', 'Account issues', 'Other']
        res = {c: {"FAIL": 0, "PASS": 0, "Total": 0} for c in categories}
        for r in self.rows:
            cat = r['category']
            verd = r['verdict']
            if cat in res:
                res[cat][verd] += 1
                res[cat]["Total"] += 1
        return res

    def get_pivot2_confusion_matrix(self) -> Dict:
        """Pivot 2: Rows Expected, Columns Actual."""
        statuses = ['ANSWERED', 'PARTIAL', 'NOT_COVERED', 'ESCALATE']
        matrix = {e: {a: 0 for a in statuses} for e in statuses}
        for r in self.rows:
            e = r['expected_status']
            a = r['actual_status']
            if e in matrix and a in matrix[e]:
                matrix[e][a] += 1
        return matrix

    def get_pivot3_avg_invented_claims(self) -> Dict:
        """Pivot 3: Average invented claims by category."""
        categories = ['Refunds', 'Delivery delays', 'Cancellations', 'Account issues', 'Other']
        sums = {c: 0 for c in categories}
        counts = {c: 0 for c in categories}
        for r in self.rows:
            cat = r['category']
            if cat in sums:
                sums[cat] += r['invented_claims']
                counts[cat] += 1
        res = {}
        for c in categories:
            res[c] = round(sums[c] / counts[c], 2) if counts[c] else 0.0
        return res
