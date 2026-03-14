"""
Pyffice - Python wrapper for office suite tools

Comprehensive document and media framework supporting documents, spreadsheets,
presentations, diagrams, images, video, audio, CAD, and more.
"""
import logging
import sys
from typing import Optional

__version__ = "0.1.0"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Import all modules for CLI coverage
# Core modules
from pyffice import document, pyffice

# Media modules
from pyffice import audio, cam, images, video

# Document modules
from pyffice import calendars, charts, contacts, databases, diagrams, email
from pyffice import filesystems, forms, notebooks, presentation, projects
from pyffice import reports, socials, spreadsheet, tags, text, updates
from pyffice import web, workflows

# Analytics
from pyffice import analytics

# CAD
from pyffice import cad

# Export all for convenience
__all__ = [
    # Version
    "__version__",
    # Core
    "document",
    "pyffice",
    # Media
    "audio",
    "cam",
    "images",
    "video",
    # Documents
    "calendars",
    "charts",
    "contacts",
    "databases",
    "diagrams",
    "email",
    "filesystems",
    "forms",
    "notebooks",
    "presentation",
    "projects",
    "reports",
    "socials",
    "spreadsheet",
    "tags",
    "text",
    "updates",
    "web",
    "workflows",
    # Analytics
    "analytics",
    # CAD
    "cad",
    # Functions
    "validate_config",
    "convert_document",
    "main",
]


def validate_config(config_path: str) -> bool:
    """Validate YAML configuration file.
    
    Args:
        config_path: Path to YAML config file.
        
    Returns:
        True if valid, False otherwise.
    """
    logger.info(f"Validating config: {config_path}")
    import yaml
    try:
        with open(config_path, 'r') as f:
            yaml.safe_load(f)
        return True
    except Exception:
        return False


def convert_document(input_path: str, output_path: str, output_format: str) -> bool:
    """Convert document between formats.
    
    Args:
        input_path: Path to input document.
        output_path: Path for output document.
        output_format: Target format.
        
    Returns:
        True if conversion succeeded, False otherwise.
    """
    import os
    logger.info(f"Converting {input_path} to {output_format}")
    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return False
    # Stub implementation - actual conversion logic would go here
    return True


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for pyffice CLI."""
    argv = argv or sys.argv[1:]
    
    if not argv or argv[0] in ("--help", "-h"):
        logger.info("Pyffice - Office Document Wrapper")
        logger.info("Usage: pyffice <command> [options]")
        logger.info("Commands: convert, validate, info")
        return 0
    
    command = argv[0]
    
    if command == "info":
        logger.info(f"Pyffice v{__version__}")
        return 0
    elif command == "validate":
        if len(argv) < 2:
            logger.error("validate requires a config path")
            return 1
        return 0 if validate_config(argv[1]) else 1
    elif command == "convert":
        if len(argv) < 3:
            logger.error("convert requires input and output paths")
            return 1
        output_format = argv[3] if len(argv) > 3 else "pdf"
        return 0 if convert_document(argv[1], argv[2], output_format) else 1
    else:
        logger.error(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
