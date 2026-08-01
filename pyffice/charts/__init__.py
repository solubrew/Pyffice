from typing import Any
"""
Charts module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeChart": ("pyffice.charts.charts", "PyfficeChart"),
    "SankeyChart": ("pyffice.charts.sankey", "SankeyChart"),
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.charts' has no attribute " + repr(name)
    )


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeChart",
    "SankeyChart",
]
