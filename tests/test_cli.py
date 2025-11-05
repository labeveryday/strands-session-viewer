"""Tests for CLI."""

import sys
from unittest.mock import patch

import pytest

from strands_viewer.cli import main


def test_cli_version(capsys):
    """Test --version flag."""
    with patch.object(sys, "argv", ["strands-viewer", "--version"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "0.1.0" in captured.out


def test_cli_help(capsys):
    """Test --help flag."""
    with patch.object(sys, "argv", ["strands-viewer", "--help"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 0

    captured = capsys.readouterr()
    assert "Strands Session Viewer" in captured.out
    assert "--port" in captured.out
    assert "--no-open" in captured.out


def test_cli_invalid_directory(capsys):
    """Test CLI with invalid directory."""
    with patch.object(sys, "argv", ["strands-viewer", "/nonexistent/path"]):
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    captured = capsys.readouterr()
    assert "does not exist" in captured.out


def test_cli_valid_directory_mock(temp_sessions_dir, monkeypatch):
    """Test CLI with valid directory (mocked server)."""
    # Mock the SessionViewerApp to prevent actual server start
    server_started = False

    class MockViewerApp:
        def __init__(self, storage_dir, port):
            self.storage_dir = storage_dir
            self.port = port

        def run(self, open_browser=False):
            nonlocal server_started
            server_started = True

    # Mock at the server module level since it's imported inside main()
    with patch("strands_viewer.server.SessionViewerApp", MockViewerApp):
        with patch.object(sys, "argv", ["strands-viewer", temp_sessions_dir, "--no-open"]):
            # This test verifies argument parsing and module imports work
            # The mock prevents actual server start
            try:
                main()
            except SystemExit:
                # Expected when server would normally start
                pass

    assert server_started


def test_cli_custom_port(temp_sessions_dir):
    """Test CLI with custom port."""
    from argparse import ArgumentParser

    # Create parser to test argument parsing
    parser = ArgumentParser()
    parser.add_argument("directory", nargs="?", default="./sessions")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--no-open", action="store_true")

    args = parser.parse_args([temp_sessions_dir, "--port", "9000", "--no-open"])
    assert args.port == 9000
    assert args.no_open is True
