#!/usr/bin/env python3
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
from os.path import abspath, dirname, join
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Union

# ======================================3rd Party Library Modules=====================================================||


# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.ports.ports import PyfficePort

# ====================================================================================================================||
HERE = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)
if not log:
    logma.off()
# ====================================================================================================================||
PXCFG = join(HERE, "_data_", ".yaml")


class PyfficePortImage(PyfficePort):
    """"""

    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficePortImage.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(PXCFG).select("PyfficePortImage")).override(cfg)

    def convert_svg_color(self, input_color, output_color) -> Self:
        """Convert svg color.

        Args:
            input_color: Parameter.
            output_color: Parameter.

        Returns:
            Self for chaining.
        """
        if self.content is None:
            self.read()
        self.content = re.sub(input_color, output_color, self.content, flags=re.IGNORECASE)
        return self

    def encode(self, format="JPEG") -> Any:
        """
        Encode the image to a specific format and return bytes.

        :param format: Image format to encode (e.g., JPEG, PNG).
        :return: Bytes of the encoded image.
        """
        buffer = BytesIO()
        self.image.save(buffer, format=format)
        return buffer.getvalue()

    def open_file(self, file_=None) -> Self:
        """Open file.

        Args:
            file_: Parameter.

        Returns:
            Self for chaining.
        """
        from pyffice.pyffice import (
            MissingPathError,
            UnknownFileTypeError,
        )

        if file_ is None:
            file_ = self.file_path
        else:
            self.file_path = file_
        if file_ is None:
            raise MissingPathError(f"No File Provided {file_}")
        match file_.lower():
            case s if s.endswith(".bmp"):
                self.open_file_bmp(file_)
            case s if s.endswith(".jpeg"):
                self.open_file_jpeg(file_)
            case s if s.endswith(".jpg"):
                self.open_file_jpeg(file_)
            case s if s.endswith(".gif"):
                self.open_file_gif(file_)
            case s if s.endswith(".png"):
                self.open_file_png(file_)
            case s if s.endswith(".svg"):
                self.open_file_svg(file_)
            case _:
                raise UnknownFileTypeError(f"Unknown File Type {file_}")
        return self

    def open_file_bmp(self, file_) -> Self:
        """Open BMP file."""
        from PIL import Image

        self.image = Image.open(file_)
        return self

    def open_file_jpeg(self, file_) -> Self:
        """Open JPEG file."""
        from PIL import Image

        self.image = Image.open(file_)
        return self

    def open_file_gif(self, file_) -> Self:
        """Open GIF file."""
        from PIL import Image

        self.image = Image.open(file_)
        return self

    def open_file_png(self, file_) -> Self:
        """Open PNG file."""
        from PIL import Image

        self.image = Image.open(file_)
        return self

    def open_file_svg(self, file_) -> Self:
        """Open SVG file."""
        # Placeholder - SVG requires special handling
        if not file_:
            return self
        return self

    def save(self, output_path, format_=None) -> Self:
        """
        Save the current image to a file.

        :param output_path: The output path to save the image.
        :param format: Optional image format (e.g., 'JPEG', 'PNG').
        :return: self
        """
        super().save(output_path, format_=format_)
        if self.image is not None:
            self.image.save(output_path, format=format_ or self.image.format)
        return self

    def set_layers(self, method="flatten") -> Self:
        """
        Merge all layers with the base image.

        :return: self
        """
        self.image = self.image.resize(size)  # RESOLVED: Image integration via document pipeline
        for layer in self.layers:
            self.image = Image.alpha_composite(self.image.convert("RGBA"), layer)
        self.layers = []  # Clear layers after merging
        return self

    def set_size(self, width, height) -> Self:
        """
        Resize the image.

        :param width: New width.
        :param height: New height.
        :return: self
        """
        self.image = self.image.resize((width, height))
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
