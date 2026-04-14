# Resource API Documentation Template

**Document Version**: 1.0.0
**Created**: 2026-04-13T19:30:00Z
**Last Updated**: 2026-04-13T19:30:00Z
**Owner**: AI Assistant
**Status**: Template
**Version**: 1.0.0

---

## 📋 Overview

This template is for documenting Plane SDK resources. Copy this file and customize for each resource.

---

## Resource Information

**Resource Name**: [Resource Name]
**API Endpoint**: `/workspaces/{workspace_slug}/{resource}`
**Level**: [Workspace | Project | Work Item]
**SDK Version**: plane-python-sdk
**API Instance**: [URL]
**Edition**: [Community | Enterprise]
**Last Tested**: [YYYY-MM-DDTHH:MM:SSZ]

---

## ✅ Working Endpoints

[Document each working endpoint below]

### 1. [list/retrieve/create/update/delete]

**Endpoint**: `{resource}.method()`
**Level**: [Workspace | Project]
**Parameters**: `workspace_slug`, [other_params]

```python
# Example code here
result = client.{resource}.{method}(
    workspace_slug="your-workspace-slug",
    # other parameters
)
```

**Returns**: [Response type]

**Response Structure**:

```python
{
    # response structure
}
```

---

## 📊 Data Structure

### [Resource] Model Fields

| Field   | Type | Description | Example |
| ------- | ---- | ----------- | ------- |
| `field` | Type | Description | Example |

---

## 🔧 MCP Tool Implementation Example

```python
from fastmcp import FastMCP

mcp = FastMCP("[Resource] Tools")

@mcp.tool(description="[Tool description]")
async def [tool_name]([params]) -> dict:
    """[Tool documentation]."""
    # Implementation here
    pass
```

---

## 🧪 Test Results

| Test   | Status     | Notes   |
| ------ | ---------- | ------- |
| [test] | ✅ SUCCESS | [Notes] |

**Test Script**: [path]
**Test Output**: [Results]

---

## 📝 Important Notes

[Key observations, limitations, or special considerations]

---

## 🔗 Related Documentation

[Links to other documentation]

---

## 📚 References

- **SDK Source**: `plane.api.{resource}`
- **SDK Models**: `plane.models.{resource}`
- **Test Script**: `/tmp/test_{resource}.py`

---

**Last Updated**: 2026-04-13T19:30:00Z
**Document Version**: 1.0.0
