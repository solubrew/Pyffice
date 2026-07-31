"""
Media module for pyffice.
"""

# T-NEW-051: lazy __getattr__ proxy to break circular imports
# when subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeHeic": ("pyffice.media.heic", "PyfficeHeic"),
    "MediaType": ("pyffice.media.media", "MediaType"),
    "MediaError": ("pyffice.media.media", "MediaError"),
    "Media": ("pyffice.media.media", "Media"),
    "MediaProcessor": ("pyffice.media.media", "MediaProcessor"),
    "load": ("pyffice.media.media_video", "load"),
    "read": ("pyffice.media.media_video", "read"),
    "write": ("pyffice.media.media_video", "write"),
    "dump": ("pyffice.media.media_video", "dump"),
    "load": ("pyffice.media.media_video", "load"),
    "read": ("pyffice.media.media_video", "read"),
    "write": ("pyffice.media.media_video", "write"),
    "dump": ("pyffice.media.media_video", "dump"),
    "PyfficeRaw": ("pyffice.media.raw", "PyfficeRaw"),
}

def __getattr__(name: str):
    if name in _LAZY_EXPORTS:
        import importlib
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = importlib.import_module(mod_path)
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.media' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeHeic",
    "MediaType",
    "MediaError",
    "Media",
    "MediaProcessor",
    "load",
    "read",
    "write",
    "dump",
    "load",
    "read",
    "write",
    "dump",
    "PyfficeRaw",
]
