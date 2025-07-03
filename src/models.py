"""Data models for Hercules MCP server."""

import uuid
from datetime import datetime
from typing import List, Optional

try:
    from pydantic import BaseModel, Field
except ImportError:
    # Fallback if pydantic not available
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
        
        def dict(self):
            return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        
        def model_dump(self):
            return self.dict()
    
    def Field(**kwargs):
        return kwargs.get('default')


class HerculesTestCase(BaseModel):
    """Represents a test case that can be executed by Hercules."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    steps: List[str]
    expected_outcome: str
    created_at: datetime = Field(default_factory=datetime.now)
    file_path: Optional[str] = None

    class Config:
        # Avoid pydantic v2 issues
        arbitrary_types_allowed = True


class HerculesTestResult(BaseModel):
    """Represents the result of a test execution."""
    
    test_id: str
    test_name: str
    status: str = "pending"  # running, passed, failed, error
    logs: List[str] = Field(default_factory=list)
    screenshots: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True


# Aliases for backward compatibility and to avoid pytest collection
TestCase = HerculesTestCase
TestResult = HerculesTestResult