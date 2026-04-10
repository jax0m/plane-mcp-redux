# FastMCP 3.x Patterns Used in Plane MCP Redux

This document explains the modern FastMCP patterns we used, based on the official documentation.

## 1. Tool Definition with Decorators

**Old way (MCP SDK):**

```python
from mcp import Server
server = Server()

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [Tool(name="add", description="...", inputSchema={...})]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[Content]:
    if name == "add":
        return [TextContent(text=str(arguments["a"] + arguments["b"]))]
```

**FastMCP way (what we used):**

```python
from fastmcp import FastMCP

mcp = FastMCP("MyServer")

@mcp.tool
async def add(a: int, b: int) -> int:
    """Adds two integers."""
    return a + b
```

**Benefits:**

- Declarative and Pythonic
- Automatic schema generation from type hints
- Automatic validation
- Docstrings become tool descriptions

## 2. Dependency Injection for Lazy Loading

**Pattern:**

```python
from fastmcp.dependencies import Depends

def get_database() -> Database:
    """Create DB connection only when needed."""
    return Database.connect()

@mcp.tool
async def query_data(
    query: str,
    db: Database = Depends(get_database),  # Lazy!
) -> list[dict]:
    return db.execute(query)
```

**How it works:**

- `Depends(factory)` wraps a function
- Factory is called **once per request**
- Result is injected into the tool
- Caches the result for the duration of the request

**Why we used it:**

```python
def get_plane_client() -> PlaneClientWrapper:
    """Lazy client creation."""
    return PlaneClientWrapper(
        base_url=PlaneConfig().PLANE_BASE_URL,
        api_key=PlaneConfig().PLANE_API_KEY,
    )

@mcp.tool
async def list_issues(
    workspace_id: str,
    project_id: str,
    client: PlaneClientWrapper = Depends(get_plane_client),  # Lazy!
) -> dict:
    # Client created on first tool call
```

## 3. Context Injection

**Pattern:**

```python
from fastmcp.server.context import Context

@mcp.tool
async def process_data(
    data: str,
    ctx: Context,  # Auto-injected!
) -> str:
    # Log progress
    await ctx.info(f"Processing: {data}")
    await ctx.warning("Some warning")
    await ctx.error("An error")

    # Report progress
    await ctx.set_progress(50, 100)

    return "Done"
```

**Available context methods:**

- `ctx.info(msg)` - Log info message
- `ctx.warning(msg)` - Log warning
- `ctx.error(msg)` - Log error
- `ctx.set_progress(current, total)` - Report progress
- `ctx.get_request_id()` - Get request ID
- `ctx.get_session_id()` - Get session ID

## 4. Tool Annotations

**Pattern:**

```python
@mcp.tool(
    annotations={
        "title": "Add Numbers",
        "readOnlyHint": False,  # Modifies state
        "destructiveHint": False,  # Not destructive
        "idempotentHint": True,  # Safe to call multiple times
        "openWorldHint": False,  # Closed domain
    }
)
async def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b
```

**Common annotations:**

- `readOnlyHint`: Does the tool read or modify state?
- `destructiveHint`: Does it perform destructive operations?
- `idempotentHint`: Safe to call multiple times?
- `openWorldHint`: Interacts with external entities?

## 5. Tags for Tool Organization

**Pattern:**

```python
@mcp.tool(tags={"public", "utility"})
async def public_tool() -> str:
    return "Public"

@mcp.tool(tags={"internal", "admin"})
async def admin_tool() -> str:
    return "Admin only"

# Filter tools
mcp.enable(tags={"public"}, only=True)  # Only show public tools
mcp.disable(tags={"deprecated"})  # Hide deprecated tools
```

## 6. Optional Parameters with Defaults

**Pattern:**

```python
@mcp.tool
async def search(
    query: str,              # Required
    limit: int = 10,         # Optional with default
    offset: int = 0,         # Optional
    filters: dict | None = None,  # Optional, can be None
) -> list[dict]:
    """Search with optional filters."""
    ...
```

**Rules:**

- Parameters without defaults = required
- Parameters with defaults = optional
- `| None` means truly optional (can be omitted)

## 7. Async Tools

**FastMCP supports both sync and async:**

```python
# Async (preferred for I/O)
@mcp.tool
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

# Sync (runs in threadpool)
@mcp.tool
def sync_heavy_computation(x: int) -> int:
    time.sleep(1)  # Won't block event loop
    return x * 2
```

## 8. Output Schemas

**Pattern:**

```python
from pydantic import BaseModel

class Result(BaseModel):
    status: str
    data: dict

@mcp.tool(output_schema=Result.model_json_schema())
async def process_data(data: dict) -> Result:
    return Result(status="success", data=data)
```

**Why use it:**

- Enforces structured output
- Better LLM understanding
- Easier to parse results

## 9. Timeouts

**Pattern:**

```python
@mcp.tool(timeout=30.0)  # 30 second timeout
async def slow_operation() -> str:
    await asyncio.sleep(60)  # Will timeout!
    return "Done"
```

## 10. Versioning

**Pattern:**

```python
@mcp.tool(version="1.0")
async def tool_v1() -> str:
    return "V1"

@mcp.tool(version="2.0")
async def tool_v2() -> str:
    return "V2"

# Server handles version negotiation
```

## 11. Server Configuration

**Pattern:**

```python
mcp = FastMCP(
    name="MyServer",
    instructions="This server helps you with X, Y, Z.",

    # Behavior
    strict_input_validation=False,  # Flexible validation
    dereference_schemas=True,       # Flatten JSON schemas

    # Limits
    list_page_size=50,              # Max items per list

    # Handlers
    sampling_handler=my_sampling_handler,
)
```

## 12. Middleware

**Pattern:**

```python
from fastmcp.server.middleware.logging import LoggingMiddleware

mcp = FastMCP("MyServer")
mcp.add_middleware(LoggingMiddleware())
```

**Built-in middleware:**

- `LoggingMiddleware` - Request/response logging
- `TimingMiddleware` - Performance timing
- `ResponseCachingMiddleware` - Cache responses
- `RateLimitingMiddleware` - Rate limiting
- `ErrorHandlingMiddleware` - Error handling

## 13. Tool Search (for Large Catalogs)

**Pattern:**

```python
from fastmcp.server.transforms.search import BM25SearchTransform

mcp = FastMCP("MyServer", transforms=[BM25SearchTransform()])

# Instead of listing 1000 tools, LLM searches:
# 1. Calls search_tools("database operations")
# 2. Gets matching tools
# 3. Calls the tools directly
```

**Benefits:**

- Reduces context size dramatically
- Better for large tool catalogs
- On-demand discovery

## 14. Combining Patterns

**Full example:**

```python
from fastmcp import FastMCP
from fastmcp.server.context import Context
from fastmcp.dependencies import Depends
from pydantic import BaseModel

# 1. Define dependency
def get_database() -> Database:
    return Database.connect()

# 2. Create server with config
mcp = FastMCP(
    "DataServer",
    instructions="Server for data operations.",
    transforms=[BM25SearchTransform()],  # 13. Tool search
)

# 3. Add middleware
mcp.add_middleware(LoggingMiddleware())

# 4. Define tool with all patterns
@mcp.tool(
    description="Search the database",
    annotations={"readOnlyHint": True},  # 4. Annotations
    tags={"database", "search"},          # 5. Tags
    timeout=30.0,                         # 9. Timeout
)
async def search_database(
    query: str,
    limit: int = 10,
    db: Database = Depends(get_database),  # 2. Dependency injection
    ctx: Context = None,                    # 3. Context
) -> list[dict]:                          # 0. Tool definition
    """Search the database with optional filters."""  # 6. Docstring
    await ctx.info(f"Searching: {query}")  # 3. Context usage
    return db.search(query, limit)
```

## Key Takeaways

1. **Use decorators** - `@mcp.tool` instead of manual registration
2. **Type hints everywhere** - Automatic validation + documentation
3. **Dependency injection** - Lazy loading + testability
4. **Context for logging** - Built-in MCP logging
5. **Async for I/O** - Non-blocking operations
6. **Annotations for clarity** - Tell LLMs about tool behavior
7. **Middleware for cross-cutting** - Logging, caching, rate limiting
8. **Tool search for large catalogs** - On-demand discovery

## References

- [FastMCP Tools](https://gofastmcp.com/servers/tools)
- [Dependency Injection](https://gofastmcp.com/servers/dependency-injection)
- [Context](https://gofastmcp.com/servers/context)
- [Tool Search](https://gofastmcp.com/servers/transforms/tool-search)
- [Middleware](https://gofastmcp.com/servers/middleware)
