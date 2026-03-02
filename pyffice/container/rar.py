"""
Pyffice RAR Container Handler
"""

import subprocess
from pathlib import Path
from typing import List


def compress(source: str, output: str) -> None:
    """Compress file or directory to RAR using unrar."""
    cmd = ["rar", "a", "-r", output, source]
    subprocess.run(cmd, check=True, capture_output=True)


def extract(rar_path: str, output_dir: str) -> None:
    """Extract RAR archive."""
    cmd = ["unrar", "x", "-o+", rar_path, output_dir]
    subprocess.run(cmd, check=True, capture_output=True)


def list_files(rar_path: str) -> List[str]:
    """List files in RAR archive."""
    cmd = ["unrar", "l", rar_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    files = []
    for line in result.stdout.split("\n"):
        if not line.startswith(" "):
            continue
        parts = line.split()
        if len(parts) >= 5 and parts[0].replace(",", "").isdigit():
            files.append(" ".join(parts[4:]))
    return [f for f in files if f]
