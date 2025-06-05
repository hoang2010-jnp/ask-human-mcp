#!/usr/bin/env python3
"""
Comprehensive verification script for ask-human-mcp package.

This script tests all major functionality to ensure the package works correctly
before PyPI upload and after installation.
"""

import asyncio
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_status(message, status="INFO"):
    """Print a status message with color coding"""
    colors = {
        "INFO": BLUE,
        "SUCCESS": GREEN,
        "WARNING": YELLOW,
        "ERROR": RED
    }
    color = colors.get(status, BLUE)
    print(f"{color}[{status}]{RESET} {message}")


def run_command(cmd, timeout=30, check_returncode=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=isinstance(cmd, str)
        )
        
        if check_returncode and result.returncode != 0:
            print_status(f"Command failed: {' '.join(cmd) if isinstance(cmd, list) else cmd}", "ERROR")
            print_status(f"STDOUT: {result.stdout}", "ERROR")
            print_status(f"STDERR: {result.stderr}", "ERROR")
            return None
            
        return result
    
    except subprocess.TimeoutExpired:
        print_status(f"Command timed out: {' '.join(cmd) if isinstance(cmd, list) else cmd}", "ERROR")
        return None
    except Exception as e:
        print_status(f"Command error: {e}", "ERROR")
        return None


def test_basic_installation():
    """Test that the package is properly installed"""
    print_status("Testing basic installation...", "INFO")
    
    # Test importing the package
    try:
        import ask_human_mcp
        print_status("✓ Package imports successfully", "SUCCESS")
    except ImportError as e:
        print_status(f"✗ Failed to import package: {e}", "ERROR")
        return False
    
    # Test CLI entry point
    result = run_command(["ask-human-mcp", "--help"])
    if result and result.returncode == 0:
        print_status("✓ CLI entry point works", "SUCCESS")
    else:
        print_status("✗ CLI entry point failed", "ERROR")
        return False
    
    return True


def test_unit_tests():
    """Run the unit test suite"""
    print_status("Running unit tests...", "INFO")
    
    result = run_command(["python", "-m", "pytest", "tests/", "-v", "--tb=short"])
    if result and result.returncode == 0:
        print_status("✓ All unit tests pass", "SUCCESS")
        return True
    else:
        print_status("✗ Unit tests failed", "ERROR")
        if result:
            print_status(f"Test output: {result.stdout}", "ERROR")
        return False


def test_server_startup():
    """Test that the server can start up in both modes"""
    print_status("Testing server startup...", "INFO")
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        ask_file = Path(f.name)
    
    try:
        # Test stdio mode
        print_status("Testing stdio mode startup...", "INFO")
        process = subprocess.Popen(
            ["ask-human-mcp", "--file", str(ask_file)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(1)
        
        if process.poll() is None:
            print_status("✓ Server starts in stdio mode", "SUCCESS")
            process.terminate()
            process.wait(timeout=5)
        else:
            print_status("✗ Server failed to start in stdio mode", "ERROR")
            stdout, stderr = process.communicate()
            print_status(f"STDERR: {stderr}", "ERROR")
            return False
        
        # Test HTTP mode
        print_status("Testing HTTP mode startup...", "INFO")
        process = subprocess.Popen(
            ["ask-human-mcp", "--host", "127.0.0.1", "--port", "0", "--file", str(ask_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it time to start
        time.sleep(2)
        
        if process.poll() is None:
            print_status("✓ Server starts in HTTP mode", "SUCCESS")
            process.terminate()
            process.wait(timeout=5)
        else:
            print_status("✗ Server failed to start in HTTP mode", "ERROR")
            stdout, stderr = process.communicate()
            print_status(f"STDERR: {stderr}", "ERROR")
            return False
            
        return True
        
    finally:
        if 'process' in locals() and process.poll() is None:
            process.terminate()
            process.wait(timeout=5)
        ask_file.unlink(missing_ok=True)


async def test_mcp_functionality():
    """Test core MCP functionality"""
    print_status("Testing MCP functionality...", "INFO")
    
    try:
        from ask_human_mcp.server import AskHumanConfig, AskHumanServer
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            ask_file = Path(f.name)
        
        config = AskHumanConfig(
            ask_file=ask_file,
            timeout=5,
            max_question_length=1000,
            max_context_length=2000,
            max_pending_questions=10,
            max_file_size=1000000,
            rotation_size=500000,
        )
        
        server = AskHumanServer(config)
        
        try:
            # Test basic functionality
            server.start_watching()
            
            # Test asking a question and simulating an answer
            question_task = asyncio.create_task(
                server._handle_question("Test question?", "Test context")
            )
            
            # Wait for question to be written
            await asyncio.sleep(0.2)
            
            # Read and modify the file
            with open(ask_file, "r") as f:
                content = f.read()
            
            if "Test question?" in content and "PENDING" in content:
                print_status("✓ Question written to file correctly", "SUCCESS")
                
                # Simulate human answer
                updated_content = content.replace("**Answer:** PENDING", "**Answer:** Test answer")
                with open(ask_file, "w") as f:
                    f.write(updated_content)
                
                # Get the answer
                try:
                    answer = await asyncio.wait_for(question_task, timeout=3)
                    if answer == "Test answer":
                        print_status("✓ Answer received correctly", "SUCCESS")
                        return True
                    else:
                        print_status(f"✗ Wrong answer received: {answer}", "ERROR")
                        return False
                except asyncio.TimeoutError:
                    print_status("✗ Timeout waiting for answer", "ERROR")
                    return False
            else:
                print_status("✗ Question not written correctly to file", "ERROR")
                return False
                
        finally:
            server.stop_watching()
            ask_file.unlink(missing_ok=True)
            
    except Exception as e:
        print_status(f"✗ MCP functionality test failed: {e}", "ERROR")
        return False


def test_file_operations():
    """Test file operations and edge cases"""
    print_status("Testing file operations...", "INFO")
    
    try:
        from ask_human_mcp.server import safe_write_text, safe_read_text, validate_input
        
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            test_file = Path(f.name)
        
        # Test safe file operations
        test_content = "Hello\nWorld\nTest"
        if safe_write_text(test_file, test_content):
            read_content = safe_read_text(test_file)
            if read_content == test_content:
                print_status("✓ File operations work correctly", "SUCCESS")
            else:
                print_status("✗ File content mismatch", "ERROR")
                return False
        else:
            print_status("✗ File write failed", "ERROR")
            return False
        
        # Test input validation
        try:
            validate_input("Valid input", 100, "test")
            print_status("✓ Input validation works", "SUCCESS")
        except Exception as e:
            print_status(f"✗ Input validation failed: {e}", "ERROR")
            return False
        
        # Test invalid input
        try:
            validate_input("x" * 101, 100, "test")
            print_status("✗ Input validation should have failed", "ERROR")
            return False
        except Exception:
            print_status("✓ Input validation correctly rejects invalid input", "SUCCESS")
        
        test_file.unlink(missing_ok=True)
        return True
        
    except Exception as e:
        print_status(f"✗ File operations test failed: {e}", "ERROR")
        return False


def test_package_metadata():
    """Test package metadata and structure"""
    print_status("Testing package metadata...", "INFO")
    
    try:
        import ask_human_mcp
        
        # Check version
        if hasattr(ask_human_mcp, '__version__'):
            print_status(f"✓ Package version: {ask_human_mcp.__version__}", "SUCCESS")
        else:
            print_status("⚠ No version attribute found", "WARNING")
        
        # Check if pyproject.toml exists
        if Path("pyproject.toml").exists():
            print_status("✓ pyproject.toml exists", "SUCCESS")
        else:
            print_status("✗ pyproject.toml missing", "ERROR")
            return False
        
        # Check if README exists
        if Path("README.md").exists():
            print_status("✓ README.md exists", "SUCCESS")
        else:
            print_status("✗ README.md missing", "ERROR")
            return False
        
        return True
        
    except Exception as e:
        print_status(f"✗ Package metadata test failed: {e}", "ERROR")
        return False


async def main():
    """Run all verification tests"""
    print_status("=" * 50, "INFO")
    print_status("Ask-Human MCP Package Verification", "INFO")
    print_status("=" * 50, "INFO")
    
    tests = [
        ("Basic Installation", test_basic_installation),
        ("Package Metadata", test_package_metadata),
        ("Unit Tests", test_unit_tests),
        ("Server Startup", test_server_startup),
        ("MCP Functionality", test_mcp_functionality),
        ("File Operations", test_file_operations),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print_status(f"\n--- {test_name} ---", "INFO")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_status(f"✗ {test_name} failed with exception: {e}", "ERROR")
            results.append((test_name, False))
    
    # Summary
    print_status("\n" + "=" * 50, "INFO")
    print_status("VERIFICATION SUMMARY", "INFO")
    print_status("=" * 50, "INFO")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        color = "SUCCESS" if result else "ERROR"
        print_status(f"{status} {test_name}", color)
    
    print_status(f"\nTotal: {passed}/{total} tests passed", "INFO")
    
    if passed == total:
        print_status("🎉 All tests passed! Package is ready for PyPI.", "SUCCESS")
        return True
    else:
        print_status("❌ Some tests failed. Please fix issues before uploading to PyPI.", "ERROR")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1) 