"""AsciiDoc format support."""
from typing import Any, Optional
import io


def load(path: str) -> str:
    """Load AsciiDoc document contents."""
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()


def read(path: str) -> str:
    """Read AsciiDoc document contents."""
    return load(path)


def write(data: str, path: str) -> None:
    """Write data to AsciiDoc file."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def dump(data: str, path: str) -> None:
    """Dump data to AsciiDoc file."""
    write(data, path)
