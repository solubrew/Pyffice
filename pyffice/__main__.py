"""Enable running pyffice as a module: python -m pyffice"""

from pyffice.cli import cli


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
        with open(config_path, "r") as f:
            yaml.safe_load(f)
        return True
    except (OSError, yaml.YAMLError):
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
        with open(config_path, "r") as f:
            yaml.safe_load(f)
        return True
    except (OSError, yaml.YAMLError):
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


if __name__ == "__main__":
    cli()
