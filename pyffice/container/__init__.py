# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Pyffice Container
	description: >
		Container modules for binary and text document storage.
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||

# ======================================3rd Party Library Modules=====================================================||
from pyffice.container.zip import PyfficeZip, read, write, load, extract, extract_file, create, compress
from pyffice.container.tar import PyfficeTar, read_tar, write_tar, extract_tar, compress_tar
from pyffice.container.rar import PyfficeRAR, compress_rar, extract_rar
from pyffice.container.sevenzip import Pyffice7Z, compress_7z, extract_7z
from pyffice.container.binary import PyfficeBinaryContainer, get_limit_for_type, set_limit_for_type

# ======================================Solutions Brewer Library Modules==============================================||

# ====================================================================================================================||

__all__ = [
	# Binary container
	"PyfficeBinaryContainer",
	"get_limit_for_type", 
	"set_limit_for_type",
	# ZIP
	"PyfficeZip", "read", "write", "load", "extract", "extract_file", "create", "compress",
	# TAR
	"PyfficeTar", "read_tar", "write_tar", "extract_tar", "compress_tar",
	# RAR
	"PyfficeRAR", "compress_rar", "extract_rar",
	# 7Z
	"Pyffice7Z", "compress_7z", "extract_7z",
]

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
