"""Pytest fixtures for strands-session-viewer tests."""

import json
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_sessions_dir():
    """Create a temporary sessions directory with sample data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_dir = Path(tmpdir)

        # Create session_test_1
        session1_dir = sessions_dir / "session_test_1"
        agent1_dir = session1_dir / "agents" / "agent_default" / "messages"
        agent1_dir.mkdir(parents=True)

        # Session metadata
        session1_meta = {
            "session_id": "test_1",
            "session_type": "AGENT",
            "created_at": "2025-11-05T10:00:00.000000+00:00",
            "updated_at": "2025-11-05T10:05:00.000000+00:00",
        }
        with open(session1_dir / "session.json", "w") as f:
            json.dump(session1_meta, f, indent=2)

        # Agent metadata
        agent1_meta = {
            "agent_id": "agent_default",
            "created_at": "2025-11-05T10:00:00.000000+00:00",
        }
        with open(session1_dir / "agents" / "agent_default" / "agent.json", "w") as f:
            json.dump(agent1_meta, f, indent=2)

        # User message
        message1 = {
            "message": {"role": "user", "content": [{"text": "Hello, agent!"}]},
            "message_id": 1,
            "redact_message": None,
            "created_at": "2025-11-05T10:00:01.000000+00:00",
            "updated_at": "2025-11-05T10:00:01.000000+00:00",
        }
        with open(agent1_dir / "message_1.json", "w") as f:
            json.dump(message1, f, indent=2)

        # Assistant message with tool use
        message2 = {
            "message": {
                "role": "assistant",
                "content": [
                    {
                        "toolUse": {
                            "toolUseId": "shell_1",
                            "name": "shell",
                            "input": {"command": "ls -la"},
                        }
                    }
                ],
            },
            "message_id": 2,
            "redact_message": None,
            "created_at": "2025-11-05T10:00:02.000000+00:00",
            "updated_at": "2025-11-05T10:00:02.000000+00:00",
        }
        with open(agent1_dir / "message_2.json", "w") as f:
            json.dump(message2, f, indent=2)

        # Tool result message
        message3 = {
            "message": {
                "role": "user",
                "content": [
                    {
                        "toolResult": {
                            "status": "success",
                            "content": [
                                {"text": "total 0\ndrwxr-xr-x 2 user user 4096 Nov 5 10:00 ."}
                            ],
                            "toolUseId": "shell_1",
                        }
                    }
                ],
            },
            "message_id": 3,
            "redact_message": None,
            "created_at": "2025-11-05T10:00:03.000000+00:00",
            "updated_at": "2025-11-05T10:00:03.000000+00:00",
        }
        with open(agent1_dir / "message_3.json", "w") as f:
            json.dump(message3, f, indent=2)

        # Error message
        message4 = {
            "message": {
                "role": "user",
                "content": [
                    {
                        "toolResult": {
                            "status": "error",
                            "content": [{"text": "Command failed with error"}],
                            "toolUseId": "shell_2",
                        }
                    }
                ],
            },
            "message_id": 4,
            "redact_message": None,
            "created_at": "2025-11-05T10:00:04.000000+00:00",
            "updated_at": "2025-11-05T10:00:04.000000+00:00",
        }
        with open(agent1_dir / "message_4.json", "w") as f:
            json.dump(message4, f, indent=2)

        # Create session_test_2 (minimal)
        session2_dir = sessions_dir / "session_test_2"
        agent2_dir = session2_dir / "agents" / "agent_default" / "messages"
        agent2_dir.mkdir(parents=True)

        session2_meta = {
            "session_id": "test_2",
            "session_type": "AGENT",
            "created_at": "2025-11-05T11:00:00.000000+00:00",
            "updated_at": "2025-11-05T11:00:00.000000+00:00",
        }
        with open(session2_dir / "session.json", "w") as f:
            json.dump(session2_meta, f, indent=2)

        agent2_meta = {
            "agent_id": "agent_default",
            "created_at": "2025-11-05T11:00:00.000000+00:00",
        }
        with open(session2_dir / "agents" / "agent_default" / "agent.json", "w") as f:
            json.dump(agent2_meta, f, indent=2)

        message5 = {
            "message": {"role": "user", "content": [{"text": "Simple message"}]},
            "message_id": 1,
            "redact_message": None,
            "created_at": "2025-11-05T11:00:01.000000+00:00",
            "updated_at": "2025-11-05T11:00:01.000000+00:00",
        }
        with open(agent2_dir / "message_1.json", "w") as f:
            json.dump(message5, f, indent=2)

        yield str(sessions_dir)
