# changelog

all notable changes to this project will be documented in this file.

the format is based on [keep a changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [semantic versioning](https://semver.org/spec/v2.0.0.html).

## [unreleased]

## [0.1.0] - 2025-01-15

### first release! 🎉
- built the core ask-human mcp server
- created the basic toolset: `ask_human`, `list_pending_questions`, and `get_qa_stats`
- set up a simple markdown-based q&a system that just works
- added file watching so ai gets your answers instantly
- built in timeout handling so the ai won't wait forever
- support for multiple questions at once (with reasonable limits)
- simple command-line interface with all the options you need
- added examples for cursor and claude desktop
- wrote a solid test suite with 24+ tests
- works great on windows, macos, and linux

### security & keeping things safe
- validated all inputs to keep things safe
- added file locking to prevent data corruption
- set up proper file permissions (only you can access your q&a file)
- added resource limits to keep things running smoothly
- made sure files only get written where they should

### performance stuff
- used robust regex for markdown parsing instead of hacky string splitting
- added file rotation so your q&a file doesn't grow forever
- prevented memory leaks by cleaning up answered questions
- reduced file system events to avoid overwhelming your system
- used atomic file operations for reliability

### bug fixes
- fixed a memory leak where answered questions stuck around forever
- fixed a race condition that could lose questions
- added input validation to prevent overload attacks
- implemented file rotation to keep disk usage in check
- fixed file locking issues across different operating systems
- made sure line endings work correctly across platforms
- improved markdown parsing to handle different formatting styles
- added proper error handling with graceful fallbacks
- made sure observer threads clean up properly on shutdown

### config options
- adjustable question length limits (default: 10kb)
- adjustable context length limits (default: 50kb)
- configurable maximum pending questions (default: 100)
- adjustable file size limits (default: 100mb)
- configurable file rotation size (default: 50mb)
- adjustable timeout periods (default: 30 minutes)
- smart default file locations based on your os

### developer experience
- clear documentation and examples to get you started
- full type hints throughout the code
- proper exception handling with specific error types
- health check endpoint to monitor server status
- detailed stats and logging to understand what's happening
- dev dependencies and tooling ready to go