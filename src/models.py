"""Shared Pydantic data-models used by the Hercules MCP server.

The definitions are extracted into their own module so that both the
server code **and** any external tools/tests can import them without
dragging in additional heavy dependencies (e.g. FastAPI/FastMCP).
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import List, Optional

# ------------------------------------------------------------------
# Optional Pydantic dependency – most machines will have the real library
# installed but the execution environment for this assignment might not.
# In that case we fall back to a *very* thin shim that mimics just enough
# behaviour for the data-classes used in the server code.
# ------------------------------------------------------------------

try:
    from pydantic import BaseModel, Field  # type: ignore

except ModuleNotFoundError:  # pragma: no cover – shim only used in CI/Tests

    from typing import Any

    class BaseModel:  # type: ignore
        """Very small substitute for pydantic's BaseModel."""

        def __init__(self, **data: Any):
            cls = self.__class__
            hints = getattr(cls, "__annotations__", {})

            _UNSET = object()
            for field_name, _ in hints.items():
                default_value = getattr(cls, field_name, _UNSET)

                if field_name in data:
                    value = data[field_name]
                elif callable(default_value):  # default_factory returns callable in our Field stub
                    value = default_value()
                elif default_value is not _UNSET:
                    value = default_value
                else:
                    raise TypeError(f"Missing required field '{field_name}' for model '{cls.__name__}'")

                setattr(self, field_name, value)

        # pydantic v2 API
        def _convert(self, value):  # helper
            from datetime import datetime

            if isinstance(value, datetime):
                return value.isoformat()
            if isinstance(value, list):
                return [self._convert(v) for v in value]
            if isinstance(value, dict):
                return {k: self._convert(v) for k, v in value.items()}
            return value

        def model_dump(self):  # noqa: D401 – pydantic v2 API
            return {k: self._convert(v) for k, v in self.__dict__.items()}

        # pydantic v1 alias
        def dict(self):  # noqa: D401
            return self.model_dump()

        def __repr__(self):  # pragma: no cover – debugging convenience
            fields = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
            return f"<{self.__class__.__name__} {fields}>"

    def Field(*, default=None, default_factory=None):  # type: ignore
        """Return a *sentinel* that our `BaseModel` initialiser can handle.

        The sentinel is either the concrete default value or, in the case
        of a factory, a *callable* that, when invoked, yields the default
        value.
        """

        if default_factory is not None:
            return default_factory  # type: ignore
        return default


class TestCase(BaseModel):
    """Represents a Hercules test case."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    steps: List[str]
    expected_outcome: str
    created_at: datetime = Field(default_factory=datetime.now)
    file_path: Optional[str] = None  # Path to the generated test file


class TestResult(BaseModel):
    """Represents the outcome of executing a test case."""

    test_id: str
    test_name: str
    status: str  # "running", "passed", "failed", "error"
    logs: List[str] = Field(default_factory=list)
    screenshots: List[str] = Field(default_factory=list)
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
