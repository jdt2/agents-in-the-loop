import uuid
import asyncio
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from pathlib import Path
from .agent import run_browser_agent


# Create blueprint for browser agent routes
browser_bp = Blueprint('browser', __name__, url_prefix='/browser')

# Store browser sessions (use Redis or database in production)
browser_sessions = {}


def run_async(coro):
    """Helper function to run async code in Flask"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@browser_bp.route('/')
def browser_index():
    """Browser agent main page"""
    return render_template('browser/index.html')


@browser_bp.route('/run', methods=['POST'])
def run_browser_task():
    """Run a browser automation task"""
    try:
        task = request.form.get('task', '').strip()
        target_url = request.form.get('target_url', 'http://localhost:3000').strip()
        
        if not task:
            return render_template('browser/index.html', error='Task description is required')
        
        # Create session
        session_id = str(uuid.uuid4())
        
        # Store initial session data
        browser_sessions[session_id] = {
            'session_id': session_id,
            'task': task,
            'target_url': target_url,
            'status': 'running',
            'result': None,
            'error': None
        }
        
        # Run the browser agent
        result = run_async(run_browser_agent(task, target_url))
        
        # Update session with results
        status = 'completed' if result['success'] else ('cancelled' if result.get('cancelled') else 'failed')
        browser_sessions[session_id].update({
            'status': status,
            'result': result,
            'error': result.get('error') if not result['success'] else None,
            'cancelled': result.get('cancelled', False)
        })
        
        return redirect(url_for('browser.view_browser_session', session_id=session_id))
        
    except Exception as e:
        return render_template('browser/index.html', error=f'Error running browser task: {str(e)}')


@browser_bp.route('/session/<session_id>')
def view_browser_session(session_id):
    """View browser task session results"""
    session_data = browser_sessions.get(session_id)
    if not session_data:
        return render_template('browser/index.html', error='Session not found'), 404
    
    # Try to read output file if available
    output_content = None
    if session_data.get('result') and session_data['result'].get('output_file'):
        try:
            output_file = Path(session_data['result']['output_file'])
            if output_file.exists():
                output_content = output_file.read_text()
        except Exception as e:
            output_content = f"Error reading output file: {str(e)}"
    
    return render_template('browser/result.html', 
                         session=session_data, 
                         output_content=output_content)


@browser_bp.route('/api/run', methods=['POST'])
def api_run_browser_task():
    """API endpoint for running browser tasks"""
    try:
        data = request.get_json()
        if not data or 'task' not in data:
            return jsonify({'error': 'Task is required'}), 400
        
        task = data['task']
        target_url = data.get('target_url', 'http://localhost:3000')
        output_file = data.get('output_file')
        
        # Run the browser agent
        result = run_async(run_browser_agent(task, target_url, output_file))
        
        return jsonify({
            'success': result['success'],
            'session_id': str(uuid.uuid4()),
            'result': result
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@browser_bp.route('/sessions')
def list_browser_sessions():
    """List all browser sessions"""
    return jsonify({
        'sessions': [
            {
                'session_id': session_id,
                'task': session_data['task'],
                'status': session_data['status'],
                'target_url': session_data['target_url']
            }
            for session_id, session_data in browser_sessions.items()
        ]
    })
