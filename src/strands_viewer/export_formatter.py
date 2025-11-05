"""
Export formatters for converting sessions to different formats.
"""

import json
from datetime import datetime
from typing import Dict, Any


def format_timestamp(timestamp: str) -> str:
    """Format ISO timestamp to readable string."""
    try:
        dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %I:%M %p")
    except (ValueError, AttributeError):
        return timestamp


def format_markdown(session: Dict[str, Any]) -> str:
    """Format session as Markdown."""
    lines = []

    # Header
    lines.append(f"# Session: {session.get('session_id', 'Unknown')}")
    lines.append("")
    lines.append(f"**Type:** {session.get('session_type', 'N/A')}")
    lines.append(f"**Created:** {format_timestamp(session.get('created_at', ''))}")
    lines.append(f"**Updated:** {format_timestamp(session.get('updated_at', ''))}")
    lines.append(f"**Messages:** {len(session.get('messages', []))}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Messages
    lines.append("## Messages")
    lines.append("")

    for msg in session.get("messages", []):
        role = msg.get("message", {}).get("role", "unknown")
        msg_id = msg.get("message_id", "?")
        timestamp = format_timestamp(msg.get("created_at", ""))

        # Role icon
        icon = {"user": "👤", "assistant": "🤖", "system": "⚙️"}.get(role, "💬")

        lines.append(f"### {icon} {role.title()} #{msg_id}")
        lines.append(f"*{timestamp}*")
        lines.append("")

        # Content
        for content in msg.get("message", {}).get("content", []):
            # Text content
            if content.get("text"):
                lines.append(content["text"])
                lines.append("")

            # Tool use
            if content.get("toolUse"):
                tool = content["toolUse"]
                lines.append(f"**🔧 Tool Call:** `{tool.get('name', 'unknown')}`")
                lines.append("")
                lines.append("```json")
                lines.append(json.dumps(tool.get("input", {}), indent=2))
                lines.append("```")
                lines.append("")

            # Tool result
            if content.get("toolResult"):
                result = content["toolResult"]
                status = result.get("status", "unknown")
                emoji = "✅" if status == "success" else "❌"

                lines.append(f"**{emoji} Tool Result:** `{result.get('toolUseId', 'unknown')}`")
                lines.append(f"*Status: {status}*")
                lines.append("")

                # Result content
                for result_content in result.get("content", []):
                    if result_content.get("text"):
                        lines.append("```")
                        lines.append(result_content["text"])
                        lines.append("```")
                        lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def format_json(session: Dict[str, Any]) -> str:
    """Format session as pretty-printed JSON."""
    return json.dumps(session, indent=2, ensure_ascii=False)


def format_text(session: Dict[str, Any]) -> str:
    """Format session as plain text."""
    lines = []

    # Header
    lines.append("=" * 80)
    lines.append(f"Session: {session.get('session_id', 'Unknown')}")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"Type:     {session.get('session_type', 'N/A')}")
    lines.append(f"Created:  {format_timestamp(session.get('created_at', ''))}")
    lines.append(f"Updated:  {format_timestamp(session.get('updated_at', ''))}")
    lines.append(f"Messages: {len(session.get('messages', []))}")
    lines.append("")
    lines.append("=" * 80)
    lines.append("")

    # Messages
    for msg in session.get("messages", []):
        role = msg.get("message", {}).get("role", "unknown")
        msg_id = msg.get("message_id", "?")
        timestamp = format_timestamp(msg.get("created_at", ""))

        lines.append("-" * 80)
        lines.append(f"[{role.upper()} #{msg_id}] - {timestamp}")
        lines.append("-" * 80)
        lines.append("")

        # Content
        for content in msg.get("message", {}).get("content", []):
            # Text content
            if content.get("text"):
                lines.append(content["text"])
                lines.append("")

            # Tool use
            if content.get("toolUse"):
                tool = content["toolUse"]
                lines.append(f"[TOOL CALL: {tool.get('name', 'unknown')}]")
                lines.append(json.dumps(tool.get("input", {}), indent=2))
                lines.append("")

            # Tool result
            if content.get("toolResult"):
                result = content["toolResult"]
                status = result.get("status", "unknown")

                lines.append(
                    f"[TOOL RESULT: {result.get('toolUseId', 'unknown')} - {status.upper()}]"
                )

                # Result content
                for result_content in result.get("content", []):
                    if result_content.get("text"):
                        lines.append(result_content["text"])
                        lines.append("")

        lines.append("")

    return "\n".join(lines)


def get_filename(session_id: str, format_type: str) -> str:
    """Generate appropriate filename for export."""
    extensions = {"markdown": "md", "json": "json", "text": "txt"}
    ext = extensions.get(format_type, "txt")
    return f"session_{session_id}.{ext}"


def format_session(session: Dict[str, Any], format_type: str) -> str:
    """
    Format a session for export.

    Args:
        session: Session data dictionary
        format_type: One of 'markdown', 'json', 'text'

    Returns:
        Formatted string content

    Raises:
        ValueError: If format_type is not supported
    """
    formatters = {"markdown": format_markdown, "json": format_json, "text": format_text}

    formatter = formatters.get(format_type)
    if not formatter:
        raise ValueError(
            f"Unsupported format: {format_type}. Must be one of: {list(formatters.keys())}"
        )

    return formatter(session)
