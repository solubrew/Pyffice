# Copyright (c) 2025 s-langa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Pyffice Documents Module

This module provides document type handlers for various file formats.
"""

from .analytics import PyfficeSources, PyfficeDataSet, PyfficeDataView
from .audio import PyfficeAudio, PyfficePlayList
from .cad import (
    PyfficeCADAssembly,
    PyfficeCADManager,
    PyfficeCADPart,
)
from .calendars import PyfficeCalendar, PyfficeEvent
from .charts import PyfficeChart, PyfficeSankey
from .config import PyfficeConfig, PyfficeTOML, PyfficeHelp
from .contacts import PyfficeContact, PyfficePersona
from .container import (
    PyfficeContainer,
    PyfficeZip,
    PyfficeTar,
    PyfficeRAR,
    PyfficeSevenZip,
    PyfficeBinary,
)
from .data import (
    PyfficeCSVData,
    PyfficeJSONData,
    PyfficeXMLData,
    PyfficeYAMLData,
    PyfficeDataManager,
)
from .databases import PyfficeDatabase, PyfficeTable
from .diagrams import (
    PyfficeDiagrams,
    PyfficeEdge,
    PyfficeNode,
    PyfficeLayer,
    PyfficeSketch,
)
from .ebook import PyfficeEPUB, PyfficeAZW, PyfficeMOBI
from .email import PyfficeEmail
from .filesystems import PyfficeFileSystem
from .forms import PyfficeForm, PyfficeFormsManager, PyfficeSurvey
from .images import (
    PyfficeImage,
    PyfficePalette,
    PyfficeSketch,
)
from .items import (
    PyfficeItem,
    PyfficeCell,
    PyfficeShape,
    PyfficeLayer,
    PyfficeColor,
)
from .matrix import PyfficeMatrix, PyfficeSpreadsheet
from .media import PyfficeMedia
from .notebooks import PyfficeNotebook
from .ports import PyfficePort, PyfficeGPort, PyfficeMPort
from .presentation import PyfficePresentation, PyfficePPTX, PyfficeODP
from .projects import PyfficeProject, PyfficePAXN
from .reports import PyfficeReport
from .script import PyfficeScript
from .skills import PyfficeSkill, PyfficeSkillManager
from .socials import PyfficeMessage, PyfficeSocials
from .tags import PyfficeTag, PyfficeTagManager, PyfficeRating
from .text import PyfficeText, PyfficeBibliography
from .updates import PyfficeUpdate, PyfficeUpdateManager
from .video import PyfficeVideo
from .web import (
    PyfficeWebBrowser,
    PyfficeWebPage,
    PyfficeWebProfile,
)
from .workflows import PyfficeWorkflow, PyfficeAlarm, PyfficeFormula

__all__ = [
    # Analytics
    "PyfficeSources",
    "PyfficeDataSet",
    "PyfficeDataView",
    # Audio
    "PyfficeAudio",
    "PyfficePlayList",
    # CAD
    "PyfficeCADAssembly",
    "PyfficeCADManager",
    "PyfficeCADPart",
    # Calendars
    "PyfficeCalendar",
    "PyfficeEvent",
    # Charts
    "PyfficeChart",
    "PyfficeSankey",
    # Config
    "PyfficeConfig",
    "PyfficeTOML",
    "PyfficeHelp",
    # Contacts
    "PyfficeContact",
    "PyfficePersona",
    # Container
    "PyfficeContainer",
    "PyfficeZip",
    "PyfficeTar",
    "PyfficeRAR",
    "PyfficeSevenZip",
    "PyfficeBinary",
    # Data
    "PyfficeCSVData",
    "PyfficeJSONData",
    "PyfficeXMLData",
    "PyfficeYAMLData",
    "PyfficeDataManager",
    # Databases
    "PyfficeDatabase",
    "PyfficeTable",
    # Diagrams
    "PyfficeDiagrams",
    "PyfficeEdge",
    "PyfficeNode",
    "PyfficeLayer",
    "PyfficeSketch",
    # Ebook
    "PyfficeEPUB",
    "PyfficeAZW",
    "PyfficeMOBI",
    # Email
    "PyfficeEmail",
    # Filesystems
    "PyfficeFileSystem",
    # Forms
    "PyfficeForm",
    "PyfficeFormsManager",
    "PyfficeSurvey",
    # Images
    "PyfficeImage",
    "PyfficePalette",
    "PyfficeSketch",
    # Items
    "PyfficeItem",
    "PyfficeCell",
    "PyfficeShape",
    "PyfficeLayer",
    "PyfficeColor",
    # Matrix
    "PyfficeMatrix",
    "PyfficeSpreadsheet",
    # Media
    "PyfficeMedia",
    # Notebooks
    "PyfficeNotebook",
    # Ports
    "PyfficePort",
    "PyfficeGPort",
    "PyfficeMPort",
    # Presentation
    "PyfficePresentation",
    "PyfficePPTX",
    "PyfficeODP",
    # Projects
    "PyfficeProject",
    "PyfficePAXN",
    # Reports
    "PyfficeReport",
    # Script
    "PyfficeScript",
    # Skills
    "PyfficeSkill",
    "PyfficeSkillManager",
    # Socials
    "PyfficeMessage",
    "PyfficeSocials",
    # Tags
    "PyfficeTag",
    "PyfficeTagManager",
    "PyfficeRating",
    # Text
    "PyfficeText",
    "PyfficeBibliography",
    # Updates
    "PyfficeUpdate",
    "PyfficeUpdateManager",
    # Video
    "PyfficeVideo",
    # Web
    "PyfficeWebBrowser",
    "PyfficeWebPage",
    "PyfficeWebProfile",
    # Workflows
    "PyfficeWorkflow",
    "PyfficeAlarm",
    "PyfficeFormula",
]
