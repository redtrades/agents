"""
Unit tests for tools/gbrain_mcp.py
Verifies MCP JSON-RPC protocol handling, token limits, and tool routing.
"""

import io
import json
import unittest
from unittest.mock import MagicMock, patch

from tools.gbrain_mcp import (
    LEAN_TOOLS,
    GBrainClient,
    calculate_token_overhead,
    run_stdio_server,
)


class TestGBrainMcp(unittest.TestCase):
    def test_token_overhead_within_budget(self):
        """Ensure total schema resident token overhead remains strictly under 800 tokens."""
        overhead = calculate_token_overhead(LEAN_TOOLS)
        self.assertLess(overhead, 800, f"Token overhead {overhead} exceeds 800 token budget")
        self.assertEqual(len(LEAN_TOOLS), 3)
        tool_names = [t["name"] for t in LEAN_TOOLS]
        self.assertIn("recall", tool_names)
        self.assertIn("remember", tool_names)
        self.assertIn("forget", tool_names)

    def test_tool_definitions_valid_schema(self):
        """Validate input schemas for required and optional fields."""
        tools_by_name = {t["name"]: t for t in LEAN_TOOLS}
        remember_tool = tools_by_name["remember"]
        self.assertEqual(remember_tool["inputSchema"]["required"], ["fact", "provenance"])

        recall_tool = tools_by_name["recall"]
        self.assertIn("query", recall_tool["inputSchema"]["properties"])
        self.assertIn("entity", recall_tool["inputSchema"]["properties"])

        forget_tool = tools_by_name["forget"]
        self.assertEqual(forget_tool["inputSchema"]["required"], ["id"])

    @patch("tools.gbrain_mcp.os.path.exists", return_value=True)
    @patch("tools.gbrain_mcp.subprocess.Popen")
    def test_gbrain_client_initialization(self, mock_popen, mock_exists):
        """Test persistent process initialization."""
        mock_proc = MagicMock()
        mock_proc.stdin = MagicMock()
        mock_proc.stdout = MagicMock()
        mock_proc.stdout.readline.return_value = (
            json.dumps({"result": {"serverInfo": {"name": "gbrain"}}}) + "\n"
        )
        mock_popen.return_value = mock_proc

        client = GBrainClient(gbrain_bin="/fake/gbrain")
        self.assertIsNotNone(client.proc)
        client.close()
        mock_proc.terminate.assert_called_once()

    @patch("tools.gbrain_mcp.subprocess.run")
    def test_gbrain_client_cli_fallback(self, mock_run):
        """Test CLI fallback when subprocess is not active."""
        mock_run.return_value = MagicMock(returncode=0, stdout='{"status": "ok"}', stderr="")
        client = GBrainClient(gbrain_bin="/fake/gbrain")
        client.proc = None  # Force fallback

        result = client.call_tool("recall", {"query": "test"})
        self.assertIn("content", result)
        self.assertEqual(result["content"][0]["text"], '{"status": "ok"}')

    @patch("tools.gbrain_mcp.GBrainClient")
    def test_stdio_server_lifecycle(self, mock_client_cls):
        """Test standard MCP stdio JSON-RPC sequence: init, list, call."""
        mock_client = MagicMock()
        mock_client.call_tool.return_value = {"content": [{"type": "text", "text": "result-1"}]}
        mock_client_cls.return_value = mock_client

        requests = [
            json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}}),
            json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}),
            json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}}),
            json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": "recall", "arguments": {"query": "test"}},
                }
            ),
            json.dumps({"jsonrpc": "2.0", "id": 4, "method": "ping"}),
        ]
        input_stream = io.StringIO("\n".join(requests) + "\n")
        output_stream = io.StringIO()

        with patch("sys.stdin", input_stream), patch("sys.stdout", output_stream):
            run_stdio_server()

        lines = [json.loads(l) for l in output_stream.getvalue().strip().split("\n") if l.strip()]
        self.assertEqual(len(lines), 4)  # init, list, call, ping (notification has no reply)

        # Verify initialize reply
        self.assertEqual(lines[0]["id"], 1)
        self.assertEqual(lines[0]["result"]["serverInfo"]["name"], "gbrain-lean-mcp")

        # Verify tools/list reply
        self.assertEqual(lines[1]["id"], 2)
        self.assertEqual(len(lines[1]["result"]["tools"]), 3)

        # Verify tools/call reply
        self.assertEqual(lines[2]["id"], 3)
        self.assertEqual(lines[2]["result"]["content"][0]["text"], "result-1")

        # Verify ping reply
        self.assertEqual(lines[3]["id"], 4)


if __name__ == "__main__":
    unittest.main()
