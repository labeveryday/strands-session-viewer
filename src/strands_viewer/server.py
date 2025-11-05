"""
FastAPI server for Strands session viewer.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from pathlib import Path
from typing import Optional
import uvicorn

from strands_viewer.session_reader import SessionReader
from strands_viewer.export_formatter import format_session, get_filename


class SessionViewerApp:
    """Web application for viewing Strands sessions."""

    def __init__(self, storage_dir: str, port: int = 8000):
        self.storage_dir = storage_dir
        self.port = port
        self.reader = SessionReader(storage_dir)
        self.app = self._create_app()

    def _create_app(self) -> FastAPI:
        """Create FastAPI application."""
        app = FastAPI(
            title="Strands Session Viewer",
            description="View and explore Strands agent sessions",
            version="0.1.0",
        )

        # API Routes
        @app.get("/api/sessions")
        async def list_sessions():
            """List all available sessions."""
            try:
                sessions = self.reader.list_sessions()
                return {"success": True, "sessions": sessions}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/sessions/{session_id}")
        async def get_session(session_id: str):
            """Get detailed session information."""
            try:
                session = self.reader.get_session(session_id)
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")
                return {"success": True, "session": session}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/sessions/{session_id}/messages")
        async def get_messages(session_id: str, limit: Optional[int] = None, offset: int = 0):
            """Get messages for a session with pagination."""
            try:
                messages = self.reader.get_messages(session_id, limit, offset)
                return {"success": True, "messages": messages}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        @app.get("/api/sessions/{session_id}/export")
        async def export_session(session_id: str, format: str = "markdown"):
            """
            Export a session in the specified format.

            Args:
                session_id: Session ID to export
                format: Export format (markdown, json, text)

            Returns:
                Formatted session content
            """
            try:
                # Get session data
                session = self.reader.get_session(session_id)
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")

                # Format the session
                try:
                    content = format_session(session, format)
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))

                # Determine content type
                content_types = {
                    "markdown": "text/markdown",
                    "json": "application/json",
                    "text": "text/plain",
                }
                content_type = content_types.get(format, "text/plain")

                # Generate filename
                filename = get_filename(session_id, format)

                # Return with appropriate headers for download
                return PlainTextResponse(
                    content,
                    media_type=content_type,
                    headers={"Content-Disposition": f'attachment; filename="{filename}"'},
                )

            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))

        # Serve the HTML interface
        @app.get("/", response_class=HTMLResponse)
        async def index():
            """Serve the main HTML interface."""
            html_path = Path(__file__).parent / "static" / "index.html"
            if html_path.exists():
                return FileResponse(html_path)
            raise HTTPException(status_code=404, detail="Interface not found")

        return app

    def run(self, open_browser: bool = False):
        """Run the server."""
        import webbrowser

        if open_browser:
            webbrowser.open(f"http://localhost:{self.port}")

        print("\n🚀 Strands Session Viewer starting...")
        print(f"📁 Storage directory: {self.storage_dir}")
        print(f"🌐 Open your browser to: http://localhost:{self.port}\n")

        # Binding to all interfaces is intentional for LAN accessibility
        uvicorn.run(self.app, host="0.0.0.0", port=self.port, log_level="info")  # nosec B104


def main(storage_dir: str = "./sessions", port: int = 8000, open_browser: bool = True):
    """Main entry point."""
    viewer = SessionViewerApp(storage_dir, port)
    viewer.run(open_browser=open_browser)


if __name__ == "__main__":
    import sys

    # Simple argument parsing
    storage_dir = sys.argv[1] if len(sys.argv) > 1 else "./sessions"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    main(storage_dir, port)
