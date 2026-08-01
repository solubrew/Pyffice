from typing import Any
"""
Tags module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeTagsManager": ("pyffice.tags.manager", "PyfficeTagsManager"),
    "PyfficeRating": ("pyffice.tags.ratings", "PyfficeRating"),
    "PyfficeReference": ("pyffice.tags.references", "PyfficeReference"),
    "PyfficeTag": ("pyffice.tags.tags", "PyfficeTag"),
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.tags' has no attribute " + repr(name)
    )


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeTagsManager",
    "PyfficeRating",
    "PyfficeReference",
    "PyfficeTag",
]
