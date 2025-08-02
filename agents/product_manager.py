"""
Product Manager Agent - Creates project specifications from user requests
"""

from typing import Dict, Any, Optional
from claude_code_sdk import ClaudeCodeOptions
from .base_agent import BaseAgent
from .utils import get_project_info, format_file_list


class ProductManager(BaseAgent):
    """
    Product Manager agent that creates comprehensive project specifications
    Takes user requests and generates detailed SPEC.md files
    Does not write application code - only creates specifications and requirements
    """
    
    def __init__(self, project_directory: str = "project", max_turns: int = 50):
        """
        Initialize the Product Manager agent
        
        Args:
            project_directory: Directory where SPEC.md will be created/updated
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(project_directory, max_turns)
        self.agent_name = "Product Manager"
        self.analysis_areas = [
            "Problem Analysis", "User Stories", "Requirements", "Technical Architecture",
            "Data Models", "User Experience", "Quality Requirements", "Success Criteria"
        ]
    
    def get_agent_type(self) -> str:
        """Return the type/name of this agent"""
        return "Product Manager"
    
    async def query_claude_code_sdk(self, prompt: str, options: Optional[ClaudeCodeOptions] = None) -> list:
        """
        Override to restrict tool access - no bash commands allowed
        Product Manager should only read existing specs and write documentation
        """
        if options is None:
            options = ClaudeCodeOptions(
                max_turns=self.max_turns,
                allowed_tools=["read", "write", "edit", "grep", "glob"],  # No bash
                permission_mode="bypassPermissions"
            )
        
        return await super().query_claude_code_sdk(prompt, options)
    
    def _enhance_prompt(self, user_request: str) -> str:
        """
        Enhance the user request with Product Manager context and structured analysis
        """
        project_info = get_project_info(self.working_directory)
        
        enhanced_prompt = f"""
You are an experienced Product Manager at a tech company. A stakeholder has come to you with this request:

"{user_request}"

IMPORTANT CONTEXT:
- You are working in the directory: {self.working_directory}
- You create comprehensive project specifications (SPEC.md files)
- You do NOT write application code - only specifications and requirements
- Current directory info: {project_info}

PRODUCT MANAGER RESPONSIBILITIES:
1. Analyze stakeholder requests and translate them into technical specifications
2. Create detailed user stories with acceptance criteria
3. Define functional and non-functional requirements
4. Specify technical architecture and technology stack
5. Create comprehensive SPEC.md files for development teams
6. Ensure specifications are clear, actionable, and complete

ANALYSIS AREAS:
{', '.join(self.analysis_areas)}

Please analyze this request and create a comprehensive project specification in SPEC.md format. Structure your response as follows:

# [Project Name] Specification

## Project Overview
[Clear project description and goals]

## Core Features
[Detailed feature breakdown with user-facing capabilities]

## Technical Requirements

### Frontend Specifications
- **Framework**: [Recommended frontend technology]
- **Styling**: [Styling approach]
- **Build Tool**: [Build tool choice]
- **State Management**: [State management approach]
- **Development Port**: 3001

### Backend Specifications
- **Framework**: [Recommended backend technology]
- **Database**: [Database choice and rationale]
- **API Style**: [REST/GraphQL approach]
- **Development Port**: 8000

## API Specification
[Detailed API endpoints with request/response formats]

## Data Models
[Complete data model specifications with validation rules]

## User Experience Requirements
[UI/UX specifications and user interaction details]

## Quality Requirements
[Performance, accessibility, testing requirements]

## Success Criteria
[Measurable success metrics and acceptance criteria]

CRITICAL REQUIREMENTS:
- Use port 3001 for frontend development
- Use port 8000 for backend development
- Ensure frontend and backend specifications are aligned
- Include comprehensive API contracts
- Specify exact data models and validation rules
- Create specifications that engineering teams can implement directly

Please create a complete, implementable specification that covers all aspects needed for a development team to build this project successfully.
"""
        return enhanced_prompt
    
    def create_specification(self, user_request: str) -> Dict[str, Any]:
        """
        Main method to create project specification from user request
        
        Args:
            user_request: The stakeholder's project request
            
        Returns:
            Dictionary containing specification creation results
        """
        task = f"""
Create a comprehensive project specification based on the following user request.

USER REQUEST: {user_request}

STEP 1: Analyze the Request
- Understand the core problem and user needs
- Identify key features and capabilities required
- Determine technical complexity and scope

STEP 2: Create SPEC.md File
Create a detailed SPEC.md file in the current directory with the following structure:

### Required Sections:
1. **Project Overview** - Clear description of what will be built
2. **Core Features** - Detailed feature breakdown
3. **Technical Requirements** - Frontend and backend specifications
4. **API Specification** - Complete API contract with endpoints
5. **Data Models** - Database schemas and data structures
6. **User Experience Requirements** - UI/UX specifications
7. **Quality Requirements** - Performance, security, accessibility
8. **Success Criteria** - Measurable acceptance criteria

### Technical Standards:
- Frontend: React TypeScript on port 3001
- Backend: FastAPI Python on port 8000
- Database: Choose appropriate database for the use case
- API: RESTful design with JSON responses
- Styling: Modern, responsive design approach

STEP 3: Ensure Completeness
- All sections must be comprehensive and actionable
- Engineering teams should be able to implement directly from this spec
- Include specific technical details, not just high-level descriptions
- Specify exact ports, endpoints, data types, and validation rules

Create a specification that serves as the single source of truth for the entire development project.
"""
        
        return self.execute_task(task)
    
    def validate_specification(self) -> Dict[str, Any]:
        """
        Validate that the created specification is complete and actionable
        
        Returns:
            Dictionary containing validation results
        """
        existing_files = self._get_created_files()
        files_context = format_file_list(existing_files) if existing_files else "No existing files"
        
        task = f"""
Validate the project specification by checking for completeness and clarity:

1. Read the SPEC.md file in the current directory
2. Check that all required sections are present and detailed:
   - Project Overview (clear and comprehensive)
   - Core Features (specific and measurable)
   - Technical Requirements (complete frontend/backend specs)
   - API Specification (all endpoints with request/response formats)
   - Data Models (complete schemas with validation)
   - User Experience Requirements (actionable UI/UX specs)
   - Quality Requirements (measurable performance/security criteria)
   - Success Criteria (clear acceptance criteria)

3. Verify technical alignment:
   - Frontend port is 3001
   - Backend port is 8000
   - API endpoints are well-defined
   - Data models are consistent
   - Technology choices are appropriate

4. Check for engineering readiness:
   - Specifications are detailed enough for implementation
   - No ambiguous requirements
   - All dependencies are identified
   - Success criteria are measurable

Current project files:
{files_context}

Generate a validation report showing:
- What sections are complete and well-defined
- Any missing or incomplete sections
- Technical inconsistencies or issues
- Overall readiness score for development teams
- Specific recommendations for improvements

If issues are found, update the SPEC.md file to address them.
"""
        
        return self.execute_task(task)
    
    def get_specialized_status(self) -> Dict[str, Any]:
        """Get Product Manager specific status information"""
        base_status = self.get_status()
        project_info = get_project_info(self.working_directory)
        
        base_status.update({
            'analysis_areas': self.analysis_areas,
            'project_info': project_info,
            'has_spec': 'SPEC.md' in self._get_created_files(),
            'spec_file_path': f"{self.working_directory}/SPEC.md",
            'role': 'Specification Creation (No Code Implementation)'
        })
        
        return base_status