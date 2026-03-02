"""
Pyffice AsciiDoc Handler
"""
from pathlib import Path
from typing import List, Dict


def read(ad_path: str) -> str:
    """Read AsciiDoc file."""
    with open(ad_path, "r") as f:
        return f.read()


def write(ad_path: str, content: str) -> None:
    """Write AsciiDoc content to file."""
    with open(ad_path, "w") as f:
        f.write(content)


def extract_sections(ad_path: str) -> Dict[str, str]:
    """Extract sections and their content."""
    content = read(ad_path)
    sections = {}
    current_title = "intro"
    current_content = []
    
    for line in content.split("\n"):
        if line.strip().startswith("== "):
            if current_content:
                sections[current_title] = "\n".join(current_content)
            current_title = line.strip()[3:]
            current_content = []
        else:
            current_content.append(line)
    
    if current_content:
        sections[current_title] = "\n".join(current_content)
    
    return sections


def extract_code_blocks(ad_path: str) -> List[Dict[str, str]]:
    """Extract code blocks with language hints."""
    content = read(ad_path)
    blocks = []
    in_block = False
    current_lang = ""
    current_lines = []
    
    for line in content.split("\n"):
        if line.strip().startswith("[source,"):
            current_lang = line.strip().split(",")[1].strip("]")
            in_block = True
            current_lines = []
        elif in_block and line.startswith("----"):
            if current_lines:
                blocks.append({"language": current_lang, "code": "\n".join(current_lines)})
            in_block = False
        elif in_block:
            current_lines.append(line)
    
    return blocks
