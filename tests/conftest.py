# tests/conftest.py
"""Pytest configuration and shared fixtures."""

import pytest
import tempfile
import shutil
from pathlib import Path


@pytest.fixture(scope="session")
def temp_test_dir():
    """Create a temporary directory for test files."""
    temp_dir = Path(tempfile.mkdtemp(prefix="hercules_test_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def sample_test_case_data():
    """Sample test case data for testing."""
    return {
        "name": "Sample Login Test",
        "description": "Test user login functionality",
        "steps": [
            "Navigate to login page",
            "Enter username and password", 
            "Click login button",
            "Verify dashboard is displayed"
        ],
        "expected_outcome": "User successfully logs in and sees dashboard"
    }


@pytest.fixture
def sample_test_steps():
    """Sample test steps for testing."""
    return [
        "Open web browser",
        "Navigate to application URL",
        "Click on login link", 
        "Enter valid credentials",
        "Submit login form",
        "Verify successful login"
    ]


# Configure pytest for async tests
pytest_plugins = ('pytest_asyncio',)