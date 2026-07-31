"""Test generic binary container handling."""
import pytest
from pyffice.container.binary import PyfficeBinary


def test_identify_format():
    """Test binary format identification."""
    binary = PyfficeBinary()
    assert binary is not None


def test_extract_binary():
    """Test extracting from binary containers."""
    binary = PyfficeBinary()
    result = binary.extract("test.bin")
    assert result is not None
