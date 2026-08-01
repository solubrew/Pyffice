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
logma.off()

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class PyfficeColorPalette(PyfficeDocument):
    SERIALIZATION_VERSION = (1, 0, 0)
    """
    PyfficeColorPalette is responsible for creating and managing color palettes.
    It supports adding colors manually, retrieving colors, and extracting colors
    from various content types like images, SVG files, and videos.
    """

    def __init__(self, cfg=None):
        """
        Initialize the PyfficeColorPalette object.

        Args:
            cfg (dict, optional): Configuration dictionary.
        """
        logma.debug(f"PyfficeColorPalette.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeColorPalette")).override(cfg)
        self.parent = self.config.dikt.get("parent", None)
        self.colors = None  # Store colors as PyfficeColor objects
        self.hex_colors = None  # Store as HEX values for quick lookup
        self.palette_table = None

    def add_color(self, color):
        """
        Add a new color to the palette.

        Args:
            color (PyfficeColor | dict | str | tuple): The color to add.
                It can be a PyfficeColor object, a dictionary definition, a HEX string, or an RGB tuple.
        """
        if isinstance(color, PyfficeColor):
            pyffice_color = color
        elif isinstance(color, str) and color.startswith("#"):  # HEX string
            cfg = {"hex": color}
            pyffice_color = PyfficeColor(cfg)
        elif isinstance(color, tuple) and len(color) in (3, 4):  # RGB / RGBA tuple
            cfg = {"rgb": color}
            pyffice_color = PyfficeColor(cfg)
        else:
            raise ValueError("Unsupported color type provided.")
        self.colors.append(pyffice_color)
        self.add_change("colors", self.colors, color, "add")
        self.hex_colors.append(pyffice_color.get_hex())
        self.add_change("hex_colors", self.hex_colors, color, "add")
        return self

    def convert_color_palette(self, red_fx, green_fx, blue_fx):
        """
        Generalized algorithm to transform any color palette to any target mapping.

        Args:
            palette: A list of colors in RGB format [(R, G, B), ...].
            red_function: A function that determines the new Red value.
            green_function: A function that determines the new Green value.
            blue_function: A function that determines the new Blue value.

        Returns:
            A transformed list of colors in RGB format [(R', G', B'), ...].
        """
        transformed_palette = []
        for color in self.colors:
            r, g, b = color
            # Apply transformation rules to each channel
            new_r = red_fx(r, g, b)
            new_g = green_fx(r, g, b)
            new_b = blue_fx(r, g, b)
            # Ensure values are clamped to [0, 255]
            new_color = (
                max(0, min(255, new_r)),
                max(0, min(255, new_g)),
                max(0, min(255, new_b)),
            )
            transformed_palette.append(new_color)
        return transformed_palette

    def create_analogous_colors(self, color):
        """Create a analogous colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        new_color = PyfficeColor(color.to_dict())
        h, s, l = new_color.get_hsl()
        h = (h + (-30 / 360)) % 1.0
        s = (h, s, l)
        l = (h + (30 / 360)) % 1.0
        new_color.set_hsl(h, s, l)
        return new_color

    def create_clash_colors(self, color):
        """Create a clash colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        new_color = PyfficeColor(color.to_dict())
        h, s, l = new_color.get_hsl()
        h = ((h + (-30 / 360)) % 1.0, s, l)
        s = (h, s, l)
        l = ((h + (150 / 360)) % 1.0, s, l)
        new_color.set_hsl(h, s, l)
        return new_color

    def create_complimentary_colors(self, color):
        """Create a complimentary colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        new_color = PyfficeColor(color.to_dict())
        _h, _s, _l = new_color.get_hsl()
        return new_color

    def create_neutral_colors(self, color):
        """Create a neutral colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        new_color = PyfficeColor(color.to_dict())
        h, s, l = new_color.get_hsl()
        h = (h, s * 0.5, l)
        s = (h, s * 0.25, l)
        l = (h, s * 0.0, l)
        new_color.set_hsl(h, s, l)
        return new_color

    def create_square_colors(self, color):
        """Create a square colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.create_tone_colors(color, num_tones=4)
        return self

    def create_tone_colors(self, color, num_tones=5):
        """Create a tone colors.
        
        Args:
            color: Parameter.
            num_tones: Parameter.
        
        Returns:
            Self for chaining.
        """
        for i in range(num_tones - 1):
            new_color = PyfficeColor(color.to_dict())
            h, _s, _l = new_color.get_hsl()
            new_color.set_hsl((h + (i * 360 / num_tones)) % 1.0)
            self.add_color(new_color)

    def create_tetradic_colors(self, color):
        """Create a tetradic colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.create_tone_colors(color, num_tones=4)
        return self

    def create_triadic_colors(self, color):
        """Create a triadic colors.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.create_tone_colors(color, num_tones=3)
        return self

    def del_color(self, color):
        """Remove the color.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.colors.remove(color)
        self.hex_colors.remove(color.get_hex())
        self.add_change("colors", self.colors, color, "del")
        self.add_change("hex_colors", self.hex_colors, color, "del")
        return self

    def extract_colors(self, content_path):
        """
        Extract colors from the provided content file.
        Args:
            content_path (str): Path to the content file.
        Raises:
            ValueError: If the file type is unsupported.
        """
        # Determine content type and extract colors
        if content_path.endswith((".jpg", ".png")):
            extract_colors_from_image(file_path=self.file_path)
        elif content_path.endswith(".svg"):
            extract_colors_from_svg(file_path=self.file_path)
        elif content_path.endswith((".mp4", ".mkv", ".avi")):
            extract_colors_from_video(file_path=self.file_path)
        else:
            raise ValueError("Invalid file type. Supported types are: images, SVG, or videos.")

    def get_color(self, color_name):
        """
        Retrieve a color from the palette by its name.

        Args:
            color_name (str): The name of the color to retrieve.

        Returns:
            PyfficeColor: The matching color object if found.
        """
        for color in self.colors:
            if color.name == color_name:
                return color
        raise ValueError(f"Color with name '{color_name}' not found in the palette.")

    def get_palette(self, format_="table"):
        """Return the palette.
        
        Args:
            format_: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.extract_colors(self.parent)
        cfg = {"columns": [], "records": [[x.name, x.hex, self.get_usage(x)] for x in self.colors]}
        palette_table = PyfficeTable(cfg)
        if self.palette_table != palette_table:
            self.palette_table = palette_table
            self.add_change("palette_table", self.palette_table, palette_table, "add")
        if format_ == "table":
            return self.palette_table.to_table()
        elif format_ == "dataframe":
            return self.palette_table.to_dataframe()
        return self.palette_table.to_dict("records-only")

    def get_usage(self, color):
        """Return the usage.
        
        Args:
            color: Parameter.
        
        Returns:
            Self for chaining.
        """
        if self.parent is None:
            return None
        usage = 0
        return usage

    def load_document(self, document=None):
        """
        Load an image file using PIL.

        Args:
            image_path (str): Path to the image.

        Returns:
            PIL.Image.Image: The loaded image object.
        """
        if document is None:
            document = {}
        super().load_document(document)
        # return Image.open(self.file_path)
        return self

    def scale_fx(self, factor):
        """Scale fx.
        
        Args:
            factor: Parameter.
        
        Returns:
            Self for chaining.
        """
        return lambda r, g, b: (r * factor, g * factor, b * factor)

    def set_palette(self):
        """Set color palette."""
        _p = True  # placeholder
        return self

    def set_palette_darker(self, factor):
        """Set the palette darker.
        
        Args:
            factor: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.scale_fx(factor)

    def set_palette_grayscale(self):
        """Set the palette grayscale.
        
        Returns:
            Self for chaining.
        """
        grayscale_fx = lambda r, g, b: (r * 0.2126 + g * 0.7152 + b * 0.0722) / 255.0
        self.convert_color_palette(grayscale_fx, grayscale_fx, grayscale_fx)

    def set_palette_lighter(self, factor):
        """Set the palette lighter.
        
        Args:
            factor: Parameter.
        
        Returns:
            Self for chaining.
        """
        self.scale_fx(1 - factor)

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
