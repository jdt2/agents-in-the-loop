# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
python app.py
```
The Flask app runs on port 3000 by default, accessible at `http://localhost:3000`.

### Installing Dependencies
```bash
pip install -r requirements.txt
```
Install the browser:
```bash
playwright install chromium --with-deps --no-shell
```

### Environment Setup
Copy `.env.example` to `.env` and configure:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

## Project Architecture

This is a Flask web application that integrates with the Claude Code SDK, providing both web interface and API endpoints for programmatic interaction with Claude Code.

### Core Architecture
- **SDK-Only Integration**: The app requires the Claude Code SDK and will fail if not available
- **Session Management**: In-memory session storage (sessions dict) tracks conversation history
- **Async Integration**: Uses `anyio` and custom `run_async()` helper to bridge Flask's sync nature with Claude Code SDK's async API

### Key Components

#### app.py (Main Application)
- `query_claude_code_sdk()`: Core method using Claude Code SDK with async/await
- `query_claude_code()`: Wrapper function that calls the SDK method with proper configuration
- Session storage in `sessions` dict with UUID-based session IDs

#### API Endpoints
- `GET /`: Main web interface (renders templates/index.html)
- `POST /query`: Web form submission handler
- `GET /session/<session_id>`: View saved session results  
- `POST /api/query`: JSON API endpoint for programmatic access
- `GET /health`: Health check endpoint

#### Templates & Static Files
- `templates/index.html`: Main query form interface
- `templates/result.html`: Results display with conversation history
- `static/style.css`: Application styling

### Dependencies Integration
- **Flask**: Web framework handling HTTP routes and templating
- **claude-code-sdk**: Required integration with Claude Code SDK
- **anyio**: Async compatibility layer for Flask
- **python-dotenv**: Environment variable management

### Error Handling Strategy
- Required SDK imports will fail fast if SDK is not available
- Comprehensive exception handling for SDK methods
- User-friendly error messages in web interface
- HTTP error handlers for 404/500 responses

### Configuration Options
Environment variables support:
- `ANTHROPIC_API_KEY` (required)
- `FLASK_ENV`, `FLASK_DEBUG` (Flask configuration)
- `SECRET_KEY` (session security)
- `CLAUDE_CODE_USE_BEDROCK=1` (Bedrock integration)
- `CLAUDE_CODE_USE_VERTEX=1` (Vertex AI integration)