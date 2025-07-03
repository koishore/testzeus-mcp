"""Data models for Hercules MCP server."""

import uuid
from datetime import datetime
from typing import List, Optional

try:
    from pydantic import BaseModel, Field, ConfigDict
except ImportError:
    # Fallback if pydantic not available
    class BaseModel:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
            if not hasattr(self, 'id'):
                self.id = str(uuid.uuid4())
            if not hasattr(self, 'created_at'):
                self.created_at = datetime.now()
        
        def dict(self):
            result = {}
            for key, value in self.__dict__.items():
                if not key.startswith('_'):
                    if isinstance(value, datetime):
                        result[key] = value.isoformat()
                    else:
                        result[key] = value
            return result
        
        def model_dump(self):
            return self.dict()
    
    def Field(**kwargs):
        return kwargs.get('default')
    
    def ConfigDict(**kwargs):
        return kwargs


class MCPTestCase(BaseModel):
    """Test case model - renamed to avoid pytest collection."""
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    steps: List[str]
    expected_outcome: str
    created_at: datetime = Field(default_factory=datetime.now)
    file_path: Optional[str] = None

    # Use ConfigDict for Pydantic v2 compatibility
    model_config = ConfigDict(arbitrary_types_allowed=True)


class MCPTestResult(BaseModel):
    """Test result model - renamed to avoid pytest collection."""
    
    test_id: str
    test_name: str
    status: str = "pending"  # running, passed, failed, error
    logs: List[str] = Field(default_factory=list)
    screenshots: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Use ConfigDict for Pydantic v2 compatibility
    model_config = ConfigDict(arbitrary_types_allowed=True)


# Export with the expected names for backward compatibility
TestCase = MCPTestCase
TestResult = MCPTestResult