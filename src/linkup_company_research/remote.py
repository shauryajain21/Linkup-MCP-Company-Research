"""Remote MCP Server with SSE Transport.

This module provides an HTTP server that exposes the MCP tools via Server-Sent Events (SSE).
Users can pass their Linkup API key in the URL: /sse?apiKey=lk-xxxxx
If no key is provided, a fallback key is used with rate limiting.

Deploy to Railway, Render, or any platform that supports Python web servers.
"""

import asyncio
import os
import time
import logging
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager

from pathlib import Path

from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse, FileResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from mcp.server.sse import SseServerTransport

# Path to docs folder for static files
DOCS_DIR = Path(__file__).parent.parent.parent / "docs"

# Import the MCP server instance and helpers
from .server import mcp, set_api_key, close_http_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# SESSION MANAGEMENT
# =============================================================================

# Store API keys by session ID (session_id -> api_key)
session_api_keys: dict[str, str] = {}

# Store transports by session ID (session_id -> SseServerTransport)
session_transports: dict[str, SseServerTransport] = {}

# Session timestamps for cleanup
session_timestamps: dict[str, float] = {}

# Session cleanup lock
session_lock = asyncio.Lock()

# Session expiry time (1 hour)
SESSION_EXPIRY_SECONDS = 3600


async def cleanup_expired_sessions():
    """Remove expired sessions."""
    async with session_lock:
        now = time.time()
        expired = [
            sid for sid, ts in session_timestamps.items()
            if now - ts > SESSION_EXPIRY_SECONDS
        ]
        for sid in expired:
            session_api_keys.pop(sid, None)
            session_transports.pop(sid, None)
            session_timestamps.pop(sid, None)
        if expired:
            logger.info(f"Cleaned up {len(expired)} expired sessions")


# =============================================================================
# CONFIGURATION
# =============================================================================

# Fallback API key (set via environment variable on Railway)
FALLBACK_API_KEY = os.environ.get("LINKUP_API_KEY", "")

# Rate limiting for free tier (users without their own API key)
RATE_LIMIT_QPS = 2  # Queries per second
RATE_LIMIT_DAILY = 50  # Requests per day per IP

# In-memory rate limiting (use Redis for production scale)
rate_limit_qps: dict[str, list[float]] = defaultdict(list)
rate_limit_daily: dict[str, int] = defaultdict(int)
rate_limit_daily_reset: float = time.time()

# Lock for thread-safe rate limit updates
rate_limit_lock = asyncio.Lock()


# =============================================================================
# HELPERS
# =============================================================================


def get_client_ip(request) -> str:
    """Extract client IP from request headers (handles proxies)."""
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()

    real_ip = request.headers.get("x-real-ip")
    if real_ip:
        return real_ip

    cf_ip = request.headers.get("cf-connecting-ip")
    if cf_ip:
        return cf_ip

    return request.client.host if request.client else "unknown"


def extract_api_key(request) -> str | None:
    """Extract Linkup API key from URL query parameters."""
    return request.query_params.get("apiKey") or request.query_params.get("api_key")


async def check_rate_limit(client_ip: str) -> tuple[bool, str]:
    """Check if client is within rate limits. Returns (allowed, error_message)."""
    global rate_limit_daily_reset

    async with rate_limit_lock:
        now = time.time()

        # Reset daily counters every 24 hours
        if now - rate_limit_daily_reset > 86400:
            rate_limit_daily.clear()
            rate_limit_daily_reset = now

        # Check QPS limit (sliding window)
        recent_requests = [t for t in rate_limit_qps[client_ip] if now - t < 1.0]
        rate_limit_qps[client_ip] = recent_requests

        if len(recent_requests) >= RATE_LIMIT_QPS:
            return False, f"Rate limit exceeded: {RATE_LIMIT_QPS} requests per second. Add your own API key to remove limits."

        # Check daily limit
        if rate_limit_daily[client_ip] >= RATE_LIMIT_DAILY:
            return False, f"Daily limit exceeded: {RATE_LIMIT_DAILY} requests per day. Add your own API key to remove limits."

        # Record this request
        rate_limit_qps[client_ip].append(now)
        rate_limit_daily[client_ip] += 1

        return True, ""


def get_api_key_for_request(request) -> tuple[str, bool]:
    """Get API key to use. Returns (api_key, is_user_provided)."""
    user_key = extract_api_key(request)

    # Accept any non-empty API key from user
    if user_key and len(user_key) > 10:
        return user_key, True

    return FALLBACK_API_KEY, False


# =============================================================================
# HANDLERS
# =============================================================================


async def handle_sse(request):
    """Handle SSE connections for MCP protocol.

    URL format: /sse or /sse?apiKey=lk-xxxxx

    Creates a unique session for each connection, storing the API key
    so it persists across all messages in the session.
    """
    api_key, is_user_provided = get_api_key_for_request(request)
    client_ip = get_client_ip(request)

    # Check if we have any API key to use
    if not api_key:
        return JSONResponse(
            {"error": "No API key available. Please provide your Linkup API key: /sse?apiKey=lk-xxxxx"},
            status_code=401
        )

    # Apply rate limiting only for free tier (fallback key users)
    if not is_user_provided:
        allowed, error_msg = await check_rate_limit(client_ip)
        if not allowed:
            return JSONResponse({"error": error_msg}, status_code=429)
        logger.info(f"Free tier connection from {client_ip}")
    else:
        logger.info(f"User API key connection from {client_ip}")

    # Cleanup expired sessions periodically
    await cleanup_expired_sessions()

    # Create a unique session ID for this connection
    session_id = str(uuid.uuid4())

    # Store the API key and create transport for this session
    async with session_lock:
        session_api_keys[session_id] = api_key
        session_timestamps[session_id] = time.time()
        # Create a transport that points to /messages/{session_id}
        transport = SseServerTransport(f"/messages/{session_id}")
        session_transports[session_id] = transport

    logger.info(f"Created session {session_id[:8]}... for client {client_ip}")

    try:
        # Use session-specific transport
        async with transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            # Set the API key for this session's context
            set_api_key(api_key)
            await mcp._mcp_server.run(
                streams[0],
                streams[1],
                mcp._mcp_server.create_initialization_options()
            )
    finally:
        # Cleanup session when connection closes
        async with session_lock:
            session_api_keys.pop(session_id, None)
            session_transports.pop(session_id, None)
            session_timestamps.pop(session_id, None)
        logger.info(f"Closed session {session_id[:8]}...")


async def handle_messages(request):
    """Handle POST messages for SSE transport.

    URL format: /messages/{session_id}
    Looks up the API key from the session store.
    """
    # Extract session ID from path
    session_id = request.path_params.get("session_id", "")

    if not session_id:
        return JSONResponse({"error": "Missing session ID"}, status_code=400)

    # Look up API key and transport for this session
    async with session_lock:
        api_key = session_api_keys.get(session_id)
        transport = session_transports.get(session_id)
        # Update session timestamp
        if session_id in session_timestamps:
            session_timestamps[session_id] = time.time()

    if not api_key or not transport:
        return JSONResponse({"error": "Session not found or expired"}, status_code=404)

    # Set the API key for this request
    set_api_key(api_key)

    # Use the session's transport to handle the message
    return await transport.handle_post_message(request.scope, request.receive, request._send)


async def handle_health(request):
    """Health check endpoint for Railway/load balancers."""
    return JSONResponse({
        "status": "healthy",
        "service": "linkup-company-research-mcp",
        "active_sessions": len(session_api_keys)
    })


async def handle_home(request):
    """Serve the custom homepage from docs/index.html."""
    index_path = DOCS_DIR / "index.html"
    if index_path.exists():
        return FileResponse(index_path, media_type="text/html")
    # Fallback if docs/index.html doesn't exist
    return HTMLResponse("<h1>Linkup Company Research MCP</h1><p>Visit /sse to connect.</p>")


async def handle_logo(request):
    """Serve the logo image."""
    logo_path = DOCS_DIR / "logo.png"
    if logo_path.exists():
        return FileResponse(logo_path, media_type="image/png")
    return JSONResponse({"error": "Logo not found"}, status_code=404)


@asynccontextmanager
async def lifespan(app):
    """Manage startup and shutdown events."""
    logger.info("Linkup Company Research MCP server starting...")
    logger.info(f"Fallback API key configured: {bool(FALLBACK_API_KEY)}")
    yield
    logger.info("Linkup Company Research MCP server shutting down...")
    await close_http_client()


# Create Starlette app with routes
routes = [
    Route("/", handle_home),
    Route("/logo.png", handle_logo),
    Route("/health", handle_health),
    Route("/sse", handle_sse),
    Route("/messages/{session_id}", handle_messages, methods=["POST"]),
]

# Mount static files from docs folder (for logo, etc.) if it exists
if DOCS_DIR.exists():
    routes.append(Mount("/static", app=StaticFiles(directory=DOCS_DIR), name="static"))

app = Starlette(routes=routes, lifespan=lifespan)


def main():
    """Run the remote MCP server."""
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    logger.info(f"Binding to {host}:{port}")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    main()
