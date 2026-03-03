"""
Pyffice - Polygot Office Document Package

Creates YAML versions of office files with bidirectional conversion.
AI Agent enhanced with tool-ready functions.
"""

__version__ = "0.0.1.0.1.0"

# Core classes
from pyffice.pyffice import PyfficeCodex
from pyffice.document import PyfficeDocument, PyfficeDocumentManager

# AI Agent interface
from pyffice import agent
from pyffice.agent import (
    create_codex,
    to_yaml,
    from_yaml,
    to_summary,
    to_json_schema,
    to_chunks,
    save,
    TOOL_DEFINITIONS,
)

__all__ = [
    # Core
    "PyfficeCodex",
    "PyfficeDocument",
    "PyfficeDocumentManager",
    # Agent interface
    "create_codex",
    "to_yaml",
    "from_yaml",
    "to_summary",
    "to_json_schema",
    "to_chunks",
    "save",
    "TOOL_DEFINITIONS",
    "agent",
    # CLI
    "cli",
]

# CLI entry point
from pyffice import cli
