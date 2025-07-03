# tests/test_server.py
"""Tests for MCP server functionality - testing the manager directly."""

import pytest
import sys
from pathlib import Path

# Add src to path
repo_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(repo_root))

from src.hercules_manager import HerculesManager


class TestMCPFunctionality:
    """Test MCP server functionality through the manager."""

    def setup_method(self):
        """Set up a fresh manager for each test."""
        self.manager = HerculesManager()

    def test_create_test_case_functionality(self):
        """Test create_test_case functionality."""
        test_case = self.manager.create_test_case(
            name="API Test",
            description="Test API endpoints",
            steps=["Send request", "Verify response"],
            expected_outcome="Response is valid"
        )

        assert test_case.name == "API Test"
        assert test_case.description == "Test API endpoints"
        assert len(test_case.steps) == 2
        assert test_case.expected_outcome == "Response is valid"
        assert test_case.id is not None

    @pytest.mark.asyncio
    async def test_run_test_functionality(self):
        """Test run_test functionality."""
        # Create test first
        test_case = self.manager.create_test_case(
            name="Test to Run",
            description="A test for running",
            steps=["Step 1"],
            expected_outcome="Success"
        )

        # Run it
        result = await self.manager.run_test(test_case.id)

        assert result.test_id == test_case.id
        assert result.test_name == test_case.name
        assert result.status == "passed"
        assert len(result.logs) > 0

    @pytest.mark.asyncio
    async def test_run_nonexistent_test(self):
        """Test running a nonexistent test."""
        with pytest.raises(ValueError):
            await self.manager.run_test("nonexistent-id")

    def test_get_test_result_functionality(self):
        """Test get_test_result functionality."""
        # Test with nonexistent ID
        result = self.manager.get_test_result("nonexistent-id")
        assert result is None

    def test_list_test_cases_functionality(self):
        """Test list_test_cases functionality."""
        # Initially empty
        cases = self.manager.list_test_cases()
        assert len(cases) == 0

        # Create a test case
        self.manager.create_test_case(
            name="Listed Test",
            description="A test to be listed",
            steps=["Step 1"],
            expected_outcome="Success"
        )

        # Now should have one
        cases = self.manager.list_test_cases()
        assert len(cases) == 1
        assert cases[0].name == "Listed Test"

    def test_list_test_results_functionality(self):
        """Test list_test_results functionality."""
        # Initially empty
        results = self.manager.list_test_results()
        assert len(results) == 0

    def test_get_test_status_functionality(self):
        """Test get_test_status functionality."""
        # Test with nonexistent ID
        result = self.manager.get_test_result("nonexistent-id")
        assert result is None

    @pytest.mark.asyncio
    async def test_complete_workflow_functionality(self):
        """Test complete workflow."""
        # 1. Create test case
        test_case = self.manager.create_test_case(
            name="Workflow Test",
            description="Complete workflow test",
            steps=["Step 1", "Step 2", "Step 3"],
            expected_outcome="All steps complete"
        )
        
        assert test_case.name == "Workflow Test"

        # 2. List test cases
        cases = self.manager.list_test_cases()
        assert len(cases) == 1

        # 3. Run test
        result = await self.manager.run_test(test_case.id)
        assert result.status == "passed"

        # 4. Get test result
        stored_result = self.manager.get_test_result(test_case.id)
        assert stored_result is not None
        assert stored_result.test_id == test_case.id

        # 5. List test results
        results = self.manager.list_test_results()
        assert len(results) == 1


# Test MCP wrapper functions (if they can be imported)
def test_mcp_server_import():
    """Test that MCP server can be imported without errors."""
    try:
        import src.main
        # If we get here, the import worked
        assert hasattr(src.main, 'mcp')
        assert hasattr(src.main, '_manager')
    except ImportError:
        # FastMCP not available - that's fine
        pytest.skip("FastMCP not available")


def test_manager_direct_usage():
    """Test using the manager directly."""
    manager = HerculesManager()
    
    # Test basic functionality
    test = manager.create_test_case(
        name="Direct Test",
        description="Direct manager test",
        steps=["Step 1"],
        expected_outcome="Works"
    )
    
    assert test.name == "Direct Test"
    assert len(manager.list_test_cases()) == 1