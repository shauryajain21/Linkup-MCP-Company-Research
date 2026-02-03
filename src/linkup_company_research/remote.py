"""Remote MCP Server with SSE Transport.

This module provides an HTTP server that exposes the MCP tools via Server-Sent Events (SSE).
Users pass their Linkup API key in the URL: /sse?apiKey=lk-xxxxx

Deploy to Railway, Render, or any platform that supports Python web servers.
"""

import os
import logging
from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.responses import JSONResponse, HTMLResponse
from starlette.routing import Route
from mcp.server.sse import SseServerTransport

# Import the MCP server instance and all tools
from .server import mcp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_api_key(request) -> str | None:
    """Extract Linkup API key from URL query parameters."""
    return request.query_params.get("apiKey") or request.query_params.get("api_key")


async def handle_sse(request):
    """Handle SSE connections for MCP protocol.

    URL format: /sse?apiKey=lk-xxxxx
    """
    api_key = extract_api_key(request)

    if not api_key:
        return JSONResponse(
            {"error": "Missing apiKey parameter. Use /sse?apiKey=lk-xxxxx"},
            status_code=401
        )

    if not api_key.startswith("lk-") and not api_key.startswith("lk_"):
        return JSONResponse(
            {"error": "Invalid API key format. Linkup API keys start with 'lk-'"},
            status_code=401
        )

    # Set the API key for this request
    # This is thread-safe in async context since each request runs in its own coroutine
    os.environ["LINKUP_API_KEY"] = api_key

    logger.info(f"New SSE connection from {request.client.host}")

    # Create SSE transport and handle the connection
    sse_transport = SseServerTransport("/messages")

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
    api_key = extract_api_key(request)

    if not api_key:
        return JSONResponse(
            {"error": "Missing apiKey parameter"},
            status_code=401
        )

    os.environ["LINKUP_API_KEY"] = api_key

    sse_transport = SseServerTransport("/messages")
    return await sse_transport.handle_post_message(request.scope, request.receive, request._send)


async def handle_health(request):
    """Health check endpoint for Railway/load balancers."""
    return JSONResponse({"status": "healthy", "service": "linkup-company-research-mcp"})


async def handle_home(request):
    """Home page with usage instructions."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Linkup Company Research MCP</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            code { background: #f4f4f4; padding: 2px 6px; border-radius: 4px; }
            pre { background: #f4f4f4; padding: 15px; border-radius: 8px; overflow-x: auto; }
            .tools { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin: 20px 0; }
            .tool { background: #e8f4fd; padding: 10px; border-radius: 6px; }
            a { color: #0066cc; }
        </style>
    </head>
    <body>
        <h1>Linkup Company Research MCP</h1>
        <p>A comprehensive company research platform powered by <a href="https://linkup.so">Linkup's</a> agentic search API.</p>

        <h2>Quick Start</h2>
        <p>Add this MCP server to Claude Desktop or any MCP client:</p>
        <pre>https://YOUR_DEPLOYMENT_URL/sse?apiKey=YOUR_LINKUP_API_KEY</pre>

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
            <li><code>GET /sse?apiKey=xxx</code> - SSE endpoint for MCP clients</li>
            <li><code>POST /messages?apiKey=xxx</code> - Message endpoint for SSE transport</li>
            <li><code>GET /health</code> - Health check</li>
        </ul>

        <p><a href="https://github.com/LinkupPlatform/linkup-company-research-mcp">GitHub Repository</a></p>
    </body>
    </html>
    """
    return HTMLResponse(html)


# Create Starlette app with routes
app = Starlette(
    routes=[
        Route("/", handle_home),
        Route("/health", handle_health),
        Route("/sse", handle_sse),
        Route("/messages", handle_messages, methods=["POST"]),
    ]
)


def main():
    """Run the remote MCP server."""
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")

    logger.info(f"Starting Linkup Company Research MCP server on {host}:{port}")
    logger.info(f"SSE endpoint: http://{host}:{port}/sse?apiKey=YOUR_API_KEY")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
