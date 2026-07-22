# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid:
    name:
    description: >
    version: 0.0.0.0.0.0
    authority: filesystem
    security: seclvl2
    <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join, exists
import datetime as dt
import os
import re
from copy import deepcopy
from io import BytesIO
import json as j
import base64

# ======================================3rd Party Library Modules=====================================================||
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.images.palettes import PyfficeColorPalette
from pyffice.document import PyfficeDocument, PyfficeDocumentManager
from squirl.orgnql import fonql
from pyffice.items.items import PyfficeTable
from pycurity.pyhash import encode64, decode64

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = False
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
pxcfg = join(here, "_data_", "images.yaml")


class PyfficeImage(PyfficeDocument):
    """
    A class to work with images in various formats, supporting
    layers, shapes, tags, and other image operations.
    """

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """
        Initialize the image object.

        :param path: Path to the image file (optional).
        :param cfg: Additional configuration (optional).
        """
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeImage").override(cfg))
        self.image = None  # The main image
        self.canvas = None
        self.content = None
        self.mode = None
        self.images = None  # Embedded images
        self.info = None
        self.exif = None
        self.thumbnail = None
        self.layers = None  # List of image layers
        self.lock = None
        self.objects = None
        self.palette = None
        self.shapes = None  # Shape objects
        self.texts = None  # Text objects
        self.doc_type = "image"

    def add_filter(self, filter_type):
        """
        Apply a filter to the image (BLUR, CONTOUR, DETAIL, etc.).

        :param filter_type: An ImageFilter constant (e.g., ImageFilter.BLUR).
        :return: self
        """
        self.image = self.image.filter(filter_type)
        return self

    def add_image(self, image_path, x=0, y=0):
        """
        Add another image on top of the current image at the specified position.

        :param image_path: Path to the image to add.
        :param x: X-coordinate where the image starts.
        :param y: Y-coordinate where the image starts.
        :return: self
        """
        overlay = Image.open(image_path)
        self.image.paste(overlay, (x, y), overlay if overlay.mode == "RGBA" else None)
        return self

    def add_layer(self, layer_path=None):
        """
        Add a new image layer.

        :param layer_path: Path to the layer image (optional, creates a blank layer if None).
        :return: self
        """
        if layer_path:
            layer = Image.open(layer_path)
        else:
            layer = Image.new("RGBA", self.image.size, (255, 255, 255, 0))  # Transparent layer
        self.layers.append(layer)
        return self

    def add_shape(self, x, y, w, h, shape="rectangle", color="red"):
        """
        Add a shape to the image (rectangle or ellipse).

        :param x: X-coordinate for the top-left corner.
        :param y: Y-coordinate for the top-left corner.
        :param w: Width of the shape.
        :param h: Height of the shape.
        :param shape: Type of shape ('rectangle' or 'ellipse').
        :param color: Color of the shape.
        :return: self
        """
        draw = ImageDraw.Draw(self.image)
        if shape == "rectangle":
            draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
        elif shape == "ellipse":
            draw.ellipse([x, y, x + w, y + h], outline=color, width=3)
        self.shapes.append((x, y, w, h, shape, color))
        return self

    def add_tag(self, tag_name, tag_value):
        """"""

    def add_text(self, text, position=(10, 10), font_size=20, color="black", font_path=None):
        """
        Add text to the image.

        :param text: Text string to add.
        :param position: Tuple (x, y) where the text starts.
        :param font_size: Font size of the text.
        :param color: Font color.
        :param font_path: Path to a custom font (optional).
        :return: self
        """
        draw = ImageDraw.Draw(self.image)
        font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        draw.text(position, text, fill=color, font=font)
        self.texts.append((text, position, font_size, color))
        return self

    def create_thumbnail(self, size=(128, 128)):
        """
        Generate a thumbnail image.

        :param size: Tuple (width, height) for the thumbnail size.
        :return: self
        """
        self.thumbnail = self.image.copy()
        self.thumbnail.thumbnail(size)
        return self

    def del_filter(self):
        """"""

    def del_image(self):
        """"""

    def del_layer(self):
        """"""

    def del_shape(self):
        """"""

    def del_tag(self, tag_name):
        """
        Remove a specific EXIF tag if present.

        :param tag_name: Name of the EXIF tag to remove (e.g., "GPSInfo").
        :return: self
        """
        if self.exif:
            for tag_id, tag_value in self.exif.items():
                tag_name_resolved = Image.ExifTags.TAGS.get(tag_id, str(tag_id))
                if tag_name_resolved == tag_name:
                    del self.exif[tag_id]
                    break
        return self

    def del_text(self):
        """"""
        return self

    def get_image_palette(self):
        """
        Get the color palette of the image (if applicable).

        :return: List of palette colors.
        """
        if self.palette is None:
            cfg = {}
            self.palette = PyfficeColorPalette(cfg)
        # if self.image is None:
        # self.load_image(self.path)
        # if self.image.mode == "P":  # Check if the image contains a palette
        #     return self.image.getpalette()
        return None

    def load_document(self, document=None):
        """
        Load an image from the specified path.

        :param path: Path to an image file to load.
        :return: self
        """
        logma.info(f"Load Document {document}")
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        logma.info(f"Load Document {document}")
        super().load_document(document)
        self.get_image_palette()
        return self

    def open_file(self, file=None, if_text_only=True):
        """"""
        if file is None:
            file = self.file_path
        self.set_syntax("file")
        if exists(file):
            self.set_file_path(file)
        return self

    def remove_background(self):
        """"""
        return self

    def remove_faces(self):
        """"""
        return self

    def set_content(self, content):
        """"""
        if content is None:
            return self
        logma.info(f"Content {content}")
        if self.location is None:
            self.set_location(None)
        if self.location == "internal":
            pass
        elif self.location == "external":
            self.set_file_path(content.get("file_path", None))
            content = {"file_path": self.file_path}
        else:
            raise Exception(f"Unknown Location {self.location}")
        if content != self.content:
            self.add_change("content", self.content, content)
            self.content = content
        return self

    def set_crop(self, box):
        """
        Crop the image to the specified bounding box.

        :param box: A tuple (left, upper, right, lower).
        :return: self
        """
        if self.image is None:
            return self
        self.image = self.image.crop(box)
        return self

    def set_objects(self, objects):
        """"""
        if objects != self.objects:
            self.add_change("objects", self.objects, objects)
            self.objects = objects
        return self

    def set_palette(self, palette):
        """"""
        if palette != self.palette:
            self.add_change("palette", self.palette, palette)
            self.palette = palette
        return self

    def set_size(self, width, height):
        """
        Resize the image.

        :param width: New width.
        :param height: New height.
        :return: self
        """
        size = [width, height]
        if size != self.image.size:
            self.add_change("size", self.image.size, size)
            self.size = size
            self.image = self.image.resize(size)
        return self

    def to_dict(self):
        """"""
        doc = super().to_dict()
        doc["data"]["document_type"] = "image"
        doc["data"]["path"] = self.file_path
        return doc


class PyfficeImageManager(PyfficeDocumentManager):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeImageManager").override(cfg))
        self.images = None
        if self.config.dikt.get("document", None) is not None:
            self.load_document(self.config.dikt.get("document", {}))

    def add_image(self, image):
        """"""
        image = PyfficeImage(image)
        self.images.append(image)
        return self

    def copy_image(self, image):
        """"""
        return self

    def get_similar_images(self, image):
        """
        compare images being managed using tools to determine similarity
        :param image:
        :return:
        """
        return self

    def load_document(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        return self

    def move_image(self, image):
        """"""
        return self

    def remove_image(self, image, delete_=False):
        """"""
        if isinstance(image, str):
            image = PyfficeImage(image)
        self.images.pop(self.images.index(image.finger_print))
        if delete_:
            fonql.remove_file(image.path)

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


class PyfficeScreenShot(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, cfg=None):
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).override("PyfficeScreenShot")).override(cfg)
        self.image = None

    def load_document(self, document=None):
        """"""
        if document is None:
            document = self.config.dikt.get("document", {})
            if document is None:
                document = {}
        super().load_document(document)
        return self

    def set_image(self):
        """"""

    def set_position(self, x, y):
        """"""

    def set_size(self, width, height):
        """"""

    def to_dict(self):
        """"""
        doc = super().to_dict()
        return doc


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
