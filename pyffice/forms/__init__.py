"""
Forms module for pyffice.
"""

# T-NEW-051: lazy __getattr__ proxy to break circular imports
# when subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeForm": ("pyffice.forms.forms", "PyfficeForm"),
    "PyfficeFormsManager": ("pyffice.forms.forms", "PyfficeFormsManager"),
    "PyfficeSurvey": ("pyffice.forms.forms", "PyfficeSurvey"),
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
        "module 'pyffice.forms' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeForm",
    "PyfficeFormsManager",
    "PyfficeSurvey",
]
