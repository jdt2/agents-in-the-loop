#!/usr/bin/env python3
"""
Demo script for testing the Product Manager agent
"""

import asyncio
import sys
import os

# Add the parent directory to the path so we can import our agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.product_manager import ProductManager


async def demo_product_manager():
    """Demo the Product Manager agent with a sample user request"""
    
    print("🎯 Product Manager Agent Demo")
    print("=" * 50)
    
    # Initialize the Product Manager agent
    print("📋 Initializing Product Manager agent...")
    pm = ProductManager(project_directory="project", max_turns=20)
    
    print(f"Agent: {pm.get_agent_type()}")
    print(f"Working Directory: {pm.working_directory}")
    print()
    
    # Sample user request
    user_request = """
    I need a social media management platform where businesses can:
    - Schedule posts across multiple platforms (Twitter, Instagram, LinkedIn)
    - Monitor engagement metrics and analytics
    - Collaborate with team members on content creation
    - Generate AI-powered content suggestions
    - Track competitor performance
    
    The platform should be user-friendly, scalable, and support both individual creators and enterprise teams.
    """
    
    print("🚀 Sample User Request:")
    print("-" * 30)
    print(user_request.strip())
    print()
    
    # Create specification
    print("📝 Creating project specification...")
    print("This will generate a comprehensive SPEC.md file...")
    print()
    
    try:
        # Execute the specification creation
        result = pm.create_specification(user_request)
        
        print("✅ Specification Creation Results:")
        print("-" * 40)
        
        if result.get('success'):
            print("✅ SPEC.md created successfully!")
            
            # Get status information
            status = pm.get_specialized_status()
            print(f"📁 Working Directory: {status['working_directory']}")
            print(f"📄 Has SPEC.md: {status['has_spec']}")
            print(f"📋 Analysis Areas: {', '.join(status['analysis_areas'])}")
            print()
            
            # Show files created
            created_files = pm._get_created_files()
            if created_files:
                print("📂 Files Created/Modified:")
                for file in created_files:
                    print(f"  - {file}")
            print()
            
            # Validate the specification
            print("🔍 Validating specification...")
            validation_result = pm.validate_specification()
            
            if validation_result.get('success'):
                print("✅ Specification validation completed!")
            else:
                print(f"❌ Validation failed: {validation_result.get('error', 'Unknown error')}")
                
        else:
            print(f"❌ Specification creation failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    print()
    print("🎯 Product Manager Demo Complete!")
    print("Check the project/SPEC.md file to see the generated specification.")


def run_demo():
    """Run the demo in an async context"""
    asyncio.run(demo_product_manager())


if __name__ == "__main__":
    run_demo()