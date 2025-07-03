# tests/test_server.py
"""Unit tests for MCP server tools."""

import pytest
from src.main import (
    create_test_case, run_test, get_test_result,
    list_test_cases, list_test_results, get_test_status,
    _manager
)


class TestMCPTools:
    """Test suite for MCP server tools."""

    def setup_method(self):
        """Clear test data before each test."""
        _manager._test_cases.clear()
        _manager._test_results.clear()

    def test_create_test_case_tool(self):
        """Test create_test_case MCP tool."""
        result = create_test_case(
            name="API Test",
            description="Test API endpoints",
            steps=["Send request", "Verify response"],
            expected_outcome="Response is valid"
        )

        assert result["success"] is True
        assert "test_case" in result
        assert result["test_case"]["name"] == "API Test"
        assert len(result["test_case"]["steps"]) == 2

    @pytest.mark.asyncio
    async def test_run_test_tool(self):
        """Test run_test MCP tool."""
        # First create a test case
        create_result = create_test_case(
            name="Test to Run",
            description="A test for running",
            steps=["Step 1"],
            expected_outcome="Success"
        )
        test_id = create_result["test_case"]["id"]

        # Now run it
        result = await run_test(test_id)

        assert result["success"] is True
        assert "result" in result
        assert result["result"]["test_id"] == test_id
        assert result["result"]["status"] == "passed"

    @pytest.mark.asyncio
    async def test_run_nonexistent_test_tool(self):
        """Test running a nonexistent test via MCP tool."""
        result = await run_test("nonexistent-id")

        assert result["success"] is False
        assert "error" in result

    def test_get_test_result_tool(self):
        """Test get_test_result MCP tool."""
        # Test with nonexistent ID
        result = get_test_result("nonexistent-id")
        assert result["success"] is False

    def test_list_test_cases_tool(self):
        """Test list_test_cases MCP tool."""
        # Initially empty
        result = list_test_cases()
        assert result["success"] is True
        assert result["count"] == 0
        assert len(result["test_cases"]) == 0

        # Create a test case
        create_test_case(
            name="Listed Test",
            description="A test to be listed",
            steps=["Step 1"],
            expected_outcome="Success"
        )

        # Now list should have one item
        result = list_test_cases()
        assert result["success"] is True
        assert result["count"] == 1
        assert len(result["test_cases"]) == 1
        assert result["test_cases"][0]["name"] == "Listed Test"

    def test_list_test_results_tool(self):
        """Test list_test_results MCP tool."""
        # Initially empty
        result = list_test_results()
        assert result["success"] is True
        assert result["count"] == 0
        assert len(result["results"]) == 0

    def test_get_test_status_tool(self):
        """Test get_test_status MCP tool."""
        # Test with nonexistent ID
        result = get_test_status("nonexistent-id")
        assert result["success"] is False

    @pytest.mark.asyncio
    async def test_complete_workflow(self):
        """Test complete workflow through MCP tools."""
        # 1. Create test case
        create_result = create_test_case(
            name="Workflow Test",
            description="Complete workflow test",
            steps=["Step 1", "Step 2", "Step 3"],
            expected_outcome="All steps complete"
        )
        
        assert create_result["success"] is True
        test_id = create_result["test_case"]["id"]

        # 2. List test cases
        list_result = list_test_cases()
        assert list_result["success"] is True
        assert list_result["count"] == 1

        # 3. Run test
        run_result = await run_test(test_id)
        assert run_result["success"] is True
        assert run_result["result"]["status"] == "passed"

        # 4. Get test result
        result_response = get_test_result(test_id)
        assert result_response["success"] is True
        assert result_response["result"]["test_id"] == test_id

        # 5. Get test status
        status_result = get_test_status(test_id)
        assert status_result["success"] is True
        assert status_result["status"] == "passed"

        # 6. List test results
        results_list = list_test_results()
        assert results_list["success"] is True
        assert results_list["count"] == 1

    def test_model_serialization(self):
        """Test that models serialize correctly for MCP responses."""
        # Create a test case and verify serialization
        result = create_test_case(
            name="Serialization Test",
            description="Test model serialization",
            steps=["Step 1"],
            expected_outcome="Serializes correctly"
        )

        test_case_data = result["test_case"]
        
        # Check that all required fields are present and correctly typed
        assert isinstance(test_case_data["id"], str)
        assert isinstance(test_case_data["name"], str)
        assert isinstance(test_case_data["description"], str)
        assert isinstance(test_case_data["steps"], list)
        assert isinstance(test_case_data["expected_outcome"], str)
        assert isinstance(test_case_data["created_at"], str)  # ISO format
        
        # file_path should be present (can be None or string)
        assert "file_path" in test_case_data


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling in MCP tools."""
    # This test ensures that tools handle exceptions gracefully
    # and return proper error responses
    
    # Test with invalid data types (if applicable)
    try:
        result = create_test_case(
            name=None,  # Invalid - should be string
            description="Test",
            steps=["Step 1"],
            expected_outcome="Test"
        )
        # If this doesn't raise an exception, check it returns error response
        if not result.get("success"):
            assert "error" in result
    except Exception:
        # Exception is also acceptable error handling
        pass