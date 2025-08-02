import asyncio
from dotenv import load_dotenv
load_dotenv()
from browser_use import Agent, Controller
from browser_use.mcp.client import MCPClient
from browser_use.llm import ChatAnthropic
from browser_use.browser import BrowserSession, BrowserProfile, BrowserConfig
from pathlib import Path

async def main():
    target_url = "http://localhost:3000"
    test_task = "Design a REST API endpoint for user authentication"
    target_directory = Path.cwd() / "browser_use"
    prompt = f"""Go to {target_url} and test it with a prompt {test_task}, 
    write any issues or failing points into the file {target_directory}/analysis/cua_analysis.txt"""

    # Initialize controller
    controller = Controller()
    
    # Connect to multiple MCP servers
    filesystem_client = MCPClient(
        server_name="filesystem",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", str(target_directory)]
    )
    
    # Connect and register tools from both servers
    await filesystem_client.connect()
    await filesystem_client.register_to_controller(controller)

    # Browser session
    profile_dir = Path.cwd() / "browseruse" / "profiles" / "myprofile"
    profile_dir.mkdir(parents=True, exist_ok=True)
    browser_profile = BrowserProfile(
        headless=False,
        user_data_dir=str(profile_dir),
        disable_security=True
    )
    browser_session = BrowserSession(browser_profile=browser_profile)
    
    # Create agent with MCP-enabled controller
    agent = Agent(
        task=prompt,
        llm=ChatAnthropic(model="claude-sonnet-4-0", temperature=1.0),
        controller=controller,  # Controller has tools from both MCP servers,
        browser_session=browser_session,
    )
    
    # Run the agent
    await agent.run()
    
    # Cleanup
    await filesystem_client.disconnect()

asyncio.run(main())