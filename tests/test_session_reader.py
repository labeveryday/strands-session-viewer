"""Tests for SessionReader."""

import pytest

from strands_viewer.session_reader import SessionReader


def test_session_reader_init(temp_sessions_dir):
    """Test SessionReader initialization."""
    reader = SessionReader(temp_sessions_dir)
    assert reader.storage_dir.exists()


def test_session_reader_invalid_dir():
    """Test SessionReader with invalid directory."""
    with pytest.raises(ValueError, match="Storage directory does not exist"):
        SessionReader("/nonexistent/path")


def test_list_sessions(temp_sessions_dir):
    """Test listing all sessions."""
    reader = SessionReader(temp_sessions_dir)
    sessions = reader.list_sessions()

    assert len(sessions) == 2
    assert all("session_id" in s for s in sessions)
    assert all("message_count" in s for s in sessions)

    # Should be sorted by updated_at descending
    session_ids = [s["session_id"] for s in sessions]
    assert "test_2" in session_ids
    assert "test_1" in session_ids


def test_get_session(temp_sessions_dir):
    """Test getting a specific session."""
    reader = SessionReader(temp_sessions_dir)
    session = reader.get_session("test_1")

    assert session is not None
    assert session["session_id"] == "test_1"
    assert session["session_type"] == "AGENT"
    assert "agents" in session
    assert "messages" in session
    assert len(session["messages"]) == 4


def test_get_nonexistent_session(temp_sessions_dir):
    """Test getting a session that doesn't exist."""
    reader = SessionReader(temp_sessions_dir)
    session = reader.get_session("nonexistent")
    assert session is None


def test_get_messages(temp_sessions_dir):
    """Test getting messages for a session."""
    reader = SessionReader(temp_sessions_dir)
    messages = reader.get_messages("test_1")

    assert len(messages) == 4
    # Should be sorted by message_id
    assert messages[0]["message_id"] == 1
    assert messages[1]["message_id"] == 2


def test_get_messages_with_pagination(temp_sessions_dir):
    """Test getting messages with limit and offset."""
    reader = SessionReader(temp_sessions_dir)

    # Get first 2 messages
    messages = reader.get_messages("test_1", limit=2)
    assert len(messages) == 2
    assert messages[0]["message_id"] == 1

    # Get messages with offset
    messages = reader.get_messages("test_1", offset=2)
    assert len(messages) == 2
    assert messages[0]["message_id"] == 3

    # Combine limit and offset
    messages = reader.get_messages("test_1", limit=1, offset=1)
    assert len(messages) == 1
    assert messages[0]["message_id"] == 2


def test_message_content_structure(temp_sessions_dir):
    """Test that message content has expected structure."""
    reader = SessionReader(temp_sessions_dir)
    session = reader.get_session("test_1")

    # Check user message
    user_msg = session["messages"][0]
    assert user_msg["message"]["role"] == "user"
    assert "content" in user_msg["message"]
    assert len(user_msg["message"]["content"]) > 0

    # Check assistant message with tool use
    assistant_msg = session["messages"][1]
    assert assistant_msg["message"]["role"] == "assistant"
    assert "toolUse" in assistant_msg["message"]["content"][0]

    # Check tool result
    tool_result_msg = session["messages"][2]
    assert "toolResult" in tool_result_msg["message"]["content"][0]
    assert tool_result_msg["message"]["content"][0]["toolResult"]["status"] == "success"

    # Check error result
    error_msg = session["messages"][3]
    assert "toolResult" in error_msg["message"]["content"][0]
    assert error_msg["message"]["content"][0]["toolResult"]["status"] == "error"


def test_count_messages(temp_sessions_dir):
    """Test message counting."""
    reader = SessionReader(temp_sessions_dir)
    sessions = reader.list_sessions()

    session1 = next(s for s in sessions if s["session_id"] == "test_1")
    session2 = next(s for s in sessions if s["session_id"] == "test_2")

    assert session1["message_count"] == 4
    assert session2["message_count"] == 1
