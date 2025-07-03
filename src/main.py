"""Entry-point that spins up a *FastMCP* server exposing the
`HerculesManager` through a handful of tools.

The implementation is largely copied from the original *server.py* file
but lives inside the **src/** package so that imports remain stable once
the repository matches the documented directory structure.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

# ------------------------------------------------------------------
# Optional FastMCP import – when the real library is unavailable we fall
# back to a dummy implementation that provides just enough behaviour for
# unit-tests to import `src.main` without exploding.  Running the actual
# server obviously requires the real package.
# ------------------------------------------------------------------


try:
    from fastmcp import FastMCP  # type: ignore

except ModuleNotFoundError:  # pragma: no cover

    class _FastMCPStub:  # pylint: disable=too-few-public-methods
        """Very small subset of the FastMCP API used in the project."""

        def __init__(self, name: str):
            self.name = name
            self._tools: Dict[str, Any] = {}

        # The real decorator supports params – we ignore them.
        def tool(self, *_, **__):  # noqa: D401
            def decorator(func):
                self._tools[func.__name__] = func
                return func

            return decorator

        def run(self, *_, **__):  # noqa: D401
            logging.warning(
                "FastMCP is not installed – the stub server will not listen "
                "for incoming connections.  Registered tools: %s",
                list(self._tools),
            )

    FastMCP = _FastMCPStub  # type: ignore  # noqa: N816 – mimic external class name


# ------------------------------------------------------------------
# Actual server implementation
# ------------------------------------------------------------------


from .hercules_manager import HerculesManager


logger = logging.getLogger(__name__)

mcp = FastMCP("TestZeus Hercules MCP Server")

_manager = HerculesManager()


# ------------------------------------------------------------------
# Tool definitions – these are intentionally *thin* wrappers around the
# corresponding HerculesManager methods so that tests can mock / inspect
# behaviour directly.
# ------------------------------------------------------------------


@mcp.tool()
def create_test_case(
    name: str,
    description: str,
    steps: List[str],
    expected_outcome: str,
) -> Dict[str, Any]:
    try:
# Use `.model_dump()` for Pydantic v2 and `.dict()` for v1 so the code
# remains compatible with either major version that might be present in
# the execution environment.
        case = _manager.create_test_case(
            name=name,
            description=description,
            steps=steps,
            expected_outcome=expected_outcome,
        )
        dump = case.model_dump() if hasattr(case, "model_dump") else case.dict()
        return {
            "success": True,
            "test_case": dump,
            "message": "Test case created successfully",
        }
    except Exception as exc:  # pragma: no cover – defensive
        logger.exception("Failed to create test-case")
        return {"success": False, "error": str(exc)}


@mcp.tool()
async def run_test(test_id: str) -> Dict[str, Any]:
    try:
        res = await _manager.run_test(test_id)
        dump = res.model_dump() if hasattr(res, "model_dump") else res.dict()
        return {"success": True, "result": dump}
    except Exception as exc:  # pragma: no cover
        logger.exception("Running test %s failed", test_id)
        return {"success": False, "error": str(exc)}


@mcp.tool()
def get_test_result(test_id: str) -> Dict[str, Any]:
    res = _manager.get_test_result(test_id)
    if res is None:
        return {"success": False, "message": "No result for given id"}
    dump = res.model_dump() if hasattr(res, "model_dump") else res.dict()
    return {"success": True, "result": dump}


@mcp.tool()
def list_test_cases() -> Dict[str, Any]:
    cases = _manager.list_test_cases()
    def _dump(obj):
        return obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()

    return {
        "success": True,
        "count": len(cases),
        "test_cases": [_dump(c) for c in cases],
    }


@mcp.tool()
def list_test_results() -> Dict[str, Any]:
    results = _manager.list_test_results()
    def _dump(obj):
        return obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()

    return {
        "success": True,
        "count": len(results),
        "results": [_dump(r) for r in results],
    }


@mcp.tool()
def get_test_status(test_id: str) -> Dict[str, Any]:
    res = _manager.get_test_result(test_id)
    if res is None:
        return {"success": False, "message": "Unknown test id"}

    return {
        "success": True,
        "status": res.status,
        "started_at": res.started_at.isoformat() if res.started_at else None,
        "completed_at": res.completed_at.isoformat() if res.completed_at else None,
        "execution_time": res.execution_time,
    }


# ------------------------------------------------------------------
# CLI helper – only executed when the module is run directly.
# ------------------------------------------------------------------


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    mcp.run()
