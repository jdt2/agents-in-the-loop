#!/usr/bin/env python3
"""
Demo script to test the Frontend Engineer agent

This script demonstrates various capabilities of the Frontend Engineer agent
by running different tasks and showing the results.
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict, Any

# Add the parent directory to sys.path so we can import the agents
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from agents import FrontendEngineer, BackendEngineer


def print_separator(title: str = ""):
    """Print a visual separator with optional title"""
    if title:
        print(f"\n{'='*60}")
        print(f" {title}")
        print(f"{'='*60}")
    else:
        print(f"{'='*60}")


def print_result(result: Dict[str, Any], task_name: str):
    """Print the result of a task execution"""
    print(f"\n🔍 Task: {task_name}")
    print(f"✅ Success: {result.get('success', False)}")
    
    if result.get('success'):
        print(f"📁 Working Directory: {result.get('working_directory', 'N/A')}")
        print(f"🆔 Session ID: {result.get('session_id', 'N/A')}")
        
        files = result.get('files_created', [])
        if files:
            print(f"📄 Files Created ({len(files)}):")
            for file in sorted(files)[:10]:  # Show first 10 files
                print(f"   - {file}")
            if len(files) > 10:
                print(f"   ... and {len(files) - 10} more files")
        else:
            print("📄 No files were created")
            
        # Show first few messages from Claude Code SDK
        messages = result.get('messages', [])
        if messages:
            print(f"💬 SDK Messages: {len(messages)} total")
            # Note: In practice, you might want to parse and display these messages
            # For demo purposes, we'll just show the count
    else:
        print(f"❌ Error: {result.get('error', 'Unknown error')}")


def demo_fullstack_todo_app():
    """Demo: Create a Full-Stack Todo App (Frontend + Backend)"""
    print_separator("Full-Stack Todo App Demo")
    print("Creating a complete todo application with React frontend and FastAPI backend...")
    
    # Step 1: Create Frontend (React Todo App)
    print_separator("Step 1: Frontend (React Todo App)")
    frontend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'frontend')
    frontend_agent = FrontendEngineer(frontend_dir)
    
    print(f"🤖 Frontend Agent: {frontend_agent.get_agent_type()}")
    print(f"📂 Frontend Directory: {frontend_agent.working_directory}")
    
    frontend_task = "Create a modern React TypeScript todo application with the following features: add/remove/edit todos, mark as complete, filter by status (all/active/completed), API integration for backend communication, and clean Tailwind CSS styling. Include API service layer for HTTP requests."
    
    print(f"\n🚀 Creating frontend...")
    frontend_result = frontend_agent.execute_task(frontend_task)
    print_result(frontend_result, "React Frontend Creation")
    
    # Step 2: Create Backend (FastAPI Todo API)
    print_separator("Step 2: Backend (FastAPI Todo API)")
    backend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'backend')
    backend_agent = BackendEngineer(backend_dir)
    
    print(f"🤖 Backend Agent: {backend_agent.get_agent_type()}")
    print(f"📂 Backend Directory: {backend_agent.working_directory}")
    
    backend_task = "Create a FastAPI REST API for a todo application with the following features: CRUD operations for todos (create, read, update, delete), SQLite database with SQLAlchemy ORM, CORS middleware for frontend integration, input validation with Pydantic models, proper error handling, and API documentation. Include endpoints: GET /todos, POST /todos, PUT /todos/{id}, DELETE /todos/{id}."
    
    print(f"\n🚀 Creating backend...")
    backend_result = backend_agent.execute_task(backend_task)
    print_result(backend_result, "FastAPI Backend Creation")
    
    # Step 3: Test Frontend Implementation
    print_separator("Step 3: Testing Frontend Implementation")
    print("🧪 Installing dependencies and validating frontend...")
    frontend_test_result = frontend_agent.test_implementation()
    print_result(frontend_test_result, "Frontend Implementation Test")
    
    # Step 4: Test Backend Implementation
    print_separator("Step 4: Testing Backend Implementation")
    print("🧪 Installing dependencies and validating backend...")
    backend_test_result = backend_agent.test_implementation()
    print_result(backend_test_result, "Backend Implementation Test")
    
    # Summary
    print_separator("Full-Stack Todo App Summary")
    print("✅ Complete todo application created and tested!")
    print(f"📁 Frontend: {frontend_dir}")
    print(f"📁 Backend: {backend_dir}")
    
    # Show test results summary
    frontend_success = frontend_test_result.get('success', False)
    backend_success = backend_test_result.get('success', False)
    
    print(f"\n🧪 Test Results:")
    print(f"   Frontend Tests: {'✅ PASSED' if frontend_success else '❌ FAILED'}")
    print(f"   Backend Tests: {'✅ PASSED' if backend_success else '❌ FAILED'}")
    
    if frontend_success and backend_success:
        print("\n🎯 Ready to Run:")
        print("   1. Navigate to backend directory and start the FastAPI server")
        print("   2. Navigate to frontend directory and start the React development server")
        print("   3. The frontend will communicate with the backend API")
    else:
        print("\n⚠️  Some tests failed. Check the detailed output above for issues to resolve.")
    
    return {
        'frontend': {'agent': frontend_agent, 'result': frontend_result, 'test_result': frontend_test_result},
        'backend': {'agent': backend_agent, 'result': backend_result, 'test_result': backend_test_result}
    }


def demo_component_library():
    """Demo: Create a Component Library"""
    print_separator("Demo 2: Component Library")
    
    # Create a new agent instance with a different directory
    components_dir = os.path.join(os.path.dirname(current_dir), 'project', 'frontend', 'component-library')
    agent = FrontendEngineer(components_dir)
    
    print(f"🤖 Agent Type: {agent.get_agent_type()}")
    print(f"📂 Working Directory: {agent.working_directory}")
    
    # Test 2: Create a component library
    result = agent.create_component_library("my-ui-components")
    print_result(result, "Component Library Creation")
    
    return agent, result


def demo_dashboard_app():
    """Demo: Create a Dashboard"""
    print_separator("Demo 3: Admin Dashboard")
    
    # Create a new agent instance
    dashboard_dir = os.path.join(os.path.dirname(current_dir), 'project', 'frontend', 'admin-dashboard')
    agent = FrontendEngineer(dashboard_dir)
    
    print(f"🤖 Agent Type: {agent.get_agent_type()}")
    print(f"📂 Working Directory: {agent.working_directory}")
    
    # Test 3: Create an admin dashboard
    result = agent.create_dashboard_app("admin")
    print_result(result, "Admin Dashboard Creation")
    
    return agent, result


def demo_agent_status():
    """Demo: Show agent status"""
    print_separator("Demo 4: Agent Status")
    
    frontend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'frontend')
    agent = FrontendEngineer(frontend_dir)
    
    status = agent.get_specialized_status()
    
    print("📊 Agent Status:")
    print(f"   Agent Type: {status.get('agent_type')}")
    print(f"   Session ID: {status.get('session_id')}")
    print(f"   Working Directory: {status.get('working_directory')}")
    print(f"   Max Turns: {status.get('max_turns')}")
    print(f"   Conversations: {status.get('conversation_count')}")
    print(f"   Files in Directory: {status.get('files_in_directory')}")
    print(f"   Has package.json: {status.get('has_package_json')}")
    print(f"   Has README: {status.get('has_readme')}")
    print(f"   Supported Frameworks: {', '.join(status.get('supported_frameworks', []))}")


def demo_backend_api():
    """Demo: Create a Backend API"""
    print_separator("Demo: Backend API")
    
    # Create agent instance pointing to project/backend directory
    backend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'backend')
    agent = BackendEngineer(backend_dir)
    
    print(f"🤖 Agent Type: {agent.get_agent_type()}")
    print(f"📂 Working Directory: {agent.working_directory}")
    
    # Test: Create a FastAPI server with authentication
    result = agent.create_api_server("fastapi", "todo-api", include_auth=True)
    print_result(result, "FastAPI Server with Authentication")
    
    return agent, result


def demo_backend_microservice():
    """Demo: Create a Microservice"""
    print_separator("Demo: Backend Microservice")
    
    # Create a new agent instance with a different directory
    microservice_dir = os.path.join(os.path.dirname(current_dir), 'project', 'backend', 'user-microservice')
    agent = BackendEngineer(microservice_dir)
    
    print(f"🤖 Agent Type: {agent.get_agent_type()}")
    print(f"📂 Working Directory: {agent.working_directory}")
    
    # Test: Create a microservice
    result = agent.create_microservice("user-service", "fastapi")
    print_result(result, "User Microservice Creation")
    
    return agent, result


def demo_backend_status():
    """Demo: Show backend agent status"""
    print_separator("Demo: Backend Agent Status")
    
    backend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'backend')
    agent = BackendEngineer(backend_dir)
    
    status = agent.get_specialized_status()
    
    print("📊 Backend Agent Status:")
    print(f"   Agent Type: {status.get('agent_type')}")
    print(f"   Session ID: {status.get('session_id')}")
    print(f"   Working Directory: {status.get('working_directory')}")
    print(f"   Max Turns: {status.get('max_turns')}")
    print(f"   Conversations: {status.get('conversation_count')}")
    print(f"   Files in Directory: {status.get('files_in_directory')}")
    print(f"   Has Requirements: {status.get('has_requirements')}")
    print(f"   Has Dockerfile: {status.get('has_dockerfile')}")
    print(f"   Has Tests: {status.get('has_tests')}")
    print(f"   Supported Frameworks: {', '.join(status.get('supported_frameworks', [])[:5])}...")
    print(f"   Supported Databases: {', '.join(status.get('supported_databases', []))}")


def main():
    """Main demo function"""
    print_separator("Agents Demo - Full-Stack Todo App")
    print("This demo creates a complete todo application with React frontend and FastAPI backend.")
    print("Both agents work together to create a full-stack application.")
    print("\nNote: Make sure you have ANTHROPIC_API_KEY set in your environment.")
    
    # Check if API key is available
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERROR: ANTHROPIC_API_KEY environment variable is not set!")
        print("Please set your API key and try again.")
        return
    
    print(f"\n⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Default to full-stack todo app demo
        print("\n🎯 Creating a full-stack todo application...")
        print("This will demonstrate both Frontend and Backend Engineer agents working together.")
        
        # Ask user if they want to continue
        response = input("\nProceed with full-stack todo app demo? (y/n): ").lower().strip()
        if response != 'y':
            print("Demo cancelled.")
            return
        
        # Run the main demo
        demo_result = demo_fullstack_todo_app()
        
        # Ask if they want to see more demos
        print("\n" + "="*60)
        response = input("Would you like to see additional demos? (y/n): ").lower().strip()
        if response == 'y':
            print("\nAdditional demo options:")
            print("1. Frontend component library")
            print("2. Frontend dashboard")
            print("3. Backend microservice")
            print("4. Agent status info")
            
            choice = input("Enter choice (1-4): ").strip()
            
            if choice == '1':
                demo_component_library()
            elif choice == '2':
                demo_dashboard_app()
            elif choice == '3':
                demo_backend_microservice()
            elif choice == '4':
                demo_agent_status()
                demo_backend_status()
        
        print_separator("Demo Complete")
        print("✅ All demos completed successfully!")
        print("Check the 'project/' directory for the generated full-stack todo application.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()