"""Simple example demonstrating the Claude Agent SDK.

This example shows how to use the query() function for one-off tasks.
"""

import asyncio
import os

from decouple import config

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)


async def main() -> None:
    """Run a simple agent query."""
    # Load API key from .env file or environment variable
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Set for the SDK to use
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Configure the agent options
    options = ClaudeAgentOptions(
        system_prompt="You are a helpful coding assistant. Be concise and clear.",
        allowed_tools=["Read", "Bash"],  # Limit tools for safety
        permission_mode="default",
        cwd=os.getcwd(),
    )

    prompt = "What Python version is installed on this system? Use the Bash tool to check."

    print(f"Prompt: {prompt}\n")
    print("-" * 50)

    # Stream responses from the agent
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Agent: {block.text}")

    print("-" * 50)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
