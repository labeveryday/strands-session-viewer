# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Session analysis capabilities using Strands agents framework
- Multiple model provider support (Anthropic, OpenAI, Ollama)
- Custom analysis tools using @tool decorator pattern
  - `get_session_summary`: Session statistics and information
  - `extract_session_errors`: Find and list all errors
  - `analyze_tool_usage`: Tool usage statistics
  - `get_conversation_messages`: Full conversation flow
  - `search_session_content`: Search within messages
- API endpoints for analysis operations
  - `/api/ai/status`: Check analysis availability
  - `/api/sessions/{id}/analyze`: Quick analysis (summarize, errors, improvements)
  - `/api/sessions/{id}/chat`: Interactive Q&A
- Frontend analysis panel with quick actions and chat interface
- CLI flags for model provider selection (`--model-provider`, `--model-id`)
- Optional installation via `pip install 'strands-session-viewer[ai]'`

### Changed
- SessionAnalyzer now accepts model instances instead of model ID strings
- Updated documentation with multi-provider configuration examples

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
