"""
Demo script for TestingEngineer agent - Browser Testing Focus
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from agents.testing_engineer import TestingEngineer


def main():
    """Test the TestingEngineer agent with browser testing scenarios"""
    
    # Create testing engineer instance
    testing_dir = Path.cwd() / "project" / "testing" / "browser_tests"
    engineer = TestingEngineer(str(testing_dir))
    
    print(f"Testing Engineer initialized in: {engineer.working_directory}")
    print(f"Agent type: {engineer.get_agent_type()}")
    print("-" * 50)
    
    # Test 1: Basic web application test
    print("\n1. Testing web application at localhost:3000...")
    result = engineer.test_web_application(
        url="http://localhost:3000",
        test_prompt="Test the main query form by entering 'Create fibonacci function' and submitting it"
    )
    
    if result['success']:
        print("✓ Web application testing completed successfully")
        print(f"  Files created: {len(result['files_created'])}")
        for file in result['files_created'][:5]:  # Show first 5 files
            print(f"    - {file}")
    else:
        print(f"✗ Web application testing failed: {result['error']}")
    

if __name__ == "__main__":
    # Check for API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Error: ANTHROPIC_API_KEY environment variable is required")
        print("Please set it in your .env file or environment")
        sys.exit(1)
    
    main()