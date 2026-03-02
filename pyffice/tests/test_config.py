"""Test config module."""
import pytest
from pyffice.config.config import PyfficeConfig


def test_load():
    """Test config loading."""
    config = PyfficeConfig()
    assert config is not None
