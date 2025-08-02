import os
import asyncio
import uuid
from flask import Flask, render_template, request, jsonify, redirect, url_for
from dotenv import load_dotenv
import anyio
from claude_code_sdk import query, ClaudeCodeOptions

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')

# Store sessions in memory (use Redis or database in production)
sessions = {}

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

@app.route('/')
def index():
    """Main page with query form"""
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def handle_query():
    """Handle Claude Code queries"""
    try:
        prompt = request.form.get('prompt', '').strip()
        max_turns = int(request.form.get('max_turns', 3))
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        # Create session
        session_id = str(uuid.uuid4())
        
        # Query Claude Code
        messages = query_claude_code(prompt, max_turns)
        
        # Store session
        sessions[session_id] = {
            'prompt': prompt,
            'messages': messages,
            'session_id': session_id
        }
        
        return redirect(url_for('view_session', session_id=session_id))
        
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/session/<session_id>')
def view_session(session_id):
    """View session results"""
    session_data = sessions.get(session_id)
    if not session_data:
        return render_template('index.html', error='Session not found'), 404
    
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
    
    app.run(debug=True, host='0.0.0.0', port=3000)