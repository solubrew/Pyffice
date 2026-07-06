"""LaTeX document format support."""
from typing import Any, Optional
import io


def load(path: str) -> str:
    """Load LaTeX document contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read LaTeX document contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to LaTeX file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to LaTeX file."""
    write(data, path)
