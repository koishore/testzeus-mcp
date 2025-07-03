#!/usr/bin/env python3
"""Convenience wrapper that simply executes the *root level* demo script.

The logic itself lives in the repository root so that users can run:

    $ python demo_script.py

or

    $ ./scripts/demo_script.py

Both commands yield the same behaviour which is handy for quick testing
and for CI pipelines that rely on the **scripts/** directory specified
in the project documentation.
"""

import runpy
from pathlib import Path


RUNNER = Path(__file__).resolve().parent.parent / "demo_script.py"

if __name__ == "__main__":
    runpy.run_path(str(RUNNER), run_name="__main__")

