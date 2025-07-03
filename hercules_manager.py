"""Compatibility wrapper.

Historically the *HerculesManager* class lived in the project root.  To
keep backwards-compatibility (and to make life easier for any automated
tests that still import it from the old location) we forward all imports
to the new canonical implementation in **src.hercules_manager**.
"""

from src.hercules_manager import *  # noqa: F401,F403 – re-export everything

