"""
Engineering Manager Agent - Coordinates frontend and backend development
"""

from typing import Dict, Any, Optional
from claude_code_sdk import ClaudeCodeOptions
from .base_agent import BaseAgent
from .utils import get_project_info, format_file_list


class EngineeringManager(BaseAgent):
    """
    Engineering Manager agent that coordinates frontend and backend development
    Reads specifications and generates precise instructions for other agents
    Does not write application code - only creates coordination documentation
    """
    
    def __init__(self, project_directory: str = "project", max_turns: int = 50):
        """
        Initialize the Engineering Manager agent
        
        Args:
            project_directory: Directory containing SPEC.md and frontend/backend folders
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(project_directory, max_turns)
        self.agent_name = "Engineering Manager"
        self.coordination_areas = [
            "API Contracts", "Data Models", "Port Configuration", "Authentication",
            "Error Handling", "Development Workflow", "Testing Strategy"
        ]
    
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        return "Engineering Manager"
    
    async def query_claude_code_sdk(self, prompt: str, options: Optional[ClaudeCodeOptions] = None) -> list:
        """
        Override to restrict tool access - no bash commands allowed
        Engineering Manager should only read specs and write documentation
        """
        if options is None:
            options = ClaudeCodeOptions(
                max_turns=self.max_turns,
                allowed_tools=["read", "write", "edit", "grep", "glob"],  # No bash
                permission_mode="bypassPermissions"
            )
        
        return await super().query_claude_code_sdk(prompt, options)
    
    def _enhance_prompt(self, task_description: str) -> str:
        """
        Enhance the task description with engineering management context
        """
        project_info = get_project_info(self.working_directory)
        
        enhanced_prompt = f"""
You are an Engineering Manager agent working in the directory: {self.working_directory}

IMPORTANT CONTEXT:
- You coordinate frontend and backend development teams
- You do NOT write application code - only create specifications and instructions
- You ensure perfect alignment between frontend and backend implementations
- Current directory info: {project_info}

ENGINEERING MANAGEMENT RESPONSIBILITIES:
1. Read and analyze project specifications (SPEC.md)
2. Create detailed, precise instructions for frontend and backend teams
3. Ensure API contracts are perfectly aligned between layers
4. Specify exact ports, endpoints, and data models
5. Coordinate development workflow and integration points
6. Generate CLAUDE.md files with actionable, specific instructions
7. Validate that frontend API calls exactly match backend implementations

COORDINATION AREAS:
{', '.join(self.coordination_areas)}

CRITICAL REQUIREMENTS:
- Always read SPEC.md first to understand requirements
- Ensure frontend and backend use consistent ports (e.g., backend:8000, frontend:3001)
- API endpoints must match exactly between frontend calls and backend routes
- Data models must be identical across layers (TypeScript ↔ Pydantic)
- Authentication flows must be coordinated
- Error handling must use consistent formats
- CORS settings must allow frontend-backend communication

TASK TO COMPLETE:
{task_description}

Please read the project specification and create coordinated instructions that ensure 
frontend and backend implementations will work together seamlessly.

IMPORTANT: You should read files and write documentation, but NOT execute any bash commands 
or write application code. Your role is coordination and specification, not implementation.
"""
        return enhanced_prompt
    
    def coordinate_project(self, specification_file: str = "SPEC.md") -> Dict[str, Any]:
        """
        Main coordination method - reads specification and generates instructions for both teams
        
        Args:
            specification_file: Name of the specification file to read
            
        Returns:
            Dictionary containing coordination results
        """
        task = f"""
Read the project specification from {specification_file} and coordinate a full-stack development project.

STEP 1: Read and Analyze Specification
- Read the {specification_file} file in the current directory
- Understand the project requirements, features, and technical needs
- Identify what needs to be built for frontend and backend

STEP 2: Generate Frontend Instructions (frontend/CLAUDE.md)
Create detailed instructions for the frontend team including:
- Exact API endpoints to call (with full URLs including ports)
- Required data models and TypeScript interfaces
- Component specifications and user interface requirements
- Authentication and state management requirements
- Specific port configuration for development server
- Integration points with backend services

STEP 3: Generate Backend Instructions (backend/CLAUDE.md)
Create detailed instructions for the backend team including:
- Exact API endpoints to implement (matching frontend calls)
- Database models and schemas (matching frontend data needs)
- Authentication and authorization implementation
- CORS configuration to allow frontend access
- Specific port configuration for API server
- Data validation and error handling specifications

STEP 4: Ensure Perfect Alignment
- API endpoint paths must match exactly between frontend and backend
- Data models must be consistent (same field names, types, validation)
- Port numbers must be coordinated (no conflicts)
- Authentication tokens and flows must align
- Error response formats must be consistent

Generate both CLAUDE.md files with precise, actionable instructions that will result 
in a perfectly coordinated full-stack application.
"""
        
        return self.execute_task(task)
    
    def validate_project_alignment(self) -> Dict[str, Any]:
        """
        Validate that frontend and backend instructions are properly aligned
        
        Returns:
            Dictionary containing validation results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Validate that the frontend and backend instructions are properly coordinated by:

1. Reading both frontend/CLAUDE.md and backend/CLAUDE.md files
2. Checking API endpoint alignment:
   - Frontend API calls match backend endpoint implementations
   - HTTP methods are consistent
   - Request/response data formats match
3. Verifying port configuration:
   - No port conflicts
   - CORS settings allow frontend-backend communication
4. Validating data model consistency:
   - Same field names and types
   - Consistent validation rules
5. Checking authentication alignment:
   - Token formats match
   - Auth flows are coordinated

Current project files:
{files_context}

Generate a validation report showing:
- What is properly aligned
- Any mismatches or issues found
- Specific fixes needed for perfect coordination
- Overall readiness score for development teams

If issues are found, update the CLAUDE.md files to fix alignment problems.
"""
        
        return self.execute_task(task)
    
    def get_specialized_status(self) -> Dict[str, Any]:
        """Get engineering management specific status information"""
        base_status = self.get_status()
        project_info = get_project_info(self.working_directory)
        
        base_status.update({
            'coordination_areas': self.coordination_areas,
            'project_info': project_info,
            'has_spec': 'SPEC.md' in self._get_created_files(),
            'has_frontend_instructions': 'frontend/CLAUDE.md' in self._get_created_files(),
            'has_backend_instructions': 'backend/CLAUDE.md' in self._get_created_files(),
            'role': 'Coordination and Specification (No Code Implementation)'
        })
        
        return base_status