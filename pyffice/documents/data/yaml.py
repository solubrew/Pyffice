"""Pyffice YAML Data Module

Provides YAML parsing and manipulation capabilities.
"""

from dataclasses import dataclass, field
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


@dataclass
class PyfficeYAMLConfig:
    """Configuration for YAML operations."""
    indent: int = 2
    width: int = 120
    sort_keys: bool = False
    allow_unicode: bool = True


class PyfficeYAML:
    """YAML parser and manipulator for Pyffice.
    
    Provides utilities for parsing, creating, and manipulating YAML documents.
    """
    
    def __init__(self, source: str | None = None, content: str | None = None):
        """Initialize PyfficeYAML.
        
        Args:
            source: File path to YAML document
            content: YAML content as string
        """
        self.source = source
        self.content = content
        self.data: dict = {}
        self.config = PyfficeYAMLConfig()
        
        if source and not content:
            self.load_file(source)
        elif content:
            self.parse(content)

    def parse(self, content: str) -> 'PyfficeYAML':
        """Parse YAML content string.
        
        Args:
            content: YAML content as string
            
        Returns:
            Self for chaining
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        self.data = yaml.safe_load(content)
        self.content = content
        return self

    def load_file(self, filepath: str) -> 'PyfficeYAML':
        """Load YAML from file.
        
        Args:
            filepath: Path to YAML file
            
        Returns:
            Self for chaining
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        with open(filepath, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f) or {}
        self.source = filepath
        return self

    def to_string(self, pretty: bool = True) -> str:
        """Convert data to YAML string.
        
        Args:
            pretty: Enable pretty printing
            
        Returns:
            YAML as string
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        
        if pretty:
            return yaml.dump(
                self.data,
                indent=self.config.indent,
                width=self.config.width,
                sort_keys=self.config.sort_keys,
                allow_unicode=self.config.allow_unicode,
                default_flow_style=False
            )
        return yaml.dump(self.data, allow_unicode=self.config.allow_unicode)

    def save(self, filepath: str) -> None:
        """Save YAML to file.
        
        Args:
            filepath: Output file path
        """
        content = self.to_string()
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def get(self, key: str, default: Any = None) -> Any:
        """Get value by key with dot notation support.
        
        Args:
            key: Key path (e.g., 'database.host')
            default: Default value if key not found
            
        Returns:
            Value or default
        """
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value if value is not None else default

    def set(self, key: str, value: Any) -> 'PyfficeYAML':
        """Set value by key with dot notation support.
        
        Args:
            key: Key path (e.g., 'database.host')
            value: Value to set
            
        Returns:
            Self for chaining
        """
        keys = key.split('.')
        data = self.data
        
        for k in keys[:-1]:
            if k not in data:
                data[k] = {}
            data = data[k]
        
        data[keys[-1]] = value
        return self

    def merge(self, other: dict) -> 'PyfficeYAML':
        """Merge another dictionary into data.
        
        Args:
            other: Dictionary to merge
            
        Returns:
            Self for chaining
        """
        self.data = self._deep_merge(self.data, other)
        return self

    def _deep_merge(self, base: dict, override: dict) -> dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    @staticmethod
    def from_dict(data: dict) -> 'PyfficeYAML':
        """Create PyfficeYAML from dictionary.
        
        Args:
            data: Dictionary to convert
            
        Returns:
            PyfficeYAML instance
        """
        yaml_obj = PyfficeYAML()
        yaml_obj.data = data
        return yaml_obj

    @staticmethod
    def from_json(json_obj: Any) -> 'PyfficeYAML':
        """Convert JSON object to YAML.
        
        Args:
            json_obj: JSON-like object
            
        Returns:
            PyfficeYAML instance
        """
        return PyfficeYAML.from_dict(json_obj)

    @staticmethod
    def load_multiple(filepath: str) -> list['PyfficeYAML']:
        """Load multiple YAML documents from single file.
        
        Args:
            filepath: Path to YAML file with multiple documents
            
        Returns:
            List of PyfficeYAML instances
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            documents = yaml.safe_load_all(f)
        
        return [PyfficeYAML.from_dict(doc) for doc in documents if doc]

    def validate_schema(self, schema: dict) -> tuple[bool, list[str]]:
        """Validate data against a schema.
        
        Args:
            schema: Schema definition
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        def validate(value: Any, path: str, schema_def: dict) -> None:
            required_type = schema_def.get('type')
            required_fields = schema_def.get('fields', {})
            
            if required_type == 'dict' and not isinstance(value, dict):
                errors.append(f"{path}: expected dict, got {type(value).__name__}")
            elif required_type == 'list' and not isinstance(value, list):
                errors.append(f"{path}: expected list, got {type(value).__name__}")
            elif required_type == 'str' and not isinstance(value, str):
                errors.append(f"{path}: expected str, got {type(value).__name__}")
            elif required_type == 'int' and not isinstance(value, int):
                errors.append(f"{path}: expected int, got {type(value).__name__}")
            elif required_type == 'float' and not isinstance(value, (int, float)):
                errors.append(f"{path}: expected float, got {type(value).__name__}")
            
            for field_name, field_schema in required_fields.items():
                if field_name in value:
                    validate(value[field_name], f"{path}.{field_name}", field_schema)
        
        validate(self.data, "root", schema)
        return (len(errors) == 0, errors)
