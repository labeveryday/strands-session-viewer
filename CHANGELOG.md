# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **AI-Powered Analysis** using Strands agents framework
  - Session analysis capabilities with custom tools
  - Multiple model provider support (Anthropic, OpenAI, Ollama)
  - Default to Claude Haiku 4.5 for fast, cost-effective analysis
  - Custom analysis tools using @tool decorator pattern:
    - `get_session_summary`: Session statistics and information
    - `extract_session_errors`: Find and list all errors
    - `analyze_tool_usage`: Tool usage statistics
    - `get_conversation_messages`: Full conversation flow
    - `search_session_content`: Search within messages
  - API endpoints for analysis operations:
    - `/api/ai/status`: Check analysis availability
    - `/api/sessions/{id}/analyze`: Quick analysis (summarize, errors, improvements)
    - `/api/sessions/{id}/chat`: Interactive Q&A
  - CLI flags for model provider selection (`--model-provider`, `--model-id`)
  - Optional installation via `pip install 'strands-session-viewer[ai]'`

- **Modern Three-Panel UI**
  - Collapsible left sidebar (280px) with hamburger menu toggle
  - Expanded middle panel for messages with flex-grow layout
  - Fixed right panel (400px) for AI chat (visible on xl screens)
  - Responsive breakpoints (mobile, tablet, desktop)
  - Mobile-first design with sidebar overlay on small screens
  - Smooth slide animations for sidebar collapse/expand
  - Custom scrollbar styling for better aesthetics
  - Session state persistence across page loads

- **Enhanced UX**
  - Markdown rendering for AI responses using marked.js
    - Proper formatting for headings, code blocks, lists, blockquotes
    - Syntax highlighting for inline code
    - Dark theme for code blocks
  - Collapsible tool calls with "Show Input" button
  - Collapsible tool results with "Show Output" button
  - Chronological conversation flow for AI interactions
  - Session ID display in AI panel header
  - Word wrapping to prevent content overflow
  - "Clear Conversation" button for AI chat

### Changed
- SessionAnalyzer now accepts model instances instead of model ID strings
- Reorganized UI from stacked vertical layout to three-panel dashboard
- AI analysis results now flow chronologically in chat history (no separate "Latest Response" section)
- Tool results now collapsed by default (matching tool calls behavior)
- Default model provider is now Anthropic with Haiku 4.5
- Updated documentation with multi-provider configuration examples
- Clarified installation and usage workflow in README
  - Separated viewer installation from agent projects
  - Added step-by-step typical workflow
  - Explained navigation to sessions directory
  - Documented new UI layout and features

### Fixed
- Word wrapping for long headings and text in AI responses
- Chat conversation flow to avoid duplicate responses
- Tool results now properly collapsible like tool calls

## [0.1.0] - 2025-01-11

### Added
- Initial release
- Browser-based session viewer for Strands agents
- Session list and detail views
- Message timeline with role-based formatting
- Tool call and result visualization
- Search and filter capabilities
- Error highlighting for failed tool executions
- Export functionality (Markdown, JSON, plain text)
- FastAPI backend with REST API
- Modern web interface using Tailwind CSS and Alpine.js
- CLI with customizable port and directory options
- Comprehensive test suite
