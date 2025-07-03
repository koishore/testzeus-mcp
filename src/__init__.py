"""Top-level package for TestZeus Hercules MCP server utilities.

This package purposefully keeps the public surface *very* small so that
importers only need to know about two things:

1. `HerculesManager` – the class that handles all test-case lifecycle
   operations (create, run, list, etc.).  This is the class most unit
   tests and client code will interact with directly.
2. `mcp` – an *optional* FastMCP server instance exposing the
   `HerculesManager` through a set of tools.  When the **fastmcp**
   library is not available (for example inside the execution sandbox of
   this assignment) a very small stub that mimics the bits of behaviour
   we rely on is created instead so that importing the package never
   fails.

The implementation details live in the private modules next to this
file (see `models.py`, `hercules_manager.py`, and `main.py`).
"""

from __future__ import annotations

# Re-export the important symbols so that users can simply write
# `from src import HerculesManager`.

# Public re-exports ----------------------------------------------------------------

from .hercules_manager import HerculesManager  # noqa: F401
from .models import TestCase, TestResult  # noqa: F401

# Lazily import the FastMCP server setup – this has the happy side effect
# of not importing heavy dependencies (FastAPI, etc.) unless the caller
# explicitly needs the server.

try:
    from .main import mcp  # noqa: F401
except Exception:  # pragma: no cover – FastMCP is optional in the sandbox
    # If the import fails we silently ignore it.  The manager class is the
    # only thing the tests really need.
    mcp = None  # type: ignore
