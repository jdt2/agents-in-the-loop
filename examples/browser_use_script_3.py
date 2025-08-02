import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message
from pathlib import Path
from dataclasses import dataclass
from claude_code_sdk.types import ResultMessage, SystemMessage, UserMessage, AssistantMessage

from typing import Dict, List, Optional

@dataclass
class McpServerConfig:
    command: str
    args: List[str] = None
    env: Dict[str, str] = None
    transport: str = "stdio"  # "stdio", "sse", or "http"
    url: Optional[str] = None
    headers: Dict[str, str] = None

    
async def main(prompt):
    mcp_servers = {
        "playwright": {
            "type": "stdio",  # Optional for stdio, but explicit is better
            "command": "npx",
            "args": ["@playwright/mcp@latest", "--headless"],
            "env": {}
        }
    }

    # Configuration options for Claude Code with Playwright MCP
    options = ClaudeCodeOptions(
        max_turns=5,
        system_prompt="You are a browser use assistant tasked to do quality assurance using Playwright.",
        cwd=Path.cwd() / "project" / "testing",
        mcp_servers=mcp_servers,
        permission_mode="bypassPermissions",
        # Core tools - always available
        mcp_tools=[
            # Essential browser automation
            "mcp__playwright__browser_navigate",
            "mcp__playwright__browser_snapshot", 
            "mcp__playwright__browser_click",
            "mcp__playwright__browser_type",
            "mcp__playwright__browser_take_screenshot",
            "mcp__playwright__browser_wait_for",
            "mcp__playwright__browser_evaluate",
            
            # Navigation and interaction
            "mcp__playwright__browser_navigate_back",
            "mcp__playwright__browser_navigate_forward",
            "mcp__playwright__browser_hover",
            "mcp__playwright__browser_press_key",
            "mcp__playwright__browser_select_option",
            "mcp__playwright__browser_drag",
            
        ]
    )
    
    messages: list[Message] = []
    
    async for message in query(
        prompt=prompt,
        options=options
    ):
        messages.append(message)
        # Messages are dataclass objects, not dictionaries
        # if isinstance(message, ResultMessage):
        #     print(f"Task completed: {message.result or 'No result'}")
        # elif hasattr(message, 'subtype'):
        #     print(f"Message: {type(message).__name__} - {message.subtype}")
        # else:
        #     print(f"Message: {type(message).__name__}")
        #     print(message)
    
    return messages


if __name__ == "__main__":
    # Run examples
    target_url = "http://localhost:3000"
    test_task = "Design a REST API endpoint for user authentication"
    target_directory = Path.cwd() / "project" / "testing" / "analysis"
    prompt = f"""Go to {target_url} and test it with a prompt {test_task}, 
    write any issues or failing points into the file {target_directory}/fixes.MD"""
    
    # Create async wrapper function
    async def run_main():
        return await main(prompt)
    
    # Run the async function
    anyio.run(run_main)