"""
Pyffice Skills Module (placeholder).

Provides skill management and capability framework for Pyffice.
Skills allow extending Pyffice functionality with custom behaviors.

This module is a PLACEHOLDER. The classes listed below
(PyfficeSkill, PyfficeSkillManager, PyfficeCapability, SkillRegistry)
are referenced by `__init__.py` re-exports but are NOT yet defined
in `pyffice/skills/skills.py` — the underlying protocol design is
tracked under T-NEW-054 (open) and T-NEW-066 step 4 (open).

Until the design is decided and the classes are implemented, this
module MUST remain importable (no eager imports), so the rest of
the CLI / codex can load. See T-NEW-067 for the future-sprint
implementation card.
"""

# Lazy __getattr__ proxy (PEP 562) — the eager `from pyffice.skills.skills
# import PyfficeSkill, PyfficeSkillManager, PyfficeCapability, SkillRegistry`
# pattern was broken because skills.py defines none of those classes.
# When the placeholder is closed (T-NEW-067), restore the eager pattern
# (or keep the lazy proxy — either works).
_LAZY_EXPORTS = {
    "PyfficeSkill": ("pyffice.skills.skills", "PyfficeSkill"),
    "PyfficeSkillManager": ("pyffice.skills.skills", "PyfficeSkillManager"),
    "PyfficeCapability": ("pyffice.skills.skills", "PyfficeCapability"),
    "SkillRegistry": ("pyffice.skills.skills", "SkillRegistry"),
}


def __getattr__(name: str):
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.skills' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))


__all__ = [
    "PyfficeSkill",
    "PyfficeSkillManager",
    "PyfficeCapability",
    "SkillRegistry",
]
