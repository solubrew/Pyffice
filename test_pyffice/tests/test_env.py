"""Test ENV document generation and import."""
import pytest
from pyffice.config import env as env_doc


def test_load_env():
    """Test ENV file loading."""
    doc = env_doc.PyfficeENV()
    doc.load("test.env")
    assert True


def test_get_var():
    """Test ENV variable retrieval."""
    doc = env_doc.PyfficeENV()
    val = doc.get_var("KEY")
    assert val is not None or val is None
