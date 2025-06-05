# Ask-Human MCP 🧑‍💻🤝🤖

[![PyPI version](https://badge.fury.io/py/ask-human-mcp.svg)](https://badge.fury.io/py/ask-human-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A Model Context Protocol (MCP) server that lets AI agents escalate questions to humans instead of hallucinating answers. Perfect for AI coding assistants like Cursor, Claude Desktop, or any MCP-compatible client.

## 🚀 Quick Start

### Installation

```bash
pip install ask-human-mcp
```

### Start the Server

```bash
ask-human-mcp
```

The server will start and create an `ask_human.md` file in your home directory for Q&A logging.

### Connect to Cursor

Create or edit `.cursor/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "ask-human": {
      "command": "ask-human-mcp"
    }
  }
}
```

Restart Cursor and you're ready to go!

## 🎯 How It Works

1. **AI gets stuck** → Calls `ask_human(question, context)`
2. **Question logged** → Appears in `ask_human.md` with unique ID
3. **Human answers** → Replace "PENDING" with your response
4. **AI continues** → Uses your answer to proceed

### Example Flow

```markdown
### Q8c4f1e2a
**Timestamp:** 2025-01-15 14:30:22
**Question:** What's the correct API endpoint for user authentication?
**Context:** Building login form in auth.js, unclear which endpoint to use
**Answer:** PENDING
```

You edit it to:

```markdown
**Answer:** Use `/api/v2/auth/login` with POST method
```

The AI receives your answer and continues coding!

## 🔧 Configuration Options

### Command Line Options

```bash
ask-human-mcp --help
ask-human-mcp --port 3000 --host 0.0.0.0  # HTTP mode
ask-human-mcp --timeout 1800               # 30min timeout
ask-human-mcp --file custom_qa.md          # Custom Q&A file
ask-human-mcp --max-pending 50             # Max concurrent questions
ask-human-mcp --max-question-length 5000   # Max question size
ask-human-mcp --rotation-size 10485760     # Rotate file at 10MB
```

### MCP Client Configurations

#### Cursor (Local)
```json
{
  "mcpServers": {
    "ask-human": {
      "command": "ask-human-mcp",
      "args": ["--timeout", "900"]
    }
  }
}
```

#### Cursor (HTTP)
```json
{
  "mcpServers": {
    "ask-human": {
      "url": "http://localhost:3000/sse"
    }
  }
}
```

#### Claude Desktop
```json
{
  "mcpServers": {
    "ask-human": {
      "command": "ask-human-mcp"
    }
  }
}
```

## 🛠️ Features

- ✅ **Zero Configuration** - Works out of the box
- ✅ **File Watching** - Instant response when you save answers
- ✅ **Timeout Handling** - Questions don't hang forever
- ✅ **Concurrent Questions** - Handle multiple AI agents
- ✅ **Persistent Logging** - Full Q&A history in markdown
- ✅ **Cross-Platform** - Windows, macOS, Linux
- ✅ **MCP Standard** - Works with any MCP client
- ✅ **Input Validation** - Size limits and sanitization
- ✅ **File Rotation** - Automatic archiving of large files
- ✅ **Resource Limits** - Prevent DoS and memory leaks
- ✅ **Robust Parsing** - Handles malformed markdown gracefully

## 🔒 Security Features

- **Input sanitization** - Removes control characters and validates sizes
- **File locking** - Prevents corruption from concurrent access
- **Secure permissions** - Files created with restricted access
- **Resource limits** - Prevents memory exhaustion and DoS attacks
- **Path validation** - Ensures files are written to safe locations

## 📊 Resource Limits

| Setting | Default | Description |
|---------|---------|-------------|
| Question Length | 10KB | Maximum characters per question |
| Context Length | 50KB | Maximum characters per context |
| Pending Questions | 100 | Maximum concurrent questions |
| File Size | 100MB | Maximum ask file size |
| Rotation Size | 50MB | Size at which files are archived |

## 🌍 Platform Support

- **Windows** - Full support with native file locking
- **macOS** - Full support with FSEvents file watching
- **Linux** - Full support with inotify file watching

## 📚 API Reference

### Available Tools

#### `ask_human(question: str, context: str = "") -> str`
Ask the human a question and wait for response.

**Parameters:**
- `question`: The question you want answered
- `context`: Additional context (file paths, error messages, etc.)

**Returns:** The human's response

**Example:**
```python
answer = await ask_human(
    "What database should I use for this project?",
    "Building a chat app with 1000+ concurrent users"
)
```

#### `list_pending_questions() -> str`
Get a list of questions waiting for answers.

#### `get_qa_stats() -> str`
Get statistics about the Q&A session.

## 🚀 Development

### Running from Source

```bash
git clone https://github.com/masonyarbrough/ask-human-mcp.git
cd ask-human-mcp
pip install -e ".[dev]"
ask-human-mcp
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Quality

```bash
black ask_human_mcp tests
ruff check ask_human_mcp tests
mypy ask_human_mcp
```

## 🤝 Contributing

We welcome contributions! 

### Reporting Issues

Please use the GitHub issue tracker to report bugs or request features.
Include:
- Python version
- Operating system
- MCP client (Cursor, Claude Desktop, etc.)
- Error messages or logs
- Steps to reproduce

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://github.com/modelcontextprotocol) for the excellent standard
- [Anthropic](https://anthropic.com) for Claude and MCP support
- [Cursor](https://cursor.sh) for MCP integration
- All contributors and users providing feedback

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=masonyarbrough/ask-human-mcp&type=Date)](https://star-history.com/#masonyarbrough/ask-human-mcp&Date)