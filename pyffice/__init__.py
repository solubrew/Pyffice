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

    from pyffice import __version__
    if __version__ >= (0, 2, 0):
        ...
"""

__version_info__ = (0, 1, 0)
__version__ = ".".join(str(p) for p in __version_info__)
