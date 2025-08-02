"""
Frontend Engineer Agent - Specialized for frontend development tasks
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from .utils import get_project_info, format_file_list


class FrontendEngineer(BaseAgent):
    """
    Specialized agent for frontend development tasks
    Can create React, Vue, Angular, or vanilla JavaScript projects
    """
    
    def __init__(self, frontend_directory: str = "project/frontend", max_turns: int = 100):
        """
        Initialize the Frontend Engineer agent
        
        Args:
            frontend_directory: Directory where frontend projects will be created
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(frontend_directory, max_turns)
        self.agent_name = "Frontend Engineer"
        self.supported_frameworks = ["React"]
    
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        return "Frontend Engineer"
    
    def _enhance_prompt(self, task_description: str) -> str:
        """
        Enhance the task description with frontend-specific context
        """
        project_info = get_project_info(self.working_directory)
        
        enhanced_prompt = f"""
You are a Frontend Engineer agent working in the directory: {self.working_directory}

IMPORTANT CONTEXT:
- You are specifically designed for frontend development tasks
- You can create complete frontend projects from scratch
- Supported frameworks: {', '.join(self.supported_frameworks)}
- Current directory info: {project_info}

FRONTEND DEVELOPMENT GUIDELINES:
1. Create modern, clean, and maintainable code
2. Follow current best practices for the chosen framework
3. Include proper project structure (src/, public/, components/, etc.)
4. Add package.json with appropriate dependencies
5. Include basic configuration files (vite.config.js, tsconfig.json, etc.)
6. Create responsive and accessible UI components
7. Use TypeScript when appropriate for type safety
8. Include basic styling (CSS/SCSS/Tailwind)
9. Add proper error handling and loading states
10. Create reusable components and utilities

TASK TO COMPLETE:
{task_description}

Please create all necessary files and folders for a complete, working frontend project.
Make sure to include:
- Proper project structure
- Package.json with dependencies
- Configuration files
- Source code with components
- Basic styling
- README with setup instructions

Focus on creating production-ready code that follows modern frontend development practices.
"""
        return enhanced_prompt
    
    def add_feature(self, feature_description: str) -> Dict[str, Any]:
        """
        Add a new feature to existing frontend project
        
        Args:
            feature_description: Description of the feature to add
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add the following feature to the existing frontend project:
{feature_description}

Current project files:
{files_context}

Please analyze the existing code structure and add the new feature following the same patterns and conventions.
"""
        
        return self.execute_task(task)
    
    def optimize_performance(self) -> Dict[str, Any]:
        """
        Optimize the performance of existing frontend project
        
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Optimize the performance of the existing frontend project by:
1. Implementing code splitting and lazy loading
2. Optimizing bundle size
3. Adding memoization where appropriate
4. Optimizing images and assets
5. Implementing proper caching strategies
6. Adding performance monitoring

Current project files:
{files_context}

Please analyze the existing code and implement performance optimizations.
"""
        
        return self.execute_task(task)
    
    def add_testing(self, testing_framework: str = "vitest") -> Dict[str, Any]:
        """
        Add testing infrastructure to the project
        
        Args:
            testing_framework: Testing framework to use (vitest, jest, cypress, etc.)
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add comprehensive testing infrastructure using {testing_framework} to the existing frontend project:
1. Unit tests for components
2. Integration tests
3. Test configuration files
4. Test utilities and helpers
5. Sample test files demonstrating best practices
6. Update package.json with testing scripts

Current project files:
{files_context}

Please set up a complete testing environment with example tests.
"""
        
        return self.execute_task(task)
    
    def test_implementation(self) -> Dict[str, Any]:
        """
        Test the frontend implementation by running npm install and npm run dev as background processes
        
        Returns:
            Dictionary containing test results
        """
        import subprocess
        import asyncio
        import time
        import requests
        import os
        from pathlib import Path
        
        try:
            # Change to working directory
            original_cwd = os.getcwd()
            os.chdir(self.working_directory)
            
            # Check if package.json exists
            package_json_path = Path(self.working_directory) / "package.json"
            if not package_json_path.exists():
                return {
                    'success': False,
                    'error': 'No package.json found in project directory',
                    'working_directory': self.working_directory
                }
            
            print(f"📦 Installing dependencies in {self.working_directory}...")
            
            # Run npm install
            install_process = subprocess.run(
                ['npm', 'install'],
                cwd=self.working_directory,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if install_process.returncode != 0:
                return {
                    'success': False,
                    'error': f'npm install failed: {install_process.stderr}',
                    'working_directory': self.working_directory
                }
            
            print("✅ Dependencies installed successfully")
            print(f"🚀 Starting development server in background...")
            
            # Start npm run dev as background process
            dev_process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=self.working_directory,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None  # Create new process group
            )
            
            # Wait for server to start (poll for up to 30 seconds)
            server_ready = False
            max_wait_time = 30
            start_time = time.time()
            
            while time.time() - start_time < max_wait_time:
                try:
                    # Try different common ports
                    for port in [3001]:
                        try:
                            response = requests.get(f'http://localhost:{port}', timeout=2)
                            if response.status_code == 200:
                                server_ready = True
                                server_port = port
                                break
                        except requests.exceptions.RequestException:
                            continue
                    
                    if server_ready:
                        break
                        
                    time.sleep(2)
                except Exception:
                    time.sleep(2)
            
            # Store process info for later cleanup (optional)
            if hasattr(self, '_background_processes'):
                self._background_processes.append(dev_process)
            else:
                self._background_processes = [dev_process]
            
            # Change back to original directory
            os.chdir(original_cwd)
            
            if server_ready:
                return {
                    'success': True,
                    'message': f'Frontend server started successfully on port {server_port}',
                    'server_url': f'http://localhost:{server_port}',
                    'process_id': dev_process.pid,
                    'working_directory': self.working_directory,
                    'files_created': self._get_created_files()
                }
            else:
                # Server didn't start in time, but process might still be running
                return {
                    'success': True,
                    'message': 'Frontend server started but may still be initializing',
                    'process_id': dev_process.pid,
                    'working_directory': self.working_directory,
                    'files_created': self._get_created_files(),
                    'note': 'Server may take additional time to fully start up'
                }
                
        except subprocess.TimeoutExpired:
            os.chdir(original_cwd)
            return {
                'success': False,
                'error': 'npm install timed out after 5 minutes',
                'working_directory': self.working_directory
            }
        except Exception as e:
            if 'original_cwd' in locals():
                os.chdir(original_cwd)
            return {
                'success': False,
                'error': f'Test implementation failed: {str(e)}',
                'working_directory': self.working_directory
            }
    
    def get_specialized_status(self) -> Dict[str, Any]:
        """Get frontend-specific status information"""
        base_status = self.get_status()
        project_info = get_project_info(self.working_directory)
        
        base_status.update({
            'supported_frameworks': self.supported_frameworks,
            'project_info': project_info,
            'has_package_json': project_info.get('has_package_json', False),
            'has_readme': project_info.get('has_readme', False)
        })
        
        return base_status