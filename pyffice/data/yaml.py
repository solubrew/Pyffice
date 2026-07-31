"""Pyffice YAML Data Module

Provides YAML parsing and manipulation capabilities.
"""

from typing import Any

from pyffice.data.base import PyfficeDictBase

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


class PyfficeYAML(PyfficeDictBase):
    """YAML parser and manipulator for Pyffice.
    
    Inherits common functionality from PyfficeDictBase:
    - Dot notation get/set/merge
    - Chainable methods
    """
    
    def __init__(self, source: str | None = None, content: str | None = None):
        """Initialize PyfficeYAML.
        
        Args:
            source: File path to YAML document
            content: YAML content as string
        """
        super().__init__()
        self.source = source
        self.content = content
        
        if source and not content:
            self.load_file(source)
        elif content:
            self.parse(content)

    def parse(self, content: str) -> "PyfficeYAML":
        """Parse YAML content string.
        
        Args:
            content: YAML content as string
            
        Returns:
            Self for chaining
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        self._data = yaml.safe_load(content)
        self.content = content
        return self

    def load_file(self, filepath: str) -> "PyfficeYAML":
        """Load YAML from file.
        
        Args:
            filepath: Path to YAML file
            
        Returns:
            Self for chaining
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        with open(filepath, "r", encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}
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
                self._data,
                indent=2,
                width=120,
                sort_keys=False,
                allow_unicode=True,
                default_flow_style=False
            )
        return yaml.dump(self._data, allow_unicode=True)

    def save(self, filepath: str) -> None:
        """Save YAML to file.
        
        Args:
            filepath: Output file path
        """
        content = self.to_string()
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def from_json(json_obj: Any) -> "PyfficeYAML":
        """Convert JSON object to YAML.
        
        Args:
            json_obj: JSON-like object
            
        Returns:
            PyfficeYAML instance
        """
        return PyfficeYAML.from_dict(json_obj)

    @staticmethod
    def load_multiple(filepath: str) -> list["PyfficeYAML"]:
        """Load multiple YAML documents from single file.
        
        Args:
            filepath: Path to YAML file with multiple documents
            
        Returns:
            List of PyfficeYAML instances
        """
        if not HAS_YAML:
            raise ImportError("yaml library is required")
        
        with open(filepath, "r", encoding="utf-8") as f:
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
            """Validate a value or configuration against the schema.
            
            Args:
                value: Parameter.
                path: Parameter.
                schema_def: Parameter.
            
            Returns:
                Self for chaining.
            """
            required_type = schema_def.get("type")
            required_fields = schema_def.get("fields", {})
            
            if required_type == "dict" and not isinstance(value, dict):
                errors.append(f"{path}: expected dict, got {type(value).__name__}")
            elif required_type == "list" and not isinstance(value, list):
                errors.append(f"{path}: expected list, got {type(value).__name__}")
            elif required_type == "str" and not isinstance(value, str):
                errors.append(f"{path}: expected str, got {type(value).__name__}")
            elif required_type == "int" and not isinstance(value, int):
                errors.append(f"{path}: expected int, got {type(value).__name__}")
            elif required_type == "float" and not isinstance(value, (int, float)):
                errors.append(f"{path}: expected float, got {type(value).__name__}")
            
            for field_name, field_schema in required_fields.items():
                if field_name in value:
                    validate(value[field_name], f"{path}.{field_name}", field_schema)
        
        validate(self._data, "root", schema)
        return (len(errors) == 0, errors)
