"""
Testing Engineer Agent - Specialized for browser-based testing using Playwright
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
from claude_code_sdk import ClaudeCodeOptions
from .base_agent import BaseAgent
from .utils import get_project_info, format_file_list
import os
from claude_code_sdk import query

import uuid

class TestingEngineer(BaseAgent):
    """
    Specialized agent for browser-based automated testing
    Uses Playwright MCP for comprehensive browser testing and QA
    """
    
    def __init__(self, testing_directory: str = "project/testing", max_turns: int = 100):
        """
        Initialize the Testing Engineer agent
        
        Args:
            testing_directory: Directory where test results and reports will be created
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(testing_directory, max_turns)
        self.agent_name = "Testing Engineer"
        self.mcp_servers = {
            "playwright": {
                "type": "stdio",
                "command": "npx",
                "args": ["@playwright/mcp@latest", "--headless"],
                "env": {}
            }
        }
    
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        return "Testing Engineer"
    
    async def query_claude_code_sdk_with_playwright(self, prompt: str) -> List[Any]:
        """Query Claude Code SDK with Playwright MCP server support"""
        
        options = ClaudeCodeOptions(
            max_turns=self.max_turns,
            cwd=Path(self.working_directory),
            mcp_servers=self.mcp_servers,
            permission_mode="bypassPermissions",
            allowed_tools=["read", "write"],
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
                
                # Advanced features
                "mcp__playwright__browser_network_requests",
                "mcp__playwright__browser_console_messages",
                "mcp__playwright__browser_handle_dialog",
                "mcp__playwright__browser_file_upload",
                "mcp__playwright__browser_close",
                "mcp__playwright__browser_resize",
                
                # Tab management
                "mcp__playwright__browser_tab_list",
                "mcp__playwright__browser_tab_new",
                "mcp__playwright__browser_tab_select",
                "mcp__playwright__browser_tab_close"
            ]
        )
        
        messages = []
        try:
            # Change to working directory before querying
            original_cwd = os.getcwd()
            os.chdir(self.working_directory)
            
            async for message in query(prompt=prompt, options=options):
                print(message)
                messages.append(message)
                
            # Change back to original directory
            os.chdir(original_cwd)
            
        except Exception as e:
            # Change back to original directory even on error
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            raise Exception(f"Claude Code SDK error: {str(e)}")
        
        return messages

    def _enhance_prompt(self, task_description: str) -> str:
        """
        Enhance the task description with agent-specific context
        
        Args:
            task_description: Original task description
            
        Returns:
            Enhanced prompt with agent-specific context
        """
        return task_description
    
    def test_web_application(self, url: str, test_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Test a web application using browser automation
        
        Args:
            url: URL of the web application to test
            test_prompt: Optional specific test instructions
            
        Returns:
            Dictionary containing test results
        """
        if test_prompt:
            task = f"""
1. Navigate to {url} using Playwright browser automation
2. {test_prompt}
3. Document all issues or failures - DO NOT save screenshots
4. Save the analysis in analysis/fixes.MD
"""
        else:
            task = f"""
Test the web application at {url} comprehensively:
1. Navigate to the application
2. Test all interactive elements and user flows
3. Verify page functionality and navigation
4. Document all findings, issues, or test results - DO NOT save screenshots
5. Save the analysis in analysis/fixes.MD
"""
        
        try:
            messages = self.run_async(self.query_claude_code_sdk_with_playwright(
                self._enhance_prompt(task)
            ))
            
            # Store conversation history
            self.conversation_history.append({
                'task': task,
                'url': url,
                'messages': messages,
                'timestamp': uuid.uuid4().hex
            })
            
            return {
                'success': True,
                'messages': messages,
                'session_id': self.session_id,
                'working_directory': self.working_directory,
                'files_created': self._get_created_files()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'session_id': self.session_id,
                'working_directory': self.working_directory
            }
