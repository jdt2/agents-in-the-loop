"""
Base Agent class for Claude Code SDK powered agents
"""

import os
import asyncio
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import uuid
from dotenv import load_dotenv
import anyio
from claude_code_sdk import query, ClaudeCodeOptions

load_dotenv()


class BaseAgent(ABC):
    """Base class for all Claude Code SDK powered agents"""
    
    def __init__(self, working_directory: str, max_turns: int = 5):
        """
        Initialize the base agent
        
        Args:
            working_directory: Directory where the agent will create/modify files
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        self.working_directory = os.path.abspath(working_directory)
        self.max_turns = max_turns
        self.session_id = str(uuid.uuid4())
        self.conversation_history = []
        
        # Ensure working directory exists
        os.makedirs(self.working_directory, exist_ok=True)
        
        # Verify API key
        if not os.getenv('ANTHROPIC_API_KEY'):
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    
    def run_async(self, coro):
        """Helper function to run async code"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    
    async def query_claude_code_sdk(self, prompt: str, options: Optional[ClaudeCodeOptions] = None) -> List[Any]:
        """Query Claude Code SDK with error handling"""
        if options is None:
            options = ClaudeCodeOptions(
                max_turns=self.max_turns,
                allowed_tools=["read", "write", "edit", "grep", "Bash", "glob", "Bash(npm install)", "Bash(npm run dev)", "Bash(npm run build)", "Bash(python -m venv .venv)", "Bash(source .venv/bin/activate)"],
                permission_mode="bypassPermissions"
            )
        
        messages = []
        try:
            # Change to working directory before querying
            original_cwd = os.getcwd()
            os.chdir(self.working_directory)
            
            async for message in query(prompt=prompt, options=options):
                messages.append(message)
                
            # Change back to original directory
            os.chdir(original_cwd)
            
        except Exception as e:
            # Change back to original directory even on error
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            raise Exception(f"Claude Code SDK error: {str(e)}")
        
        return messages
    
    def execute_task(self, task_description: str) -> Dict[str, Any]:
        """
        Execute a task using Claude Code SDK
        
        Args:
            task_description: Description of the task to execute
            
        Returns:
            Dictionary containing task results and metadata
        """
        try:
            # Add agent-specific context to the prompt
            enhanced_prompt = self._enhance_prompt(task_description)
            
            # Query Claude Code SDK
            messages = self.run_async(self.query_claude_code_sdk(enhanced_prompt))

            print(messages)
            
            # Store conversation history
            self.conversation_history.append({
                'task': task_description,
                'enhanced_prompt': enhanced_prompt,
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
    
    def _get_created_files(self) -> List[str]:
        """Get list of files in the working directory"""
        files = []
        for root, dirs, filenames in os.walk(self.working_directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                relative_path = os.path.relpath(file_path, self.working_directory)
                files.append(relative_path)
        return files
    
    @abstractmethod
    def _enhance_prompt(self, task_description: str) -> str:
        """
        Enhance the task description with agent-specific context
        
        Args:
            task_description: Original task description
            
        Returns:
            Enhanced prompt with agent-specific context
        """
        pass
    
    @abstractmethod
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        pass
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the agent"""
        return {
            'agent_type': self.get_agent_type(),
            'session_id': self.session_id,
            'working_directory': self.working_directory,
            'max_turns': self.max_turns,
            'conversation_count': len(self.conversation_history),
            'files_in_directory': len(self._get_created_files())
        }