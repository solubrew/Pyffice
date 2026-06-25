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
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeDocument

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


# define file types
# FreeCAD
# LibreCAD
# AutoCAD
#
class PyfficeShape(PyfficeDocument):
    """"""

    VERSION = "0.0.1.0.1.0"

    def __init__(self, center=(0, 0, 0), dimensions=2, cfg=None):
        """"""
        self.config = kahndor.Instruct(pxcfg).override("")
        super().__init__(self)
        self.config.override(cfg)
        self.dimensions = dimensions
        self.center = center[: self.dimensions]  # (x, y) coordinates
        self.origin = self.center
        self.offset = (0, 0, 0)[: self.dimensions]
        self.envelope_corners = []

    def get_corner(self, corner_label="A"):
        """"""

    def get_center(self):
        """"""

    def get_envelope_corner(self, corner_label="A"):
        """"""
        raise ValueError("Only 2D and 3D shapes are supported.")

    def get_envelope_center(self):
        """"""

    def get_envelope(self):
        """"""
        envelope_corners = ["A", "B", "C", "D", "E", "F"][: self.dimensions]
        for corner in envelope_corners:
            self.envelope_corners.append(self.get_envelope_corner(corner))

    def get_origin(self):
        """"""

    def peform_mirror(self, axis="x"):
        """"""
        return

    def perform_origin_offset(self, offset):
        """"""
        self.offset = offset
        self.origin = (self.center[x] + offset[x] for x in range(len(self.center)))
        return self

    def perform_rotate(self, axis="x"):
        """"""
        return

    def set_center(self, center):
        """"""
        self.center = center
        self.perform_origin_offset(self.offset)
        return self

    def set_color(self, color):
        """"""
        self.color = color
        return self

    def set_origin_to_envelope_corner(self, corner):
        """"""
        self.origin = self.get_envelope_corner(corner)

    def set_origin_to_envelope_center(self):
        """"""
        self.origin = self.get_envelope_center()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
