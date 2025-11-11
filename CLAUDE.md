# Development Notes

## Project Structure

This is a session viewer for Strands agents, built with FastAPI backend and vanilla HTML/CSS/JS frontend.

## Key Components

### Backend (`src/strands_viewer/`)

- **`server.py`** - FastAPI application with API endpoints
- **`session_reader.py`** - Reads and parses session JSON files
- **`export_formatter.py`** - Formats sessions for export (Markdown, JSON, text)
- **`ai_analysis.py`** - Optional analysis features using Strands agents
- **`models/`** - Model provider factory functions (Anthropic, OpenAI, Ollama)
- **`cli.py`** - Command-line interface
- **`static/index.html`** - Web interface (single file, no build process)

### Testing (`tests/`)

- Full test coverage using pytest
- Tests for CLI, server endpoints, session reading, and export functionality
- Run with: `pytest` or `pytest --cov=strands_viewer --cov-report=html`

## Design Decisions

### No Build Process
- Frontend uses CDN-hosted Tailwind CSS and Alpine.js
- Single HTML file with embedded JavaScript
- Makes it easy to modify and deploy

### Optional Analysis Features
- Analysis features are completely optional (`pip install 'strands-session-viewer[ai]'`)
- Graceful degradation when not installed
- Supports multiple model providers via factory pattern

### Model Provider Pattern
- Factory functions in `models/` directory
- Each provider (Anthropic, OpenAI, Ollama) has its own configuration
- Model instances passed to SessionAnalyzer at initialization

### Tool-Based Analysis
- Uses Strands `@tool` decorator for custom analysis tools
- Agent intelligently calls only needed tools
- More efficient than passing large text context

## Development Workflow

### Setup
```bash
# Install in development mode
pip install -e ".[dev]"

# With analysis features
pip install -e ".[ai,dev]"
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=strands_viewer --cov-report=html

# Specific test
pytest tests/test_server.py::test_list_sessions_endpoint -v
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint
ruff check src/ tests/

# Fix linting issues
ruff check --fix src/ tests/
```

### Running Locally
```bash
# From source
python -m strands_viewer.cli --dir ./sessions

# After install
strands-viewer --dir ./sessions
```

## API Endpoints

### Core Endpoints
- `GET /` - Serve web interface
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details
- `GET /api/sessions/{session_id}/messages` - Get session messages (paginated)
- `GET /api/sessions/{session_id}/export?format={markdown|json|text}` - Export session

### Analysis Endpoints (Optional)
- `GET /api/ai/status` - Check if analysis is available
- `POST /api/sessions/{session_id}/analyze` - Run analysis (summarize, errors, improvements)
- `POST /api/sessions/{session_id}/chat` - Interactive Q&A about session

## Session File Format

Sessions are stored as JSON files following the Strands `FileSessionManager` format:

```json
{
  "session_id": "session-123",
  "session_type": "agent",
  "created_at": "2025-01-11T12:00:00",
  "updated_at": "2025-01-11T12:30:00",
  "messages": [
    {
      "message": {
        "role": "user|assistant",
        "content": [
          {"text": "..."},
          {"toolUse": {...}},
          {"toolResult": {...}}
        ]
      }
    }
  ]
}
```

## Adding New Model Providers

To add a new model provider:

1. Add factory function to `src/strands_viewer/models/models.py`:
```python
def newprovider_model(api_key: str = os.getenv("PROVIDER_API_KEY"), ...) -> NewProviderModel:
    """Create a new provider model instance."""
    return NewProviderModel(...)
```

2. Export in `src/strands_viewer/models/__init__.py`:
```python
from .models import anthropic_model, openai_model, ollama_model, newprovider_model

__all__ = ["anthropic_model", "openai_model", "ollama_model", "newprovider_model"]
```

3. Add CLI option in `src/strands_viewer/cli.py`:
```python
parser.add_argument(
    "--model-provider",
    choices=["anthropic", "openai", "ollama", "newprovider"],
    ...
)

# In main():
elif args.model_provider == "newprovider":
    model = newprovider_model(**model_kwargs)
```

4. Update README with configuration instructions

## Common Tasks

### Adding a New Analysis Tool

Edit `ai_analysis.py` and add to `_create_session_tools()`:

```python
@tool
def my_new_tool(param: str) -> str:
    """Tool description for the agent."""
    # Access session via self._current_session
    # Return string result
    return result

# Add to return list
return [
    get_session_summary,
    extract_session_errors,
    analyze_tool_usage,
    get_conversation_messages,
    search_session_content,
    my_new_tool,  # Add here
]
```

### Adding a New Export Format

1. Add formatter function to `export_formatter.py`
2. Add to `FORMAT_HANDLERS` dict
3. Add content type to server endpoint
4. Update tests

## Notes

- The viewer binds to `0.0.0.0` by default for LAN accessibility
- Sessions directory must exist before starting
- Analysis features require valid API credentials
- All dependencies are pinned in `pyproject.toml`
