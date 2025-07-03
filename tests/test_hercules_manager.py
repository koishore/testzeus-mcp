# tests/test_hercules_manager.py
"""Tests for HerculesManager functionality."""

import asyncio
import pytest
from src.hercules_manager import HerculesManager
from src.models import TestCase, TestResult


class TestHerculesManager:
    """Test the main manager class."""

    def setup_method(self):
        self.manager = HerculesManager()

    def test_create_test_case(self):
        """Test creating a basic test case."""
        test_case = self.manager.create_test_case(
            name="Sample Test",
            description="A test case",
            steps=["Step 1", "Step 2", "Step 3"],
            expected_outcome="Should work"
        )

        assert isinstance(test_case, TestCase)
        assert test_case.name == "Sample Test"
        assert test_case.description == "A test case"
        assert len(test_case.steps) == 3
        assert test_case.expected_outcome == "Should work"
        assert test_case.id is not None
        assert test_case.created_at is not None
        assert test_case.file_path is not None

        # Check it's stored
        assert test_case.id in self.manager._test_cases

    @pytest.mark.asyncio
    async def test_run_test_simulation(self):
        """Test running a test in simulation mode."""
        # Create test first
        test_case = self.manager.create_test_case(
            name="Login Test",
            description="Test login",
            steps=["Go to login", "Enter creds", "Click login"],
            expected_outcome="User logged in"
        )

        # Run it
        result = await self.manager.run_test(test_case.id)

        assert isinstance(result, TestResult)
        assert result.test_id == test_case.id
        assert result.test_name == test_case.name
        assert result.status == "passed"  # simulation always passes
        assert len(result.logs) > 0
        assert result.execution_time is not None
        assert result.started_at is not None
        assert result.completed_at is not None

        # Should be stored
        assert test_case.id in self.manager._test_results

    @pytest.mark.asyncio
    async def test_run_missing_test(self):
        """Test running a test that doesn't exist."""
        with pytest.raises(ValueError, match="not found"):
            await self.manager.run_test("fake-id")

    def test_list_test_cases(self):
        """Test listing test cases."""
        # Should be empty initially
        cases = self.manager.list_test_cases()
        assert len(cases) == 0

        # Add some tests
        test1 = self.manager.create_test_case(
            name="Test 1", description="First test", 
            steps=["Step 1"], expected_outcome="Works"
        )
        test2 = self.manager.create_test_case(
            name="Test 2", description="Second test",
            steps=["Step 1", "Step 2"], expected_outcome="Also works"
        )

        cases = self.manager.list_test_cases()
        assert len(cases) == 2
        assert test1 in cases
        assert test2 in cases

    @pytest.mark.asyncio
    async def test_list_test_results(self):
        """Test listing test results."""
        # Empty initially
        results = self.manager.list_test_results()
        assert len(results) == 0

        # Create and run some tests
        test1 = self.manager.create_test_case(
            name="Test 1", description="First test",
            steps=["Step 1"], expected_outcome="Works"
        )
        test2 = self.manager.create_test_case(
            name="Test 2", description="Second test", 
            steps=["Step 1"], expected_outcome="Works"
        )

        await self.manager.run_test(test1.id)
        await self.manager.run_test(test2.id)

        results = self.manager.list_test_results()
        assert len(results) == 2

    def test_get_test_result(self):
        """Test getting specific test results."""
        # Non-existent should return None
        result = self.manager.get_test_result("fake-id")
        assert result is None

    def test_test_file_generation(self):
        """Test that generated test files look right."""
        test_case = TestCase(
            name="Sample Test",
            description="A sample test",
            steps=["Step 1", "Step 2"],
            expected_outcome="Success"
        )

        file_content = self.manager._generate_test_file(test_case)

        assert "class Sample_TestTest(HerculesTest):" in file_content
        assert f'self.test_id = "{test_case.id}"' in file_content
        assert 'Step 1: Step 1' in file_content
        assert 'Step 2: Step 2' in file_content
        assert "Success" in file_content


@pytest.mark.asyncio
async def test_concurrent_execution():
    """Test running multiple tests at the same time."""
    manager = HerculesManager()

    # Create a couple tests
    test1 = manager.create_test_case(
        name="Concurrent Test 1", description="First concurrent test",
        steps=["Step 1"], expected_outcome="Works"
    )
    test2 = manager.create_test_case(
        name="Concurrent Test 2", description="Second concurrent test", 
        steps=["Step 1"], expected_outcome="Works"
    )

    # Run them together
    results = await asyncio.gather(
        manager.run_test(test1.id),
        manager.run_test(test2.id)
    )

    assert len(results) == 2
    assert all(result.status == "passed" for result in results)
    assert results[0].test_id == test1.id
    assert results[1].test_id == test2.id