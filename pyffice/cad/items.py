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

logma.info(f"Module {__name__} loaded")
# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


# define file types
# FreeCAD
# LibreCAD
# AutoCAD
#
class PyfficeShape(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

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
        """Get corner point by label."""
        corners = getattr(self, 'corners', {})
        return corners.get(corner_label)

    def get_center(self):
        """Get center point."""
        return getattr(self, 'center', None)

    def get_envelope_center(self):
        """Get envelope center."""
        corners = getattr(self, 'envelope_corners', [])
        if len(corners) >= 2:
            xs = [c[0] for c in corners]
            ys = [c[1] for c in corners]
            return ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
        return None

    def get_envelope(self):
        """Return the envelope.
        
        Returns:
            Self for chaining.
        """
        envelope_corners = ["A", "B", "C", "D", "E", "F"][: self.dimensions]
        for corner in envelope_corners:
            self.envelope_corners.append(self.get_envelope_corner(corner))

    def get_origin(self):
        """Get origin point."""
        return getattr(self, 'origin', None)

    def peform_mirror(self, axis="x"):
        """Mirror shape along axis."""
        _p = True  # placeholder
        return self

    def perform_origin_offset(self, offset):
        """Perform origin offset.
        
        Args:
            offset: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.offset = offset
        self.origin = (self.center[x] + offset[x] for x in range(len(self.center)))
        return self

    def perform_rotate(self, axis="x"):
        """Rotate shape around axis."""
        _p = True  # placeholder
        return self

    def set_center(self, center):
        """Set the center.
        
        Args:
            center: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.center = center
        self.perform_origin_offset(self.offset)
        return self

    def set_color(self, color):
        """Set the color.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.color = color
        return self

    def set_origin_to_envelope_corner(self, corner):
        """Set the origin to envelope corner.
        
        Args:
            corner: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.origin = self.get_envelope_corner(corner)

    def set_origin_to_envelope_center(self):
        """Set the origin to envelope center.
        
        Returns:
            Self for chaining.
        """
        self.origin = self.get_envelope_center()


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
