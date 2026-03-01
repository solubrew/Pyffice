"""
AI Agent Interface Layer for Pyffice.

This module provides LLM/AI agent-friendly methods for working with
office documents through PyfficeCodex.
"""

from typing import Any, Dict, List, Optional
from pyffice.pyffice import PyfficeCodex


def create_codex(config: Optional[Dict[str, Any]] = None) -> PyfficeCodex:
    """
    Create a PyfficeCodex instance.
    
    Args:
        config: Optional configuration dictionary
    
    Returns:
        PyfficeCodex instance
    """
    return PyfficeCodex(config)


def to_yaml(codex: PyfficeCodex) -> str:
    """
    Serialize a PyfficeCodex to YAML string.
    
    Args:
        codex: PyfficeCodex instance
    
    Returns:
        YAML string representation
    """
    return codex.to_yaml()


def from_yaml(yaml_string: str, config: Optional[Dict[str, Any]] = None) -> PyfficeCodex:
    """
    Create a PyfficeCodex from YAML string.
    
    Args:
        yaml_string: YAML representation of a codex
        config: Optional configuration dictionary
    
    Returns:
        PyfficeCodex instance
    """
    return PyfficeCodex.from_yaml(yaml_string, config)


def to_summary(codex: PyfficeCodex) -> Dict[str, Any]:
    """
    Get a token-efficient summary of the codex.
    
    Args:
        codex: PyfficeCodex instance
    
    Returns:
        Summary dictionary
    """
    return codex.to_summary()


def to_json_schema(codex: PyfficeCodex) -> Dict[str, Any]:
    """
    Get JSON Schema for validating LLM output.
    
    Args:
        codex: PyfficeCodex instance
    
    Returns:
        JSON Schema dictionary
    """
    return codex.to_json_schema()


def to_chunks(
    codex: PyfficeCodex,
    chunk_size: int = 1000,
    overlap: int = 100
) -> List[Dict[str, Any]]:
    """
    Split codex into embedding-ready chunks.
    
    Args:
        codex: PyfficeCodex instance
        chunk_size: Target size per chunk (default 1000)
        overlap: Overlap between chunks (default 100)
    
    Returns:
        List of chunk dictionaries with 'content' and 'metadata'
    """
    return codex.to_chunks(chunk_size, overlap)


def save(codex: PyfficeCodex, path: str = None, syntax: str = None) -> PyfficeCodex:
    """
    Save codex to file.
    
    Args:
        codex: PyfficeCodex instance
        path: Path to save to
        syntax: Format ('yaml', 'json')
    
    Returns:
        PyfficeCodex instance (for chaining)
    """
    return codex.save(path, syntax)


# Tool definitions for LLM function calling
TOOL_DEFINITIONS = [
    {
        "name": "pyffice_create_codex",
        "description": "Create a PyfficeCodex instance",
        "parameters": {
            "type": "object",
            "properties": {
                "config": {"type": "object", "description": "Optional configuration dictionary"}
            },
            "required": []
        }
    },
    {
        "name": "pyffice_to_yaml",
        "description": "Serialize codex to YAML string",
        "parameters": {
            "type": "object",
            "properties": {
                "codex": {"type": "object", "description": "PyfficeCodex instance"}
            },
            "required": ["codex"]
        }
    },
    {
        "name": "pyffice_from_yaml",
        "description": "Create codex from YAML string",
        "parameters": {
            "type": "object",
            "properties": {
                "yaml_string": {"type": "string", "description": "YAML representation"},
                "config": {"type": "object", "description": "Optional configuration"}
            },
            "required": ["yaml_string"]
        }
    },
    {
        "name": "pyffice_to_summary",
        "description": "Get token-efficient summary",
        "parameters": {
            "type": "object",
            "properties": {
                "codex": {"type": "object", "description": "PyfficeCodex instance"}
            },
            "required": ["codex"]
        }
    },
    {
        "name": "pyffice_to_json_schema",
        "description": "Get JSON Schema for validation",
        "parameters": {
            "type": "object",
            "properties": {
                "codex": {"type": "object", "description": "PyfficeCodex instance"}
            },
            "required": ["codex"]
        }
    },
    {
        "name": "pyffice_to_chunks",
        "description": "Split codex into embedding-ready chunks",
        "parameters": {
            "type": "object",
            "properties": {
                "codex": {"type": "object", "description": "PyfficeCodex instance"},
                "chunk_size": {"type": "integer", "description": "Chunk size (default 1000)"},
                "overlap": {"type": "integer", "description": "Overlap (default 100)"}
            },
            "required": ["codex"]
        }
    },
    {
        "name": "pyffice_save",
        "description": "Save codex to file",
        "parameters": {
            "type": "object",
            "properties": {
                "codex": {"type": "object", "description": "PyfficeCodex instance"},
                "path": {"type": "string", "description": "Output file path"},
                "syntax": {"type": "string", "description": "Format: yaml or json"}
            },
            "required": ["codex"]
        }
    }
]
