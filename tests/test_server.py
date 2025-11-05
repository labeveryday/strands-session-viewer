"""Tests for FastAPI server."""

import pytest
from fastapi.testclient import TestClient

from strands_viewer.server import SessionViewerApp


@pytest.fixture
def test_client(temp_sessions_dir):
    """Create a test client for the FastAPI app."""
    app = SessionViewerApp(temp_sessions_dir, port=8000)
    client = TestClient(app.app)
    return client


def test_list_sessions_endpoint(test_client):
    """Test the /api/sessions endpoint."""
    response = test_client.get("/api/sessions")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "sessions" in data
    assert len(data["sessions"]) == 2


def test_get_session_endpoint(test_client):
    """Test the /api/sessions/{session_id} endpoint."""
    response = test_client.get("/api/sessions/test_1")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "session" in data
    assert data["session"]["session_id"] == "test_1"
    assert len(data["session"]["messages"]) == 4


def test_get_nonexistent_session_endpoint(test_client):
    """Test getting a nonexistent session returns 404."""
    response = test_client.get("/api/sessions/nonexistent")

    assert response.status_code == 404
    data = response.json()
    assert "detail" in data


def test_get_messages_endpoint(test_client):
    """Test the /api/sessions/{session_id}/messages endpoint."""
    response = test_client.get("/api/sessions/test_1/messages")

    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "messages" in data
    assert len(data["messages"]) == 4


def test_get_messages_with_limit(test_client):
    """Test getting messages with limit parameter."""
    response = test_client.get("/api/sessions/test_1/messages?limit=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 2


def test_get_messages_with_offset(test_client):
    """Test getting messages with offset parameter."""
    response = test_client.get("/api/sessions/test_1/messages?offset=2")

    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 2
    assert data["messages"][0]["message_id"] == 3


def test_get_messages_with_limit_and_offset(test_client):
    """Test getting messages with both limit and offset."""
    response = test_client.get("/api/sessions/test_1/messages?limit=1&offset=1")

    assert response.status_code == 200
    data = response.json()
    assert len(data["messages"]) == 1
    assert data["messages"][0]["message_id"] == 2


def test_index_endpoint(test_client):
    """Test the root / endpoint returns HTML."""
    response = test_client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert b"Strands Session Viewer" in response.content


def test_api_error_handling(test_client):
    """Test that API errors are handled gracefully."""
    # Try to get messages for nonexistent session
    response = test_client.get("/api/sessions/nonexistent/messages")

    assert response.status_code == 200  # Returns empty list, not an error
    data = response.json()
    assert data["messages"] == []
