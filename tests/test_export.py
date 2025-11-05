"""Tests for export functionality."""

import json

import pytest
from fastapi.testclient import TestClient

from strands_viewer.export_formatter import (
    format_markdown,
    format_json,
    format_text,
    format_session,
    get_filename,
)
from strands_viewer.server import SessionViewerApp


@pytest.fixture
def sample_session():
    """Create a sample session for testing."""
    return {
        "session_id": "test_session",
        "session_type": "AGENT",
        "created_at": "2025-11-05T10:00:00.000000+00:00",
        "updated_at": "2025-11-05T10:05:00.000000+00:00",
        "messages": [
            {
                "message": {"role": "user", "content": [{"text": "Hello!"}]},
                "message_id": 1,
                "created_at": "2025-11-05T10:00:01.000000+00:00",
            },
            {
                "message": {
                    "role": "assistant",
                    "content": [
                        {
                            "toolUse": {
                                "toolUseId": "test_1",
                                "name": "test_tool",
                                "input": {"arg": "value"},
                            }
                        }
                    ],
                },
                "message_id": 2,
                "created_at": "2025-11-05T10:00:02.000000+00:00",
            },
        ],
    }


def test_format_markdown(sample_session):
    """Test Markdown formatting."""
    result = format_markdown(sample_session)

    assert "# Session: test_session" in result
    assert "## Messages" in result
    assert "👤 User #1" in result
    assert "🤖 Assistant #2" in result
    assert "Hello!" in result
    assert "test_tool" in result


def test_format_json(sample_session):
    """Test JSON formatting."""
    result = format_json(sample_session)

    # Should be valid JSON
    parsed = json.loads(result)
    assert parsed["session_id"] == "test_session"
    assert len(parsed["messages"]) == 2


def test_format_text(sample_session):
    """Test plain text formatting."""
    result = format_text(sample_session)

    assert "Session: test_session" in result
    assert "[USER #1]" in result
    assert "[ASSISTANT #2]" in result
    assert "Hello!" in result
    assert "test_tool" in result


def test_format_session_markdown(sample_session):
    """Test format_session with markdown."""
    result = format_session(sample_session, "markdown")
    assert "# Session: test_session" in result


def test_format_session_json(sample_session):
    """Test format_session with json."""
    result = format_session(sample_session, "json")
    parsed = json.loads(result)
    assert parsed["session_id"] == "test_session"


def test_format_session_text(sample_session):
    """Test format_session with text."""
    result = format_session(sample_session, "text")
    assert "Session: test_session" in result


def test_format_session_invalid_format(sample_session):
    """Test format_session with invalid format."""
    with pytest.raises(ValueError, match="Unsupported format"):
        format_session(sample_session, "invalid")


def test_get_filename():
    """Test filename generation."""
    assert get_filename("test_123", "markdown") == "session_test_123.md"
    assert get_filename("test_123", "json") == "session_test_123.json"
    assert get_filename("test_123", "text") == "session_test_123.txt"


def test_export_endpoint_markdown(temp_sessions_dir):
    """Test the export endpoint with markdown format."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/test_1/export?format=markdown")

    assert response.status_code == 200
    assert "text/markdown" in response.headers["content-type"]
    assert 'attachment; filename="session_test_1.md"' in response.headers["content-disposition"]
    assert "# Session: test_1" in response.text


def test_export_endpoint_json(temp_sessions_dir):
    """Test the export endpoint with json format."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/test_1/export?format=json")

    assert response.status_code == 200
    assert "application/json" in response.headers["content-type"]
    assert 'attachment; filename="session_test_1.json"' in response.headers["content-disposition"]

    # Should be valid JSON
    parsed = json.loads(response.text)
    assert parsed["session_id"] == "test_1"


def test_export_endpoint_text(temp_sessions_dir):
    """Test the export endpoint with text format."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/test_1/export?format=text")

    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    assert 'attachment; filename="session_test_1.txt"' in response.headers["content-disposition"]
    assert "Session: test_1" in response.text


def test_export_endpoint_invalid_format(temp_sessions_dir):
    """Test the export endpoint with invalid format."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/test_1/export?format=invalid")

    assert response.status_code == 400


def test_export_endpoint_nonexistent_session(temp_sessions_dir):
    """Test the export endpoint with nonexistent session."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/nonexistent/export?format=markdown")

    assert response.status_code == 404


def test_export_default_format(temp_sessions_dir):
    """Test that default format is markdown."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)

    response = client.get("/api/sessions/test_1/export")

    assert response.status_code == 200
    assert "text/markdown" in response.headers["content-type"]
