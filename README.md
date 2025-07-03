# TestZeus Hercules MCP Server

An MCP server for integrating AI assistants with TestZeus Hercules. Makes it easy to create and run tests through various editors and AI tools.

## What This Does

This project fulfills the TestZeus hiring assignment:

- **MCP Server**: Creates test cases, runs them via Hercules, returns results
- **VSCode Extension**: Full editor integration with UI for authoring/running tests  
- **AI Integration**: Works with Claude Desktop and Cursor for natural language testing

Built this using FastMCP (Python) + TypeScript for the VSCode extension.

## Quick Setup

Need:
- Python 3.8+
- Node.js 16+ (for VSCode stuff)
- VSCode or Claude Desktop or Cursor
- TestZeus Hercules (optional - will simulate if not installed)

```bash
git clone <repo>
cd hercules-mcp-server
pip install -r requirements.txt

# Start server
python src/main.py

# For VSCode extension
cd vscode-extension
npm install && npm run compile
vsce package
code --install-extension hercules-mcp-extension-1.0.0.vsix
```

## Using with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "hercules": {
      "command": "python",
      "args": ["src/main.py"],
      "cwd": "/path/to/hercules-mcp-server"
    }
  }
}
```

Config file locations:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

Then just ask Claude: "Create a test for login functionality" and it'll use the MCP tools.

## Using with Cursor

Install the VSCode extension (works in Cursor too) or configure direct MCP integration:

```json
{
  "cursor.mcp.servers": {
    "hercules": {
      "url": "http://localhost:8000",
      "tools": ["create_test_case", "run_test", "get_test_result", "list_test_cases"]
    }
  }
}
```

## Demo

Run `python demo_script.py` to see it work end-to-end.

Or in VSCode:
1. Ctrl+Shift+P → "Hercules: Create Test"
2. Fill in test details
3. Right-click test in sidebar → "Run Test"
4. View results in the webview panel

## How It Works

```
AI Assistant ↔ MCP Server ↔ TestZeus Hercules
      ↕              ↕
VSCode Plugin    Test Storage
```

The MCP server exposes these tools:
- `create_test_case` - Makes new tests with given steps
- `run_test` - Executes tests (real Hercules or simulation)
- `get_test_result` - Gets execution results  
- `list_test_cases` / `list_test_results` - List stuff

## Project Structure

```
src/               # MCP server code
vscode-extension/   # Complete VSCode extension
tests/             # Unit tests
scripts/           # Utility scripts
demo_script.py     # Working demo
```

## API Examples

Create test:
```python
{
  "name": "Login Test",
  "description": "Test user login", 
  "steps": ["Navigate to login", "Enter creds", "Click login"],
  "expected_outcome": "User logs in successfully"
}
```

Run test:
```python
{"test_id": "uuid-string"}
```

Results include status, logs, timing, errors, etc.

## Testing

```bash
python demo_script.py        # See it work
python -m pytest tests/      # Run unit tests
cd vscode-extension && npm test  # Test extension
```

## Configuration

Environment vars:
- `HERCULES_PATH` - Path to Hercules binary
- `MCP_SERVER_PORT` - Server port (default 8000)
- `LOG_LEVEL` - Logging level

VSCode settings:
- `hercules.mcpServerUrl` - Server URL
- `hercules.autoRefresh` - Auto-refresh results

## Development Notes

The FastMCP integration was pretty straightforward. Main challenge was getting the VSCode extension webview to communicate properly with the MCP server - had to figure out the right HTTP endpoints.

For Hercules integration, I added a fallback simulation mode since not everyone will have it installed. The test file generation creates Python classes that inherit from HerculesTest.

Error handling tries to be robust but there might be edge cases I missed. The async test execution was tricky to get right.

## License

MIT