"""
Pyffice reStructuredText Handler
"""
from pathlib import Path
from typing import List, Dict, Optional


def read(rst_path: str) -> str:
    """Read RST file."""
    with open(rst_path, "r") as f:
        return f.read()


def write(rst_path: str, content: str) -> None:
    """Write RST content to file."""
    with open(rst_path, "w") as f:
        f.write(content)


def extract_headings(rst_path: str) -> Dict[str, List[str]]:
    """Extract headings and their levels."""
    content = read(rst_path)
    headings = {}
    for line in content.split("\n"):
        if line.strip() and all(c in "=-~`+*" for c in line.strip()):
            continue
        if line.strip() and any(line.startswith(m) for m in "#*=-~"):
            continue
        for i, char in enumerate(line):
            if char in "=-~`+*":
                level = ["#", "*", "=", "-", "~", "`", "+"].index(char) + 1
                headings[line.strip()] = level
                break
    return headings


def extract_code_blocks(rst_path: str) -> List[Dict[str, str]]:
    """Extract code blocks with language hints."""
    content = read(rst_path)
    blocks = []
    in_block = False
    current_lang = ""
    current_lines = []
    
    for line in content.split("\n"):
        if line.strip().startswith(".. code::"):
            current_lang = line.strip().split("::", 1)[1].strip()
            in_block = True
            current_lines = []
        elif in_block and line.startswith(" "):
            current_lines.append(line)
        elif in_block:
            if current_lines:
                blocks.append({"language": current_lang, "code": "\n".join(current_lines)})
            in_block = False
    
    return blocks
