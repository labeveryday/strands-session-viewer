# Strands Session Viewer

[![CI](https://github.com/labeveryday/strands-session-viewer/workflows/CI/badge.svg)](https://github.com/labeveryday/strands-session-viewer/actions)
[![Python Versions](https://img.shields.io/pypi/pyversions/strands-session-viewer.svg)](https://pypi.org/project/strands-session-viewer/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A clean, browser-based viewer for [Strands](https://github.com/strands-agents/sdk-python) agent sessions. View your agent conversations, tool calls, and results in an intuitive web interface.

Perfect for debugging, teaching, and understanding how your AI agents work.

## Features

- 📋 **Session Browser** - List and browse all your agent sessions
- 💬 **Message Timeline** - View full conversation flow chronologically
- 🔧 **Tool Call Visualization** - See tool calls and their results clearly
- 🔍 **Search & Filter** - Find messages by content, role, or tool usage
- ❌ **Error Highlighting** - Quickly spot failed tool executions
- 📥 **Export Sessions** - Download as Markdown, JSON, or plain text
- 🎨 **Clean UI** - Modern interface built with Tailwind CSS
- ⚡ **Fast & Lightweight** - No build process, runs instantly
- 🔄 **Real-time Refresh** - Reload sessions to see new messages

## Quick Start

### Installation

```bash
pip install strands-session-viewer
```

### Usage

```bash
# View sessions in ./sessions directory
strands-viewer

# Or specify a custom directory
strands-viewer /path/to/your/sessions

# Use a different port
strands-viewer --port 8080

# See all options
strands-viewer --help
```

The viewer will automatically open in your browser at `http://localhost:8000`

## Interface Overview

### Session List (Left Sidebar)
- Click any session to view its messages
- Shows message count and last update time
- Sessions sorted by most recent first

### Message View (Main Panel)
- **User messages** (blue) - Your prompts to the agent
- **Assistant messages** (purple) - Agent responses
- **Tool calls** (yellow) - Tools the agent invoked
- **Tool results** (green/red) - Successful or failed tool outputs

### Filters & Search
- **Search** - Find text in messages, tool names, or outputs
- **Role Filter** - Show only user or assistant messages
- **Tool Calls** - Show only messages with tool usage
- **Errors** - Show only failed tool executions

### Export Options
- **Markdown** - Perfect for documentation and course materials
- **JSON** - For programmatic analysis and archiving
- **Plain Text** - Simple, readable format for sharing

## Use Cases

### For Developers
- Debug agent behavior and tool usage
- Track token usage and performance
- Understand conversation flow
- Spot errors and failures quickly

### For Teachers
- Show students how agents work
- Demonstrate tool calling in action
- Compare different agent runs
- Create course materials from sessions

### For Researchers
- Analyze agent decision-making
- Study tool usage patterns
- Export sessions for documentation
- Share results with collaborators

## Project Structure

```
strands-session-viewer/
├── src/
│   └── strands_viewer/
│       ├── __init__.py       # Package initialization
│       ├── __version__.py    # Version info
│       ├── cli.py            # Command-line interface
│       ├── server.py         # FastAPI server
│       ├── session_reader.py # Session file parser
│       └── static/
│           └── index.html    # Web interface
├── pyproject.toml           # Package configuration
├── LICENSE                  # MIT License
└── README.md               # This file
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

Dependencies are automatically installed with the package.

## API Endpoints

The viewer exposes a simple REST API:

- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details
- `GET /api/sessions/{session_id}/messages` - Get session messages (with pagination)
- `GET /api/sessions/{session_id}/export?format=markdown` - Export session (formats: markdown, json, text)

## Development

### Local Installation

```bash
# Clone the repository
git clone https://github.com/labeveryday/strands-session-viewer
cd strands-session-viewer

# Install in development mode
pip install -e .

# Or with dev dependencies
pip install -e ".[dev]"
```

### Run from Source

```bash
python -m strands_viewer.cli --dir ./sessions
```

## Tech Stack

- **Backend**: FastAPI + uvicorn
- **Frontend**: HTML + Tailwind CSS (CDN) + Alpine.js (CDN)
- **No build process required!**

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see [LICENSE](LICENSE) file for details

## Acknowledgments

Built for the [Strands](https://github.com/strands-agents/sdk-python) agent framework.

## Links

- **PyPI**: https://pypi.org/project/strands-session-viewer/
- **GitHub**: https://github.com/labeveryday/strands-session-viewer
- **Strands SDK**: https://github.com/strands-agents/sdk-python
- **Issues**: https://github.com/labeveryday/strands-session-viewer/issues

---

Made with ❤️ for the Strands community
