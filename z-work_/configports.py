"""
Pyffice Config Ports - External format converters for configuration data.
"""
from pyffice.config.config import PyfficeConfig
from pyffice.ports.ports import PyfficePort


class JSONConfigPort(PyfficePort):
    """Port for JSON configuration format."""

    def read(self, file_path: str) -> PyfficeConfig:
        """Read JSON config file and convert to PyfficeConfig."""
        pass

    def write(self, config: PyfficeConfig, file_path: str) -> None:
        """Write PyfficeConfig to JSON file."""
        pass


class YAMLConfigPort(PyfficePort):
    """Port for YAML configuration format."""

    def read(self, file_path: str) -> PyfficeConfig:
        """Read YAML config file and convert to PyfficeConfig."""
        pass

    def write(self, config: PyfficeConfig, file_path: str) -> None:
        """Write PyfficeConfig to YAML file."""
        pass


class TOMLConfigPort(PyfficePort):
    """Port for TOML configuration format."""

    def read(self, file_path: str) -> PyfficeConfig:
        """Read TOML config file and convert to PyfficeConfig."""
        pass

    def write(self, config: PyfficeConfig, file_path: str) -> None:
        """Write PyfficeConfig to TOML file."""
        pass


class INIPort(PyfficePort):
    """Port for INI configuration format."""

    def read(self, file_path: str) -> PyfficeConfig:
        """Read INI config file and convert to PyfficeConfig."""
        pass

    def write(self, config: PyfficeConfig, file_path: str) -> None:
        """Write PyfficeConfig to INI file."""
        pass
