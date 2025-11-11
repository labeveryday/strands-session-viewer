"""
FastAPI server for Strands session viewer.
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import HTMLResponse, FileResponse, PlainTextResponse
from pathlib import Path
from typing import Optional, Dict, List
import uvicorn

from strands_viewer.session_reader import SessionReader
from strands_viewer.export_formatter import format_session, get_filename

try:
    from strands_viewer.ai_analysis import SessionAnalyzer, STRANDS_AVAILABLE

    AI_AVAILABLE = STRANDS_AVAILABLE
except ImportError:
    AI_AVAILABLE = False
    SessionAnalyzer = None


class SessionViewerApp:
    """Web application for viewing Strands sessions."""

    def __init__(self, storage_dir: str, port: int = 8000, model=None):
        self.storage_dir = storage_dir
        self.port = port
        self.reader = SessionReader(storage_dir)
        self.analyzer = SessionAnalyzer(model=model) if AI_AVAILABLE and SessionAnalyzer else None
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

        # AI Analysis Routes
        @app.get("/api/ai/status")
        async def ai_status():
            """Check if AI analysis is available."""
            return {
                "available": AI_AVAILABLE and self.analyzer is not None,
                "features": (
                    {
                        "summarize": AI_AVAILABLE,
                        "analyze_errors": AI_AVAILABLE,
                        "chat": AI_AVAILABLE,
                        "suggest_improvements": AI_AVAILABLE,
                    }
                    if AI_AVAILABLE
                    else {}
                ),
            }

        @app.post("/api/sessions/{session_id}/analyze")
        async def analyze_session(session_id: str, analysis_type: str = Body(..., embed=True)):
            """
            Analyze a session using AI.

            Args:
                session_id: Session ID to analyze
                analysis_type: Type of analysis (summarize, errors, improvements)

            Returns:
                Analysis results
            """
            if not AI_AVAILABLE or not self.analyzer:
                raise HTTPException(
                    status_code=503,
                    detail="AI analysis not available. Install with: pip install strands-session-viewer[ai]",
                )

            try:
                # Get session data
                session = self.reader.get_session(session_id)
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")

                # Perform analysis based on type
                if analysis_type == "summarize":
                    result = self.analyzer.summarize_session(session)
                elif analysis_type == "errors":
                    result = self.analyzer.analyze_errors(session)
                    if result is None:
                        result = "No errors found in this session."
                elif analysis_type == "improvements":
                    result = self.analyzer.suggest_improvements(session)
                else:
                    raise HTTPException(
                        status_code=400, detail=f"Unknown analysis type: {analysis_type}"
                    )

                return {"success": True, "analysis": result}

            except HTTPException:
                raise
            except Exception as e:
                import traceback

                print(f"❌ Error during analysis: {e}")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(e))

        @app.post("/api/sessions/{session_id}/chat")
        async def chat_about_session(
            session_id: str,
            question: str = Body(..., embed=True),
            chat_history: Optional[List[Dict[str, str]]] = Body(None, embed=True),
        ):
            """
            Ask questions about a session using AI.

            Args:
                session_id: Session ID to analyze
                question: User's question
                chat_history: Optional previous conversation history

            Returns:
                AI response
            """
            if not AI_AVAILABLE or not self.analyzer:
                raise HTTPException(
                    status_code=503,
                    detail="AI analysis not available. Install with: pip install strands-session-viewer[ai]",
                )

            try:
                # Get session data
                session = self.reader.get_session(session_id)
                if not session:
                    raise HTTPException(status_code=404, detail="Session not found")

                # Get AI response
                answer = self.analyzer.answer_question(session, question, chat_history)

                return {"success": True, "answer": answer}

            except HTTPException:
                raise
            except Exception as e:
                import traceback

                print(f"❌ Error during chat: {e}")
                traceback.print_exc()
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


def main(storage_dir: str = "./sessions", port: int = 8000, open_browser: bool = True, model=None):
    """Main entry point."""
    viewer = SessionViewerApp(storage_dir, port, model=model)
    viewer.run(open_browser=open_browser)


if __name__ == "__main__":
    import sys

    # Simple argument parsing
    storage_dir = sys.argv[1] if len(sys.argv) > 1 else "./sessions"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    main(storage_dir, port)
