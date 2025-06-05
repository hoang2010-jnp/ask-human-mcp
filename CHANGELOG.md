# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-15

### Added
- First release! 🎉 Built the core Ask-Human MCP Server
- Created the basic toolset: `ask_human`, `list_pending_questions`, and `get_qa_stats`
- Set up a simple markdown-based Q&A system that just works
- Added file watching so AI gets your answers instantly
- Built in timeout handling so the AI won't wait forever
- Support for multiple questions at once (with reasonable limits)
- Simple command-line interface with all the options you need
- Added examples for Cursor and Claude Desktop
- Wrote a solid test suite with 24+ tests
- Works great on Windows, macOS, and Linux

### Security & Reliability
- Validated all inputs to keep things safe
- Added file locking to prevent data corruption
- Set up proper file permissions (only you can access your Q&A file)
- Added resource limits to keep things running smoothly
- Made sure files only get written where they should

### Performance
- Used robust regex for markdown parsing instead of hacky string splitting
- Added file rotation so your Q&A file doesn't grow forever
- Prevented memory leaks by cleaning up answered questions
- Reduced file system events to avoid overwhelming your system
- Used atomic file operations for reliability

### Bug Fixes
- Fixed a memory leak where answered questions stuck around forever
- Fixed a race condition that could lose questions
- Added input validation to prevent overload attacks
- Implemented file rotation to keep disk usage in check
- Fixed file locking issues across different operating systems
- Made sure line endings work correctly across platforms
- Improved markdown parsing to handle different formatting styles
- Added proper error handling with graceful fallbacks
- Made sure observer threads clean up properly on shutdown

### Configuration
- Adjustable question length limits (default: 10KB)
- Adjustable context length limits (default: 50KB)
- Configurable maximum pending questions (default: 100)
- Adjustable file size limits (default: 100MB)
- Configurable file rotation size (default: 50MB)
- Adjustable timeout periods (default: 30 minutes)
- Smart default file locations based on your OS

### Developer Experience
- Clear documentation and examples to get you started
- Full type hints throughout the code
- Proper exception handling with specific error types
- Health check endpoint to monitor server status
- Detailed stats and logging to understand what's happening
- Dev dependencies and tooling ready to go