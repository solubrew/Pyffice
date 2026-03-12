# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Pyffice Ports Module
	description: >
		Common ports layer for converting between different file formats.
		Uses universal intermediate formats for clean conversions.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
# ======================================3rd Party Library Modules=====================================================||
# ======================================Solutions Brewer Library Modules==============================================||

# Export CAD ports
from pyffice.ports.cad import (
    NchantdCADPart,
    CADPort,
    STLPort,
    OBJPort,
    STEPPort,
    CADPortManager,
    get_port_manager,
    import_cad,
    export_cad,
    convert_cad
)

__all__ = [
    # CAD
    'NchantdCADPart',
    'CADPort',
    'STLPort',
    'OBJPort',
    'STEPPort',
    'CADPortManager',
    'get_port_manager',
    'import_cad',
    'export_cad',
    'convert_cad',
]

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
