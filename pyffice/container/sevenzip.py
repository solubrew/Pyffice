"""
Pyffice 7-Zip Container Handler
"""

import subprocess
from pathlib import Path
from typing import List


def compress(source: str, output: str, compression_level: int = 5) -> None:
    """Compress file or directory to 7z."""
    cmd = ["7z", "a", f"-mx={compression_level}", output, source]
    subprocess.run(cmd, check=True, capture_output=True)


def extract(sz_path: str, output_dir: str) -> None:
    """Extract 7z archive."""
    cmd = ["7z", "x", f"-o{output_dir}", "-y", sz_path]
    subprocess.run(cmd, check=True, capture_output=True)


def list_files(sz_path: str) -> List[str]:
    """List files in 7z archive."""
    cmd = ["7z", "l", sz_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    files = []
    for line in result.stdout.split("\n"):
        parts = line.split()
        if len(parts) >= 5 and not parts[0].startswith("-"):
            try:
                if parts[0].replace("-", "").isdigit():
                    files.append(" ".join(parts[4:]))
            except:
                pass
    return [f for f in files if f and f != "..."]


def add(sz_path: str, file_path: str) -> None:
    """Add file to existing 7z archive."""
    cmd = ["7z", "a", sz_path, file_path]
    subprocess.run(cmd, check=True, capture_output=True)
