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
    
    def __init__(self, frontend_directory: str = "project/frontend", max_turns: int = 30):
        """
        Initialize the Frontend Engineer agent
        
        Args:
            frontend_directory: Directory where frontend projects will be created
            max_turns: Maximum number of turns for Claude Code SDK interactions
        """
        super().__init__(frontend_directory, max_turns)
        self.agent_name = "Frontend Engineer"
        self.supported_frameworks = [
            "React", "Vue.js", "Angular", "Svelte", "Next.js", "Nuxt.js", 
            "Vanilla JavaScript", "TypeScript", "Vite"
        ]
    
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
    
    def create_react_app(self, app_name: str = "react-app", use_typescript: bool = True) -> Dict[str, Any]:
        """
        Create a React application
        
        Args:
            app_name: Name of the React app
            use_typescript: Whether to use TypeScript
            
        Returns:
            Dictionary containing task results
        """
        tech_stack = "React with TypeScript" if use_typescript else "React with JavaScript"
        task = f"Create a {tech_stack} application named '{app_name}' with modern best practices, Vite as build tool, and a sample component structure."
        
        return self.execute_task(task)
    
    def create_vue_app(self, app_name: str = "vue-app", use_typescript: bool = True) -> Dict[str, Any]:
        """
        Create a Vue.js application
        
        Args:
            app_name: Name of the Vue app
            use_typescript: Whether to use TypeScript
            
        Returns:
            Dictionary containing task results
        """
        tech_stack = "Vue.js 3 with TypeScript" if use_typescript else "Vue.js 3 with JavaScript"
        task = f"Create a {tech_stack} application named '{app_name}' with Composition API, Vite, and modern component structure."
        
        return self.execute_task(task)
    
    def create_component_library(self, library_name: str = "ui-components") -> Dict[str, Any]:
        """
        Create a reusable component library
        
        Args:
            library_name: Name of the component library
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a React TypeScript component library named '{library_name}' with Storybook, multiple reusable components (Button, Input, Card, Modal), proper TypeScript definitions, and build configuration for publishing."
        
        return self.execute_task(task)
    
    def create_dashboard_app(self, dashboard_type: str = "admin") -> Dict[str, Any]:
        """
        Create a dashboard application
        
        Args:
            dashboard_type: Type of dashboard (admin, analytics, user, etc.)
            
        Returns:
            Dictionary containing task results
        """
        task = f"Create a modern {dashboard_type} dashboard using React with TypeScript, including sidebar navigation, data tables, charts (using Chart.js or similar), responsive design, and sample data. Include routing and state management."
        
        return self.execute_task(task)
    
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