# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name: Pyffice Ports Module
        description: >
                Ports layer for converting between external file formats and Pyffice formats.
                All external formats import/export to PyfficeXXX document types.
        version: 0.0.1.0.1.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
# ======================================3rd Party Library Modules=====================================================||
# ======================================Solutions Brewer Library Modules==============================================||

# CAD ports
from pyffice.ports.cadports import (
    CADPort,
    STLPort,
    OBJPort,
    STEPPort,
    DWGPort,
    DXFPort,
    FBXPort,
    GLTFPort,
    IGESPort,
    BLENDPort,
    SCADPort,
    CADPortsManager,
    get_ports_manager as get_cad_ports_manager,
    import_cad,
    export_cad,
    convert_cad,
)

# Spreadsheet ports
from pyffice.ports.spreadsheetports import (
    SpreadsheetPort,
    XLSXPort,
    XlsPort,
    CSVPort,
    ODSPort,
    TSVPort,
    SpreadsheetPortsManager,
    get_ports_manager as get_spreadsheet_ports_manager,
    import_spreadsheet,
    export_spreadsheet,
    convert_spreadsheet,
)

# Presentation ports
from pyffice.ports.presentationports import (
    PresentationPort,
    PPTXPort,
    KeyPort,
    PresentationPortsManager,
    get_ports_manager as get_presentation_ports_manager,
    import_presentation,
    export_presentation,
    convert_presentation,
)

# Audio ports
from pyffice.ports.audioports import (
    AudioPort,
    MP3Port,
    WAVPort,
    FLACPort,
    AACPort,
    OGGPort,
    AudioPortsManager,
    get_ports_manager as get_audio_ports_manager,
    import_audio,
    export_audio,
    convert_audio,
)

# Video ports
from pyffice.ports.videoports import (
    VideoPort,
    MP4Port,
    AVIPort,
    MKVPort,
    MOVPort,
    FLVPort,
    VideoPortsManager,
    get_ports_manager as get_video_ports_manager,
    import_video,
    export_video,
    convert_video,
)

# Image ports
from pyffice.ports.imageports import (
    ImagePort,
    PNGPort,
    JPEGPort,
    GIFPort,
    BMPPort,
    TIFFPort,
    ImagePortsManager,
    get_ports_manager as get_image_ports_manager,
    import_image,
    export_image,
    convert_image,
)

# Database ports
from pyffice.ports.databasesports import (
    DatabasePort,
    SQLPort,
    SQLitePort,
    DatabasePortsManager,
    get_ports_manager as get_database_ports_manager,
    import_database,
    export_database,
    convert_database,
)

__all__ = [
    # CAD ports
    "CADPort",
    "STLPort",
    "OBJPort",
    "STEPPort",
    "DWGPort",
    "DXFPort",
    "FBXPort",
    "GLTFPort",
    "IGESPort",
    "BLENDPort",
    "SCADPort",
    "CADPortsManager",
    "get_cad_ports_manager",
    "import_cad",
    "export_cad",
    "convert_cad",
    # Spreadsheet ports
    "SpreadsheetPort",
    "XLSXPort",
    "XlsPort",
    "CSVPort",
    "ODSPort",
    "TSVPort",
    "SpreadsheetPortsManager",
    "get_spreadsheet_ports_manager",
    "import_spreadsheet",
    "export_spreadsheet",
    "convert_spreadsheet",
    # Presentation ports
    "PresentationPort",
    "PPTXPort",
    "KeyPort",
    "PresentationPortsManager",
    "get_presentation_ports_manager",
    "import_presentation",
    "export_presentation",
    "convert_presentation",
    # Audio ports
    "AudioPort",
    "MP3Port",
    "WAVPort",
    "FLACPort",
    "AACPort",
    "OGGPort",
    "M4APort",
    "AudioPortsManager",
    "get_audio_ports_manager",
    "import_audio",
    "export_audio",
    "convert_audio",
    # Video ports
    "VideoPort",
    "MP4Port",
    "AVIPort",
    "MKVPort",
    "MOVPort",
    "WEBMPort",
    "FLVPort",
    "VideoPortsManager",
    "get_video_ports_manager",
    "import_video",
    "export_video",
    "convert_video",
    # Image ports
    "ImagePort",
    "PNGPort",
    "JPEGPort",
    "JPGPort",
    "GIFPort",
    "WEBPPort",
    "SVGRasterPort",
    "BMPPort",
    "TIFFPort",
    "ImagePortsManager",
    "get_image_ports_manager",
    "import_image",
    "export_image",
    "convert_image",
    # Database ports
    "DatabasePort",
    "SQLPort",
    "NoSQLPort",
    "GraphDBPort",
    "SQLitePort",
    "PostgreSQLPort",
    "MySQLPort",
    "MongoDBPort",
    "Neo4jPort",
    "DatabasePortsManager",
    "get_database_ports_manager",
    "import_database",
    "export_database",
    "convert_database",
]

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
