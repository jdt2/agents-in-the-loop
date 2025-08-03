#!/usr/bin/env python3
"""
Master Workflow - Orchestrates all agents sequentially to build complete applications

This workflow takes a user request and runs through all development agents in sequence:
1. ProductManager - Creates SPEC.md from user request
2. EngineeringManager - Creates CLAUDE.md instructions from SPEC.md
3. FrontendEngineer - Builds React app following instructions
4. BackendEngineer - Builds API server following instructions  
5. TestingEngineer - Tests complete application end-to-end

Usage:
    workflow = MasterWorkflow()
    result = workflow.run_full_workflow("Build a todo application with authentication")
"""

import os
import sys
import time
import json
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path

# Add the current directory to sys.path so we can import agents
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from agents import (
    ProductManager, 
    EngineeringManager, 
    FrontendEngineer, 
    BackendEngineer, 
    TestingEngineer
)


class MasterWorkflow:
    """
    Master workflow orchestrator that runs all development agents sequentially
    to build complete applications from user requests
    """
    
    def __init__(self, project_directory: str = "project", verbose: bool = True):
        """
        Initialize the master workflow
        
        Args:
            project_directory: Base directory for the project
            verbose: Enable detailed progress output
        """
        self.project_directory = project_directory
        self.verbose = verbose
        self.start_time = None
        self.workflow_id = f"workflow_{int(time.time())}"
        
        # Initialize all agents
        self.product_manager = ProductManager(project_directory)
        self.engineering_manager = EngineeringManager(project_directory)
        self.frontend_engineer = FrontendEngineer(os.path.join(project_directory, "frontend"))
        self.backend_engineer = BackendEngineer(os.path.join(project_directory, "backend"))
        self.testing_engineer = TestingEngineer(os.path.join(project_directory, "testing"))
        
        # Track results from each step
        self.step_results = {}
        self.workflow_status = "initialized"
        
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp if verbose mode is enabled"""
        if self.verbose:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {message}")
    
    def print_separator(self, title: str = "", char: str = "=", width: int = 80):
        """Print a visual separator with optional title"""
        if self.verbose:
            if title:
                print(f"\n{char * width}")
                print(f" {title}")
                print(f"{char * width}")
            else:
                print(f"{char * width}")
    
    def print_step_header(self, step_num: int, total_steps: int, title: str, agent_type: str):
        """Print a formatted step header"""
        if self.verbose:
            self.print_separator(f"Step {step_num}/{total_steps}: {title} ({agent_type})")
            self.log(f"Starting {title}...")
    
    def print_step_result(self, step_name: str, result: Dict[str, Any], duration: float):
        """Print formatted step results"""
        if not self.verbose:
            return
            
        success = result.get('success', False)
        status_icon = "✅" if success else "❌"
        
        print(f"\n{status_icon} {step_name} {'COMPLETED' if success else 'FAILED'} ({duration:.1f}s)")
        
        if success:
            # Show key success metrics
            working_dir = result.get('working_directory', 'N/A')
            files_created = result.get('files_created', [])
            
            print(f"   📁 Working Directory: {working_dir}")
            if files_created:
                print(f"   📄 Files Created: {len(files_created)} files")
                # Show first few files
                for file in files_created[:3]:
                    print(f"      - {file}")
                if len(files_created) > 3:
                    print(f"      ... and {len(files_created) - 3} more files")
        else:
            error = result.get('error', 'Unknown error')
            print(f"   ❌ Error: {error}")
    
    def run_full_workflow(self, user_request: str) -> Dict[str, Any]:
        """
        Run the complete development workflow from user request to tested application
        
        Args:
            user_request: The user's description of what they want built
            
        Returns:
            Dictionary containing complete workflow results
        """
        self.start_time = time.time()
        self.workflow_status = "running"
        
        self.print_separator("🚀 MASTER WORKFLOW STARTED", "=", 80)
        self.log(f"Workflow ID: {self.workflow_id}")
        self.log(f"Project Directory: {self.project_directory}")
        self.log(f"User Request: {user_request}")
        
        try:
            # Step 1: Product Manager - Create SPEC.md
            step_1_result = self._run_product_manager_step(user_request)
            
            # Step 2: Engineering Manager - Create coordination instructions
            step_2_result = self._run_engineering_manager_step()
            
            # Step 3: Frontend Engineer - Build React application
            step_3_result = self._run_frontend_engineer_step()
            
            # Step 4: Backend Engineer - Build API server
            step_4_result = self._run_backend_engineer_step()
            
            # Step 5: Testing Engineer - Test complete application
            step_5_result = self._run_testing_engineer_step()
            
            # Generate final workflow summary
            workflow_result = self._generate_workflow_summary()
            
            self.workflow_status = "completed"
            self._print_final_summary(workflow_result)
            
            return workflow_result
            
        except Exception as e:
            self.workflow_status = "failed"
            self.log(f"Workflow failed with error: {str(e)}", "ERROR")
            
            return {
                'success': False,
                'workflow_id': self.workflow_id,
                'error': str(e),
                'status': self.workflow_status,
                'step_results': self.step_results,
                'duration': time.time() - self.start_time
            }
    
    def _run_product_manager_step(self, user_request: str) -> Dict[str, Any]:
        """Step 1: Product Manager creates SPEC.md"""
        step_start = time.time()
        self.print_step_header(1, 5, "Product Manager - Specification Creation", "ProductManager")
        
        try:
            self.log("Creating comprehensive project specification...")
            result = self.product_manager.create_specification(user_request)
            
            # Validate that SPEC.md was created
            spec_path = os.path.join(self.project_directory, "SPEC.md")
            if not os.path.exists(spec_path):
                result['success'] = False
                result['error'] = "SPEC.md file was not created"
            
            duration = time.time() - step_start
            self.step_results['product_manager'] = {
                'result': result,
                'duration': duration,
                'agent_type': 'ProductManager'
            }
            
            self.print_step_result("Product Manager", result, duration)
            return result
            
        except Exception as e:
            duration = time.time() - step_start
            error_result = {'success': False, 'error': str(e)}
            self.step_results['product_manager'] = {
                'result': error_result,
                'duration': duration,
                'agent_type': 'ProductManager'
            }
            self.print_step_result("Product Manager", error_result, duration)
            raise e
    
    def _run_engineering_manager_step(self) -> Dict[str, Any]:
        """Step 2: Engineering Manager creates coordination instructions"""
        step_start = time.time()
        self.print_step_header(2, 5, "Engineering Manager - Coordination", "EngineeringManager")
        
        try:
            self.log("Reading SPEC.md and creating team coordination instructions...")
            result = self.engineering_manager.coordinate_project("SPEC.md")
            
            # Validate that CLAUDE.md files were created
            frontend_claude = os.path.join(self.project_directory, "frontend", "CLAUDE.md")
            backend_claude = os.path.join(self.project_directory, "backend", "CLAUDE.md")
            
            if not os.path.exists(frontend_claude):
                result['success'] = False
                result['error'] = "Frontend CLAUDE.md file was not created"
            elif not os.path.exists(backend_claude):
                result['success'] = False
                result['error'] = "Backend CLAUDE.md file was not created"
            
            duration = time.time() - step_start
            self.step_results['engineering_manager'] = {
                'result': result,
                'duration': duration,
                'agent_type': 'EngineeringManager'
            }
            
            self.print_step_result("Engineering Manager", result, duration)
            return result
            
        except Exception as e:
            duration = time.time() - step_start
            error_result = {'success': False, 'error': str(e)}
            self.step_results['engineering_manager'] = {
                'result': error_result,
                'duration': duration,
                'agent_type': 'EngineeringManager'
            }
            self.print_step_result("Engineering Manager", error_result, duration)
            raise e
    
    def _run_frontend_engineer_step(self) -> Dict[str, Any]:
        """Step 3: Frontend Engineer builds React application"""
        step_start = time.time()
        self.print_step_header(3, 5, "Frontend Engineer - React Application", "FrontendEngineer")
        
        try:
            self.log("Building React TypeScript frontend following CLAUDE.md instructions...")
            
            # Execute frontend development task
            task = """Follow the detailed instructions in the CLAUDE.md file in this directory to create the frontend application. 
            Read the CLAUDE.md file first and implement exactly what is specified, including:
            - API endpoints and data models
            - Component architecture
            - Port configuration (3001)
            - Integration with backend
            Create a complete, production-ready frontend application."""
            
            result = self.frontend_engineer.execute_task(task)
            
            duration = time.time() - step_start
            self.step_results['frontend_engineer'] = {
                'result': result,
                'duration': duration,
                'agent_type': 'FrontendEngineer'
            }
            
            self.print_step_result("Frontend Engineer", result, duration)
            
            # If successful, run implementation test
            if result.get('success'):
                self.log("Testing frontend implementation...")
                test_result = self.frontend_engineer.test_implementation()
                self.step_results['frontend_engineer']['test_result'] = test_result
                
                test_success = test_result.get('success', False)
                self.log(f"Frontend testing {'PASSED' if test_success else 'FAILED'}")
            
            return result
            
        except Exception as e:
            duration = time.time() - step_start
            error_result = {'success': False, 'error': str(e)}
            self.step_results['frontend_engineer'] = {
                'result': error_result,
                'duration': duration,
                'agent_type': 'FrontendEngineer'
            }
            self.print_step_result("Frontend Engineer", error_result, duration)
            raise e
    
    def _run_backend_engineer_step(self) -> Dict[str, Any]:
        """Step 4: Backend Engineer builds API server"""
        step_start = time.time()
        self.print_step_header(4, 5, "Backend Engineer - API Server", "BackendEngineer")
        
        try:
            self.log("Building FastAPI Python backend following CLAUDE.md instructions...")
            
            # Execute backend development task
            task = """Follow the detailed instructions in the CLAUDE.md file in this directory to create the backend application. 
            Read the CLAUDE.md file first and implement exactly what is specified, including:
            - API endpoints and data models
            - Database configuration
            - Port configuration (8000)
            - CORS settings for frontend (port 3001)
            Create a complete, production-ready backend API server."""
            
            result = self.backend_engineer.execute_task(task)
            
            duration = time.time() - step_start
            self.step_results['backend_engineer'] = {
                'result': result,
                'duration': duration,
                'agent_type': 'BackendEngineer'
            }
            
            self.print_step_result("Backend Engineer", result, duration)
            
            # If successful, run implementation test
            if result.get('success'):
                self.log("Testing backend implementation...")
                test_result = self.backend_engineer.test_implementation()
                self.step_results['backend_engineer']['test_result'] = test_result
                
                test_success = test_result.get('success', False)
                self.log(f"Backend testing {'PASSED' if test_success else 'FAILED'}")
            
            return result
            
        except Exception as e:
            duration = time.time() - step_start
            error_result = {'success': False, 'error': str(e)}
            self.step_results['backend_engineer'] = {
                'result': error_result,
                'duration': duration,
                'agent_type': 'BackendEngineer'
            }
            self.print_step_result("Backend Engineer", error_result, duration)
            raise e
    
    def _run_testing_engineer_step(self) -> Dict[str, Any]:
        """Step 5: Testing Engineer tests complete application"""
        step_start = time.time()
        self.print_step_header(5, 5, "Testing Engineer - End-to-End Testing", "TestingEngineer")
        
        try:
            self.log("Running comprehensive end-to-end testing with Playwright...")
            
            # Test the complete application
            frontend_url = "http://localhost:3001"
            test_prompt = """Test the complete full-stack application including:
            - Frontend functionality and user interface
            - Backend API endpoints and data flow
            - Integration between frontend and backend
            - User workflows and error handling
            - Responsive design and accessibility
            Provide detailed test results and identify any issues."""
            
            result = self.testing_engineer.test_web_application(frontend_url, test_prompt)
            
            duration = time.time() - step_start
            self.step_results['testing_engineer'] = {
                'result': result,
                'duration': duration,
                'agent_type': 'TestingEngineer'
            }
            
            self.print_step_result("Testing Engineer", result, duration)
            return result
            
        except Exception as e:
            duration = time.time() - step_start
            error_result = {'success': False, 'error': str(e)}
            self.step_results['testing_engineer'] = {
                'result': error_result,
                'duration': duration,
                'agent_type': 'TestingEngineer'
            }
            self.print_step_result("Testing Engineer", error_result, duration)
            # Don't raise for testing step - allow workflow to complete
            return error_result
    
    def _generate_workflow_summary(self) -> Dict[str, Any]:
        """Generate comprehensive workflow summary"""
        total_duration = time.time() - self.start_time
        
        # Count successes and failures
        step_successes = []
        step_failures = []
        
        for step_name, step_data in self.step_results.items():
            if step_data['result'].get('success', False):
                step_successes.append(step_name)
            else:
                step_failures.append(step_name)
        
        # Collect all created files
        all_files_created = []
        for step_data in self.step_results.values():
            files = step_data['result'].get('files_created', [])
            all_files_created.extend(files)
        
        # Overall success determination
        critical_steps = ['product_manager', 'engineering_manager', 'frontend_engineer', 'backend_engineer']
        critical_successes = [step for step in critical_steps if step in step_successes]
        overall_success = len(critical_successes) == len(critical_steps)
        
        return {
            'success': overall_success,
            'workflow_id': self.workflow_id,
            'status': self.workflow_status,
            'total_duration': total_duration,
            'step_results': self.step_results,
            'summary': {
                'total_steps': len(self.step_results),
                'successful_steps': len(step_successes),
                'failed_steps': len(step_failures),
                'successful_step_names': step_successes,
                'failed_step_names': step_failures,
                'files_created_count': len(all_files_created),
                'all_files_created': all_files_created
            },
            'project_directory': self.project_directory,
            'agents_used': {
                'product_manager': self.product_manager.get_agent_type(),
                'engineering_manager': self.engineering_manager.get_agent_type(), 
                'frontend_engineer': self.frontend_engineer.get_agent_type(),
                'backend_engineer': self.backend_engineer.get_agent_type(),
                'testing_engineer': self.testing_engineer.get_agent_type()
            }
        }
    
    def _print_final_summary(self, workflow_result: Dict[str, Any]):
        """Print comprehensive final workflow summary"""
        if not self.verbose:
            return
            
        self.print_separator("🎯 WORKFLOW COMPLETE", "=", 80)
        
        success = workflow_result['success']
        duration = workflow_result['total_duration']
        summary = workflow_result['summary']
        
        status_icon = "✅" if success else "❌"
        print(f"\n{status_icon} OVERALL STATUS: {'SUCCESS' if success else 'PARTIAL SUCCESS'}")
        print(f"⏱️  Total Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
        print(f"📊 Steps: {summary['successful_steps']}/{summary['total_steps']} successful")
        print(f"📁 Project Directory: {workflow_result['project_directory']}")
        print(f"📄 Total Files Created: {summary['files_created_count']}")
        
        print(f"\n📋 STEP RESULTS:")
        for step_name, step_data in workflow_result['step_results'].items():
            step_success = step_data['result'].get('success', False)
            step_duration = step_data['duration']
            step_icon = "✅" if step_success else "❌"
            
            print(f"   {step_icon} {step_name.replace('_', ' ').title()}: "
                  f"{'PASSED' if step_success else 'FAILED'} ({step_duration:.1f}s)")
        
        if summary['successful_steps'] == summary['total_steps']:
            print(f"\n🎉 CONGRATULATIONS!")
            print(f"   Complete full-stack application successfully created and tested!")
            print(f"   🎨 Frontend: {self.project_directory}/frontend (port 3001)")
            print(f"   ⚙️  Backend: {self.project_directory}/backend (port 8000)")
            print(f"   🧪 Tests: {self.project_directory}/testing")
        elif summary['successful_steps'] >= 4:  # At least PM, EM, FE, BE
            print(f"\n🎯 DEVELOPMENT COMPLETE!")
            print(f"   Core application created successfully!")
            print(f"   Note: Testing may have encountered issues but application is functional")
        else:
            print(f"\n⚠️  PARTIAL COMPLETION")
            print(f"   Some critical steps failed. Check detailed logs above.")
            if summary['failed_step_names']:
                print(f"   Failed steps: {', '.join(summary['failed_step_names'])}")


def main():
    """Demo function to test the master workflow"""
    print("🚀 Master Workflow Demo")
    print("=" * 60)
    print("This will run the complete development pipeline:")
    print("PM → EM → Frontend → Backend → Testing")
    print()
    
    # Check if API key is available
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable is not set!")
        print("Please set your API key and try again.")
        return
    
    # Sample user request
    sample_request = """
    Build a personal finance tracker application where users can:
    - Add and categorize income and expenses
    - View spending analytics with charts and graphs
    - Set monthly budgets and track progress
    - Generate financial reports
    - Import transactions from bank CSV files
    
    The app should be modern, responsive, and easy to use on both desktop and mobile.
    """
    
    print("📝 Sample User Request:")
    print("-" * 40)
    print(sample_request.strip())
    print()
    
    # Ask user if they want to proceed
    response = input("Run the complete workflow with this request? (y/n): ").lower().strip()
    if response != 'y':
        print("Demo cancelled.")
        return
    
    # Run the master workflow
    workflow = MasterWorkflow(verbose=True)
    result = workflow.run_full_workflow(sample_request)
    
    # Save results to file
    results_file = f"workflow_results_{workflow.workflow_id}.json"
    with open(results_file, 'w') as f:
        # Convert any non-serializable objects to strings
        serializable_result = json.loads(json.dumps(result, default=str))
        json.dump(serializable_result, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: {results_file}")


if __name__ == "__main__":
    main()