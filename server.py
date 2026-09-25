"""
Local-only server for the Discovery Dashboard.

Serves dashboard.html and exposes GET /api/data, which re-runs the Jira
pipeline live and returns fresh JSON. The Jira token never leaves this
process — it is read server-side from ~/.config/jira/token and is not
sent to the browser in any response.

Run:  python3 server.py
Then open http://localhost:8765/dashboard.html
"""
import json
import os
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

import pipeline
import build as build_mod

PORT = 8765
DIRECTORY = os.path.dirname(os.path.abspath(__file__))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/data":
            self._handle_api_data()
        elif path == "/":
            self.send_response(302)
            self.send_header("Location", "/dashboard.html")
            self.end_headers()
        else:
            super().do_GET()

    def _handle_api_data(self):
        try:
            print("Refreshing from Jira...", flush=True)
            data = pipeline.run(progress=lambda m: print(" ", m, flush=True))
            body = json.dumps(data).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            # keep a local cache of the latest pull, and rebuild the static
            # dashboard.html so opening it directly (no server) also shows it
            with open(os.path.join(DIRECTORY, "data.json"), "w") as f:
                json.dump(data, f, indent=2)
            build_mod.build(data)
        except Exception as e:
            print("Refresh failed:", e, file=sys.stderr, flush=True)
            body = json.dumps({"error": str(e)}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[server] {self.address_string()} - {fmt % args}", flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("localhost", PORT), Handler)
    print(f"Discovery Dashboard server running at http://localhost:{PORT}/dashboard.html")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
        server.shutdown()
