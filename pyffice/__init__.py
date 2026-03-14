"""
Pyffice - Python wrapper for office suite tools

CLI module providing command-line interface for pyffice operations.
"""
import logging
import sys
from typing import Optional

__version__ = "0.1.0"

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def main(argv: Optional[list[str]] = None) -> int:
    """Main entry point for pyffice CLI."""
    argv = argv or sys.argv[1:]
    
    if not argv or argv[0] in ("--help", "-h"):
        print("Pyffice - Office Document Wrapper")
        print("")
        print("Usage: pyffice <command> [options]")
        print("")
        print("Commands:")
        print("  convert    Convert between document formats")
        print("  validate   Validate YAML configuration")
        print("  info       Show pyffice information")
        print("")
        return 0
    
    command = argv[0]
    
    if command == "info":
        logger.info(f"Pyffice v{__version__}")
        print("Office document wrapper with YAML configuration")
        return 0
    elif command == "validate":
        logger.info("Validating configuration...")
        # TODO: implement validation
        return 0
    elif command == "convert":
        logger.info("Converting document...")
        # TODO: implement conversion
        return 0
    else:
        logger.error(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
