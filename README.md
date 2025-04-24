# topdesk-mcp-repro-bug
Bug repro for fastmcp

## Instructions

1. `docker-compose up -d`
2. Point an agent set up for tool calling, e.g. `qwen2.5-14b-instruct-1m` to the MCP server on port 8000
3. A prompt like this will work:

```
"List all Topdesk incidents with a status of firstLine."
```
