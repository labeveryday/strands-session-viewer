# Strands Session Viewer

[![CI](https://github.com/labeveryday/strands-session-viewer/workflows/CI/badge.svg)](https://github.com/labeveryday/strands-session-viewer/actions)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A clean, browser-based viewer for [Strands](https://github.com/strands-agents/sdk-python) agent sessions. View your agent conversations, tool calls, and results in an intuitive web interface - now with **AI-powered analysis** using Strands agents.

Perfect for debugging, teaching, and understanding how your AI agents work.

## What It Does

When you use Strands' `FileSessionManager`, all your agent conversations are automatically saved to your local filesystem as JSON files. Each session includes the full conversation history, tool calls, and results - but they're stored in a raw JSON format that's difficult to read and navigate.

This viewer provides a beautiful web interface to browse and explore those locally stored sessions. Just point it at your sessions directory, and you can:
- Browse all your agent sessions in one place
- See the full conversation flow with proper formatting
- Understand what tools your agent called and why
- Export sessions for documentation or sharing

No need to manually parse JSON files or write custom scripts - just launch the viewer and start exploring your agent's behavior.

**Learn more**: [Strands Session Management Documentation](https://strandsagents.com/latest/documentation/docs/user-guide/concepts/agents/session-management/)

![Strands Session Viewer Interface](docs/images/hero-screenshot.png)

## Features

### Core Features
- 📋 **Session Browser** - List and browse all your agent sessions
- 💬 **Message Timeline** - View full conversation flow chronologically
- 🔧 **Tool Call Visualization** - See tool calls and their results clearly
- 🔍 **Search & Filter** - Find messages by content, role, or tool usage
- ❌ **Error Highlighting** - Quickly spot failed tool executions
- 📥 **Export Sessions** - Download as Markdown, JSON, or plain text
- 🎨 **Clean UI** - Modern interface built with Tailwind CSS
- ⚡ **Fast & Lightweight** - No build process, runs instantly
- 🔄 **Real-time Refresh** - Reload sessions to see new messages

### AI-Powered Analysis (Optional)
- 🤖 **AI Session Summaries** - Get instant AI-generated summaries of your sessions
- 🔍 **Error Analysis** - AI-powered debugging and error explanations
- 💡 **Improvement Suggestions** - Get recommendations to optimize your agents
- 💬 **Interactive Q&A** - Ask questions about sessions and get AI answers
- 🧠 **Powered by Strands** - Uses Strands agents for consistent, high-quality analysis
- 📝 **Markdown Formatted** - AI responses render with proper formatting (headings, code blocks, lists)
- 💬 **Conversation History** - Maintains context for multi-turn discussions about sessions

### Modern UI/UX
- 📱 **Three-Panel Layout** - Sessions (left), Messages (center), AI Chat (right)
- 🍔 **Collapsible Sidebar** - Toggle sessions panel with hamburger menu
- 📱 **Responsive Design** - Works on mobile, tablet, and desktop
- 🎯 **Collapsible Tool Details** - Tool calls and results are collapsed by default
- ⚡ **Optimized for Speed** - Defaults to Claude Haiku 4.5 for fast, cost-effective AI analysis

## Quick Start

### Installation

**Important**: Install the viewer globally or in a dedicated environment - **not** in your agent project's virtual environment.

```bash
# Basic installation (without AI features)
pip install git+https://github.com/labeveryday/strands-session-viewer.git

# With AI analysis features
pip install 'strands-session-viewer[ai] @ git+https://github.com/labeveryday/strands-session-viewer.git'
```

### Usage

The viewer works by pointing it at your agent's sessions directory. There are two ways to do this:

#### Option 1: Navigate to your sessions directory

```bash
# Go to your agent project where sessions are stored
cd /path/to/your-agent-project/src

# Launch the viewer (it will find ./sessions automatically)
strands-viewer
```

#### Option 2: Specify the path from anywhere

```bash
# Point to your agent's sessions from any directory
strands-viewer /path/to/your-agent-project/src/sessions

# Or use relative paths
strands-viewer ../my-agent/src/sessions
```

#### Common Examples

```bash
# Launch with default AI analysis (Anthropic Haiku 4.5 - fast and cost-effective)
strands-viewer

# Use a more powerful model for complex analysis
strands-viewer --model-id claude-sonnet-4-5-20250929

# View sessions with AI analysis using OpenAI
strands-viewer --model-provider openai --model-id gpt-5-mini-2025-08-07

# Use Ollama for local AI analysis
strands-viewer --model-provider ollama --model-id qwen3:4b

# Use a different port
strands-viewer --port 8080

# Specify sessions directory
strands-viewer /path/to/sessions

# See all options
strands-viewer --help
```

The viewer will automatically open in your browser at `http://localhost:8000`

**To stop the server:** Press `Ctrl+C` (or `Command+C` on Mac) in the terminal where it's running.

### Typical Workflow

1. **Install the viewer** (one time):
   ```bash
   pip install 'strands-session-viewer[ai] @ git+https://github.com/labeveryday/strands-session-viewer.git'
   ```

2. **Run your Strands agent** to generate sessions (in your agent project)

3. **Navigate to where your sessions are**:
   ```bash
   cd /path/to/your-agent-project/src
   ```

4. **Launch the viewer**:
   ```bash
   strands-viewer
   ```

5. **Browse and analyze** your sessions in the web interface

## AI-Powered Session Analysis

Enhance your debugging with AI-powered analysis using Strands agents. The viewer can automatically analyze your sessions, explain errors, suggest improvements, and answer questions about agent behavior.

### Installation

To enable AI analysis features, install with the `ai` extra:

```bash
pip install 'strands-session-viewer[ai] @ git+https://github.com/labeveryday/strands-session-viewer.git'
```

This installs the `strands-agents` package, which powers the AI analysis features.

### Configuration

AI analysis supports multiple model providers. By default, the viewer uses **Claude Haiku 4.5** via Anthropic for fast, cost-effective analysis.

#### **Anthropic** (Default)

```bash
# Configure AWS credentials for Bedrock
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-east-1"  # Optional, defaults to us-east-1

# Or use Anthropic API directly
export ANTHROPIC_API_KEY="your-api-key"

# Launch with default model (Haiku 4.5 - fast and cheap)
strands-viewer

# Or use a more powerful model
strands-viewer --model-id claude-sonnet-4-5-20250929
```

#### **OpenAI**

```bash
# Configure OpenAI API key
export OPENAI_API_KEY="your-api-key"

# Launch with OpenAI model
strands-viewer --model-provider openai --model-id gpt-5-mini-2025-08-07
```

#### **Ollama** (Local)

```bash
# Configure Ollama host (optional, defaults to localhost)
export OLLAMA_HOST="http://localhost:11434"

# Launch with Ollama model
strands-viewer --model-provider ollama --model-id qwen3:4b
```

**Learn more**: [Strands Quickstart Guide](https://strandsagents.com/latest/documentation/docs/user-guide/quickstart/)

### Features

Once configured, you'll see an **AI Analysis** panel on the right side when viewing any session:

#### Quick Analysis Buttons
- **📊 Summarize** - Get an AI-generated summary of the entire session
- **❌ Errors** - Analyze errors and get debugging suggestions
- **💡 Suggest** - Get recommendations to optimize your agent

Each quick analysis adds to the conversation history, maintaining context for follow-up questions.

#### Interactive Chat
Ask custom questions about the session and get instant AI-powered answers:
- "Why did this tool call fail?"
- "How could this agent be more efficient?"
- "What was the agent trying to accomplish here?"
- "Are there any security concerns in this session?"

**Features:**
- Maintains full conversation history for context
- Markdown-formatted responses with code blocks, headings, and lists
- Session ID displayed in panel header
- Clear conversation button to start fresh
- Powered by custom Strands analysis tools

### Example Workflow

```bash
# 1. Install with AI support
pip install 'strands-session-viewer[ai] @ git+https://github.com/labeveryday/strands-session-viewer.git'

# 2. Configure your preferred model provider (example: AWS for Bedrock)
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"

# 3. Navigate to your agent's sessions directory
cd /path/to/your-agent-project/src

# 4. Launch viewer with model provider
strands-viewer --model-provider anthropic --model-id claude-sonnet-4-5-20250929

# 5. Select a session and use the AI Analysis panel in the web interface
```

### No AI? No Problem

The AI features are completely optional. Without the `ai` extra installed, the viewer works perfectly for browsing and exporting sessions - you just won't see the AI Analysis panel.

## Interface Overview

The viewer features a modern three-panel layout optimized for session analysis:

![Interface Overview](docs/images/interface-overview.png)

### Left Panel - Session List
- Click any session to view its messages
- Shows session ID, message count, and last update time
- Sessions sorted by most recent first
- **Collapsible** - Toggle with hamburger menu to maximize space
- Responsive - Hidden on mobile, overlay mode on tablets

### Middle Panel - Message View
- **User messages** (blue) - Your prompts to the agent
- **Assistant messages** (purple) - Agent responses
- **Tool calls** (yellow) - Collapsible tool invocations with inputs
- **Tool results** (green/red) - Collapsible outputs (success or error)
- **Search & Filters** - Find text, filter by role, show only errors/tools
- **Export** - Download as Markdown, JSON, or plain text

### Right Panel - AI Analysis (Optional)
- **Quick Actions** - Summarize, analyze errors, suggest improvements
- **Interactive Chat** - Ask questions about the session
- **Markdown Rendering** - AI responses with proper formatting
- **Conversation History** - Full context for multi-turn discussions
- Shows which session is being analyzed
- Only visible on larger screens (≥1280px width)

### Responsive Design
- **Desktop** (≥1280px): All three panels visible
- **Tablet** (768-1279px): Sidebar collapsible, no AI panel
- **Mobile** (<768px): Single column, sidebar as overlay

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
│       ├── __init__.py         # Package initialization
│       ├── __version__.py      # Version info
│       ├── cli.py              # Command-line interface
│       ├── server.py           # FastAPI server
│       ├── session_reader.py   # Session file parser
│       ├── export_formatter.py # Export formatters (Markdown, JSON, text)
│       ├── ai_analysis.py      # Session analysis with intelligent tools
│       ├── models/             # Model provider configurations
│       │   ├── __init__.py
│       │   └── models.py       # Factory functions for Anthropic, OpenAI, Ollama
│       └── static/
│           └── index.html      # Web interface
├── tests/                      # Test suite
├── pyproject.toml             # Package configuration
├── CHANGELOG.md               # Version history
├── CLAUDE.md                  # Development notes
├── LICENSE                    # MIT License
└── README.md                 # This file
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn

Dependencies are automatically installed with the package.

## API Endpoints

The viewer exposes a REST API:

### Core Endpoints
- `GET /api/sessions` - List all sessions
- `GET /api/sessions/{session_id}` - Get session details
- `GET /api/sessions/{session_id}/messages` - Get session messages (with pagination)
- `GET /api/sessions/{session_id}/export?format=markdown` - Export session (formats: markdown, json, text)

### Analysis Endpoints (Optional)
- `GET /api/ai/status` - Check if analysis features are available
- `POST /api/sessions/{session_id}/analyze` - Run analysis (types: summarize, errors, improvements)
- `POST /api/sessions/{session_id}/chat` - Interactive Q&A about session

## Development

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/labeveryday/strands-session-viewer.git
cd strands-session-viewer

# Install in development mode
pip install -e .

# Or with dev dependencies (recommended)
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=strands_viewer --cov-report=html
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

- **GitHub**: https://github.com/labeveryday/strands-session-viewer
- **Strands SDK**: https://github.com/strands-agents/sdk-python
- **Issues**: https://github.com/labeveryday/strands-session-viewer/issues

---

Made with ❤️ for the Strands community
