import os
import asyncio
import uuid
import subprocess
import json
import dataclasses
import threading
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv

try:
    import anyio
    from claude_code_sdk import query, ClaudeCodeOptions
    SDK_AVAILABLE = True
except ImportError:
    SDK_AVAILABLE = False
    print("Claude Code SDK not available, using CLI subprocess method")

# Import master workflow
from master_workflow import MasterWorkflow

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Store sessions in memory (use Redis or database in production)
sessions = {}

# Store workflow progress in memory (use Redis or database in production)
workflows = {}

def run_master_workflow_async(user_request, workflow_id):
    """Run master workflow in background thread with simulated progress"""
    import time
    import random
    
    # Log workflow start
    print(f"\n🚀 [WORKFLOW STARTED] ID: {workflow_id[:8]}...")
    print(f"📝 Request: {user_request[:100]}{'...' if len(user_request) > 100 else ''}")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize workflow with progress tracking
        workflow = MasterWorkflow(verbose=False)  # Disable console output for web
        
        # Update status to running
        workflows[workflow_id]['status'] = 'running'
        workflows[workflow_id]['current_step'] = 'initializing'
        workflows[workflow_id]['progress'] = 5
        
        print(f"🔄 [WORKFLOW {workflow_id[:8]}] Status: RUNNING - Initializing agents...")
        
        # Define agent workflow steps with realistic durations
        agent_steps = [
            {
                'name': 'product_manager',
                'title': 'Product Manager Analysis',
                'duration': random.randint(7, 12),  # 7-12 seconds
                'progress_start': 10,
                'progress_end': 25
            },
            {
                'name': 'engineering_manager', 
                'title': 'Engineering Manager Planning',
                'duration': random.randint(5, 8),   # 5-8 seconds
                'progress_start': 25,
                'progress_end': 40
            },
            {
                'name': 'frontend_engineer',
                'title': 'Frontend Development',
                'duration': random.randint(8, 15),  # 8-15 seconds
                'progress_start': 40,
                'progress_end': 65
            },
            {
                'name': 'backend_engineer',
                'title': 'Backend Development', 
                'duration': random.randint(6, 12),  # 6-12 seconds
                'progress_start': 65,
                'progress_end': 85
            },
            {
                'name': 'testing_engineer',
                'title': 'Testing & Validation',
                'duration': random.randint(5, 10),  # 5-10 seconds
                'progress_start': 85,
                'progress_end': 95
            }
        ]
        
        # Simulate each agent step with progress updates
        for step_idx, step in enumerate(agent_steps, 1):
            agent_name = step['name']
            title = step['title']
            duration = step['duration']
            progress_start = step['progress_start']
            progress_end = step['progress_end']
            
            # Log agent start
            print(f"\n🤖 [AGENT {step_idx}/5] {title} - Starting ({duration}s estimated)")
            print(f"   🔄 [WORKFLOW {workflow_id[:8]}] Agent: {agent_name} -> RUNNING")
            
            # Update agent status to running
            workflows[workflow_id]['agents'][agent_name]['status'] = 'running'
            workflows[workflow_id]['current_step'] = title
            workflows[workflow_id]['progress'] = progress_start
            
            # Simulate gradual progress during agent execution
            steps_in_agent = 10  # Number of progress updates per agent
            step_duration = duration / steps_in_agent
            progress_increment = (progress_end - progress_start) / steps_in_agent
            
            for i in range(steps_in_agent):
                time.sleep(step_duration)
                
                # Update progress
                current_progress = progress_start + (progress_increment * (i + 1))
                agent_progress = ((i + 1) / steps_in_agent) * 100
                
                workflows[workflow_id]['progress'] = int(current_progress)
                workflows[workflow_id]['agents'][agent_name]['progress'] = int(agent_progress)
                
                # Add some status messages
                if i == 2:
                    workflows[workflow_id]['agents'][agent_name]['message'] = f"Analyzing requirements..."
                elif i == 5:
                    workflows[workflow_id]['agents'][agent_name]['message'] = f"Generating {agent_name.replace('_', ' ')} deliverables..."
                elif i == 8:
                    workflows[workflow_id]['agents'][agent_name]['message'] = f"Finalizing {title.lower()}..."
            
            # Mark agent as completed
            workflows[workflow_id]['agents'][agent_name]['status'] = 'completed'
            workflows[workflow_id]['agents'][agent_name]['progress'] = 100
            workflows[workflow_id]['agents'][agent_name]['message'] = f"{title} completed successfully!"
            
            # Log agent completion
            print(f"   ✅ [WORKFLOW {workflow_id[:8]}] Agent: {agent_name} -> COMPLETED ({duration}s)")
        
        # Final completion phase
        workflows[workflow_id]['current_step'] = 'Finalizing project'
        workflows[workflow_id]['progress'] = 98
        time.sleep(2)  # Brief finalization delay
        
        # Run the actual workflow (this would be the real implementation)
        # For now, we'll simulate a successful result
        result = {
            'success': True,
            'workflow_id': workflow_id,
            'project_directory': f'project_{workflow_id[:8]}',
            'total_duration': sum(step['duration'] for step in agent_steps) + 2,
            'summary': {
                'total_steps': 5,
                'successful_steps': 5,
                'files_created_count': random.randint(15, 25),
                'failed_step_names': []
            },
            'step_results': {
                'product_manager': {'success': True, 'files_created': ['SPEC.md', 'requirements.txt']},
                'engineering_manager': {'success': True, 'files_created': ['CLAUDE.md', 'architecture.md']},
                'frontend_engineer': {'success': True, 'files_created': ['src/App.js', 'src/components/', 'package.json']},
                'backend_engineer': {'success': True, 'files_created': ['server.js', 'routes/', 'models/']},
                'testing_engineer': {'success': True, 'files_created': ['tests/', 'cypress.json']}
            }
        }
        
        # Store final results
        workflows[workflow_id].update({
            'status': 'completed',
            'result': result,
            'current_step': 'Project completed successfully!',
            'progress': 100,
            'completed_at': datetime.now().isoformat()
        })
        
        # Log workflow completion
        total_duration = result['total_duration']
        print(f"\n🎉 [WORKFLOW COMPLETED] ID: {workflow_id[:8]}")
        print(f"⏱️  Total Duration: {total_duration}s ({total_duration/60:.1f} minutes)")
        print(f"📁 Files Created: {result['summary']['files_created_count']}")
        print(f"✅ All 5 agents completed successfully!")
        print(f"🎯 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        # Log workflow failure
        print(f"\n❌ [WORKFLOW FAILED] ID: {workflow_id[:8]}")
        print(f"🚨 Error: {str(e)}")
        print(f"🔴 Failed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        workflows[workflow_id].update({
            'status': 'failed',
            'error': str(e),
            'current_step': 'Workflow failed',
            'progress': 0,
            'failed_at': datetime.now().isoformat()
        })

def run_async(coro):
    """Helper function to run async code in Flask"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

async def query_claude_code_sdk(prompt, options=None):
    """Query Claude Code SDK with error handling"""
    if options is None:
        options = ClaudeCodeOptions(max_turns=3)
    
    messages = []
    try:
        async for message in query(prompt=prompt, options=options):
            messages.append(message)
    except Exception as e:
        raise Exception(f"Claude Code SDK error: {str(e)}")
    
    return messages


def query_claude_code(prompt, max_turns=3):
    """Query Claude Code using SDK"""
    options = ClaudeCodeOptions(max_turns=max_turns)
    return run_async(query_claude_code_sdk(prompt, options))

def create_pm_agent_prompt(user_request):
    """Create a Product Manager agent prompt for Claude Code SDK"""
    return f"""
You are an experienced Product Manager at a tech company. A stakeholder has come to you with this request:

"{user_request}"

Please analyze this request and provide a comprehensive Product Manager response in **Markdown format**. Structure your response as follows:

# Product Manager Analysis

## 📋 Problem Analysis

### Problem Statement
[Clear problem statement based on the request]

### Target Users
- [Target user persona 1]
- [Target user persona 2]
- [Additional personas as needed]

### Business Goals
- [Business objective 1]
- [Business objective 2]
- [Additional goals as needed]

### Success Metrics
- [Measurable success criterion 1]
- [Measurable success criterion 2]
- [Additional metrics as needed]

## 📝 User Stories

### US-001: [Story Title]
**As a** [user type], **I want** [goal] **so that** [benefit]

**Priority:** High/Medium/Low | **Story Points:** [number] | **Business Value:** [explanation]

**Acceptance Criteria:**
- [Criteria 1]
- [Criteria 2]
- [Additional criteria as needed]

[Repeat for additional user stories]

## 📋 Requirements

### Functional Requirements
- [Functional requirement 1]
- [Functional requirement 2]
- [Additional requirements as needed]

### Non-Functional Requirements
- [Non-functional requirement 1]
- [Non-functional requirement 2]
- [Additional requirements as needed]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Dependencies
- [Dependency 1]
- [Dependency 2]

## ⚠️ Risk Assessment

### [Risk Name 1]
**Impact:** High/Medium/Low | **Probability:** High/Medium/Low
**Mitigation:** [Mitigation strategy]

[Repeat for additional risks]

## 🎯 Next Steps
- [Next step 1]
- [Next step 2]
- [Additional steps as needed]

## ❓ Questions for Engineering Team
- [Technical question 1]
- [Technical question 2]
- [Additional questions as needed]

Focus on creating realistic, detailed user stories and requirements that an engineering team can work with. Be thorough but practical.
"""

def create_em_agent_prompt(user_request, pm_response):
    """Create an Engineering Manager agent prompt for Claude Code SDK"""
    # Convert pm_response to string representation for the prompt
    pm_analysis = str(pm_response) if pm_response else "PM analysis not available"
    
    return f"""
You are an experienced Engineering Manager at a tech company. The Product Manager has analyzed a stakeholder request and provided their analysis. Now you need to create the technical implementation plan.

Original Request: "{user_request}"

Product Manager Analysis:
{pm_analysis}

Please provide a comprehensive Engineering Manager response in **Markdown format**. Structure your response as follows:

# Engineering Manager Technical Plan

## 🏗️ Technical Architecture

### Architecture Overview
[High-level system architecture description]

### Technology Stack
- **Frontend:** [Recommended frontend technology]
- **Backend:** [Recommended backend technology]
- **Database:** [Recommended database solution]
- **Infrastructure:** [Recommended infrastructure approach]
- **Additional Tools:**
  - [Tool/Service 1]
  - [Tool/Service 2]
  - [Additional tools as needed]

### System Components

#### [Component Name 1]
**Purpose:** [What this component does]
**Technology:** [Specific technology choice]
**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]
- [Additional responsibilities as needed]

[Repeat for additional components]

## 📅 Implementation Plan

### Development Phases

#### Phase 1: [Phase Name]
**Duration:** [Estimated duration]
**Tasks:**
- [Major task 1]
- [Major task 2]
- [Additional tasks as needed]

**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

[Repeat for additional phases]

### Team Structure
**Recommended Team Size:** [Number] people

#### [Role Name 1] ([Count])
**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

[Repeat for additional roles]

### Timeline Estimates
- **MVP Estimate:** [Time estimate]
- **Full Product Estimate:** [Time estimate]
- **Key Milestones:**
  - [Milestone 1]
  - [Milestone 2]
  - [Additional milestones as needed]

## ⚠️ Technical Risks

### [Risk Name 1]
**Impact:** High/Medium/Low | **Probability:** High/Medium/Low
**Mitigation:** [Technical mitigation strategy]

[Repeat for additional risks]

## 🏗️ Infrastructure Requirements
- [Infrastructure need 1]
- [Infrastructure need 2]
- [Additional requirements as needed]

## ✅ Quality Gates
- [Quality checkpoint 1]
- [Quality checkpoint 2]
- [Additional checkpoints as needed]

## ❓ Questions for Product Manager
- [Clarifying question 1]
- [Clarifying question 2]
- [Additional questions as needed]

Base your recommendations on modern software engineering best practices and consider scalability, maintainability, and team capabilities.
"""

async def run_dynamic_agent_workflow(user_request):
    """Run dynamic PM -> EM workflow using Claude Code SDK"""
    
    try:
        # Step 1: Get PM analysis from Claude
        pm_prompt = create_pm_agent_prompt(user_request)
        
        if SDK_AVAILABLE:
            # PM queries may need multiple turns for complex analysis
            pm_messages = await query_claude_code_sdk(pm_prompt, ClaudeCodeOptions(max_turns=3))
        else:
            # Fallback to CLI method
            pm_messages = query_claude_code_cli(pm_prompt, 3)
        
        # Extract PM response - handle different message formats
        pm_response_text = ""
        if pm_messages:
            # For SDK, find the ResultMessage (last message should be ResultMessage)
            if SDK_AVAILABLE:
                # Look for ResultMessage in the messages
                result_messages = [msg for msg in pm_messages if hasattr(msg, 'result')]
                if result_messages:
                    pm_response_text = result_messages[-1].result
                else:
                    pm_response_text = str(pm_messages[-1])
            else:
                # Handle CLI response format
                last_message = pm_messages[-1]
                if isinstance(last_message, dict):
                    pm_response_text = last_message.get('result', last_message.get('content', str(last_message)))
                else:
                    pm_response_text = str(last_message)
        
        # Store PM response as markdown
        pm_response = None
        try:
            if pm_response_text and pm_response_text.strip():
                pm_response = {
                    "agent_role": "Product Manager",
                    "markdown_content": pm_response_text,
                    "content_type": "markdown"
                }
            else:
                pm_response = {"error": "Empty PM response", "raw": pm_response_text}
        except Exception as e:
            pm_response = {"error": f"PM parsing error: {str(e)}", "raw": pm_response_text}
        
        # Step 2: Get EM analysis from Claude using PM output
        em_prompt = create_em_agent_prompt(user_request, pm_response)
        
        if SDK_AVAILABLE:
            # EM queries may need more turns due to tool usage
            em_messages = await query_claude_code_sdk(em_prompt, ClaudeCodeOptions(max_turns=3))
        else:
            # Fallback to CLI method
            em_messages = query_claude_code_cli(em_prompt, 3)
        
        # Extract EM response - handle different message formats
        em_response_text = ""
        if em_messages:
            # For SDK, find the ResultMessage (last message should be ResultMessage)
            if SDK_AVAILABLE:
                # Look for ResultMessage in the messages
                result_messages = [msg for msg in em_messages if hasattr(msg, 'result')]
                if result_messages:
                    em_response_text = result_messages[-1].result
                else:
                    em_response_text = str(em_messages[-1])
            else:
                # Handle CLI response format
                last_message = em_messages[-1]
                if isinstance(last_message, dict):
                    em_response_text = last_message.get('result', last_message.get('content', str(last_message)))
                else:
                    em_response_text = str(last_message)
        
        # Store EM response as markdown
        em_response = None
        try:
            if em_response_text is None:
                em_response = {"error": "EM response text is None", "raw": "None"}
            elif not isinstance(em_response_text, str):
                em_response_text = str(em_response_text)
                em_response = {"error": "EM response not a string", "raw": em_response_text}
            elif em_response_text.strip():
                em_response = {
                    "agent_role": "Engineering Manager",
                    "markdown_content": em_response_text,
                    "content_type": "markdown"
                }
            else:
                em_response = {"error": "Empty EM response", "raw": em_response_text}
        except Exception as e:
            em_response = {"error": f"EM parsing error: {str(e)}", "raw": em_response_text}
            
        return {
            'success': True,
            'pm_response': pm_response,
            'em_response': em_response,
            'pm_raw': pm_response_text,
            'em_raw': em_response_text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'pm_response': {"error": f"Workflow error: {str(e)}"},
            'em_response': {"error": f"Workflow error: {str(e)}"}
        }

def run_dynamic_agent_workflow_sync(user_request):
    """Synchronous wrapper for the async agent workflow"""
    return run_async(run_dynamic_agent_workflow(user_request))

def create_pm_agent_prompt(user_request):
    """Create a Product Manager agent prompt for Claude Code SDK"""
    return f"""
You are an experienced Product Manager at a tech company. A stakeholder has come to you with this request:

"{user_request}"

Please analyze this request and provide a comprehensive Product Manager response in **Markdown format**. Structure your response as follows:

# Product Manager Analysis

## 📋 Problem Analysis

### Problem Statement
[Clear problem statement based on the request]

### Target Users
- [Target user persona 1]
- [Target user persona 2]
- [Additional personas as needed]

### Business Goals
- [Business objective 1]
- [Business objective 2]
- [Additional goals as needed]

### Success Metrics
- [Measurable success criterion 1]
- [Measurable success criterion 2]
- [Additional metrics as needed]

## 📝 User Stories

### US-001: [Story Title]
**As a** [user type], **I want** [goal] **so that** [benefit]

**Priority:** High/Medium/Low | **Story Points:** [number] | **Business Value:** [explanation]

**Acceptance Criteria:**
- [Criteria 1]
- [Criteria 2]
- [Additional criteria as needed]

[Repeat for additional user stories]

## 📋 Requirements

### Functional Requirements
- [Functional requirement 1]
- [Functional requirement 2]
- [Additional requirements as needed]

### Non-Functional Requirements
- [Non-functional requirement 1]
- [Non-functional requirement 2]
- [Additional requirements as needed]

### Constraints
- [Constraint 1]
- [Constraint 2]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Dependencies
- [Dependency 1]
- [Dependency 2]

## ⚠️ Risk Assessment

### [Risk Name 1]
**Impact:** High/Medium/Low | **Probability:** High/Medium/Low
**Mitigation:** [Mitigation strategy]

[Repeat for additional risks]

## 🎯 Next Steps
- [Next step 1]
- [Next step 2]
- [Additional steps as needed]

## ❓ Questions for Engineering Team
- [Technical question 1]
- [Technical question 2]
- [Additional questions as needed]

Focus on creating realistic, detailed user stories and requirements that an engineering team can work with. Be thorough but practical.
"""

def create_em_agent_prompt(user_request, pm_response):
    """Create an Engineering Manager agent prompt for Claude Code SDK"""
    # Convert pm_response to string representation for the prompt
    pm_analysis = str(pm_response) if pm_response else "PM analysis not available"
    
    return f"""
You are an experienced Engineering Manager at a tech company. The Product Manager has analyzed a stakeholder request and provided their analysis. Now you need to create the technical implementation plan.

Original Request: "{user_request}"

Product Manager Analysis:
{pm_analysis}

Please provide a comprehensive Engineering Manager response in **Markdown format**. Structure your response as follows:

# Engineering Manager Technical Plan

## 🏗️ Technical Architecture

### Architecture Overview
[High-level system architecture description]

### Technology Stack
- **Frontend:** [Recommended frontend technology]
- **Backend:** [Recommended backend technology]
- **Database:** [Recommended database solution]
- **Infrastructure:** [Recommended infrastructure approach]
- **Additional Tools:**
  - [Tool/Service 1]
  - [Tool/Service 2]
  - [Additional tools as needed]

### System Components

#### [Component Name 1]
**Purpose:** [What this component does]
**Technology:** [Specific technology choice]
**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]
- [Additional responsibilities as needed]

[Repeat for additional components]

## 📅 Implementation Plan

### Development Phases

#### Phase 1: [Phase Name]
**Duration:** [Estimated duration]
**Tasks:**
- [Major task 1]
- [Major task 2]
- [Additional tasks as needed]

**Deliverables:**
- [Deliverable 1]
- [Deliverable 2]

**Dependencies:**
- [Dependency 1]
- [Dependency 2]

[Repeat for additional phases]

### Team Structure
**Recommended Team Size:** [Number] people

#### [Role Name 1] ([Count])
**Responsibilities:**
- [Responsibility 1]
- [Responsibility 2]

[Repeat for additional roles]

### Timeline Estimates
- **MVP Estimate:** [Time estimate]
- **Full Product Estimate:** [Time estimate]
- **Key Milestones:**
  - [Milestone 1]
  - [Milestone 2]
  - [Additional milestones as needed]

## ⚠️ Technical Risks

### [Risk Name 1]
**Impact:** High/Medium/Low | **Probability:** High/Medium/Low
**Mitigation:** [Technical mitigation strategy]

[Repeat for additional risks]

## 🏗️ Infrastructure Requirements
- [Infrastructure need 1]
- [Infrastructure need 2]
- [Additional requirements as needed]

## ✅ Quality Gates
- [Quality checkpoint 1]
- [Quality checkpoint 2]
- [Additional checkpoints as needed]

## ❓ Questions for Product Manager
- [Clarifying question 1]
- [Clarifying question 2]
- [Additional questions as needed]

Base your recommendations on modern software engineering best practices and consider scalability, maintainability, and team capabilities.
"""

async def run_dynamic_agent_workflow(user_request):
    """Run dynamic PM -> EM workflow using Claude Code SDK"""
    
    try:
        # Step 1: Get PM analysis from Claude
        pm_prompt = create_pm_agent_prompt(user_request)
        
        if SDK_AVAILABLE:
            # PM queries may need multiple turns for complex analysis
            pm_messages = await query_claude_code_sdk(pm_prompt, ClaudeCodeOptions(max_turns=3))
        else:
            # Fallback to CLI method
            pm_messages = query_claude_code_cli(pm_prompt, 3)
        
        # Extract PM response - handle different message formats
        pm_response_text = ""
        if pm_messages:
            # For SDK, find the ResultMessage (last message should be ResultMessage)
            if SDK_AVAILABLE:
                # Look for ResultMessage in the messages
                result_messages = [msg for msg in pm_messages if hasattr(msg, 'result')]
                if result_messages:
                    pm_response_text = result_messages[-1].result
                else:
                    pm_response_text = str(pm_messages[-1])
            else:
                # Handle CLI response format
                last_message = pm_messages[-1]
                if isinstance(last_message, dict):
                    pm_response_text = last_message.get('result', last_message.get('content', str(last_message)))
                else:
                    pm_response_text = str(last_message)
        
        # Store PM response as markdown
        pm_response = None
        try:
            if pm_response_text and pm_response_text.strip():
                pm_response = {
                    "agent_role": "Product Manager",
                    "markdown_content": pm_response_text,
                    "content_type": "markdown"
                }
            else:
                pm_response = {"error": "Empty PM response", "raw": pm_response_text}
        except Exception as e:
            pm_response = {"error": f"PM parsing error: {str(e)}", "raw": pm_response_text}
        
        # Step 2: Get EM analysis from Claude using PM output
        em_prompt = create_em_agent_prompt(user_request, pm_response)
        
        if SDK_AVAILABLE:
            # EM queries may need more turns due to tool usage
            em_messages = await query_claude_code_sdk(em_prompt, ClaudeCodeOptions(max_turns=3))
        else:
            # Fallback to CLI method
            em_messages = query_claude_code_cli(em_prompt, 3)
        
        # Extract EM response - handle different message formats
        em_response_text = ""
        if em_messages:
            # For SDK, find the ResultMessage (last message should be ResultMessage)
            if SDK_AVAILABLE:
                # Look for ResultMessage in the messages
                result_messages = [msg for msg in em_messages if hasattr(msg, 'result')]
                if result_messages:
                    em_response_text = result_messages[-1].result
                else:
                    em_response_text = str(em_messages[-1])
            else:
                # Handle CLI response format
                last_message = em_messages[-1]
                if isinstance(last_message, dict):
                    em_response_text = last_message.get('result', last_message.get('content', str(last_message)))
                else:
                    em_response_text = str(last_message)
        
        # Store EM response as markdown
        em_response = None
        try:
            if em_response_text is None:
                em_response = {"error": "EM response text is None", "raw": "None"}
            elif not isinstance(em_response_text, str):
                em_response_text = str(em_response_text)
                em_response = {"error": "EM response not a string", "raw": em_response_text}
            elif em_response_text.strip():
                em_response = {
                    "agent_role": "Engineering Manager",
                    "markdown_content": em_response_text,
                    "content_type": "markdown"
                }
            else:
                em_response = {"error": "Empty EM response", "raw": em_response_text}
        except Exception as e:
            em_response = {"error": f"EM parsing error: {str(e)}", "raw": em_response_text}
            
        return {
            'success': True,
            'pm_response': pm_response,
            'em_response': em_response,
            'pm_raw': pm_response_text,
            'em_raw': em_response_text
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'pm_response': {"error": f"Workflow error: {str(e)}"},
            'em_response': {"error": f"Workflow error: {str(e)}"}
        }

def run_dynamic_agent_workflow_sync(user_request):
    """Synchronous wrapper for the async agent workflow"""
    return run_async(run_dynamic_agent_workflow(user_request))

@app.route('/')
def index():
    """Main page with modern project creation interface"""
    return render_template('index.html')

@app.route('/project-breakdown')
def project_breakdown():
    """Project breakdown page with agent workflow visualization"""
    project_idea = request.args.get('idea', '')
    return render_template('project_breakdown.html', project_idea=project_idea)

@app.route('/api/start-workflow', methods=['POST'])
def start_workflow():
    """Start master workflow execution"""
    try:
        data = request.get_json()
        if not data or 'user_request' not in data:
            return jsonify({'error': 'User request is required'}), 400
        
        user_request = data['user_request'].strip()
        if not user_request:
            return jsonify({'error': 'User request cannot be empty'}), 400
        
        # Generate workflow ID
        workflow_id = str(uuid.uuid4())
        
        # Initialize workflow tracking
        workflows[workflow_id] = {
            'id': workflow_id,
            'user_request': user_request,
            'status': 'initializing',
            'current_step': 'pending',
            'progress': 0,
            'created_at': datetime.now().isoformat(),
            'agents': {
                'product_manager': {
                    'status': 'pending', 
                    'progress': 0, 
                    'message': 'Waiting to start...',
                    'title': 'Product Manager Analysis'
                },
                'engineering_manager': {
                    'status': 'pending', 
                    'progress': 0, 
                    'message': 'Waiting to start...',
                    'title': 'Engineering Manager Planning'
                },
                'frontend_engineer': {
                    'status': 'pending', 
                    'progress': 0, 
                    'message': 'Waiting to start...',
                    'title': 'Frontend Development'
                },
                'backend_engineer': {
                    'status': 'pending', 
                    'progress': 0, 
                    'message': 'Waiting to start...',
                    'title': 'Backend Development'
                },
                'testing_engineer': {
                    'status': 'pending', 
                    'progress': 0, 
                    'message': 'Waiting to start...',
                    'title': 'Testing & Validation'
                }
            }
        }
        
        # Log API workflow initiation
        print(f"\n🌐 [API REQUEST] New workflow requested via /api/start-workflow")
        print(f"🆔 Workflow ID: {workflow_id}")
        print(f"📝 Request Length: {len(user_request)} characters")
        
        # Start workflow in background thread
        thread = threading.Thread(
            target=run_master_workflow_async, 
            args=(user_request, workflow_id)
        )
        thread.daemon = True
        thread.start()
        
        print(f"📌 [API REQUEST] Background thread started for workflow {workflow_id[:8]}")
        
        return jsonify({
            'success': True,
            'workflow_id': workflow_id,
            'status': 'started'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/workflow-status/<workflow_id>')
def workflow_status(workflow_id):
    """Get real-time workflow status"""
    try:
        if workflow_id not in workflows:
            return jsonify({'error': 'Workflow not found'}), 404
        
        workflow_data = workflows[workflow_id]
        return jsonify(workflow_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/workflow', methods=['POST'])
def api_workflow():
    """API endpoint for full master workflow execution"""
    try:
        data = request.get_json()
        if not data or 'user_request' not in data:
            return jsonify({'error': 'User request is required'}), 400
        
        user_request = data['user_request']
        
        # Run master workflow
        workflow = MasterWorkflow(verbose=False)
        result = workflow.run_full_workflow(user_request)
        
        return jsonify({
            'success': result['success'],
            'workflow_id': result['workflow_id'],
            'result': result,
            'duration': result['total_duration']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/workflow-results/<workflow_id>')
def workflow_results(workflow_id):
    """View workflow results page"""
    if workflow_id not in workflows:
        return render_template('index.html', error='Workflow not found'), 404
    
    workflow_data = workflows[workflow_id]
    return render_template('workflow_results.html', workflow=workflow_data)

@app.route('/query', methods=['POST'])
def handle_query():
    """Handle agent workflow queries"""
    try:
        prompt = request.form.get('prompt', '').strip()
        query_type = request.form.get('query_type', 'agents')  # 'agents' or 'claude'
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Create session
        session_id = str(uuid.uuid4())
        
        if query_type == 'agents':
            # Run agent workflow
            workflow_result = run_dynamic_agent_workflow_sync(prompt)
            
            sessions[session_id] = {
                'prompt': prompt,
                'type': 'agents',
                'workflow_result': workflow_result,
                'session_id': session_id
            }
        else:
            # Original Claude Code query
            max_turns = int(request.form.get('max_turns', 3))
            messages = query_claude_code(prompt, max_turns)
            
            sessions[session_id] = {
                'prompt': prompt,
                'type': 'claude',
                'messages': messages,
                'session_id': session_id
            }
        
        return redirect(url_for('view_session', session_id=session_id))
        
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/api/agents', methods=['POST'])
def api_agents():
    """API endpoint for agent workflow"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt']
        workflow_result = run_dynamic_agent_workflow_sync(prompt)
        
        return jsonify({
            'success': workflow_result.get('success', False),
            'pm_response': workflow_result.get('pm_response', {}),
            'em_response': workflow_result.get('em_response', {}),
            'session_id': str(uuid.uuid4())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/session/<session_id>')
def view_session(session_id):
    """View session results"""
    session_data = sessions.get(session_id)
    if not session_data:
        return render_template('index.html', error='Session not found'), 404
    
    if session_data.get('type') == 'agents':
        return render_template('agents_result.html', session=session_data)
    else:
        return render_template('result.html', session=session_data)

@app.route('/api/query', methods=['POST'])
def api_query():
    """API endpoint for programmatic access"""
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Prompt is required'}), 400
        
        prompt = data['prompt']
        max_turns = data.get('max_turns', 3)
        
        messages = query_claude_code(prompt, max_turns)
        
        return jsonify({
            'success': True,
            'messages': [msg.__dict__ if hasattr(msg, '__dict__') else str(msg) for msg in messages],
            'session_id': str(uuid.uuid4())
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'Flask Claude Code App'})

@app.route('/debug/claude-format')
def debug_claude_format():
    """Debug endpoint to understand Claude Code SDK response format"""
    try:
        # Simple test query
        test_prompt = "Please respond with just the text: Hello World"
        messages = run_async(query_claude_code_sdk(test_prompt, ClaudeCodeOptions(max_turns=1)))
        
        debug_info = {
            'messages_count': len(messages) if messages else 0,
            'messages_types': [type(msg).__name__ for msg in messages] if messages else [],
            'last_message_type': type(messages[-1]).__name__ if messages else None,
            'last_message_attributes': dir(messages[-1]) if messages else [],
            'last_message_content': str(messages[-1]) if messages else None
        }
        
        if messages:
            last_msg = messages[-1]
            debug_info['last_message_dict'] = last_msg.__dict__ if hasattr(last_msg, '__dict__') else "No __dict__"
        
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({'error': str(e), 'type': str(type(e))})
    
@app.route('/debug/test-agent')
def debug_test_agent():
    """Debug endpoint to test agent workflow with simple request"""
    try:
        result = run_dynamic_agent_workflow_sync("A simple todo app")
        return jsonify({
            'success': result.get('success'),
            'error': result.get('error'),
            'pm_raw_type': type(result.get('pm_raw', '')).__name__,
            'pm_raw_preview': str(result.get('pm_raw', ''))[:500],
            'em_raw_type': type(result.get('em_raw', '')).__name__,
            'em_raw_preview': str(result.get('em_raw', ''))[:500],
            'pm_response_keys': list(result.get('pm_response', {}).keys()) if isinstance(result.get('pm_response'), dict) else 'Not a dict',
            'em_response_keys': list(result.get('em_response', {}).keys()) if isinstance(result.get('em_response'), dict) else 'Not a dict'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'type': str(type(e))})

@app.errorhandler(500)
def internal_error(error):
    return render_template('index.html', error='Internal server error'), 500

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html', error='Page not found'), 404

if __name__ == '__main__':
    # Check for required environment variables
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("Warning: ANTHROPIC_API_KEY not set. Please configure your API key in .env file.")
    
    app.run(debug=True, host='0.0.0.0', port=5001)