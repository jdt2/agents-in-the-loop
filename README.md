# Flask Claude Code Web App

A Python Flask web application that integrates with the Claude Code SDK, providing a web interface for interacting with Claude Code programmatically.

## Features

- **Web Interface**: User-friendly form for submitting prompts to Claude Code
- **Async Processing**: Handles Claude Code SDK async operations with anyio
- **Session Management**: Track and view conversation sessions
- **API Endpoint**: RESTful API for programmatic access
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Mobile-friendly interface

## Prerequisites

- Python 3.10+
- Node.js (required by Claude Code SDK)
- Claude Code CLI: `npm install -g @anthropic-ai/claude-code`
- Anthropic API key

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd agents-in-the-loop
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   - Copy `.env` file and add your Anthropic API key:
   ```bash
   ANTHROPIC_API_KEY=your_api_key_here
   ```

4. **Run the application:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   Navigate to `http://localhost:5000`

## Usage

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Enter your coding prompt in the text area
3. Select the maximum number of turns for the conversation
4. Click "Submit Query" to process your request
5. View the results with full conversation history

### API Endpoint

Send POST requests to `/api/query`:

```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a Python function to calculate Fibonacci numbers",
    "max_turns": 3
  }'
```

### Example Prompts

- "Write a Python function to calculate Fibonacci numbers"
- "Review this code for bugs and suggest improvements"
- "Create a REST API endpoint for user authentication"
- "Add unit tests for the calculator module"

## Project Structure

```
agents-in-the-loop/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── README.md             # This file
├── templates/
│   ├── index.html        # Main interface
│   └── result.html       # Results display
└── static/
    └── style.css         # Styling
```

## API Routes

- `GET /` - Main web interface
- `POST /query` - Process Claude Code queries (web form)
- `GET /session/<session_id>` - View session results
- `POST /api/query` - API endpoint for programmatic access
- `GET /health` - Health check endpoint

## Configuration

The application supports various configuration options through environment variables:

- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)
- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_DEBUG` - Enable debug mode
- `SECRET_KEY` - Flask secret key for sessions
- `CLAUDE_CODE_USE_BEDROCK=1` - Use Amazon Bedrock (optional)
- `CLAUDE_CODE_USE_VERTEX=1` - Use Google Vertex AI (optional)

## Error Handling

The application includes comprehensive error handling:

- Input validation for required fields
- Claude Code SDK error handling
- HTTP error responses (404, 500)
- User-friendly error messages in the web interface

## Security Considerations

- Never commit API keys to version control
- Use environment variables for sensitive configuration
- Implement rate limiting in production
- Consider authentication for production deployments

## Development

To extend the application:

1. **Add new routes** in `app.py`
2. **Modify templates** in the `templates/` directory
3. **Update styling** in `static/style.css`
4. **Add dependencies** to `requirements.txt`

## Troubleshooting

1. **"ANTHROPIC_API_KEY not set"**: Ensure your API key is configured in `.env`
2. **Claude Code SDK errors**: Verify Node.js and Claude Code CLI are installed
3. **Import errors**: Run `pip install -r requirements.txt`
4. **Port conflicts**: Change the port in `app.py` if 5000 is in use

## License

This project is for educational and development purposes.