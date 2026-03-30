#!/usr/bin/env python3
"""
review_server.py — Live preview + review state server for SLASHR proposals.

Usage:
    python3 tools/review_server.py --deal-id 578

Serves the latest PROPOSAL HTML on localhost:3000 with:
- Auto-refresh when the file changes (2s polling)
- Review state persistence (REVIEW-STATE.json)
- Feedback API (POST /feedback)

Press Ctrl+C to stop.
"""

import argparse
import glob
import json
import os
import sys
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs


def find_proposal(deal_dir):
    """Find the latest PROPOSAL HTML in the deal artifacts dir."""
    pattern = str(deal_dir / "PROPOSAL-*.html")
    files = glob.glob(pattern)
    # Exclude versioned files (-v1, -v2, etc.)
    files = [f for f in files if not any(f.endswith(f"-v{i}.html") for i in range(1, 100))]
    if not files:
        return None
    return max(files, key=os.path.getmtime)


def load_review_state(state_path):
    """Load or create review state."""
    if state_path.exists():
        with open(state_path) as f:
            return json.load(f)
    return {
        "deal_id": None,
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "last_updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "status": "not_started",
        "tabs": {}
    }


def save_review_state(state_path, state):
    """Save review state to disk."""
    state["last_updated"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with open(state_path, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


LIVE_RELOAD_SNIPPET = """
<script>
(function() {
  var lastMtime = 0;
  setInterval(function() {
    fetch('/check-update')
      .then(function(r) { return r.json(); })
      .then(function(d) {
        if (lastMtime && d.mtime !== lastMtime) {
          location.reload();
        }
        lastMtime = d.mtime;
      })
      .catch(function() {});
  }, 2000);
})();
</script>
"""


class ReviewHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress default logging for polling requests
        if '/check-update' not in str(args):
            super().log_message(format, *args)

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            proposal_path = self.server.proposal_path
            if not proposal_path or not os.path.exists(proposal_path):
                self.send_error(404, "No proposal found")
                return
            with open(proposal_path, 'r', encoding='utf-8') as f:
                html = f.read()
            # Inject live-reload snippet before </body>
            html = html.replace('</body>', LIVE_RELOAD_SNIPPET + '</body>')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        elif self.path == '/check-update':
            proposal_path = self.server.proposal_path
            mtime = os.path.getmtime(proposal_path) if proposal_path and os.path.exists(proposal_path) else 0
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"mtime": mtime}).encode())

        elif self.path == '/status':
            state = load_review_state(self.server.state_path)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(state, indent=2, ensure_ascii=False).encode('utf-8'))

        elif self.path == '/review-panel':
            # Serve a simple review panel HTML
            state = load_review_state(self.server.state_path)
            html = build_review_panel(state)
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode('utf-8'))

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/feedback':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_error(400, "Invalid JSON")
                return

            state = load_review_state(self.server.state_path)
            tab = data.get("tab", "")
            slide_index = data.get("slide_index", 0)
            status = data.get("status", "approved")
            feedback = data.get("feedback", "")

            if tab not in state["tabs"]:
                state["tabs"][tab] = {"slides": []}

            slides = state["tabs"][tab]["slides"]
            # Extend list if needed
            while len(slides) <= slide_index:
                slides.append({"id": len(slides), "status": "not_reviewed", "feedback": ""})

            slides[slide_index]["status"] = status
            slides[slide_index]["feedback"] = feedback
            state["status"] = "in_progress"

            # Check if all reviewed
            all_tabs_done = True
            for t in state["tabs"].values():
                if isinstance(t, dict) and "slides" in t:
                    for s in t["slides"]:
                        if s.get("status") in ("not_reviewed", "pending", "needs_fix"):
                            all_tabs_done = False
                            break
            if all_tabs_done and state["tabs"]:
                state["status"] = "complete"

            save_review_state(self.server.state_path, state)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": True, "state": state}, indent=2, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404)


def build_review_panel(state):
    """Build a simple HTML review panel."""
    html = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Review Panel</title>
<style>
body { font-family: Inter, sans-serif; background: #1a1a1a; color: #fff; padding: 20px; }
h1 { font-size: 1.2rem; }
.tab { margin: 16px 0; padding: 12px; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; }
.tab-name { font-weight: 700; color: #E74601; }
.slide { padding: 6px 0; display: flex; align-items: center; gap: 8px; }
.badge { font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; font-weight: 600; }
.badge-approved { background: #2d5a27; color: #8fce8a; }
.badge-fixed { background: #5a4827; color: #ceab6a; }
.badge-needs_fix { background: #5a2727; color: #ce6a6a; }
.badge-not_reviewed { background: #333; color: #888; }
.badge-pending { background: #333; color: #ce8a00; }
.status { font-size: 1rem; margin: 16px 0; padding: 12px; border-radius: 8px; }
.status-complete { background: #2d5a27; }
.status-in_progress { background: #5a4827; }
.status-not_started { background: #333; }
</style></head><body>
<h1>Review State</h1>
"""
    s = state.get("status", "not_started")
    html += f'<div class="status status-{s}">Statut : <strong>{s}</strong> | Derniere MAJ : {state.get("last_updated", "?")}</div>'

    for tab_name, tab_data in state.get("tabs", {}).items():
        html += f'<div class="tab"><span class="tab-name">{tab_name}</span>'
        if isinstance(tab_data, dict) and "slides" in tab_data:
            for slide in tab_data["slides"]:
                sid = slide.get("id", "?")
                st = slide.get("status", "not_reviewed")
                fb = slide.get("feedback", "")
                html += f'<div class="slide"><span class="badge badge-{st}">{st}</span> Slide {sid}'
                if fb:
                    html += f' — <em style="color:#888">{fb}</em>'
                html += '</div>'
        else:
            html += '<div class="slide"><span class="badge badge-not_reviewed">not started</span></div>'
        html += '</div>'

    if not state.get("tabs"):
        html += '<p style="color:#888">Aucune review en cours. Utilise POST /feedback pour commencer.</p>'

    html += '</body></html>'
    return html


def main():
    parser = argparse.ArgumentParser(description="Live preview + review server for SLASHR proposals")
    parser.add_argument("--deal-id", required=True, help="Deal ID")
    parser.add_argument("--port", type=int, default=3000, help="Port (default: 3000)")
    args = parser.parse_args()

    script_dir = Path(__file__).parent.parent
    deal_dir = script_dir / ".cache" / "deals" / args.deal_id / "artifacts"

    if not deal_dir.exists():
        print(f"[ERROR] Deal directory not found: {deal_dir}", file=sys.stderr)
        sys.exit(1)

    proposal_path = find_proposal(deal_dir)
    if not proposal_path:
        print(f"[ERROR] No PROPOSAL HTML found in {deal_dir}", file=sys.stderr)
        sys.exit(1)

    state_path = deal_dir / "REVIEW-STATE.json"
    state = load_review_state(state_path)
    state["deal_id"] = int(args.deal_id)
    save_review_state(state_path, state)

    server = HTTPServer(('localhost', args.port), ReviewHandler)
    server.proposal_path = proposal_path
    server.state_path = state_path

    print(f"\n  Preview : http://localhost:{args.port}")
    print(f"  Review panel : http://localhost:{args.port}/review-panel")
    print(f"  State file : {state_path}")
    print(f"  Proposal : {os.path.basename(proposal_path)}")
    print(f"\n  Auto-refresh actif (2s). Ctrl+C pour arreter.\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()


if __name__ == "__main__":
    main()
