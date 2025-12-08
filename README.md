# Claude Agent SDK Test

Sample project demonstrating the Claude Agent SDK for building AI-powered agents.

## Overview

This repository contains examples showing how to use the Claude Agent SDK to:

- Run simple one-off queries with `query()`
- Maintain multi-turn conversations with `ClaudeSDKClient`
- Create custom tools using the `@tool` decorator
- Integrate custom tools via MCP (Model Context Protocol) servers
- Delegate tasks to specialized subagents
- Get structured JSON output with schema validation
- Handle errors gracefully with retry logic

## Prerequisites

- Python 3.10+
- An Anthropic API key ([get one here](https://console.anthropic.com/settings/keys))

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tomleelong/claude-agent-sdk-test.git
   cd claude-agent-sdk-test
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -e .
   ```

4. Configure your API key:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your Anthropic API key.

## Examples

### Simple Agent (`src/simple_agent.py`)

Demonstrates the basic `query()` function for one-off tasks:

```bash
python src/simple_agent.py
```

### Multi-turn Conversation (`src/conversation_agent.py`)

Shows how to maintain context across multiple exchanges using `ClaudeSDKClient`:

```bash
python src/conversation_agent.py
```

### Custom Tools (`src/custom_tools_agent.py`)

Demonstrates creating custom tools with the `@tool` decorator and integrating them via MCP:

```bash
python src/custom_tools_agent.py
```

### Subagents (`src/subagents_example.py`)

Shows how to delegate tasks to specialized subagents (code reviewer, test writer, doc writer):

```bash
python src/subagents_example.py
```

### Structured Output (`src/structured_output_example.py`)

Demonstrates getting validated JSON responses using JSON Schema:

```bash
python src/structured_output_example.py
```

### Error Handling (`src/error_handling_example.py`)

Shows patterns for error handling, retry logic, timeouts, and graceful degradation:

```bash
python src/error_handling_example.py
```

## Project Structure

```
.
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
├── .env.example            # Example environment variables
├── .env                    # Your local config (not tracked in git)
├── src/
│   ├── __init__.py
│   ├── simple_agent.py           # Basic query example
│   ├── conversation_agent.py     # Multi-turn conversation example
│   ├── custom_tools_agent.py     # Custom tools example
│   ├── subagents_example.py      # Subagents delegation example
│   ├── structured_output_example.py  # JSON Schema output example
│   └── error_handling_example.py # Error handling patterns
└── .gitignore
```

## Key Concepts

### ClaudeAgentOptions

Configure your agent with:

- `system_prompt`: Custom instructions for the agent
- `allowed_tools`: List of tools the agent can use
- `permission_mode`: Control permission behavior
- `cwd`: Working directory for file operations
- `mcp_servers`: Custom MCP servers for custom tools

### Available Tools

Built-in tools include:
- `Read`, `Write`, `Edit`: File operations
- `Bash`: Execute shell commands
- `Grep`, `Glob`: Search and find files
- `WebFetch`, `WebSearch`: Web access

### Custom Tools

Create custom tools using the `@tool` decorator:

```python
from claude_agent_sdk import tool

@tool("tool_name", "Description", {"param": str})
async def my_tool(args: dict) -> dict:
    return {"content": [{"type": "text", "text": "result"}]}
```

### Subagents

Define specialized agents for different tasks:

```python
options = ClaudeAgentOptions(
    agents={
        "code-reviewer": {
            "description": "Expert code reviewer",
            "prompt": "You are a code review specialist...",
            "tools": ["Read", "Grep"],
            "model": "sonnet",
        },
    }
)
```

### Structured Output

Get validated JSON responses using JSON Schema:

```python
options = ClaudeAgentOptions(
    output_format={
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string"},
                "score": {"type": "integer", "minimum": 0, "maximum": 100},
            },
            "required": ["summary", "score"],
        },
    }
)
```

## Resources

- [Claude Agent SDK Documentation](https://docs.anthropic.com/en/docs/claude-code/sdk)
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [Anthropic API Console](https://console.anthropic.com/)

## License

MIT
