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
import colorsys
import cv2
import numpy as np
from xml.etree import ElementTree as ET

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from squirl.objnql import imgonql
from ogma.logma import Logma

from pyffice.pyffice import PyfficeDocument

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "utilities.yaml")


def hex_to_rgb(hex_color):
    """Convert a hex color to an RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb_color):
    """Convert an RGB tuple back to a hex color."""
    return "#{:02x}{:02x}{:02x}".format(*rgb_color)


def rgb_to_hsl(r, g, b):
    """Convert RGB to HSL (Hue, Saturation, Lightness)."""
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return h * 360, s, l


def hsl_to_rgb(h, s, l):
    """Convert HSL (Hue, Saturation, Lightness) back to RGB."""
    r, g, b = colorsys.hls_to_rgb(h / 360, l, s)
    return int(r * 255), int(g * 255), int(b * 255)


def is_similar_hue(hue1, hue2, hue_tolerance):
    """
    Check if two hues are similar, within a certain tolerance.
    Hue is a value between 0 and 360 degrees.
    """
    diff = abs(hue1 - hue2)
    diff = min(diff, 360 - diff)  # Handle circular nature of hues
    return diff <= hue_tolerance


def convert_shades_of_color(input_path, output_path, source_color, target_color, hue_tolerance):
    """"""
    image_type = check_image_type(input_path)
    if image_type == "svg":
        convert_shades_of_color_in_svg(input_path, output_path, source_color, target_color, hue_tolerance)
    elif image_type == "png":
        convert_shades_of_color_in_png(input_path, output_path, source_color, target_color, hue_tolerance)
    elif image_type == "jpg":
        convert_shades_of_color_in_jpg(input_path, output_path, source_color, target_color, hue_tolerance)
    else:
        raise ValueError("Invalid image type.")


def convert_shades_of_color_in_svg(input_path, output_path, source_color, target_color, hue_tolerance):
    """
    Change all shades of a color in an SVG to similar shades of another color.

    :param input_svg_path: Path to the input SVG file.
    :param output_svg_path: Path to save the output SVG file.
    :param source_color: Source color in hex format (e.g., '#ff0000').
    :param target_color: Target color in hex format (e.g., '#00ff00').
    :param hue_tolerance: Tolerance for hue matching (e.g., 20 degrees).
    """
    # Parse the SVG file
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Convert source and target colors to HSL
    source_rgb = hex_to_rgb(source_color)
    target_rgb = hex_to_rgb(target_color)
    source_hsl = rgb_to_hsl(*source_rgb)
    target_hsl = rgb_to_hsl(*target_rgb)

    # Iterate over all elements and update colors
    for element in root.iter():
        for attr in ["fill", "stroke"]:
            color = element.attrib.get(attr)
            if color and color.startswith("#"):  # Ensure it's a hex color
                # Convert current color to HSL
                current_rgb = hex_to_rgb(color)
                current_hsl = rgb_to_hsl(*current_rgb)

                # Check if the hue is similar to the source hue
                if is_similar_hue(current_hsl[0], source_hsl[0], hue_tolerance):
                    # Adjust the color to match the target hue, preserving saturation and lightness
                    new_hsl = (target_hsl[0], current_hsl[1], current_hsl[2])
                    new_rgb = hsl_to_rgb(*new_hsl)
                    new_color = rgb_to_hex(new_rgb)
                    element.set(attr, new_color)

    # Save the modified SVG
    tree.write(output_path)
    logma.info(f"SVG shades updated and saved to '{output_path}'.")


def convert_shades_of_color_in_jpg(image_path, output_path, source_color, target_color, tolerance=40):
    """"""
    convert_shades_of_color_in_png(image_path, output_path, source_color, target_color, tolerance)


def convert_shades_of_color_in_png(image_path, output_path, source_color, target_color, tolerance=40):
    """
    Convert shades of `source_color` to corresponding shades of `target_color` in an image.

    :param image_path: Path to the input image.
    :param source_color: A tuple (B, G, R) representing the source color.
    :param target_color: A tuple (B, G, R) representing the target color.
    :param tolerance: Tolerance for accepting the source color range.
    :return: Modified image as a numpy array.
    """
    # Load the image
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image could not be loaded. Check the image path.")
    if "#" == source_color[0]:
        source_color = (int(source_color[1:3], 16), int(source_color[3:5], 16), int(source_color[5:7], 16))
    if "#" == target_color[0]:
        target_color = (int(target_color[1:3], 16), int(target_color[3:5], 16), int(target_color[5:7], 16))
    # Convert the source and target colors to numpy arrays
    source_color = np.array(source_color, dtype=np.uint8)
    target_color = np.array(target_color, dtype=np.uint8)

    # Define the range of colors to match
    lower_bound = np.maximum(source_color - tolerance, 0)
    upper_bound = np.minimum(source_color + tolerance, 255)

    # Convert the image to HSV for better color-based segmentation
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    source_color_hsv = cv2.cvtColor(np.uint8([[source_color]]), cv2.COLOR_BGR2HSV)[0][0]
    target_color_hsv = cv2.cvtColor(np.uint8([[target_color]]), cv2.COLOR_BGR2HSV)[0][0]

    lower_hsv = np.maximum(source_color_hsv - np.array([10, 40, 40]), 0)
    upper_hsv = np.minimum(source_color_hsv + np.array([10, 40, 40]), 255)

    # Create a mask for the source color shades
    mask = cv2.inRange(hsv_img, lower_hsv, upper_hsv)

    # Create a blank image with target color
    target_hsv = np.zeros_like(hsv_img)
    target_hsv[:, :] = target_color_hsv

    # Blend the target color into the selected area
    result_hsv = hsv_img.copy()
    result_hsv[mask > 0] = target_hsv[mask > 0]

    # Convert back to BGR color space
    result_img = cv2.cvtColor(result_hsv, cv2.COLOR_HSV2BGR)
    cv2.imwrite("output_image.jpg", result_img)
    cv2.imshow("Result", result_img)
    return result_img


def check_image_type(input_path):
    """"""
    image_type = input_path.split(".")[-1]


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
