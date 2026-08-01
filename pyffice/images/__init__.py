from typing import Any
"""
Images module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    "PyfficeImage": ("pyffice.images.images", "PyfficeImage"),
    "PyfficeImageManager": ("pyffice.images.images", "PyfficeImageManager"),
    "PyfficeScreenShot": ("pyffice.images.images", "PyfficeScreenShot"),
    "PyfficeColorPalette": ("pyffice.images.palettes", "PyfficeColorPalette"),
    "PyfficePDF": ("pyffice.images.pdfs", "PyfficePDF"),
    "PyfficeSketch": ("pyffice.images.sketches", "PyfficeSketch"),
    "hex_to_rgb": ("pyffice.images.utilities", "hex_to_rgb"),
    "rgb_to_hex": ("pyffice.images.utilities", "rgb_to_hex"),
    "rgb_to_hsl": ("pyffice.images.utilities", "rgb_to_hsl"),
    "hsl_to_rgb": ("pyffice.images.utilities", "hsl_to_rgb"),
    "is_similar_hue": ("pyffice.images.utilities", "is_similar_hue"),
    "convert_shades_of_color": ("pyffice.images.utilities", "convert_shades_of_color"),
    "convert_shades_of_color_in_svg": ("pyffice.images.utilities", "convert_shades_of_color_in_svg"),
    "convert_shades_of_color_in_jpg": ("pyffice.images.utilities", "convert_shades_of_color_in_jpg"),
    "convert_shades_of_color_in_png": ("pyffice.images.utilities", "convert_shades_of_color_in_png"),
    "check_image_type": ("pyffice.images.utilities", "check_image_type"),
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.images' has no attribute " + repr(name)
    )


def __dir__() -> Any:
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficeImage",
    "PyfficeImageManager",
    "PyfficeScreenShot",
    "PyfficeColorPalette",
    "PyfficePDF",
    "PyfficeSketch",
    "hex_to_rgb",
    "rgb_to_hex",
    "rgb_to_hsl",
    "hsl_to_rgb",
    "is_similar_hue",
    "convert_shades_of_color",
    "convert_shades_of_color_in_svg",
    "convert_shades_of_color_in_jpg",
    "convert_shades_of_color_in_png",
    "check_image_type",
]
