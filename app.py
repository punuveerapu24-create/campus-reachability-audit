#!/usr/bin/env python3
"""
Web Application for Campus Reachability and Emergency Route Audit
Provides an interactive web dashboard and REST API for deployment on Render.
"""

from collections import deque
import json
import os
import sys
from typing import Any, Dict, List, Optional, Tuple

import campus_reachability

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campus Reachability & Emergency Route Audit</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #0f172a;
            --surface: #1e293b;
            --surface-hover: #334155;
            --border: #334155;
            --accent: #38bdf8;
            --accent-glow: rgba(56, 189, 248, 0.25);
            --success: #34d399;
            --danger: #f87171;
            --warning: #fbbf24;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --mono-font: 'Fira Code', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg);
            color: var(--text-main);
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            min-height: 100vh;
            padding: 2rem 1rem;
            display: flex;
            justify-content: center;
        }

        .container {
            width: 100%;
            max-width: 1050px;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        header {
            text-align: center;
            margin-bottom: 0.5rem;
        }

        .badge-bar {
            display: flex;
            justify-content: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }

        .badge {
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 9999px;
            padding: 0.25rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        h1 {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            background: linear-gradient(135deg, #ffffff 40%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        header p {
            color: var(--text-muted);
            font-size: 1rem;
            max-width: 600px;
            margin: 0 auto;
        }

        .grid-2 {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 820px) {
            .grid-2 {
                grid-template-columns: 1fr;
            }
        }

        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 1rem;
            padding: 1.5rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card-title {
            font-size: 1.15rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .presets {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }

        .btn-preset {
            background: var(--surface-hover);
            color: var(--text-muted);
            border: 1px solid var(--border);
            border-radius: 0.5rem;
            padding: 0.35rem 0.65rem;
            font-size: 0.75rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-preset:hover {
            color: var(--text-main);
            border-color: var(--accent);
            background: rgba(56, 189, 248, 0.1);
        }

        textarea {
            width: 100%;
            height: 250px;
            background: #090d16;
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 1rem;
            color: var(--text-main);
            font-family: var(--mono-font);
            font-size: 0.9rem;
            resize: vertical;
            line-height: 1.5;
        }

        textarea:focus {
            outline: none;
            border-color: var(--accent);
            box-shadow: 0 0 0 3px var(--accent-glow);
        }

        .btn-run {
            background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
            color: #041424;
            border: none;
            border-radius: 0.75rem;
            padding: 0.85rem 1.5rem;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            transition: opacity 0.2s, transform 0.1s;
        }

        .btn-run:hover {
            opacity: 0.95;
            transform: translateY(-1px);
        }

        .btn-run:active {
            transform: translateY(0);
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
        }

        .stat-box {
            background: #090d16;
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 0.85rem;
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .stat-value {
            font-size: 1.35rem;
            font-weight: 700;
            color: var(--accent);
            margin-top: 0.25rem;
        }

        .tag-list {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.4rem;
        }

        .tag {
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent);
            border: 1px solid rgba(56, 189, 248, 0.25);
            border-radius: 0.35rem;
            padding: 0.2rem 0.5rem;
            font-family: var(--mono-font);
            font-size: 0.8rem;
        }

        .tag.arrow::after {
            content: " →";
            opacity: 0.6;
        }
        .tag.arrow:last-child::after {
            content: "";
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        th, td {
            padding: 0.65rem 0.5rem;
            text-align: left;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--text-muted);
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
        }

        .status-badge {
            display: inline-block;
            padding: 0.2rem 0.5rem;
            border-radius: 0.35rem;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .status-ok {
            background: rgba(52, 211, 153, 0.15);
            color: var(--success);
            border: 1px solid rgba(52, 211, 153, 0.3);
        }

        .status-unreachable {
            background: rgba(248, 113, 113, 0.15);
            color: var(--danger);
            border: 1px solid rgba(248, 113, 113, 0.3);
        }

        .output-box {
            background: #090d16;
            border: 1px solid var(--border);
            border-radius: 0.75rem;
            padding: 1rem;
            font-family: var(--mono-font);
            font-size: 0.85rem;
            color: #38bdf8;
            white-space: pre;
            overflow-x: auto;
            max-height: 240px;
        }

        .error-box {
            background: rgba(248, 113, 113, 0.15);
            border: 1px solid var(--danger);
            color: #fca5a5;
            border-radius: 0.75rem;
            padding: 1rem;
            font-size: 0.9rem;
            display: none;
        }

        footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 1rem;
        }

        footer a {
            color: var(--accent);
            text-decoration: none;
        }

        footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-bar">
                <span class="badge">DAA Lab Challenge</span>
                <span class="badge">Graph Theory</span>
                <span class="badge">Live Web Service</span>
            </div>
            <h1>Campus Reachability & Emergency Route Audit</h1>
            <p>Recursive DFS component partitioning, deterministic source traversals, and BFS discovery-tree emergency evacuation paths.</p>
        </header>

        <div class="grid-2">
            <!-- Input Panel -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">Walkway Graph Input</span>
                </div>
                <div class="presets">
                    <span style="font-size: 0.75rem; color: var(--text-muted); align-self: center;">Presets:</span>
                    <button class="btn-preset" onclick="loadPreset('sample1')">Connected (5 Nodes)</button>
                    <button class="btn-preset" onclick="loadPreset('sample2')">Disconnected (3 Zones)</button>
                    <button class="btn-preset" onclick="loadPreset('sample3')">Isolated Buildings</button>
                </div>
                <textarea id="graphInput" placeholder="Enter graph input:&#10;n m&#10;u v (m lines)&#10;s q&#10;t (q lines)"></textarea>
                <button class="btn-run" onclick="runAudit()">
                    <span>Execute Emergency Audit</span>
                    <svg width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                    </svg>
                </button>
                <div id="errorBox" class="error-box"></div>
            </div>

            <!-- Results Panel -->
            <div class="card">
                <div class="card-header">
                    <span class="card-title">Audit Metrics & Insights</span>
                </div>
                <div class="stats-grid">
                    <div class="stat-box">
                        <div class="stat-label">Connected Components</div>
                        <div class="stat-value" id="valComponents">-</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">Command Source (s)</div>
                        <div class="stat-value" id="valSource">-</div>
                    </div>
                </div>

                <div>
                    <div class="stat-label">Component Labels (l0 ... ln-1)</div>
                    <div id="labelsContainer" class="tag-list" style="max-height: 70px; overflow-y: auto;">-</div>
                </div>

                <div>
                    <div class="stat-label">Recursive DFS Order (Entry Pre-order)</div>
                    <div id="dfsContainer" class="tag-list">-</div>
                </div>

                <div>
                    <div class="stat-label">Queue-based BFS Order (FIFO Dequeue)</div>
                    <div id="bfsContainer" class="tag-list">-</div>
                </div>

                <div>
                    <div class="stat-label">Emergency Shortest Routes</div>
                    <div style="overflow-x: auto; max-height: 160px;">
                        <table id="routeTable">
                            <thead>
                                <tr>
                                    <th>Target</th>
                                    <th>Status</th>
                                    <th>Edges</th>
                                    <th>Evacuation Path</th>
                                </tr>
                            </thead>
                            <tbody id="routeTableBody">
                                <tr><td colspan="4" style="color: var(--text-muted); text-align: center;">Execute audit to view routes.</td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>

                <div>
                    <div class="stat-label">Standard DAA Lab Output (sys.stdout)</div>
                    <div id="outputBox" class="output-box">// Audit results will appear here</div>
                </div>
            </div>
        </div>

        <footer>
            Campus Walkway Graph Engine • Deployed on <a href="https://render.com" target="_blank">Render</a> •
            <a href="https://github.com/punuveerapu24-create/campus-reachability-audit" target="_blank">GitHub Repository</a>
        </footer>
    </div>

    <script>
        const PRESETS = {
            sample1: "5 4\\n0 1\\n0 3\\n1 2\\n3 4\\n0 3\\n2\\n4\\n0",
            sample2: "7 4\\n0 1\\n1 2\\n3 4\\n5 6\\n3 4\\n4\\n0\\n5\\n3",
            sample3: "3 0\\n1 3\\n0\\n1\\n2"
        };

        function loadPreset(name) {
            document.getElementById("graphInput").value = PRESETS[name].replace(/\\\\n/g, '\\n');
            runAudit();
        }

        async function runAudit() {
            const input = document.getElementById("graphInput").value.trim();
            const errorBox = document.getElementById("errorBox");
            errorBox.style.display = "none";

            if (!input) {
                errorBox.innerText = "Please provide walkway graph input or pick a preset.";
                errorBox.style.display = "block";
                return;
            }

            try {
                const response = await fetch("/api/audit", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ input: input })
                });

                const data = await response.json();
                if (!response.ok) {
                    throw new Error(data.error || "Failed to process graph audit.");
                }

                // Render metrics
                document.getElementById("valComponents").innerText = data.components_count;
                document.getElementById("valSource").innerText = data.source;

                // Render labels
                const labelsEl = document.getElementById("labelsContainer");
                labelsEl.innerHTML = data.labels.map((lbl, idx) => `<span class="tag">v${idx}:${lbl}</span>`).join("");

                // Render DFS
                const dfsEl = document.getElementById("dfsContainer");
                dfsEl.innerHTML = data.dfs_order.map(v => `<span class="tag arrow">${v}</span>`).join("");

                // Render BFS
                const bfsEl = document.getElementById("bfsContainer");
                bfsEl.innerHTML = data.bfs_order.map(v => `<span class="tag arrow">${v}</span>`).join("");

                // Render Routes Table
                const tbody = document.getElementById("routeTableBody");
                tbody.innerHTML = data.routes.map(r => {
                    if (r.reachable) {
                        return `<tr>
                            <td><strong>${r.target}</strong></td>
                            <td><span class="status-badge status-ok">Reachable</span></td>
                            <td>${r.distance}</td>
                            <td><span style="font-family: var(--mono-font); font-size: 0.8rem; color: var(--accent);">${r.path.join(" → ")}</span></td>
                        </tr>`;
                    } else {
                        return `<tr>
                            <td><strong>${r.target}</strong></td>
                            <td><span class="status-badge status-unreachable">UNREACHABLE</span></td>
                            <td>-</td>
                            <td><span style="color: var(--text-muted); font-size: 0.8rem;">No walkway connection</span></td>
                        </tr>`;
                    }
                }).join("");

                // Render Raw Output
                document.getElementById("outputBox").innerText = data.raw_output;

            } catch (err) {
                errorBox.innerText = err.message;
                errorBox.style.display = "block";
            }
        }

        // Load sample 1 on initial load
        window.onload = () => loadPreset("sample1");
    </script>
</body>
</html>
"""


def process_audit_request(input_text: str) -> Dict[str, Any]:
    """
    Parses graph specification and target queries, runs the DAA graph algorithms,
    and returns both formatted text and structured metrics.
    """
    tokens = input_text.split()
    if not tokens:
        raise ValueError("Input string is empty.")

    it = iter(tokens)
    try:
        n = int(next(it))
        m = int(next(it))
    except StopIteration:
        raise ValueError("Missing vertex or edge count on line 1.")

    if n < 1 or n > 200:
        raise ValueError(f"Constraint violation: n={n} must be between 1 and 200.")

    adj: List[List[int]] = [[] for _ in range(n)]
    for i in range(m):
        try:
            u = int(next(it))
            v = int(next(it))
        except StopIteration:
            raise ValueError(f"Expected {m} edges, but input ended prematurely after edge {i}.")

        if u < 0 or u >= n or v < 0 or v >= n:
            raise ValueError(f"Edge ({u}, {v}) refers to vertex outside 0..{n-1}.")
        adj[u].append(v)
        adj[v].append(u)

    for u in range(n):
        adj[u].sort()

    try:
        s = int(next(it))
        q = int(next(it))
    except StopIteration:
        raise ValueError("Missing source vertex s or query count q.")

    if s < 0 or s >= n:
        raise ValueError(f"Source vertex {s} is out of bounds (0..{n-1}).")

    queries: List[int] = []
    for i in range(q):
        try:
            queries.append(int(next(it)))
        except StopIteration:
            raise ValueError(f"Expected {q} queries, but found only {i}.")

    # Algorithmic Audits
    c, labels = campus_reachability.compute_connected_components(n, adj)
    dfs_order = campus_reachability.source_dfs(s, n, adj)
    bfs_order, dist, parent = campus_reachability.source_bfs(s, n, adj)

    # Reconstruct routes and generate raw DAA output
    raw_lines = [
        f"COMPONENTS {c}",
        f"LABELS {' '.join(map(str, labels))}",
        f"DFS {' '.join(map(str, dfs_order))}",
        f"BFS {' '.join(map(str, bfs_order))}",
    ]

    routes_data = []
    for t in queries:
        if t < 0 or t >= n:
            raw_lines.append(f"ROUTE {t} UNREACHABLE")
            routes_data.append({"target": t, "reachable": False, "distance": -1, "path": []})
            continue

        route = campus_reachability.reconstruct_route(s, t, dist, parent)
        if route is None:
            raw_lines.append(f"ROUTE {t} UNREACHABLE")
            routes_data.append({"target": t, "reachable": False, "distance": -1, "path": []})
        else:
            d = dist[t]
            raw_lines.append(f"ROUTE {t} {d} {' '.join(map(str, route))}")
            routes_data.append({"target": t, "reachable": True, "distance": d, "path": route})

    return {
        "n": n,
        "m": m,
        "source": s,
        "components_count": c,
        "labels": labels,
        "dfs_order": dfs_order,
        "bfs_order": bfs_order,
        "routes": routes_data,
        "raw_output": "\n".join(raw_lines),
    }


# Initialize Flask WSGI application
try:
    from flask import Flask, Response, jsonify, request

    app = Flask(__name__)

    @app.route("/", methods=["GET"])
    def index():
        return Response(HTML_TEMPLATE, mimetype="text/html")

    @app.route("/healthz", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok", "service": "campus-reachability-audit"})

    @app.route("/api/audit", methods=["POST"])
    def api_audit():
        try:
            if request.is_json:
                data = request.get_json()
                input_text = data.get("input", "")
            else:
                input_text = request.get_data(as_text=True)

            results = process_audit_request(input_text)
            return jsonify(results)
        except Exception as e:
            return jsonify({"error": str(e)}), 400

except ImportError:
    app = None  # Fallback to standard library when Flask is absent


def run_standalone_server(port: int = 5000):
    """Fallback standard-library HTTP server when running locally without Flask."""
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from urllib.parse import parse_qs, urlparse

    class SimpleHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            if parsed.path == "/" or parsed.path == "/index.html":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            elif parsed.path == "/healthz":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status": "ok"}')
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            parsed = urlparse(self.path)
            if parsed.path == "/api/audit":
                content_len = int(self.headers.get("Content-Length", 0))
                post_data = self.rfile.read(content_len).decode("utf-8")
                try:
                    payload = json.loads(post_data)
                    raw_input = payload.get("input", "")
                    res = process_audit_request(raw_input)
                    resp_body = json.dumps(res).encode("utf-8")
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(resp_body)
                except Exception as ex:
                    self.send_response(400)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": str(ex)}).encode("utf-8"))
            else:
                self.send_response(404)
                self.end_headers()

    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    print(f"Serving on http://0.0.0.0:{port} (Standard Library HTTP Server)")
    server.serve_forever()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    if app is not None:
        app.run(host="0.0.0.0", port=port)
    else:
        run_standalone_server(port=port)
