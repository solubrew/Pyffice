"""Test pyffice.images.utilities import chain + color helpers.

The utilities module previously imported `from pyffice.pyffice import
PyfficeDocument` (wrong — pyffice.pyffice is a façade and does not
re-export PyfficeDocument). The fix is to import from pyffice.document.

Tests also assert on real color round-trips (hex ↔ rgb ↔ hsl).
"""
import pytest

import pyffice.images.utilities as utilities


def test_utilities_module_imports():
    """pyffice.images.utilities must import without ModuleNotFoundError or AttributeError."""
    assert utilities is not None


def test_utilities_module_is_registered():
    """Importing utilities registers it under pyffice.images."""
    import pyffice.images
    # The submodule must be reachable as an attribute after import.
    assert hasattr(pyffice.images, "utilities")


def test_hex_to_rgb_6digit():
    """hex_to_rgb('#ff8040') must return (255, 128, 64)."""
    assert utilities.hex_to_rgb("#ff8040") == (255, 128, 64)


def test_hex_to_rgb_strips_hash_prefix():
    """hex_to_rgb must accept input with or without the leading '#'."""
    assert utilities.hex_to_rgb("ff8040") == (255, 128, 64)


def test_rgb_to_hex_format():
    """rgb_to_hex must return lowercase '#rrggbb'."""
    assert utilities.rgb_to_hex((255, 128, 64)) == "#ff8040"


def test_hex_rgb_roundtrip():
    """hex → rgb → hex must return identical hex string."""
    original = "#abcdef"
    rgb = utilities.hex_to_rgb(original)
    assert utilities.rgb_to_hex(rgb) == original


def test_is_similar_hue_within_tolerance():
    """Hues within tolerance must be reported as similar."""
    # 359 and 1 are 2° apart (circular) — within tolerance of 5
    assert utilities.is_similar_hue(359, 1, 5) is True
    # 0 and 0 — identical, always similar
    assert utilities.is_similar_hue(0, 0, 0) is True


def test_is_similar_hue_outside_tolerance():
    """Hues beyond tolerance must NOT be reported as similar."""
    # 0 and 180 are 180° apart — outside any reasonable tolerance
    assert utilities.is_similar_hue(0, 180, 5) is False


def test_rgb_hsl_roundtrip_red():
    """rgb_to_hsl → hsl_to_rgb for pure red must return (255, 0, 0)."""
    h, s, l = utilities.rgb_to_hsl(255, 0, 0)
    rgb = utilities.hsl_to_rgb(h, s, l)
    assert rgb == (255, 0, 0)

