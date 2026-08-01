from typing import Any
"""
Calendars module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeCalendar": ("pyffice.calendars.calendars", "PyfficeCalendar"),
    "PyfficeTimeUnit": ("pyffice.calendars.events", "PyfficeTimeUnit"),
    "PyfficeEvent": ("pyffice.calendars.events", "PyfficeEvent"),
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.calendars' has no attribute " + repr(name)
    )


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeCalendar",
    "PyfficeTimeUnit",
    "PyfficeEvent",
]
