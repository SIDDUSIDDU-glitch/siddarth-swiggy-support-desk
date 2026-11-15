"""
Siddarth Swiggy Support Desk AI Knowledge Assistant — Application Server.
Zero-dependency HTTP server powering the interactive web UI and REST API.
"""

import os
import sys
import json
import urllib.parse
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


class SupportDeskServer(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self._serve_file("static/index.html", "text/html; charset=utf-8")
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
        httpd.serve_forever()
    except OSError as e:
        if port < 8010:
            print(f"Port {port} in use, trying port {port + 1}...")
            run(port + 1)
        else:
            raise e


if __name__ == "__main__":
    run()
