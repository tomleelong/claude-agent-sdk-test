"""Example demonstrating multi-turn conversations with the Claude Agent SDK.

This example shows how to use ClaudeSDKClient for maintaining
conversation context across multiple exchanges.
"""

import asyncio
import os

from decouple import config

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    TextBlock,
)


async def main() -> None:
    """Run a multi-turn conversation agent."""
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
        system_prompt=(
            "You are a knowledgeable assistant helping with Python programming. "
            "Remember previous context in our conversation and build upon it."
        ),
        allowed_tools=["Read", "Bash"],
        permission_mode="default",
        cwd=os.getcwd(),
    )

    print("Multi-turn Conversation Demo")
    print("=" * 50)

    # Use ClaudeSDKClient to maintain conversation context
    async with ClaudeSDKClient(options=options) as client:
        # First exchange
        prompt1 = "What is a Python decorator? Give a brief explanation."
        print(f"\nUser: {prompt1}")
        print("-" * 40)

        await client.query(prompt1)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")

        # Follow-up question - agent remembers context
        prompt2 = "Can you show me a simple example of what you just explained?"
        print(f"\nUser: {prompt2}")
        print("-" * 40)

        await client.query(prompt2)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")

        # Another follow-up
        prompt3 = "How would I use this pattern for timing function execution?"
        print(f"\nUser: {prompt3}")
        print("-" * 40)

        await client.query(prompt3)
        async for message in client.receive_response():
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")

    print("\n" + "=" * 50)
    print("Conversation complete!")


if __name__ == "__main__":
    asyncio.run(main())
