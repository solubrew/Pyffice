"""
Pyffice TAR Container Handler
"""

import tarfile
from pathlib import Path
from typing import List


def compress(source: str, output: str, compression: str = "gz") -> None:
    """Compress file or directory to TAR."""
    mode = f"w:{compression}" if compression else "w"
    source_path = Path(source)
    with tarfile.open(output, mode) as tf:
        if source_path.is_file():
            tf.add(source, arcname=source_path.name)
        else:
            for file in source_path.rglob("*"):
                if file.is_file():
                    tf.add(file, arcname=file.relative_to(source_path))


def extract(tar_path: str, output_dir: str) -> None:
    """Extract TAR archive."""
    with tarfile.open(tar_path, "r:*") as tf:
        tf.extractall(output_dir)


def list_files(tar_path: str) -> List[str]:
    """List files in TAR archive."""
    with tarfile.open(tar_path, "r:*") as tf:
        return [m.name for m in tf.getmembers()]


def add(tar_path: str, file_path: str, arcname: str = None) -> None:
    """Add file to existing TAR."""
    with tarfile.open(tar_path, "a") as tf:
        tf.add(file_path, arcname=arcname or Path(file_path).name)
