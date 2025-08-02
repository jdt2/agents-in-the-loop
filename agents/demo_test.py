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

from agents import FrontendEngineer


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


def demo_react_todo_app():
    """Demo: Create a React Todo App"""
    print_separator("Demo 1: React Todo App")
    
    # Create agent instance pointing to project/frontend directory
    frontend_dir = os.path.join(os.path.dirname(current_dir), 'project', 'frontend')
    agent = FrontendEngineer(frontend_dir)
    
    print(f"🤖 Agent Type: {agent.get_agent_type()}")
    print(f"📂 Working Directory: {agent.working_directory}")
    
    # Test 1: Create a React Todo App
    task = "Create a modern React TypeScript todo application with the following features: add/remove/edit todos, mark as complete, filter by status (all/active/completed), local storage persistence, and clean Material-UI or Tailwind styling."
    
    print(f"\n🚀 Executing task...")
    result = agent.execute_task(task)
    print_result(result, "React Todo App Creation")
    
    return agent, result


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


def main():
    """Main demo function"""
    print_separator("Frontend Engineer Agent Demo")
    print("This demo will test various capabilities of the Frontend Engineer agent.")
    print("Each demo creates projects in different subdirectories of the 'project/frontend' folder.")
    print("\nNote: Make sure you have ANTHROPIC_API_KEY set in your environment.")
    
    # Check if API key is available
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ERROR: ANTHROPIC_API_KEY environment variable is not set!")
        print("Please set your API key and try again.")
        return
    
    print(f"\n⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Demo 1: React Todo App
        demo_react_todo_app()
        
        # Ask user if they want to continue
        print("\n" + "="*60)
        response = input("Continue with more demos? (y/n): ").lower().strip()
        if response != 'y':
            print("Demo completed!")
            return
        
        # Demo 2: Component Library
        demo_component_library()
        
        # Ask user if they want to continue
        print("\n" + "="*60)
        response = input("Continue with dashboard demo? (y/n): ").lower().strip()
        if response != 'y':
            print("Demo completed!")
            return
        
        # Demo 3: Dashboard App
        demo_dashboard_app()
        
        # Demo 4: Agent Status
        demo_agent_status()
        
        print_separator("Demo Complete")
        print("✅ All demos completed successfully!")
        print("Check the 'project/frontend' directory for the generated projects.")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()