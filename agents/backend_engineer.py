"""
Backend Engineer Agent - Specialized for backend development tasks
"""

from typing import Dict, Any
from .base_agent import BaseAgent
from .utils import get_project_info, format_file_list


class BackendEngineer(BaseAgent):
    """
    Specialized agent for backend development tasks
    Can create APIs, microservices, databases, and full backend systems
    """
    
    def __init__(self, backend_directory: str = "project/backend", max_turns: int = 100):
        """
        Initialize the Backend Engineer agent
        
        Args:
            backend_directory: Directory where backend projects will be created
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(backend_directory, max_turns)
        self.agent_name = "Backend Engineer"
        self.supported_frameworks = ["FastAPI"]
        self.supported_databases = ["PostgreSQL", "SQLite"]
    
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        return "Backend Engineer"
    
    def _enhance_prompt(self, task_description: str) -> str:
        """
        Enhance the task description with backend-specific context
        """
        project_info = get_project_info(self.working_directory)
        
        enhanced_prompt = f"""
You are a Backend Engineer agent working in the directory: {self.working_directory}

IMPORTANT CONTEXT:
- You are specifically designed for backend development tasks
- You can create complete backend systems from scratch
- Supported frameworks: {', '.join(self.supported_frameworks)}
- Supported databases: {', '.join(self.supported_databases)}
- Current directory info: {project_info}

BACKEND DEVELOPMENT GUIDELINES:
1. Create secure, scalable, and maintainable backend systems
2. Follow REST API and GraphQL best practices
3. Implement proper authentication and authorization
4. Include comprehensive error handling and logging
5. Set up proper database models and migrations
6. Add input validation and sanitization
7. Implement rate limiting and security middleware
8. Create comprehensive API documentation
9. Include unit tests, integration tests, and API tests
10. Set up proper configuration management
11. Add Docker containerization when appropriate
12. Follow security best practices (OWASP guidelines)
13. Implement proper CORS policies
14. Add monitoring and health check endpoints
15. Use environment variables for sensitive data

TASK TO COMPLETE:
{task_description}

Please create all necessary files and folders for a complete, production-ready backend system.
Make sure to include:
- Proper project structure
- Requirements/package files (requirements.txt, package.json, etc.)
- Configuration files
- Database models and schemas
- API routes and controllers
- Middleware and security layers
- Authentication and authorization
- Error handling
- Logging configuration
- Tests
- Docker configuration (if requested)
- API documentation
- README with setup instructions

Focus on creating secure, scalable code that follows modern backend development practices.
"""
        return enhanced_prompt
    
    def test_implementation(self) -> Dict[str, Any]:
        """
        Test the backend implementation by running dependency installation and starting server as background process
        
        Returns:
            Dictionary containing test results
        """
        import subprocess
        import time
        import requests
        import os
        from pathlib import Path
        
        try:
            # Change to working directory
            original_cwd = os.getcwd()
            os.chdir(self.working_directory)
            
            # Check for dependency files
            requirements_txt = Path(self.working_directory) / "requirements.txt"
            package_json = Path(self.working_directory) / "package.json"
            pyproject_toml = Path(self.working_directory) / "pyproject.toml"
            
            if requirements_txt.exists():
                print(f"🐍 Installing Python dependencies in {self.working_directory}...")
                
                # Install Python dependencies
                install_process = subprocess.run(
                    ['pip', 'install', '-r', 'requirements.txt'],
                    cwd=self.working_directory,
                    capture_output=True,
                    text=True,
                    timeout=300  # 5 minute timeout
                )
                
                if install_process.returncode != 0:
                    return {
                        'success': False,
                        'error': f'pip install failed: {install_process.stderr}',
                        'working_directory': self.working_directory
                    }
                
                print("✅ Python dependencies installed successfully")
                print(f"🚀 Starting backend server in background on port 8000...")
                
                # Try different common Python server commands
                server_commands = [
                    ['uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
                    ['uvicorn', 'main:app', '--reload', '--host', '0.0.0.0', '--port', '8000'],
                    ['python', 'app.py'],
                    ['python', 'main.py'],
                    ['fastapi', 'run', 'app.py', '--port', '8000'],
                    ['python', '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '0.0.0.0', '--port', '8000']
                ]
                
            elif package_json.exists():
                print(f"📦 Installing Node.js dependencies in {self.working_directory}...")
                
                # Install Node.js dependencies
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
                
                print("✅ Node.js dependencies installed successfully")
                print(f"🚀 Starting backend server in background on port 8000...")
                
                # Try different Node.js server commands
                server_commands = [
                    ['npm', 'start'],
                    ['npm', 'run', 'dev'],
                    ['node', 'server.js'],
                    ['node', 'app.js'],
                    ['node', 'index.js']
                ]
                
            else:
                return {
                    'success': False,
                    'error': 'No requirements.txt or package.json found in project directory',
                    'working_directory': self.working_directory
                }
            
            # Try to start server with different commands
            dev_process = None
            for cmd in server_commands:
                try:
                    print(f"Trying command: {' '.join(cmd)}")
                    dev_process = subprocess.Popen(
                        cmd,
                        cwd=self.working_directory,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        preexec_fn=os.setsid if hasattr(os, 'setsid') else None
                    )
                    
                    # Wait a moment to see if process starts successfully
                    time.sleep(3)
                    if dev_process.poll() is None:  # Process is still running
                        print(f"✅ Server started with command: {' '.join(cmd)}")
                        break
                    else:
                        print(f"❌ Command failed: {' '.join(cmd)}")
                        dev_process = None
                except FileNotFoundError:
                    print(f"❌ Command not found: {cmd[0]}")
                    continue
                except Exception as e:
                    print(f"❌ Error with command {' '.join(cmd)}: {str(e)}")
                    continue
            
            if dev_process is None:
                return {
                    'success': False,
                    'error': 'Could not start backend server with any of the attempted commands',
                    'working_directory': self.working_directory
                }
            
            # Wait for server to start (poll for up to 30 seconds)
            server_ready = False
            max_wait_time = 30
            start_time = time.time()
            server_port = 8000
            
            while time.time() - start_time < max_wait_time:
                try:
                    response = requests.get(f'http://localhost:{server_port}', timeout=2)
                    if response.status_code in [200, 404]:  # 404 is OK for API servers
                        server_ready = True
                        break
                except requests.exceptions.RequestException:
                    pass
                
                # Also try health endpoint
                try:
                    response = requests.get(f'http://localhost:{server_port}/health', timeout=2)
                    if response.status_code == 200:
                        server_ready = True
                        break
                except requests.exceptions.RequestException:
                    pass
                    
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
                    'message': f'Backend server started successfully on port {server_port}',
                    'server_url': f'http://localhost:{server_port}',
                    'process_id': dev_process.pid,
                    'working_directory': self.working_directory,
                    'files_created': self._get_created_files()
                }
            else:
                # Server didn't respond in time, but process might still be running
                return {
                    'success': True,
                    'message': 'Backend server started but may still be initializing',
                    'process_id': dev_process.pid,
                    'working_directory': self.working_directory,
                    'files_created': self._get_created_files(),
                    'note': 'Server may take additional time to fully start up'
                }
                
        except subprocess.TimeoutExpired:
            os.chdir(original_cwd)
            return {
                'success': False,
                'error': 'Dependency installation timed out after 5 minutes',
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
        """Get backend-specific status information"""
        base_status = self.get_status()
        project_info = get_project_info(self.working_directory)
        
        base_status.update({
            'supported_frameworks': self.supported_frameworks,
            'supported_databases': self.supported_databases,
            'project_info': project_info,
            'has_requirements': any(f in ['requirements.txt', 'package.json', 'Pipfile', 'poetry.lock'] 
                                  for f in self._get_created_files()),
            'has_dockerfile': 'Dockerfile' in self._get_created_files(),
            'has_tests': any('test' in f.lower() for f in self._get_created_files())
        })
        
        return base_status