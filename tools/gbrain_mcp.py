#!/usr/bin/env python3
"""
GBrain Lean MCP Proxy
Serves Garry Tan's GBrain PGLite WASM memory via Model Context Protocol (MCP).
Exposes a minimal, highly compressed tool schema (recall, remember, forget)
to keep resident system prompt overhead strictly under 800 tokens.
"""

import json
import os
import signal
import subprocess
import sys
from typing import Any, Dict, List, Optional

GBRAIN_BIN = os.environ.get("GBRAIN_BIN", "/Users/man/.bun/bin/gbrain")

LEAN_TOOLS: List[Dict[str, Any]] = [
    {
        "name": "recall",
        "description": "Search and retrieve facts, entities, and markdown pages from GBrain memory.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search terms for hybrid/BM25 search over brain pages.",
                },
                "entity": {
                    "type": "string",
                    "description": "Entity name or slug to retrieve stored facts about.",
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default 20).",
                },
            },
        },
    },
    {
        "name": "remember",
        "description": "Save a durable fact, decision, or entity note to GBrain memory with provenance.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "fact": {
                    "type": "string",
                    "description": "The fact, decision, or insight to remember.",
                },
                "provenance": {
                    "type": "string",
                    "description": "Source or origin of this fact (e.g. task ID, user request, document).",
                },
                "entity": {
                    "type": "string",
                    "description": "Optional entity name or slug this fact is about.",
                },
            },
            "required": ["fact", "provenance"],
        },
    },
    {
        "name": "forget",
        "description": "Expire a previously stored fact by its numeric ID.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "ID of the fact to expire.",
                },
            },
            "required": ["id"],
        },
    },
]


def calculate_token_overhead(tools: List[Dict[str, Any]]) -> int:
    """Calculate approximate token overhead of tool definitions (char/4 estimate)."""
    raw_json = json.dumps(tools, separators=(",", ":"))
    return len(raw_json) // 4


class GBrainClient:
    """Manages persistent gbrain serve process with fallback to CLI invocation."""

    def __init__(self, gbrain_bin: str = GBRAIN_BIN):
        self.gbrain_bin = gbrain_bin
        self.proc: Optional[subprocess.Popen] = None
        self._req_id = 100
        self._start_server()

    def _start_server(self) -> None:
        if not os.path.exists(self.gbrain_bin):
            return
        try:
            self.proc = subprocess.Popen(
                [self.gbrain_bin, "serve", "--surface", "verbs"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            # Initialize MCP handshake with child gbrain serve
            init_req = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "gbrain-lean-proxy", "version": "1.0.0"},
                },
            }
            if self.proc.stdin:
                self.proc.stdin.write(json.dumps(init_req) + "\n")
                self.proc.stdin.flush()
            if self.proc.stdout:
                self.proc.stdout.readline()
        except Exception:
            self.proc = None

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tool call on gbrain serve or fallback to CLI."""
        if self.proc and self.proc.poll() is None and self.proc.stdin and self.proc.stdout:
            try:
                self._req_id += 1
                req = {
                    "jsonrpc": "2.0",
                    "id": self._req_id,
                    "method": "tools/call",
                    "params": {"name": name, "arguments": arguments},
                }
                self.proc.stdin.write(json.dumps(req) + "\n")
                self.proc.stdin.flush()
                line = self.proc.stdout.readline()
                if line:
                    res = json.loads(line)
                    if "result" in res:
                        return res["result"]
                    if "error" in res:
                        return {"content": [{"type": "text", "text": f"Error: {res['error']}"}], "isError": True}
            except Exception:
                pass

        # Fallback to CLI invocation
        try:
            cmd = [self.gbrain_bin, "call", name, json.dumps(arguments)]
            run_res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            if run_res.returncode == 0:
                return {"content": [{"type": "text", "text": run_res.stdout.strip()}]}
            return {
                "content": [{"type": "text", "text": f"CLI Error: {run_res.stderr.strip()}"}],
                "isError": True,
            }
        except Exception as e:
            return {"content": [{"type": "text", "text": f"Execution failed: {str(e)}"}], "isError": True}

    def close(self) -> None:
        """Terminate child process cleanly."""
        if self.proc:
            try:
                self.proc.terminate()
                self.proc.wait(timeout=2)
            except Exception:
                try:
                    self.proc.kill()
                except Exception:
                    pass
            self.proc = None


def run_stdio_server() -> None:
    """Run standard MCP stdio JSON-RPC server loop."""
    client = GBrainClient()

    def handle_sigterm(signum, frame):
        client.close()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sigterm)
    signal.signal(signal.SIGTERM, handle_sigterm)

    try:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except Exception:
                continue

            msg_id = msg.get("id")
            method = msg.get("method")
            params = msg.get("params", {})

            # Notifications (no response required)
            if method in ("notifications/initialized", "initialized"):
                continue

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}},
                        "serverInfo": {"name": "gbrain-lean-mcp", "version": "1.0.0"},
                    },
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"tools": LEAN_TOOLS},
                }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                if tool_name not in ("recall", "remember", "forget"):
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32601, "message": f"Tool not found: {tool_name}"},
                    }
                else:
                    tool_result = client.call_tool(tool_name, tool_args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": tool_result,
                    }
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            else:
                if msg_id is not None:
                    response = {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "error": {"code": -32601, "message": f"Method not implemented: {method}"},
                    }
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()

    finally:
        client.close()


def main() -> None:
    if "--check-tokens" in sys.argv:
        overhead = calculate_token_overhead(LEAN_TOOLS)
        raw_bytes = len(json.dumps(LEAN_TOOLS, separators=(",", ":")))
        print(f"Tool count: {len(LEAN_TOOLS)}")
        print(f"Schema raw bytes: {raw_bytes}")
        print(f"Approximate token overhead: {overhead} tokens")
        if overhead > 800:
            print("FAIL: Token overhead exceeds 800 tokens limit")
            sys.exit(1)
        print("PASS: Token overhead is within 800 tokens limit")
        sys.exit(0)

    run_stdio_server()


if __name__ == "__main__":
    main()
