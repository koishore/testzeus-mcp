"""
Demo script showing the Hercules MCP server in action.
"""

import asyncio
import json
import time
from pathlib import Path
import sys
import os

# Add src to path so we can import modules
repo_root = Path(__file__).resolve().parent
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from src.hercules_manager import HerculesManager

async def demo():
    print("🧪 Hercules MCP Server Demo")
    print("=" * 40)
    
    manager = HerculesManager()
    
    # Create first test
    print("\n📝 Creating a test case...")
    test1 = manager.create_test_case(
        name="Login Flow Test",
        description="Test user login functionality",
        steps=[
            "Go to login page",
            "Enter username: demo@test.com", 
            "Enter password: test123",
            "Click login button",
            "Check if dashboard loads"
        ],
        expected_outcome="User successfully logs in"
    )
    
    print(f"✅ Created: {test1.name}")
    print(f"   ID: {test1.id}")
    print(f"   File: {test1.file_path}")
    
    # Create second test  
    print("\n📝 Creating another test...")
    test2 = manager.create_test_case(
        name="Search Products",
        description="Test product search",
        steps=[
            "Navigate to products page",
            "Enter search: laptop",
            "Click search",
            "Verify results show"
        ],
        expected_outcome="Search results displayed"
    )
    
    print(f"✅ Created: {test2.name}")
    
    # List tests
    print("\n📋 All test cases:")
    tests = manager.list_test_cases()
    for i, test in enumerate(tests, 1):
        print(f"   {i}. {test.name}")
    
    # Run first test
    print(f"\n🚀 Running '{test1.name}'...")
    result1 = await manager.run_test(test1.id)
    
    print(f"✅ Completed: {result1.status}")
    print(f"   Time: {result1.execution_time:.2f}s")
    print(f"   Logs: {len(result1.logs)} entries")
    
    # Show some logs
    print("\n📊 Execution logs:")
    for i, log in enumerate(result1.logs[:5], 1):  # just first 5
        print(f"   {i}. {log}")
    if len(result1.logs) > 5:
        print(f"   ... and {len(result1.logs) - 5} more")
    
    # Run second test
    print(f"\n🚀 Running '{test2.name}'...")
    result2 = await manager.run_test(test2.id)
    print(f"✅ Completed: {result2.status} ({result2.execution_time:.2f}s)")
    
    # Summary
    print("\n📈 Results summary:")
    results = manager.list_test_results()
    for i, res in enumerate(results, 1):
        emoji = "✅" if res.status == "passed" else "❌"
        print(f"   {i}. {res.test_name}: {emoji} {res.status}")
    
    # Show generated test file
    print(f"\n📄 Generated test file ({test1.name}):")
    if test1.file_path and os.path.exists(test1.file_path):
        content = Path(test1.file_path).read_text()
        # Show just the class definition part
        lines = content.split('\n')
        class_start = next(i for i, line in enumerate(lines) if 'class ' in line)
        relevant_lines = lines[class_start:class_start+15]  # first 15 lines of class
        print("```python")
        for line in relevant_lines:
            print(line)
        print("...")
        print("```")

    print("\n🎉 Demo finished!")
    print("\nTo try the VSCode extension:")
    print("1. Install: code --install-extension vscode-extension/hercules-mcp-extension-1.0.0.vsix")
    print("2. Start MCP server: python src/main.py")  
    print("3. Use Command Palette: 'Hercules: Create Test'")

if __name__ == "__main__":
    asyncio.run(demo())