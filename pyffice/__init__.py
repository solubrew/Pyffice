"""
Pyffice - Python wrapper for office suite tools

Comprehensive document and media framework supporting documents, spreadsheets,
presentations, diagrams, images, video, audio, CAD, and more.

T-NEW-005 (item 2): Pyffice class semver lives here. The
``__version__`` constant is the canonical source of truth for
serialization upgrade paths. When the wire format of any
PyfficeUnit / PyfficeDocument / PyfficeApplicationConfig
changes in a way that is not backward-compatible, bump the
``MINOR`` digit (or ``MAJOR`` for a breaking rewrite). The
``PATCH`` digit is reserved for serialization-compatible
fixes (e.g. clearer error messages, new optional fields).

The triple is intentionally expressed as ``(MAJOR, MINOR,
PATCH)`` so callers can compare programmatically:

    from pyffice import __version_info__
    if __version_info__ >= (0, 2, 0):
        ...
"""


from typing import Any

# Lazy __getattr__ proxy decouples package import from
# pyffice.pyffice import chain. Callers use PyfficeCodex
# directly (no Pyffice facade).
#
# Lazy import via __getattr__ (PEP 562) so the heavy import
# chain (pyffice.pyffice -> pyffice.document -> pyffice.tags.tags
# ...) doesn't trigger at package-load time. This avoids
# circular-import issues when other pyffice.<sub>.<sub> modules
# import from `pyffice` during their own initialization.
_LAZY_EXPORTS = {
    "PyfficeCodex": ("pyffice.pyffice", "PyfficeCodex"),
    "PyfficeCodexError": ("pyffice.pyffice", "PyfficeCodexError"),
    "DocumentNotFoundError": ("pyffice.pyffice", "DocumentNotFoundError"),
    "InitializationError": ("pyffice.pyffice", "InitializationError"),
}


def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(f"module 'pyffice' has no attribute {name!r}")


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))


__version_info__ = (0, 1, 0)
__version__ = ".".join(str(p) for p in __version_info__)

__all__ = [
    "__version__",
    "__version_info__",
    "PyfficeCodex",
    "PyfficeCodexError",
    "DocumentNotFoundError",
    "InitializationError",
]