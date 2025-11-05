"""
Session reader for Strands file session manager.
Reads and parses session data from the filesystem.
"""

import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class SessionReader:
    """Reads session data from FileSessionManager storage."""

    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        if not self.storage_dir.exists():
            raise ValueError(f"Storage directory does not exist: {storage_dir}")

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List all available sessions."""
        sessions = []

        for session_dir in self.storage_dir.glob("session_*"):
            if session_dir.is_dir():
                session_file = session_dir / "session.json"
                if session_file.exists():
                    try:
                        with open(session_file, "r", encoding="utf-8") as f:
                            session_data = json.load(f)

                        # Get message count
                        message_count = self._count_messages(session_dir)

                        sessions.append(
                            {
                                "session_id": session_data.get("session_id"),
                                "session_type": session_data.get("session_type"),
                                "created_at": session_data.get("created_at"),
                                "updated_at": session_data.get("updated_at"),
                                "message_count": message_count,
                                "path": str(session_dir),
                            }
                        )
                    except Exception as e:
                        print(f"Error reading session {session_dir}: {e}")

        # Sort by updated_at descending
        sessions.sort(key=lambda x: x.get("updated_at", ""), reverse=True)
        return sessions

    def _count_messages(self, session_dir: Path) -> int:
        """Count total messages in a session."""
        count = 0
        agents_dir = session_dir / "agents"
        if agents_dir.exists():
            for agent_dir in agents_dir.iterdir():
                if agent_dir.is_dir():
                    messages_dir = agent_dir / "messages"
                    if messages_dir.exists():
                        count += len(list(messages_dir.glob("message_*.json")))
        return count

    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed session information."""
        session_dir = self.storage_dir / f"session_{session_id}"

        if not session_dir.exists():
            return None

        session_file = session_dir / "session.json"
        if not session_file.exists():
            return None

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            # Get all agents
            agents = self._get_agents(session_dir)

            # Get all messages across all agents
            messages = self._get_all_messages(session_dir)

            return {
                "session_id": session_data.get("session_id"),
                "session_type": session_data.get("session_type"),
                "created_at": session_data.get("created_at"),
                "updated_at": session_data.get("updated_at"),
                "agents": agents,
                "messages": messages,
            }
        except Exception as e:
            print(f"Error reading session {session_id}: {e}")
            return None

    def _get_agents(self, session_dir: Path) -> List[Dict[str, Any]]:
        """Get all agents in a session."""
        agents = []
        agents_dir = session_dir / "agents"

        if not agents_dir.exists():
            return agents

        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                agent_file = agent_dir / "agent.json"
                if agent_file.exists():
                    try:
                        with open(agent_file, "r", encoding="utf-8") as f:
                            agent_data = json.load(f)
                        agents.append(agent_data)
                    except Exception as e:
                        print(f"Error reading agent {agent_dir}: {e}")

        return agents

    def _get_all_messages(self, session_dir: Path) -> List[Dict[str, Any]]:
        """Get all messages from all agents in chronological order."""
        messages = []
        agents_dir = session_dir / "agents"

        if not agents_dir.exists():
            return messages

        for agent_dir in agents_dir.iterdir():
            if agent_dir.is_dir():
                messages_dir = agent_dir / "messages"
                if messages_dir.exists():
                    for message_file in messages_dir.glob("message_*.json"):
                        try:
                            with open(message_file, "r", encoding="utf-8") as f:
                                message_data = json.load(f)

                            # Add agent info to message
                            message_data["agent_id"] = agent_dir.name
                            messages.append(message_data)
                        except Exception as e:
                            print(f"Error reading message {message_file}: {e}")

        # Sort by message_id (or created_at if available)
        messages.sort(key=lambda x: x.get("message_id", 0))
        return messages

    def get_messages(
        self, session_id: str, limit: Optional[int] = None, offset: int = 0
    ) -> List[Dict[str, Any]]:
        """Get messages for a session with pagination."""
        session = self.get_session(session_id)
        if not session:
            return []

        messages = session.get("messages", [])

        if offset:
            messages = messages[offset:]

        if limit:
            messages = messages[:limit]

        return messages
