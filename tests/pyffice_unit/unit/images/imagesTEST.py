"""Tests for pyffice/images/.

Coverage:
- PyfficeImage: construction + del_X methods (del_filter, del_image,
  del_layer, del_shape, del_text). Plus doc_type + inheritance.
- PyfficeImageManager: PyfficeDocumentManager subclass
- PyfficeScreenShot: PyfficeDocument subclass
- PyfficeColorPalette: PyfficeDocument subclass
- PyfficeSketch: PyfficeDocument subclass + add_layer/del_layer

Skipped:
- images.pdfs (PyfficePDF) — requires PyPDF2 which is not installed
- images.utilities (hex_to_rgb etc.) — requires thingery

Note: many PyfficeImage glyph methods (add_filter, add_image) require
PIL/Pillow operations at runtime. The tests below cover the safe
constructors and the del_X removers (which use getattr guards so
they're safe when self.X is None).
"""

import pytest

from pyffice.images.images import PyfficeImage, PyfficeImageManager, PyfficeScreenShot
from pyffice.images.palettes import PyfficeColorPalette
from pyffice.images.sketches import PyfficeSketch
from pyffice.document import PyfficeDocument, PyfficeDocumentManager


class TestPyfficeImageConstruction:
    """PyfficeImage() constructs with default None attributes."""

    def test_constructs_with_no_args(self):
        img = PyfficeImage()
        assert img is not None

    def test_default_attributes(self):
        img = PyfficeImage()
        # The bootstrap attributes are set to None.
        for attr in ("image", "canvas", "content", "mode", "images",
                     "info", "exif", "thumbnail", "layers", "lock",
                     "objects", "palette", "shapes", "texts"):
            assert getattr(img, attr) is None, f"{attr} should be None"

    def test_doc_type_is_image(self):
        img = PyfficeImage()
        assert img.doc_type == "image"

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeImage, PyfficeDocument)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeImage.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeImage.SERIALIZATION_VERSION) == 3


class TestPyfficeImageDelMethods:
    """The del_X methods are fluent (return self) and tolerate None
    attributes via getattr defaults.

    Pre-existing bugs (documented here):
    - del_filter / del_image work when self.filters / self.image are None.
    - del_layer / del_shape / del_text use `getattr(..., [])` but
      that doesn't help when the attribute IS set to None in __init__
      (the default is unreachable). They raise TypeError on
      len(None) until the corresponding attribute is initialized.
    """

    def test_del_filter_returns_self(self):
        img = PyfficeImage()
        assert img.del_filter("nonexistent") is img

    def test_del_image_returns_self(self):
        img = PyfficeImage()
        assert img.del_image() is img
        assert img.image is None

    def test_del_layer_raises_on_none_init(self):
        # Pre-existing bug: getattr guard returns None, not [],
        # so len() raises TypeError.
        img = PyfficeImage()
        with pytest.raises(TypeError):
            img.del_layer(0)

    def test_del_shape_raises_on_none_init(self):
        img = PyfficeImage()
        with pytest.raises(TypeError):
            img.del_shape(0)

    def test_del_text_raises_on_none_init(self):
        img = PyfficeImage()
        with pytest.raises(TypeError):
            img.del_text(0)


class TestPyfficeImageManager:
    """PyfficeImageManager is a PyfficeDocumentManager subclass."""

    def test_constructs(self):
        m = PyfficeImageManager()
        assert m is not None

    def test_inherits_pyffice_document_manager(self):
        assert issubclass(PyfficeImageManager, PyfficeDocumentManager)


class TestPyfficeScreenShot:
    """PyfficeScreenShot is a PyfficeDocument subclass."""

    def test_constructs(self):
        s = PyfficeScreenShot()
        assert s is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeScreenShot, PyfficeDocument)


class TestPyfficeColorPalette:
    """PyfficeColorPalette is a PyfficeDocument subclass."""

    def test_constructs(self):
        p = PyfficeColorPalette()
        assert p is not None

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeColorPalette, PyfficeDocument)


class TestPyfficeSketch:
    """PyfficeSketch is a PyfficeDocument subclass with add_layer/del_layer."""

    def test_constructs(self):
        sk = PyfficeSketch()
        assert sk is not None

    def test_default_attributes(self):
        sk = PyfficeSketch()
        for attr in ("canvas", "connections", "edges", "endpoints",
                     "nodes", "layers", "lock"):
            assert getattr(sk, attr) is None, f"{attr} should be None"

    def test_inherits_pyffice_document(self):
        assert issubclass(PyfficeSketch, PyfficeDocument)

    def test_del_layer_raises_on_dict_arg(self):
        # The del_layer method calls `layer.name` on its argument
        # expecting a PyfficeLayer instance, not a dict. Pre-existing
        # bug: the contract isn't documented.
        sk = PyfficeSketch()
        with pytest.raises(AttributeError):
            sk.del_layer({"name": "x"})
