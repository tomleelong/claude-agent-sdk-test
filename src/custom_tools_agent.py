"""Example demonstrating custom tools with the Claude Agent SDK.

This example shows how to create custom tools using the @tool decorator
and integrate them with an agent via MCP servers.
"""

import asyncio
import os
from typing import Any

from decouple import config

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
    create_sdk_mcp_server,
    tool,
)


# Define custom tools using the @tool decorator
@tool("add", "Add two numbers together", {"a": float, "b": float})
async def add(args: dict[str, Any]) -> dict[str, Any]:
    """Add two numbers and return the result."""
    result = args["a"] + args["b"]
    return {"content": [{"type": "text", "text": f"The sum is: {result}"}]}


@tool("multiply", "Multiply two numbers together", {"a": float, "b": float})
async def multiply(args: dict[str, Any]) -> dict[str, Any]:
    """Multiply two numbers and return the result."""
    result = args["a"] * args["b"]
    return {"content": [{"type": "text", "text": f"The product is: {result}"}]}


@tool("power", "Raise a number to a power", {"base": float, "exponent": float})
async def power(args: dict[str, Any]) -> dict[str, Any]:
    """Calculate base raised to the exponent power."""
    result = args["base"] ** args["exponent"]
    return {"content": [{"type": "text", "text": f"The result is: {result}"}]}


async def main() -> None:
    """Run an agent with custom calculator tools."""
    # Load API key from .env file or environment variable
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Set for the SDK to use
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Create an MCP server with our custom tools
    calculator_server = create_sdk_mcp_server(
        name="calculator",
        tools=[add, multiply, power],
    )

    # Configure agent options with the custom MCP server
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful math assistant. Use the calculator tools to perform calculations.",
        mcp_servers={"calc": calculator_server},
        allowed_tools=[
            "mcp__calc__add",
            "mcp__calc__multiply",
            "mcp__calc__power",
        ],
        permission_mode="default",
        cwd=os.getcwd(),
    )

    # Use ClaudeSDKClient for a multi-turn conversation
    async with ClaudeSDKClient(options=options) as client:
        prompts = [
            "What is 42 + 58?",
            "Now multiply that result by 7.",
            "Finally, raise 2 to the power of 10.",
        ]

        for prompt in prompts:
            print(f"\nUser: {prompt}")
            print("-" * 40)

            await client.query(prompt)

            async for message in client.receive_response():
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}")

    print("\n" + "=" * 50)
    print("Conversation complete!")


if __name__ == "__main__":
    asyncio.run(main())
