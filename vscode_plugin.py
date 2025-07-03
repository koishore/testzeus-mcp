#!/usr/bin/env python3
"""
VSCode integration helper script.
Called by VSCode tasks to interact with the MCP server.
"""

import sys
import asyncio
from pathlib import Path

# Add src to path
repo_root = Path(__file__).resolve().parent
sys.path.insert(0, str(repo_root))

from src.hercules_manager import HerculesManager

async def main():
    if len(sys.argv) < 2:
        print("Usage: python vscode_plugin.py <action> [args...]")
        return
    
    action = sys.argv[1]
    manager = HerculesManager()
    
    if action == "create":
        # Simple test creation for VSCode tasks
        test = manager.create_test_case(
            name="VSCode Test",
            description="Test created from VSCode",
            steps=["Step 1", "Step 2"],
            expected_outcome="Success"
        )
        print(f"Created test: {test.id}")
        
    elif action == "list":
        tests = manager.list_test_cases()
        for test in tests:
            print(f"{test.id}: {test.name}")
            
    elif action == "run" and len(sys.argv) > 2:
        test_id = sys.argv[2]
        result = await manager.run_test(test_id)
        print(f"Test {test_id}: {result.status}")
        
    else:
        print("Unknown action")

if __name__ == "__main__":
    asyncio.run(main())