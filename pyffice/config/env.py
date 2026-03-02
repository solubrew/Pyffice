"""
Pyffice ENV Config Handler
"""

import os
from pathlib import Path
from typing import Dict, Optional


def load(filepath: str = ".env", encoding: str = "utf-8") -> Dict[str, str]:
    """Load .env file and return dictionary of environment variables."""
    env = {}
    path = Path(filepath)
    if not path.exists():
        return env
    
    with open(filepath, "r", encoding=encoding) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip("\"'")
                env[key] = value
    return env


def read(filepath: str = ".env") -> Dict[str, str]:
    """Alias for load."""
    return load(filepath)


def setenv(env: Dict[str, str]) -> None:
    """Set environment variables from dictionary."""
    for key, value in env.items():
        os.environ[key] = value


def get(key: str, fallback: Optional[str] = None) -> Optional[str]:
    """Get environment variable."""
    return os.environ.get(key, fallback)


def set(key: str, value: str) -> None:
    """Set environment variable."""
    os.environ[key] = value


def write(filepath: str, env: Dict[str, str]) -> None:
    """Write dictionary to .env file."""
    with open(filepath, "w") as f:
        for key, value in env.items():
            f.write(f'{key}="{value}"\n')
