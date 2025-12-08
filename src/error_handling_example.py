"""Example demonstrating error handling with the Claude Agent SDK.

Shows how to gracefully handle errors, implement retry logic,
and build resilient applications.
"""

import asyncio
import os

from decouple import config

from claude_agent_sdk import (
    AssistantMessage,
    CLIJSONDecodeError,
    CLINotFoundError,
    ClaudeAgentOptions,
    ProcessError,
    TextBlock,
    query,
)


async def basic_error_handling() -> None:
    """Demonstrate basic error handling patterns."""
    print("\n1️⃣  Basic Error Handling")
    print("-" * 40)

    try:
        options = ClaudeAgentOptions(
            allowed_tools=["Read", "Bash"],
            permission_mode="default",
            cwd=os.getcwd(),
        )

        async for message in query(
            prompt="What files are in the current directory?",
            options=options,
        ):
            if isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock):
                        print(f"Agent: {block.text}")

    except CLINotFoundError:
        print("❌ Error: Claude Code CLI not found.")
        print("   Install with: npm install -g @anthropic-ai/claude-code")

    except ProcessError as e:
        print(f"❌ Process error (exit code {e.exit_code})")
        print(f"   stderr: {e.stderr}")

    except CLIJSONDecodeError as e:
        print(f"❌ Failed to parse response: {e.line}")
        print(f"   Original error: {e.original_error}")

    except Exception as e:
        print(f"❌ Unexpected error: {type(e).__name__}: {e}")


async def retry_with_backoff(
    prompt: str,
    options: ClaudeAgentOptions,
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> None:
    """Execute a query with exponential backoff retry logic.

    Args:
        prompt: The prompt to send to the agent.
        options: Agent configuration options.
        max_retries: Maximum number of retry attempts.
        base_delay: Base delay in seconds (doubles each retry).
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            async for message in query(prompt=prompt, options=options):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}")
            return  # Success, exit the function

        except ProcessError as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2**attempt)
                print(f"⚠️  Attempt {attempt + 1} failed, retrying in {delay}s...")
                await asyncio.sleep(delay)
            else:
                print(f"❌ All {max_retries} attempts failed.")

        except CLINotFoundError:
            # Don't retry if CLI is not installed
            raise

    if last_exception:
        raise last_exception


async def retry_example() -> None:
    """Demonstrate retry logic with exponential backoff."""
    print("\n2️⃣  Retry with Exponential Backoff")
    print("-" * 40)

    options = ClaudeAgentOptions(
        allowed_tools=["Read"],
        permission_mode="default",
        cwd=os.getcwd(),
    )

    try:
        await retry_with_backoff(
            prompt="Read the pyproject.toml file and summarize it.",
            options=options,
            max_retries=3,
            base_delay=1.0,
        )
    except Exception as e:
        print(f"❌ Final error: {e}")


async def timeout_example() -> None:
    """Demonstrate handling timeouts."""
    print("\n3️⃣  Timeout Handling")
    print("-" * 40)

    options = ClaudeAgentOptions(
        allowed_tools=["Read"],
        permission_mode="default",
        cwd=os.getcwd(),
        max_turns=5,  # Limit the number of turns to prevent runaway agents
    )

    try:
        # Wrap with asyncio.timeout for overall time limit
        async with asyncio.timeout(30):  # 30 second timeout
            async for message in query(
                prompt="List all Python files in the src directory.",
                options=options,
            ):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}")

        print("✅ Completed within timeout")

    except TimeoutError:
        print("❌ Operation timed out after 30 seconds")

    except Exception as e:
        print(f"❌ Error: {e}")


async def graceful_degradation() -> None:
    """Demonstrate graceful degradation when features are unavailable."""
    print("\n4️⃣  Graceful Degradation")
    print("-" * 40)

    # Try with full capabilities first, fall back to limited mode
    tool_sets = [
        (["Read", "Write", "Bash", "Grep", "Glob"], "Full capabilities"),
        (["Read", "Bash"], "Limited capabilities"),
        (["Read"], "Minimal capabilities"),
    ]

    for tools, description in tool_sets:
        try:
            print(f"Trying with {description}...")

            options = ClaudeAgentOptions(
                allowed_tools=tools,
                permission_mode="default",
                cwd=os.getcwd(),
            )

            async for message in query(
                prompt="What is this project about? Check the README.",
                options=options,
            ):
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(f"Agent: {block.text}")

            print(f"✅ Succeeded with {description}")
            return  # Success, stop trying

        except ProcessError as e:
            print(f"⚠️  Failed with {description}: {e}")
            continue  # Try next tool set

    print("❌ All capability levels failed")


async def main() -> None:
    """Run all error handling examples."""
    # Load API key from .env file or environment variable
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Set for the SDK to use
    os.environ["ANTHROPIC_API_KEY"] = api_key

    print("Error Handling Demo")
    print("=" * 50)
    print("Demonstrating various error handling patterns.\n")

    await basic_error_handling()
    await retry_example()
    await timeout_example()
    await graceful_degradation()

    print("\n" + "=" * 50)
    print("All examples complete!")


if __name__ == "__main__":
    asyncio.run(main())
