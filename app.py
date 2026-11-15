"""
Siddarth Swiggy Support Desk AI Knowledge Assistant — Application Server.
Zero-dependency HTTP server powering the interactive web UI and REST API.
"""

import os
import sys
import json
import urllib.parse
import csv
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from src.assistant import SwiggySupportAssistant
from src.benchmark import BenchmarkRunner
from src.policy_engine import PolicyEngine
from src.metrics import ReliabilityMetricsEngine
from src.v0_data import V0_PILOT_LOG_DATA

HOST = "0.0.0.0"
PORT = 8000

# Shared singletons
assistant = SwiggySupportAssistant()
benchmark_runner = BenchmarkRunner(assistant)
policy_engine = PolicyEngine()
v0_metrics_engine = ReliabilityMetricsEngine(V0_PILOT_LOG_DATA)


def generate_export_csv() -> str:
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(["# SIDDARTH SWIGGY SUPPORT DESK AI - RELIABILITY & AUDIT SPREADSHEET"])
    writer.writerow([])
    
    # 1. Pilot_Log (V0)
    writer.writerow(["# SHEET: Pilot_Log (Historical V0 Baseline - 40 Rows)"])
    v0_engine = ReliabilityMetricsEngine(V0_PILOT_LOG_DATA)
    v0_rows = v0_engine.rows
    headers = ["pid", "category", "expected_status", "actual_status", "clauses_ok", "invented_claims", "behaviour_ok", "status_match", "verdict", "esc_hit", "over_esc", "unc_expected", "unc_actual", "unc_hit"]
    writer.writerow(headers)
    for r in v0_rows:
        writer.writerow([r.get(h, "") for h in headers])
        
    writer.writerow([])
    writer.writerow([])
    
    # 2. My_Run (Final)
    writer.writerow(["# SHEET: My_Run (Final Verified Run - 20 Rows)"])
    runner = BenchmarkRunner()
    bm_res = runner.run_benchmark()
    my_engine = ReliabilityMetricsEngine(bm_res["results"])
    my_rows = my_engine.rows
    my_headers = ["qid", "category", "expected_status", "actual_status", "clauses_ok", "invented_claims", "behaviour_ok", "status_match", "verdict", "esc_hit", "over_esc", "unc_expected", "unc_actual", "unc_hit"]
    writer.writerow(my_headers)
    for r in my_rows:
        writer.writerow([r.get(h, "") for h in my_headers])
        
    writer.writerow([])
    writer.writerow([])
    
    # 3. Metrics Summary
    writer.writerow(["# SHEET: Metrics_Summary (KPIs M1 to M7)"])
    writer.writerow(["Metric_ID", "Metric_Name", "Target", "V0_Pilot_Value", "My_Run_Value", "Meets_Target_V0", "Meets_Target_MyRun"])
    v0_m = v0_engine.compute_metrics()
    my_m = my_engine.compute_metrics()
    for mid in ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]:
        vm = v0_m[mid]
        mm = my_m[mid]
        writer.writerow([
            mid,
            mm["name"],
            mm["target"],
            f"{vm['percent']}% ({vm['num']}/{vm['den']})",
            f"{mm['percent']}% ({mm['num']}/{mm['den']})",
            "Yes" if vm["meets"] else "No",
            "Yes" if mm["meets"] else "No"
        ])
        
    return output.getvalue()


class SupportDeskServer(BaseHTTPRequestHandler):
    def do_HEAD(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        if path in ["/", "/index.html", "/api/download-excel", "/api/download-csv", "/api/download-markdown", "/api/metrics", "/api/benchmark", "/api/clauses", "/api/v0_log"]:
            self.send_response(200)
            if "download-markdown" in path:
                self.send_header("Content-Type", "text/markdown; charset=utf-8")
            elif "download" in path:
                self.send_header("Content-Type", "text/csv; charset=utf-8")
            else:
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        try:
            if path == "/" or path == "/index.html":
                self._serve_file("static/index.html", "text/html; charset=utf-8")
            elif path in ["/api/download-markdown", "/api/report-md"]:
                report_path = "Swiggy_Support_Desk_AI_Knowledge_Assistant_Pilot_Report.md"
                if os.path.exists(report_path):
                    with open(report_path, "rb") as rf:
                        md_content = rf.read()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/markdown; charset=utf-8")
                    self.send_header("Content-Disposition", 'attachment; filename="Siddarth_Swiggy_Support_Desk_Pilot_Report.md"')
                    self.send_header("Content-Length", str(len(md_content)))
                    self.end_headers()
                    self.wfile.write(md_content)
                else:
                    self.send_error(404, "Report file not found")
            elif path in ["/api/download-excel", "/api/download-csv", "/api/export-logs"]:
                csv_content = generate_export_csv().encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/csv; charset=utf-8")
                self.send_header("Content-Disposition", 'attachment; filename="Siddarth_Swiggy_Support_Desk_Reliability_Report.csv"')
                self.send_header("Content-Length", str(len(csv_content)))
                self.end_headers()
                self.wfile.write(csv_content)
            elif path == "/api/clauses":
                self._send_json(policy_engine.get_all_clauses())
            elif path == "/api/benchmark":
                results = benchmark_runner.run_benchmark()
                self._send_json(results)
            elif path == "/api/metrics":
                # Run benchmark to get current run
                bm = benchmark_runner.run_benchmark()
                own_metrics = bm["metrics"]
                v0_metrics = v0_metrics_engine.compute_metrics()
                p1 = v0_metrics_engine.get_pivot1_category_vs_verdict()
                p2 = v0_metrics_engine.get_pivot2_confusion_matrix()
                p3 = v0_metrics_engine.get_pivot3_avg_invented_claims()
                self._send_json({
                    "v0_metrics": v0_metrics,
                    "own_metrics": own_metrics,
                    "pivot1": p1,
                    "pivot2": p2,
                    "pivot3": p3
                })
            elif path == "/api/v0_log":
                self._send_json(V0_PILOT_LOG_DATA)
            elif path.startswith("/static/"):
                file_path = path.lstrip("/")
                mime = "text/plain"
                if file_path.endswith(".html"):
                    mime = "text/html; charset=utf-8"
                elif file_path.endswith(".css"):
                    mime = "text/css"
                elif file_path.endswith(".js"):
                    mime = "application/javascript"
                self._serve_file(file_path, mime)
            else:
                self.send_error(404, "Endpoint Not Found")
        except Exception as e:
            self.send_error(500, f"Internal Error: {str(e)}")

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/api/chat":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                message = data.get("message", "").strip()
                if not message:
                    self._send_json({"error": "Empty message"}, status=400)
                    return
                response = assistant.answer_query(message)
                self._send_json(response)
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
        else:
            self.send_error(404, "Endpoint Not Found")

    def _serve_file(self, file_path, content_type):
        if not os.path.exists(file_path):
            self.send_error(404, f"File {file_path} not found")
            return
        with open(file_path, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, data, status=200):
        content = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def log_message(self, format, *args):
        # Clean logging
        sys.stderr.write(f"[{self.log_date_time_string()}] {format % args}\n")


def run(port=PORT):
    server_address = (HOST, port)
    try:
        httpd = HTTPServer(server_address, SupportDeskServer)
        print("=" * 70)
        print(f"🚀 Siddarth Swiggy Support Desk AI Server Running on http://localhost:{port}")
        print("💡 Open your browser at http://localhost:8000 to interact with the UI")
        print("=" * 70)
        while True:
            try:
                httpd.serve_forever()
            except (ConnectionResetError, BrokenPipeError):
                continue
            except KeyboardInterrupt:
                break
            except Exception as e:
                sys.stderr.write(f"Server loop error: {e}\n")
                continue
    except OSError as e:
        if port < 8010:
            print(f"Port {port} in use, trying port {port + 1}...")
            run(port + 1)
        else:
            raise e


if __name__ == "__main__":
    run()
