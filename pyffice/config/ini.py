"""
Pyffice INI Config Handler
"""

import configparser
from pathlib import Path
from typing import Dict, Optional


def read(filepath: str, encoding: str = "utf-8") -> configparser.ConfigParser:
    """Read INI file and return ConfigParser object."""
    config = configparser.ConfigParser()
    config.read(filepath, encoding=encoding)
    return config


def load(filepath: str, encoding: str = "utf-8") -> Dict[str, Dict[str, str]]:
    """Read INI file and return as nested dictionary."""
    config = read(filepath, encoding)
    return {section: dict(config[section]) for section in config.sections()}


def write(filepath: str, data: Dict[str, Dict[str, str]], encoding: str = "utf-8") -> None:
    """Write dictionary to INI file."""
    config = configparser.ConfigParser()
    for section, values in data.items():
        if section.upper() == 'DEFAULT':
            continue
        config.add_section(section)
        for key, value in values.items():
            config.set(section, key, value)
    with open(filepath, "w", encoding=encoding) as f:
        config.write(f)


def get(config: configparser.ConfigParser, section: str, key: str, fallback: str = None) -> Optional[str]:
    """Get value from config."""
    return config.get(section, key, fallback=fallback)


def set(config: configparser.ConfigParser, section: str, key: str, value: str) -> None:
    """Set value in config."""
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, value)


def save(config: configparser.ConfigParser, filepath: str, encoding: str = "utf-8") -> None:
    """Save ConfigParser to file."""
    with open(filepath, "w", encoding=encoding) as f:
        config.write(f)
