"""
Pyffice LaTeX Handler
"""
import subprocess
from pathlib import Path
from typing import Optional, List, Dict


def create(tex_path: str, content: str) -> None:
    """Write LaTeX content to file."""
    with open(tex_path, "w") as f:
        f.write(content)


def read(tex_path: str) -> str:
    """Read LaTeX file content."""
    with open(tex_path, "r") as f:
        return f.read()


def compile(tex_path: str, output_dir: Optional[str] = None) -> str:
    """Compile LaTeX to PDF using pdflatex."""
    tex_file = Path(tex_path)
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = tex_file.parent
    
    cmd = ["pdflatex", "-interaction=nonstopmode", "-output-directory", str(out_dir), str(tex_file)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    pdf_path = out_dir / tex_file.with_suffix(".pdf").name
    return str(pdf_path) if pdf_path.exists() else ""


def extract_commands(tex_path: str) -> List[str]:
    """Extract LaTeX commands from file."""
    import re
    content = read(tex_path)
    commands = re.findall(r'\\(\w+)(?:\[.*?\])?\{.*?\}', content)
    return list(set(commands))


def extract_references(tex_path: str) -> Dict[str, List[str]]:
    """Extract labels and references."""
    import re
    content = read(tex_path)
    
    labels = re.findall(r'\\label\{([^}]+)\}', content)
    refs = re.findall(r'\\ref\{([^}]+)\}', content)
    cites = re.findall(r'\\cite\{([^}]+)\}', content)
    
    return {"labels": labels, "refs": refs, "cites": cites}
