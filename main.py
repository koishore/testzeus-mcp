"""Compatibility stub that simply delegates to *src.main*.

Having a *main.py* in the repository root allows quick one-liners such
as

    $ python main.py

to start the server while the canonical implementation lives in the
module package.
"""

from src.main import *  # noqa: F401,F403 – re-export everything

if __name__ == "__main__":
    from src.main import mcp  # pylint: disable=wrong-import-position

    mcp.run()

