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
        self.supported_frameworks = [
            "FastAPI", "Flask", "Django", "Express.js", "Node.js", "NestJS",
            "Spring Boot", "Go Gin", "Ruby on Rails", "ASP.NET Core"
        ]
        self.supported_databases = [
            "PostgreSQL", "MongoDB", "SQLite", "MySQL", "Redis", "DynamoDB"
        ]
    
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
    
    def create_api_server(self, framework: str = "fastapi", app_name: str = "api-server", include_auth: bool = True) -> Dict[str, Any]:
        """
        Create a REST API server
        
        Args:
            framework: Backend framework to use (fastapi, flask, express, etc.)
            app_name: Name of the API server
            include_auth: Whether to include authentication
            
        Returns:
            Dictionary containing task results
        """
        auth_info = "with JWT authentication and protected routes" if include_auth else "without authentication"
        task = f"Create a {framework.upper()} REST API server named '{app_name}' {auth_info}. Include CRUD operations, input validation, error handling, API documentation, and a SQLite database for development."
        
        return self.execute_task(task)
    
    def create_microservice(self, service_name: str = "user-service", framework: str = "fastapi") -> Dict[str, Any]:
        """
        Create a microservice
        
        Args:
            service_name: Name of the microservice
            framework: Backend framework to use
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a {framework.upper()} microservice named '{service_name}' with Docker containerization, health checks, metrics endpoint, proper logging, database integration, and API documentation. Include service discovery patterns and configuration management."
        
        return self.execute_task(task)
    
    def create_graphql_api(self, app_name: str = "graphql-api", framework: str = "fastapi") -> Dict[str, Any]:
        """
        Create a GraphQL API server
        
        Args:
            app_name: Name of the GraphQL API
            framework: Backend framework to use
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a {framework.upper()} GraphQL API server named '{app_name}' with schema definitions, resolvers, mutations, subscriptions, authentication, and a database layer. Include GraphQL Playground for development."
        
        return self.execute_task(task)
    
    def create_database_layer(self, db_type: str = "postgresql", orm: str = "sqlalchemy") -> Dict[str, Any]:
        """
        Create database models and connection layer
        
        Args:
            db_type: Type of database (postgresql, mongodb, sqlite, etc.)
            orm: ORM to use (sqlalchemy, mongoose, prisma, etc.)
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a complete database layer using {db_type.upper()} with {orm.upper()} ORM. Include models, migrations, connection management, database configuration, and seed data. Add proper indexing and relationships."
        
        return self.execute_task(task)
    
    def add_authentication(self, auth_type: str = "jwt") -> Dict[str, Any]:
        """
        Add authentication system to existing backend
        
        Args:
            auth_type: Type of authentication (jwt, oauth2, session, etc.)
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add {auth_type.upper()} authentication system to the existing backend project:
1. User registration and login endpoints
2. Password hashing and validation
3. Token generation and validation
4. Protected route middleware
5. User profile management
6. Password reset functionality
7. Role-based access control (RBAC)

Current project files:
{files_context}

Please integrate authentication following security best practices.
"""
        
        return self.execute_task(task)
    
    def add_testing(self, testing_framework: str = "pytest") -> Dict[str, Any]:
        """
        Add comprehensive testing infrastructure
        
        Args:
            testing_framework: Testing framework to use (pytest, jest, mocha, etc.)
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add comprehensive testing infrastructure using {testing_framework} to the existing backend project:
1. Unit tests for models and business logic
2. Integration tests for API endpoints
3. Database testing with fixtures
4. Authentication/authorization testing
5. Error handling tests
6. Performance tests
7. Test configuration files
8. Mock data and fixtures
9. Test coverage reporting

Current project files:
{files_context}

Please set up a complete testing environment with example tests.
"""
        
        return self.execute_task(task)
    
    def add_containerization(self, include_compose: bool = True) -> Dict[str, Any]:
        """
        Add Docker containerization to the project
        
        Args:
            include_compose: Whether to include docker-compose.yml
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add Docker containerization to the existing backend project:
1. Multi-stage Dockerfile for production builds
2. Docker ignore file
3. Environment variable configuration
4. Health checks
5. Volume management for data persistence
{f"6. Docker-compose file with database and other services" if include_compose else ""}
7. Container security best practices
8. Build and deployment scripts

Current project files:
{files_context}

Please create production-ready containerization setup.
"""
        
        return self.execute_task(task)
    
    def add_monitoring(self) -> Dict[str, Any]:
        """
        Add monitoring and logging infrastructure
        
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add comprehensive monitoring and logging to the existing backend project:
1. Structured logging with proper log levels
2. Request/response logging middleware
3. Performance monitoring
4. Health check endpoints
5. Metrics collection (Prometheus format)
6. Error tracking and alerting
7. Database query monitoring
8. Security event logging
9. Log rotation and archival

Current project files:
{files_context}

Please implement production-ready monitoring and observability.
"""
        
        return self.execute_task(task)
    
    def create_websocket_server(self, app_name: str = "websocket-server") -> Dict[str, Any]:
        """
        Create a WebSocket server for real-time communication
        
        Args:
            app_name: Name of the WebSocket server
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a WebSocket server named '{app_name}' with room management, authentication, message broadcasting, connection handling, and proper error management. Include both server-side and example client code."
        
        return self.execute_task(task)
    
    def add_caching(self, cache_type: str = "redis") -> Dict[str, Any]:
        """
        Add caching layer to existing backend
        
        Args:
            cache_type: Type of cache (redis, memcached, in-memory, etc.)
            
        Returns:
            Dictionary containing task results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Add {cache_type.upper()} caching layer to the existing backend project:
1. Cache configuration and connection management
2. Cache middleware for API responses
3. Database query result caching
4. Session caching
5. Cache invalidation strategies
6. Cache warming mechanisms
7. Cache monitoring and metrics

Current project files:
{files_context}

Please implement a comprehensive caching strategy for improved performance.
"""
        
        return self.execute_task(task)
    
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
3. Run any database migrations or setup scripts
4. Start the server briefly to ensure it starts without errors
5. Test API endpoints with basic HTTP requests (health check, main endpoints)
6. Validate database connections and basic CRUD operations
7. Check for any import errors or missing dependencies
8. Run any existing tests (pytest, npm test, etc.)
9. Generate a test report showing what works and any issues found

Current project files:
{files_context}

IMPORTANT: Actually run the installation and testing commands to verify everything works.
Make sure to:
- Use the appropriate package manager (pip, poetry, npm, yarn)
- Set up virtual environment if using Python
- Handle any dependency conflicts or version issues
- Test actual API functionality with real HTTP requests
- Report specific error messages if anything fails
- Suggest fixes for any problems found
- Create a summary of the validation results
- Test database connectivity and basic operations

Please perform actual testing and validation, not just theoretical checks.
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