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
        Test the backend implementation by installing dependencies and running checks
        
        Returns:
            Dictionary containing test results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Test and validate the backend implementation by performing the following steps:
1. Check if requirements.txt, pyproject.toml, or package.json exists with valid dependencies
2. Install all dependencies (pip install -r requirements.txt, poetry install, or npm install)
3. Set up virtual environment if using Python
4. Run any database migrations or setup scripts
5. Start API server in background (uvicorn app.main:app --reload --host 0.0.0.0 --port 8000)
6. Wait for server ready signal (poll localhost:8000/health until responding)
7. Test all API endpoints with actual HTTP requests (GET, POST, PUT, DELETE)
8. Validate CORS headers allow frontend access (http://localhost:3001)
9. Test database CRUD operations end-to-end with real data
10. Validate authentication and authorization if implemented
11. Stop background server and cleanup processes
12. Check for any import errors or missing dependencies
13. Run any existing tests (pytest, npm test, etc.)
14. Generate a test report showing what works and any issues found

Current project files:
{files_context}

IMPORTANT: Actually run the installation, server startup, and API testing commands to verify everything works.
Make sure to:
- Use the appropriate package manager (pip, poetry, npm, yarn)
- Set up virtual environment if using Python
- Handle any dependency conflicts or version issues
- Start API server in background with timeout handling
- Test actual API functionality with real HTTP requests to all endpoints
- Verify CORS configuration allows frontend communication (port 3001)
- Test database connectivity and CRUD operations with real data
- Properly cleanup background processes when done
- Report specific error messages if anything fails
- Suggest fixes for any problems found
- Create a summary of the validation results including server and API testing

Please perform actual testing and validation with real server startup and API calls, not just theoretical checks.
"""
        
        return self.execute_task(task)
    
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