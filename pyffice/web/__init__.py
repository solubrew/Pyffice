"""
Web module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeContext": ("pyffice.web.prompts", "PyfficeContext"),
    "PyfficePrompt": ("pyffice.web.prompts", "PyfficePrompt"),
    "PyfficeResponse": ("pyffice.web.prompts", "PyfficeResponse"),
    "PyfficePromptsManager": ("pyffice.web.prompts", "PyfficePromptsManager"),
    "PyfficeService": ("pyffice.web.services", "PyfficeService"),
    "PyfficeURL": ("pyffice.web.url", "PyfficeURL"),
    "PyfficeURLLibrary": ("pyffice.web.url", "PyfficeURLLibrary"),
    "PyfficeWebBrowser": ("pyffice.web.web", "PyfficeWebBrowser"),
    "PyfficeWebPage": ("pyffice.web.web", "PyfficeWebPage"),
    "PyfficeWebProfile": ("pyffice.web.web", "PyfficeWebProfile"),
    "PyfficeWebProfileManager": ("pyffice.web.web", "PyfficeWebProfileManager"),
}

def __getattr__(name: str):
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.web' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeContext",
    "PyfficePrompt",
    "PyfficeResponse",
    "PyfficePromptsManager",
    "PyfficeService",
    "PyfficeURL",
    "PyfficeURLLibrary",
    "PyfficeWebBrowser",
    "PyfficeWebPage",
    "PyfficeWebProfile",
    "PyfficeWebProfileManager",
]
