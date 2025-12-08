"""Simple example demonstrating the Claude Agent SDK.

This example shows how to use the query() function for one-off tasks.
"""

import asyncio
import os

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    TextBlock,
    query,
)


async def main() -> None:
    """Run a simple agent query."""
    # Ensure API key is set
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY environment variable is not set.")
        print("Set it with: export ANTHROPIC_API_KEY='your-api-key'")
        return

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
