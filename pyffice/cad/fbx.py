"""FBX 3D model format support (Filmbox)."""
from typing import Any, Optional
import io


def load(path: str) -> bytes:
    """Load FBX file contents."""
    with open(path, 'rb') as f:
        return f.read()


def read(path: str) -> bytes:
    """Read FBX file contents."""
    return load(path)


def write(data: bytes, path: str) -> None:
    """Write data to FBX file."""
    with open(path, 'wb') as f:
        f.write(data)


def dump(data: bytes, path: str) -> None:
    """Dump data to FBX file."""
    write(data, path)
