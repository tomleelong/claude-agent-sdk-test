"""Example demonstrating structured output with the Claude Agent SDK.

Use JSON Schema to get validated, predictable response formats
that are easy to parse and use in your application.
"""

import asyncio
import json
import os

from decouple import config

from claude_agent_sdk import (
    ClaudeAgentOptions,
    ResultMessage,
    query,
)


async def main() -> None:
    """Run an agent that returns structured JSON output."""
    # Load API key from .env file or environment variable
    api_key = config("ANTHROPIC_API_KEY", default="")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY is not set.")
        print("Create a .env file with: ANTHROPIC_API_KEY=your-api-key")
        return

    # Set for the SDK to use
    os.environ["ANTHROPIC_API_KEY"] = api_key

    # Define a JSON Schema for the expected output
    code_analysis_schema = {
        "type": "json_schema",
        "schema": {
            "type": "object",
            "properties": {
                "file_name": {
                    "type": "string",
                    "description": "Name of the analyzed file",
                },
                "summary": {
                    "type": "string",
                    "description": "Brief summary of what the code does",
                },
                "issues": {
                    "type": "array",
                    "description": "List of identified issues",
                    "items": {
                        "type": "object",
                        "properties": {
                            "severity": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                            "category": {
                                "type": "string",
                                "enum": [
                                    "bug",
                                    "security",
                                    "performance",
                                    "style",
                                    "maintainability",
                                ],
                            },
                            "description": {"type": "string"},
                            "line_number": {"type": "integer"},
                            "suggestion": {"type": "string"},
                        },
                        "required": ["severity", "category", "description"],
                    },
                },
                "metrics": {
                    "type": "object",
                    "properties": {
                        "lines_of_code": {"type": "integer"},
                        "functions_count": {"type": "integer"},
                        "complexity_score": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 10,
                        },
                    },
                    "required": ["lines_of_code", "functions_count", "complexity_score"],
                },
                "recommendations": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of improvement recommendations",
                },
            },
            "required": ["file_name", "summary", "issues", "metrics", "recommendations"],
        },
    }

    options = ClaudeAgentOptions(
        system_prompt="You are a code analysis tool. Analyze code and return structured results.",
        output_format=code_analysis_schema,
        allowed_tools=["Read"],
        permission_mode="default",
        cwd=os.getcwd(),
    )

    print("Structured Output Demo")
    print("=" * 50)
    print("Analyzing code and returning structured JSON...\n")

    prompt = "Analyze the file src/simple_agent.py and provide a structured analysis."

    print(f"Prompt: {prompt}\n")
    print("-" * 50)

    async for message in query(prompt=prompt, options=options):
        if isinstance(message, ResultMessage):
            if message.result:
                # Parse the structured JSON response
                analysis = json.loads(message.result)

                print("\n📊 Code Analysis Results")
                print("=" * 40)
                print(f"File: {analysis['file_name']}")
                print(f"\n📝 Summary:\n{analysis['summary']}")

                print(f"\n📈 Metrics:")
                metrics = analysis["metrics"]
                print(f"  • Lines of code: {metrics['lines_of_code']}")
                print(f"  • Functions: {metrics['functions_count']}")
                print(f"  • Complexity: {metrics['complexity_score']}/10")

                if analysis["issues"]:
                    print(f"\n⚠️  Issues Found ({len(analysis['issues'])}):")
                    for issue in analysis["issues"]:
                        severity_icon = {
                            "low": "🟢",
                            "medium": "🟡",
                            "high": "🔴",
                        }.get(issue["severity"], "⚪")
                        print(f"  {severity_icon} [{issue['category']}] {issue['description']}")
                        if "suggestion" in issue:
                            print(f"     💡 {issue['suggestion']}")
                else:
                    print("\n✅ No issues found!")

                if analysis["recommendations"]:
                    print(f"\n💡 Recommendations:")
                    for rec in analysis["recommendations"]:
                        print(f"  • {rec}")

    print("\n" + "-" * 50)
    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
