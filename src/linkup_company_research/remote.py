"""Remote MCP Server with SSE Transport.

This module provides an HTTP server that exposes the MCP tools via Server-Sent Events (SSE).
Users can optionally pass their Linkup API key in the URL: /sse?apiKey=lk-xxxxx
If no key is provided, a fallback key is used with rate limiting.

Deploy to Railway, Render, or any platform that supports Python web servers.
"""

import asyncio
import os
import time
import logging
from collections import defaultdict

from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from mcp.server.sse import SseServerTransport

# Import the MCP server instance and helpers
from .server import mcp, set_api_key, close_http_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Shared SSE transport instance (must be shared between /sse and /messages)
sse_transport = SseServerTransport("/messages")

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
    # Check common proxy headers
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
    """Check if client is within rate limits (thread-safe). Returns (allowed, error_message)."""
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

    # Set the API key for this request (async-safe via contextvars)
    set_api_key(api_key)

    # Use shared SSE transport
    async with sse_transport.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0],
            streams[1],
            mcp._mcp_server.create_initialization_options()
        )


async def handle_messages(request):
    """Handle POST messages for SSE transport."""
    # Use the shared transport's message handler
    return await sse_transport.handle_post_message(request.scope, request.receive, request._send)


async def handle_health(request):
    """Health check endpoint for Railway/load balancers."""
    return JSONResponse({"status": "healthy", "service": "linkup-company-research-mcp"})


async def handle_home(request):
    """Home page with usage instructions."""
    has_fallback = bool(FALLBACK_API_KEY)
    free_tier_info = f"""
        <h2>Free Tier</h2>
        <p>Try it without an API key (rate limited to {RATE_LIMIT_DAILY} requests/day):</p>
        <pre>https://YOUR_DEPLOYMENT_URL/sse</pre>
        <p>For unlimited access, add your own API key:</p>
        <pre>https://YOUR_DEPLOYMENT_URL/sse?apiKey=YOUR_LINKUP_API_KEY</pre>
    """ if has_fallback else """
        <h2>Quick Start</h2>
        <p>Add this MCP server to Claude or any MCP client:</p>
        <pre>https://YOUR_DEPLOYMENT_URL/sse?apiKey=YOUR_LINKUP_API_KEY</pre>
    """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Linkup Company Research MCP</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }}
            h1 {{ color: #333; }}
            code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }}
            pre {{ background: #f4f4f4; padding: 15px; border-radius: 8px; overflow-x: auto; }}
            .tools {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 20px 0; }}
            .tool {{ background: #e8f4fd; padding: 10px; border-radius: 6px; }}
            a {{ color: #0066cc; }}
            .free-tier {{ background: #e8fde8; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Linkup Company Research MCP</h1>
        <p>A comprehensive company research platform powered by <a href="https://linkup.so">Linkup's</a> agentic search API.</p>

        {free_tier_info}

        <h2>Get Your API Key</h2>
        <p>Get a Linkup API key at <a href="https://linkup.so">linkup.so</a></p>

        <h2>Available Tools (17)</h2>
        <div class="tools">
            <div class="tool"><strong>company_overview</strong> - Identity, location, size</div>
            <div class="tool"><strong>company_products</strong> - Products, services, pricing</div>
            <div class="tool"><strong>company_business_model</strong> - Revenue streams, GTM</div>
            <div class="tool"><strong>company_target_market</strong> - ICP, segments, geos</div>
            <div class="tool"><strong>company_financials</strong> - Revenue, metrics</div>
            <div class="tool"><strong>company_funding</strong> - Funding, valuation, investors</div>
            <div class="tool"><strong>company_leadership</strong> - C-suite, board, hires</div>
            <div class="tool"><strong>company_culture</strong> - Glassdoor, employer brand</div>
            <div class="tool"><strong>company_clients</strong> - Customers, case studies</div>
            <div class="tool"><strong>company_partnerships</strong> - Partners, integrations</div>
            <div class="tool"><strong>company_technology</strong> - Tech stack, patents</div>
            <div class="tool"><strong>competitive_landscape</strong> - Competitors, positioning</div>
            <div class="tool"><strong>company_market</strong> - TAM/SAM/SOM, trends</div>
            <div class="tool"><strong>company_news</strong> - Recent activity, news</div>
            <div class="tool"><strong>company_strategy</strong> - Growth plans, M&A, IPO</div>
            <div class="tool"><strong>company_risks</strong> - Risk assessment</div>
            <div class="tool"><strong>company_esg</strong> - ESG, sustainability</div>
        </div>

        <h2>API Endpoints</h2>
        <ul>
            <li><code>GET /sse</code> - SSE endpoint (free tier with rate limits)</li>
            <li><code>GET /sse?apiKey=xxx</code> - SSE endpoint (unlimited with your key)</li>
            <li><code>GET /health</code> - Health check</li>
        </ul>

        <p><a href="https://github.com/LinkupPlatform/linkup-company-research-mcp">GitHub Repository</a></p>
    </body>
    </html>
    """
    return HTMLResponse(html)


# Lifespan for startup/shutdown logging
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app):
    """Manage startup and shutdown events."""
    logger.info("Linkup Company Research MCP server starting...")
    logger.info(f"Fallback API key configured: {bool(FALLBACK_API_KEY)}")
    yield
    # Cleanup shared HTTP client on shutdown
    logger.info("Linkup Company Research MCP server shutting down...")
    await close_http_client()


# Create Starlette app with routes
app = Starlette(
    routes=[
        Route("/", handle_home),
        Route("/health", handle_health),
        Route("/sse", handle_sse),
        Route("/messages", handle_messages, methods=["POST"]),
    ],
    lifespan=lifespan,
)


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
