from typing import Any
"""
Databases module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeDatabaseConnection": ("pyffice.databases.databases", "PyfficeDatabaseConnection"),
    "PyfficeDatabaseManager": ("pyffice.databases.databases", "PyfficeDatabaseManager"),
    # NOTE: PyfficeTable is NOT re-exported here. The canonical
    # implementation lives at pyffice.items.items:PyfficeTable
    # (PyfficeUnit base, used by sources.py / ports.py / images.py
    # / matrix.py / colors.py). The phantom PyfficeDocument-based
    # PyfficeTable in databases/table.py is unused and was removed.
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.databases' has no attribute " + repr(name)
    )


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeDatabaseConnection",
    "PyfficeDatabaseManager",
]
