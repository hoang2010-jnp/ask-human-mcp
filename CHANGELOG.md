# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-15

### Added
- Initial release of Ask-Human MCP Server
- Basic MCP server functionality with `ask_human`, `list_pending_questions`, and `get_qa_stats` tools
- File-based Q&A system using markdown format
- Cross-platform file watching for instant response detection
- Timeout handling with configurable timeouts
- Concurrent question support with resource limits
- Command-line interface with comprehensive options
- Cursor and Claude Desktop integration examples
- Comprehensive test suite with 24+ test cases
- Cross-platform compatibility (Windows, macOS, Linux)

### Security
- Input validation and sanitization to prevent malicious content
- File locking to prevent corruption from concurrent access
- Secure file permissions (owner-only access)
- Resource limits to prevent DoS attacks and memory exhaustion
- Path validation to ensure files are written to safe locations

### Performance
- Robust markdown parsing using regex instead of fragile string operations
- File rotation to prevent infinite growth (configurable size limits)
- Memory leak prevention with proper cleanup of answered questions
- Debounced file change notifications to prevent event flooding
- Atomic file operations for consistency

### Bug Fixes
- **CRITICAL**: Fixed memory leak where answered questions were never cleaned up from memory
- **CRITICAL**: Fixed race condition in question registration that could cause lost questions
- **CRITICAL**: Added input validation with size limits to prevent DoS attacks
- **CRITICAL**: Implemented file rotation to prevent unlimited disk usage
- Fixed cross-platform file locking issues
- Fixed line ending normalization across platforms
- Fixed brittle markdown parsing that broke with formatting variations
- Added proper error handling and graceful degradation
- Fixed observer thread cleanup on shutdown

### Configuration
- Configurable question length limits (default: 10KB)
- Configurable context length limits (default: 50KB)
- Configurable maximum pending questions (default: 100)
- Configurable file size limits (default: 100MB)
- Configurable file rotation size (default: 50MB)
- Configurable timeout periods (default: 30 minutes)
- Platform-appropriate default file locations

### Developer Experience
- Comprehensive documentation and examples
- Type hints throughout the codebase
- Proper exception hierarchy with specific error types
- Health check endpoint for monitoring
- Detailed statistics and logging
- Development dependencies and tooling setup 