"""Pyffice skills module.

This module provides extensible skills for document processing and automation.
"""

from typing import Any, Callable, Protocol
from dataclasses import dataclass, field
from enum import Enum

__all__ = ["Skill", "SkillRegistry", "SkillCategory", "register_skill"]


class SkillCategory(Enum):
    """Categories for organizing skills."""
    PARSER = "parser"
    CONVERTER = "converter"
    VALIDATOR = "validator"
    GENERATOR = "generator"
    ANALYZER = "analyzer"
    TRANSFORMER = "transformer"


@dataclass
class Skill:
    """Represents a reusable skill capability."""
    name: str
    category: SkillCategory
    handler: Callable[..., Any]
    description: str = ""
    parameters: dict = field(default_factory=dict)
    enabled: bool = True
    
    def execute(self, *args, **kwargs) -> Any:
        """Execute the skill handler."""
        if not self.enabled:
            raise RuntimeError(f"Skill '{self.name}' is disabled")
        return self.handler(*args, **kwargs)


class SkillRegistry:
    """Central registry for all skills."""
    
    def __init__(self):
        self._skills: dict[str, Skill] = {}
        self._categories: dict[SkillCategory, list[str]] = {c: [] for c in SkillCategory}
    
    def register(self, skill: Skill) -> None:
        """Register a new skill."""
        self._skills[skill.name] = skill
        self._categories[skill.category].append(skill.name)
    
    def get(self, name: str) -> Skill | None:
        """Get a skill by name."""
        return self._skills.get(name)
    
    def list_by_category(self, category: SkillCategory) -> list[Skill]:
        """List all skills in a category."""
        return [self._skills[name] for name in self._categories[category] if name in self._skills]
    
    def list_all(self) -> list[Skill]:
        """List all registered skills."""
        return list(self._skills.values())


# Global registry instance
_registry = SkillRegistry()


def register_skill(
    name: str,
    category: SkillCategory,
    handler: Callable[..., Any],
    description: str = "",
    parameters: dict | None = None
) -> Skill:
    """Decorator to register a skill."""
    skill = Skill(
        name=name,
        category=category,
        handler=handler,
        description=description,
        parameters=parameters or {}
    )
    _registry.register(skill)
    return skill
