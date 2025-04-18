import os
import httpx
import logging
import json
import importlib.resources
from dotenv import load_dotenv
from base64 import b64encode
from httpx import AsyncClient
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, RouteType, FastMCPOpenAPI

# Load environment variables from .env file if running locally
load_dotenv()

# Initialize handlers and MCP server
logger = logging.getLogger(__name__)
logger.setLevel(os.getenv("LOG_LEVEL", "INFO").upper())

# Topdesk API settings
TOPDESK_BASE_URL = os.getenv("TOPDESK_BASE_URL", "")
TOPDESK_AUTH_HEADER = {
    "Authorization": f"Basic {b64encode(f'{os.getenv('TOPDESK_USERNAME')}:{os.getenv('TOPDESK_PASSWORD')}'.encode()).decode()}"
}

http_client: AsyncClient = None
mcp_server: FastMCPOpenAPI = None

def init():
    global mcp_server
    global http_client

    http_client = httpx.AsyncClient(
        base_url=TOPDESK_BASE_URL,
        headers=TOPDESK_AUTH_HEADER,
    )
    
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "incident_api_openapi_3.0.1.json")
        with open(file_path, 'r') as file:
            openapi_spec = json.load(file)
            logger.info(f"Successfully loaded OpenAPI specification from {file_path}")
    except FileNotFoundError:
        logger.error("OpenAPI specification file not found in package resources")
        raise
    except json.JSONDecodeError:
        logger.error("Invalid JSON in OpenAPI specification file")
        raise

    # Define custom route mappings
    custom_mappings = [
        # Map all endpoints to Tool
        RouteMap(
            methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
            pattern=r".*",
            route_type=RouteType.TOOL
        )
    ]

    mcp_server = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        route_maps=custom_mappings,
        client=http_client,
        port=os.getenv("PORT", 8000),
        host=os.getenv("HOST", "0.0.0.0"),
        debug=True if os.getenv("LOG_LEVEL", "INFO").lower() == "debug" else False
    )

# Run the MCP server
if __name__ == "__main__":
    logger.info("Starting up...")
    init()
    logger.info("Topdesk MCP server initialized.")
    mcp_server.run(transport="sse")