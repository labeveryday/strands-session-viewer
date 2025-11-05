#!/usr/bin/env python3
"""
CLI entry point for Strands Session Viewer.
"""
import argparse
import sys
from pathlib import Path

from strands_viewer.__version__ import __version__


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Strands Session Viewer - View your agent sessions in the browser",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View sessions in current ./sessions directory
  strands-viewer

  # Specify a different sessions directory
  strands-viewer --dir /path/to/sessions

  # Use a different port
  strands-viewer --port 8080

  # Don't auto-open browser
  strands-viewer --no-open
        """,
    )

    parser.add_argument(
        "--version", action="version", version=f"strands-session-viewer {__version__}"
    )

    parser.add_argument(
        "directory",
        nargs="?",
        default="./sessions",
        help="Path to sessions directory (default: ./sessions)",
    )

    parser.add_argument(
        "--dir", dest="directory", help="Path to sessions directory (alternative to positional arg)"
    )

    parser.add_argument(
        "--port", type=int, default=8000, help="Port to run the server on (default: 8000)"
    )

    parser.add_argument(
        "--no-open", action="store_true", help="Don't automatically open the browser"
    )

    parser.add_argument(
        "--host",
        default="0.0.0.0",  # nosec B104 - Local dev tool, users may want LAN access
        help="Host to bind to (default: 0.0.0.0)",
    )

    args = parser.parse_args()

    # Validate sessions directory exists
    sessions_dir = Path(args.directory).resolve()
    if not sessions_dir.exists():
        print(f"❌ Error: Sessions directory does not exist: {args.directory}")
        print(f"   Resolved path: {sessions_dir}")
        print("   Please check the path and try again.")
        sys.exit(1)

    if not sessions_dir.is_dir():
        print(f"❌ Error: Path is not a directory: {args.directory}")
        sys.exit(1)

    # Import and run the server
    try:
        from strands_viewer.server import SessionViewerApp

        print(f"\n🚀 Strands Session Viewer v{__version__}")
        print(f"📁 Storage directory: {sessions_dir}")
        print(f"🌐 Starting server on http://localhost:{args.port}\n")

        viewer = SessionViewerApp(str(sessions_dir), args.port)
        viewer.run(open_browser=not args.no_open)

    except ImportError as e:
        print("❌ Error: Missing required dependencies.")
        print("   Please install: pip install strands-session-viewer")
        print(f"   Details: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down viewer...")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting viewer: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
