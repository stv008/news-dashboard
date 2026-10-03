#!/usr/bin/env python3
"""
News Dashboard Local Server
Serves the dashboard in your browser with a live refresh button.

Usage:
    python server.py              # Start on default port
    python server.py 9000         # Start on custom port

Then open http://localhost:8080 in your browser.
"""

import os
import sys
import json
import time
import threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from fetcher import fetch_all
from dashboard_builder import build_dashboard
from summarizer import generate_briefing, is_available
from config import OUTPUT_HTML, SERVER_PORT

refresh_lock = threading.Lock()
last_generation_time = 0
bound_port = SERVER_PORT  # updated at startup if we fall back to another port


class DashboardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "":
            self._serve_dashboard()
        elif path == "/status":
            self._json_response({"status": "ok", "last_generated": last_generation_time, "refreshing": refresh_lock.locked()})
        else:
            self._json_response({"error": "Not found"}, status=404)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/refresh":
            origin = self.headers.get("Origin", "")
            referer = self.headers.get("Referer", "")
            allowed = [f"http://localhost:{bound_port}", f"http://127.0.0.1:{bound_port}"]
            if origin and origin not in allowed:
                self._json_response({"error": "Forbidden"}, status=403)
                return
            if not origin and referer and not any(referer.startswith(o) for o in allowed):
                self._json_response({"error": "Forbidden"}, status=403)
                return
            self._handle_refresh()
        else:
            self._json_response({"error": "Not found"}, status=404)

    def _serve_dashboard(self):
        if not os.path.exists(OUTPUT_HTML):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>Dashboard not yet generated.</h1>")
            return
        with open(OUTPUT_HTML, "r", encoding="utf-8") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))

    def _handle_refresh(self):
        global last_generation_time
        if not refresh_lock.acquire(blocking=False):
            self._json_response({"status": "busy", "message": "Refresh already in progress"})
            return
        try:
            self._json_response({"status": "started", "message": "Refreshing..."})
        except Exception:
            refresh_lock.release()
            return

        def do_refresh():
            global last_generation_time
            try:
                print("\n[Refresh] Fetching articles...")
                fetch_all()
                ai_summary = None
                if is_available():
                    print("[Refresh] Generating AI briefing...")
                    ai_summary = generate_briefing()
                print("[Refresh] Building dashboard...")
                build_dashboard(ai_summary)
                last_generation_time = time.time()
                print("[Refresh] Done!\n")
            except Exception as e:
                print(f"[Refresh] Error: {e}")
            finally:
                refresh_lock.release()

        threading.Thread(target=do_refresh, daemon=True).start()

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def log_message(self, format, *args):
        pass


def _start_server(requested_port):
    """Start the HTTP server, falling back to the next free port if busy."""
    for port in range(requested_port, requested_port + 10):
        try:
            return ThreadingHTTPServer(("127.0.0.1", port), DashboardHandler), port
        except OSError as e:
            if getattr(e, "errno", None) in (48, 98, 10048):  # macOS/Linux/Windows "in use"
                print(f"  Port {port} in use, trying {port + 1}...")
                continue
            raise
    raise RuntimeError(f"Could not bind to any port in {requested_port}..{requested_port + 9}")


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else SERVER_PORT
    global last_generation_time, bound_port
    if not os.path.exists(OUTPUT_HTML):
        print("No dashboard found. Running initial fetch...")
        fetch_all()
        ai_summary = generate_briefing() if is_available() else None
        build_dashboard(ai_summary)
        last_generation_time = time.time()
    server, bound_port = _start_server(port)
    print(f"News Dashboard running at http://localhost:{bound_port}")
    print("Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
