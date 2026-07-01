"""Pyffice Skills Module

Provides skill management and capability framework for Pyffice.
Skills allow extending Pyffice functionality with custom behaviors.
"""

from pyffice.skills.skills import (
    PyfficeSkill,
    PyfficeSkillManager,
    PyfficeCapability,
    SkillRegistry,
)

__all__ = [
    "PyfficeSkill",
    "PyfficeSkillManager", 
    "PyfficeCapability",
    "SkillRegistry",
]
