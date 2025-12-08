"""Example demonstrating subagents with the Claude Agent SDK.

Subagents allow you to delegate specialized tasks to purpose-built agents,
each with their own tools and system prompts.
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
    """Run an agent with specialized subagents."""
    # Load API key from .env file or environment variable
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Set for the SDK to use
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Define specialized subagents
    options = ClaudeAgentOptions(
        system_prompt="You are a project manager that delegates tasks to specialized agents.",
        agents={
            "code-reviewer": {
                "description": "Expert code reviewer. Use for quality and security reviews.",
                "prompt": """You are a code review specialist. When reviewing code:
- Identify potential bugs and security vulnerabilities
- Check for performance issues
- Suggest improvements following best practices
- Be concise but thorough""",
                "tools": ["Read", "Grep", "Glob"],
                "model": "sonnet",
            },
            "test-writer": {
                "description": "Test specialist. Use for writing and analyzing tests.",
                "prompt": """You are a testing specialist. When working with tests:
- Write comprehensive unit tests using pytest
- Cover edge cases and error conditions
- Follow testing best practices
- Ensure tests are readable and maintainable""",
                "tools": ["Read", "Write", "Bash"],
                "model": "sonnet",
            },
            "doc-writer": {
                "description": "Documentation specialist. Use for creating documentation.",
                "prompt": """You are a documentation specialist. When writing docs:
- Write clear, concise documentation
- Include usage examples
- Follow Google/NumPy docstring conventions
- Make documentation accessible to all skill levels""",
                "tools": ["Read", "Write"],
                "model": "haiku",
            },
        },
        allowed_tools=["Read", "Write", "Bash", "Grep", "Glob"],
        permission_mode="default",
        cwd=os.getcwd(),
    )

    print("Subagents Demo")
    print("=" * 50)
    print("The main agent will delegate to specialized subagents as needed.\n")

    # This prompt will trigger the agent to use subagents
    prompt = """Please help me with this Python project:
1. Review the code in src/simple_agent.py for any issues
2. Suggest what tests should be written for it
3. Summarize what documentation would be helpful

Use the appropriate specialist for each task."""

    print(f"Prompt: {prompt}\n")
    print("-" * 50)

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    print(f"Agent: {block.text}")

    print("-" * 50)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
