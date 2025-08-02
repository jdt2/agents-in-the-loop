import asyncio
from browser_use import Agent, Controller
from browser_use.mcp.client import MCPClient
from browser_use.llm import ChatAnthropic
from browser_use.browser import BrowserSession, BrowserProfile
from pathlib import Path


class BrowserUseAgent:
    """Browser Use Agent wrapper for Flask integration"""
    
    def __init__(self):
        self.controller = None
        self.filesystem_client = None
        self.browser_session = None
        
    async def setup(self, target_directory: Path):
        """Setup the agent with MCP clients and browser session"""
        # Initialize controller
        self.controller = Controller()
        
        # Connect to filesystem MCP server
        self.filesystem_client = MCPClient(
            server_name="filesystem",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", str(target_directory)]
        )
        
        # Connect and register tools
        await self.filesystem_client.connect()
        await self.filesystem_client.register_to_controller(self.controller)

        # Browser session setup
        profile_dir = Path.cwd() / "browseruse" / "profiles" / "webapp"
        profile_dir.mkdir(parents=True, exist_ok=True)
        browser_profile = BrowserProfile(
            headless=False,
            user_data_dir=str(profile_dir),
            disable_security=True
        )
        self.browser_session = BrowserSession(browser_profile=browser_profile)
        
    async def run_task(self, task: str, target_url: str = "http://localhost:3000"):
        """Run a browser automation task"""
        if not self.controller or not self.browser_session:
            raise Exception("Agent not properly initialized. Call setup() first.")
            
        # Create the agent
        agent = Agent(
            task=task,
            llm=ChatAnthropic(model="claude-sonnet-4-0", temperature=1.0),
            controller=self.controller,
            browser_session=self.browser_session,
        )
        
        # Run the agent
        result = await agent.run()
        return result
        
    async def cleanup(self):
        """Cleanup resources"""
        if self.filesystem_client:
            await self.filesystem_client.disconnect()


async def run_browser_agent(task: str, target_url: str = "http://localhost:3000", 
                          output_file: str = None):
    """
    Run browser automation task
    
    Args:
        task: The task description for the agent
        target_url: URL to navigate to
        output_file: Optional file path to save results
    
    Returns:
        dict: Result information
    """
    target_directory = Path.cwd() / "browser_use"
    target_directory.mkdir(exist_ok=True)
    
    if output_file is None:
        output_file = target_directory / "analysis" / "task_results.txt"
    else:
        output_file = Path(output_file)
        
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Create full task prompt
    full_task = f"""Go to {target_url} and {task}. 
    Write any results, issues, or findings into the file {output_file}"""
    
    agent = BrowserUseAgent()
    
    try:
        await agent.setup(target_directory)
        result = await agent.run_task(full_task, target_url)
        
        return {
            'success': True,
            'task': task,
            'target_url': target_url,
            'output_file': str(output_file),
            'result': str(result) if result else 'Task completed'
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'task': task,
            'target_url': target_url
        }
        
    finally:
        await agent.cleanup()
