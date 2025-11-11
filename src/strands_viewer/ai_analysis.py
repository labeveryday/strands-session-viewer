"""AI-powered session analysis using Strands agents with custom tools."""

from typing import Dict, Any, List, Optional

try:
    from strands import Agent, tool

    STRANDS_AVAILABLE = True
except ImportError:
    STRANDS_AVAILABLE = False
    tool = None  # type: ignore


class SessionAnalyzer:
    """Analyze agent sessions using Strands AI agents with custom analysis tools."""

    def __init__(self, model: Optional[Any] = None):
        """
        Initialize the session analyzer.

        Args:
            model: Optional model instance from models.anthropic_model(), models.openai_model(),
                   or models.ollama_model(). Defaults to Claude 4 on Bedrock if not provided.
        """
        if not STRANDS_AVAILABLE:
            raise ImportError(
                "Strands agents not installed. Install with: pip install strands-session-viewer[ai]"
            )

        self.model = model
        self._agent = None
        self._current_session = None

    def _create_session_tools(self, session: Dict[str, Any]) -> List:
        """
        Create custom tools for analyzing the current session.

        Args:
            session: Session data dictionary

        Returns:
            List of tool functions
        """
        # Store session in instance for tools to access
        self._current_session = session

        @tool
        def get_session_summary() -> str:
            """Get a summary of the session's basic information and statistics.

            Returns:
                Summary with session ID, type, message count, creation date
            """
            s = self._current_session
            messages = s.get("messages", [])

            # Count different message types
            user_msgs = sum(1 for m in messages if m.get("message", {}).get("role") == "user")
            assistant_msgs = sum(
                1 for m in messages if m.get("message", {}).get("role") == "assistant"
            )

            # Count tool usage
            tool_calls = 0
            tool_results = 0
            for msg in messages:
                for content in msg.get("message", {}).get("content", []):
                    if "toolUse" in content:
                        tool_calls += 1
                    if "toolResult" in content:
                        tool_results += 1

            return f"""Session Summary:
- Session ID: {s.get('session_id', 'Unknown')}
- Type: {s.get('session_type', 'Unknown')}
- Created: {s.get('created_at', 'Unknown')}
- Updated: {s.get('updated_at', 'Unknown')}
- Total Messages: {len(messages)}
  - User messages: {user_msgs}
  - Assistant messages: {assistant_msgs}
- Tool Activity:
  - Tool calls made: {tool_calls}
  - Tool results received: {tool_results}
"""

        @tool
        def extract_session_errors() -> str:
            """Find and extract all errors that occurred in the session.

            Returns:
                Detailed list of all errors with context, or message if no errors found
            """
            errors = []
            messages = self._current_session.get("messages", [])

            for msg_idx, msg_wrapper in enumerate(messages, 1):
                msg = msg_wrapper.get("message", {})
                for content_idx, content in enumerate(msg.get("content", [])):
                    if "toolResult" in content:
                        tool_result = content["toolResult"]
                        if tool_result.get("status") == "error":
                            # Get error details
                            error_text = ""
                            for rc in tool_result.get("content", []):
                                if "text" in rc:
                                    error_text = rc["text"]
                                    break

                            # Find the corresponding tool call
                            tool_use_id = tool_result.get("toolUseId", "unknown")

                            errors.append(
                                {
                                    "message_number": msg_idx,
                                    "tool_use_id": tool_use_id,
                                    "error_text": error_text[:500],  # Limit length
                                }
                            )

            if not errors:
                return "No errors found in this session."

            result = [f"Found {len(errors)} error(s) in the session:\n"]
            for i, error in enumerate(errors, 1):
                result.append(
                    f"\nError #{i}:"
                    f"\n- Message: #{error['message_number']}"
                    f"\n- Tool Use ID: {error['tool_use_id']}"
                    f"\n- Error: {error['error_text']}"
                )

            return "\n".join(result)

        @tool
        def analyze_tool_usage() -> str:
            """Analyze which tools were used and how often.

            Returns:
                Statistics about tool usage in the session
            """
            tool_stats = {}
            messages = self._current_session.get("messages", [])

            for msg_wrapper in messages:
                msg = msg_wrapper.get("message", {})
                for content in msg.get("content", []):
                    if "toolUse" in content:
                        tool_name = content["toolUse"].get("name", "unknown")
                        tool_stats[tool_name] = tool_stats.get(tool_name, 0) + 1

            if not tool_stats:
                return "No tools were used in this session."

            result = ["Tool Usage Analysis:\n"]
            for tool_name, count in sorted(tool_stats.items(), key=lambda x: x[1], reverse=True):
                result.append(f"- {tool_name}: {count} call(s)")

            return "\n".join(result)

        @tool
        def get_conversation_messages() -> str:
            """Get the full conversation flow with all messages.

            Returns:
                Complete conversation with user prompts and assistant responses
            """
            messages = self._current_session.get("messages", [])
            result = ["Complete Conversation:\n"]

            for msg_idx, msg_wrapper in enumerate(messages, 1):
                msg = msg_wrapper.get("message", {})
                role = msg.get("role", "unknown")
                result.append(f"\nMessage #{msg_idx} ({role.upper()}):")

                for content in msg.get("content", []):
                    if "text" in content:
                        text = content["text"]
                        # Limit very long texts
                        if len(text) > 1000:
                            text = text[:1000] + "... (truncated)"
                        result.append(f"  {text}")

                    if "toolUse" in content:
                        tool_use = content["toolUse"]
                        result.append(f"  [Tool Call: {tool_use.get('name', 'unknown')}]")

                    if "toolResult" in content:
                        tool_result = content["toolResult"]
                        status = tool_result.get("status", "unknown")
                        result.append(f"  [Tool Result: {status}]")

            return "\n".join(result)

        @tool
        def search_session_content(query: str) -> str:
            """Search for specific text or patterns in the session messages.

            Args:
                query: Text to search for (case-insensitive)

            Returns:
                Messages containing the search query with context
            """
            query_lower = query.lower()
            matches = []
            messages = self._current_session.get("messages", [])

            for msg_idx, msg_wrapper in enumerate(messages, 1):
                msg = msg_wrapper.get("message", {})
                role = msg.get("role", "unknown")

                for content in msg.get("content", []):
                    if "text" in content:
                        text = content["text"]
                        if query_lower in text.lower():
                            # Get context around the match
                            match_pos = text.lower().index(query_lower)
                            start = max(0, match_pos - 100)
                            end = min(len(text), match_pos + len(query) + 100)
                            context = text[start:end]
                            if start > 0:
                                context = "..." + context
                            if end < len(text):
                                context = context + "..."

                            matches.append(
                                {
                                    "message": msg_idx,
                                    "role": role,
                                    "context": context,
                                }
                            )

            if not matches:
                return f"No matches found for '{query}' in session messages."

            result = [f"Found {len(matches)} match(es) for '{query}':\n"]
            for match in matches:
                result.append(
                    f"\nMessage #{match['message']} ({match['role']}):" f"\n  {match['context']}"
                )

            return "\n".join(result)

        return [
            get_session_summary,
            extract_session_errors,
            analyze_tool_usage,
            get_conversation_messages,
            search_session_content,
        ]

    def _get_agent(self, session: Dict[str, Any]) -> "Agent":
        """Get or create the analysis agent with session-specific tools."""
        # Create tools for this session
        tools = self._create_session_tools(session)

        # Create agent with tools
        if self.model:
            return Agent(model=self.model, tools=tools)
        else:
            return Agent(tools=tools)  # Uses default Claude 4 on Bedrock

    def summarize_session(self, session: Dict[str, Any]) -> str:
        """
        Generate an AI summary of the session.

        Args:
            session: Session data dictionary

        Returns:
            Summary text
        """
        agent = self._get_agent(session)

        prompt = """Analyze this Strands agent session and provide a concise summary.

Use the available tools to gather information about the session, then provide:
1. Brief overview of what the agent did
2. Key tools used and their purposes
3. Any errors or failures that occurred
4. Overall assessment of the session

Keep the summary clear and actionable."""

        result = agent(prompt)
        return str(result)

    def analyze_errors(self, session: Dict[str, Any]) -> Optional[str]:
        """
        Analyze errors in the session and suggest fixes.

        Args:
            session: Session data dictionary

        Returns:
            Error analysis and suggestions, or None if no errors found
        """
        agent = self._get_agent(session)

        # First check if there are errors
        prompt_check = (
            "Use extract_session_errors to check if there are any errors in this session."
        )
        check_result = agent(prompt_check)

        if "No errors found" in str(check_result):
            return None

        prompt = """Analyze the errors in this Strands agent session and provide debugging help.

Use the available tools to gather information about the errors, then provide:
1. Identification of all errors that occurred
2. Likely causes of each error
3. Specific suggestions for fixing the issues
4. Best practices to avoid similar errors

Be specific and actionable in your recommendations."""

        result = agent(prompt)
        return str(result)

    def answer_question(
        self,
        session: Dict[str, Any],
        question: str,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        """
        Answer a question about the session.

        Args:
            session: Session data dictionary
            question: User's question
            chat_history: Optional previous conversation history

        Returns:
            Answer text
        """
        agent = self._get_agent(session)

        # Build prompt with history if available
        if chat_history:
            conversation_context = "\nPrevious conversation:\n"
            for entry in chat_history[-3:]:  # Last 3 exchanges for context
                role = entry.get("role", "user")
                content = entry.get("content", "")
                conversation_context += f"{role}: {content}\n"

            prompt = f"""{conversation_context}

User Question: {question}

Use the available tools to analyze the session and answer the user's question accurately."""
        else:
            prompt = f"""User Question: {question}

Use the available tools to analyze the session and answer the user's question accurately."""

        result = agent(prompt)
        return str(result)

    def suggest_improvements(self, session: Dict[str, Any]) -> str:
        """
        Suggest improvements for the agent behavior.

        Args:
            session: Session data dictionary

        Returns:
            Improvement suggestions
        """
        agent = self._get_agent(session)

        prompt = """Analyze this Strands agent session and suggest improvements.

Use the available tools to understand the session, then provide:
1. Opportunities to optimize tool usage
2. Suggestions for better prompting or configuration
3. Ways to improve efficiency or reduce token usage
4. Any patterns that could be improved

Focus on actionable, specific recommendations."""

        result = agent(prompt)
        return str(result)

    @staticmethod
    def is_available() -> bool:
        """Check if AI analysis is available."""
        return STRANDS_AVAILABLE
