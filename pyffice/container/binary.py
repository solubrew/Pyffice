# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Pyffice Binary Container
	description: >
		Handles binary document storage - decides between inline (base64) 
		or path (reference) based on configurable file size limits.
	version: 0.0.0.0.0.1
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import base64
import os
from os.path import abspath, dirname, join, getsize

# ======================================3rd Party Library Modules=====================================================||
from condor import condor

# ======================================Solutions Brewer Library Modules==============================================||
from ogma.logma import Logma

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "binary.yaml")


class PyfficeBinaryContainer:
	"""
	Generic container for binary objects.
	Decides between inline (base64 embed) or path (file reference) based on file size.
	
	Size limits are configurable per file type. Default is 256MB.
	"""
	
	VERSION = "0.0.0.0.0.1"
	
	# Default limit: 256MB
	DEFAULT_INLINE_SIZE = 256 * 1024 * 1024
	
	# Configurable limits by file type (in bytes)
	INLINE_SIZE_LIMITS = {
		# Images
		"png": 64 * 1024 * 1024,       # 64MB
		"jpg": 64 * 1024 * 1024,        # 64MB
		"jpeg": 64 * 1024 * 1024,       # 64MB
		"gif": 32 * 1024 * 1024,        # 32MB
		"webp": 128 * 1024 * 1024,      # 128MB
		"bmp": 64 * 1024 * 1024,        # 64MB
		"tiff": 256 * 1024 * 1024,      # 256MB
		"tif": 256 * 1024 * 1024,       # 256MB
		"svg": 8 * 1024 * 1024,         # 8MB
		"ico": 4 * 1024 * 1024,         # 4MB
		
		# Videos
		"mp4": 512 * 1024 * 1024,       # 512MB
		"m4v": 512 * 1024 * 1024,       # 512MB
		"avi": 1024 * 1024 * 1024,      # 1GB
		"mkv": 2048 * 1024 * 1024,      # 2GB
		"mov": 1024 * 1024 * 1024,      # 1GB
		"webm": 512 * 1024 * 1024,      # 512MB
		"wmv": 1024 * 1024 * 1024,      # 1GB
		"flv": 256 * 1024 * 1024,       # 256MB
		"mpeg": 1024 * 1024 * 1024,     # 1GB
		"mpg": 1024 * 1024 * 1024,      # 1GB
		"3gp": 128 * 1024 * 1024,       # 128MB
		"ogx": 256 * 1024 * 1024,       # 256MB
		
		# Audio
		"mp3": 128 * 1024 * 1024,       # 128MB
		"wav": 256 * 1024 * 1024,       # 256MB
		"flac": 512 * 1024 * 1024,      # 512MB
		"ogg": 256 * 1024 * 1024,       # 256MB
		"aac": 128 * 1024 * 1024,       # 128MB
		"m4a": 128 * 1024 * 1024,       # 128MB
		"wma": 128 * 1024 * 1024,       # 128MB
		"opus": 256 * 1024 * 1024,      # 256MB
		
		# Office Documents
		"pdf": 512 * 1024 * 1024,       # 512MB
		"docx": 256 * 1024 * 1024,      # 256MB
		"xlsx": 256 * 1024 * 1024,      # 256MB
		"pptx": 512 * 1024 * 1024,      # 512MB
		"doc": 256 * 1024 * 1024,       # 256MB
		"xls": 256 * 1024 * 1024,       # 256MB
		"ppt": 512 * 1024 * 1024,       # 512MB
		"odt": 256 * 1024 * 1024,       # 256MB
		"ods": 512 * 1024 * 1024,       # 512MB
		"odp": 512 * 1024 * 1024,       # 512MB
		
		# Text/Data formats
		"txt": 32 * 1024 * 1024,        # 32MB
		"md": 32 * 1024 * 1024,         # 32MB
		"markdown": 32 * 1024 * 1024,   # 32MB
		"json": 128 * 1024 * 1024,      # 128MB
		"xml": 128 * 1024 * 1024,       # 128MB
		"yaml": 128 * 1024 * 1024,      # 128MB
		"yml": 128 * 1024 * 1024,       # 128MB
		"csv": 256 * 1024 * 1024,       # 256MB
		"tsv": 256 * 1024 * 1024,       # 256MB
		
		# Web
		"html": 64 * 1024 * 1024,       # 64MB
		"htm": 64 * 1024 * 1024,        # 64MB
		"css": 16 * 1024 * 1024,        # 16MB
		"js": 16 * 1024 * 1024,         # 16MB
		"rtf": 64 * 1024 * 1024,        # 64MB
		
		# Config
		"ini": 8 * 1024 * 1024,         # 8MB
		"toml": 8 * 1024 * 1024,        # 8MB
		"env": 4 * 1024 * 1024,         # 4MB
		"cfg": 8 * 1024 * 1024,         # 8MB
		"conf": 8 * 1024 * 1024,        # 8MB
		
		# CAD
		"obj": 256 * 1024 * 1024,       # 256MB
		"stl": 512 * 1024 * 1024,       # 512MB
		"off": 256 * 1024 * 1024,       # 256MB
		"gltf": 128 * 1024 * 1024,      # 128MB
		"glb": 256 * 1024 * 1024,       # 256MB
		"scad": 32 * 1024 * 1024,       # 32MB
		"dxf": 256 * 1024 * 1024,       # 256MB
		"amf": 256 * 1024 * 1024,       # 256MB
		"3ds": 256 * 1024 * 1024,        # 256MB
		"blend": 2048 * 1024 * 1024,    # 2GB
		
		# Archives
		"zip": 2048 * 1024 * 1024,      # 2GB
		"rar": 2048 * 1024 * 1024,      # 2GB
		"7z": 4096 * 1024 * 1024,       # 4GB
		"tar": 4096 * 1024 * 1024,      # 4GB
		"gz": 2048 * 1024 * 1024,       # 2GB
		"bz2": 2048 * 1024 * 1024,      # 2GB
		"xz": 4096 * 1024 * 1024,       # 4GB
		
		# Notes
		"ctb": 512 * 1024 * 1024,       # 512MB
		
		# Fonts
		"ttf": 64 * 1024 * 1024,         # 64MB
		"otf": 64 * 1024 * 1024,        # 64MB
		"woff": 32 * 1024 * 1024,       # 32MB
		"woff2": 32 * 1024 * 1024,      # 32MB
		"eot": 16 * 1024 * 1024,        # 16MB
		
		# E-books
		"epub": 256 * 1024 * 1024,      # 256MB
		"mobi": 512 * 1024 * 1024,      # 512MB
		"azw": 512 * 1024 * 1024,       # 512MB
		"azw3": 512 * 1024 * 1024,      # 512MB
		
		# Executables
		"exe": 1024 * 1024 * 1024,      # 1GB
		"elf": 1024 * 1024 * 1024,      # 1GB
		"dll": 512 * 1024 * 1024,       # 512MB
		"so": 512 * 1024 * 1024,        # 512MB
		"dylib": 512 * 1024 * 1024,     # 512MB
	}
	
	def __init__(self, source=None, mode="auto", cfg=None):
		"""
		Initialize binary container.
		
		Args:
			source: File path or None
			mode: "auto", "inline", or "path"
				- auto: decides based on file size vs limit
				- inline: always embed as base64
				- path: always use file reference
			cfg: Configuration dict
		"""
		self.config = condor.Instruct(pxcfg).select("PyfficeBinaryContainer").override(cfg or {})
		self.mode = mode
		self.source = source
		self.file_path = None
		self.file_size = 0
		self.file_type = None
		self.inline_data = None
		self.encoding = None
		self.metadata = {}
		
		if source:
			self.load(source)
	
	def get_limit(self, file_type=None):
		"""
		Get inline size limit for specific file type.
		
		Args:
			file_type: File extension (without dot)
			
		Returns:
			int: Size limit in bytes
		"""
		if file_type is None:
			file_type = self.file_type
		return self.INLINE_SIZE_LIMITS.get(
			file_type.lower() if file_type else "",
			self.DEFAULT_INLINE_SIZE
		)
	
	@classmethod
	def set_limit(cls, file_type, limit_bytes):
		"""
		Set custom inline size limit for a file type.
		
		Args:
			file_type: File extension (without dot)
			limit_bytes: Size limit in bytes
		"""
		cls.INLINE_SIZE_LIMITS[file_type.lower()] = limit_bytes
	
	def load(self, source):
		"""
		Load a file and decide storage mode.
		
		Args:
			source: File path string
		"""
		self.source = source
		self.file_path = abspath(source)
		
		# Get file info
		if os.path.exists(self.file_path):
			self.file_size = getsize(self.file_path)
			self.file_type = os.path.splitext(self.file_path)[1].lstrip(".").lower()
		
		# Decide mode
		self._decide_mode()
		
		# Load data based on mode
		if self.mode == "inline":
			self._load_inline()
		else:
			self._load_path()
	
	def _decide_mode(self):
		"""Decide between inline or path based on file size and limits."""
		if self.mode != "auto":
			return
		
		limit = self.get_limit()
		
		if self.file_size > limit:
			self.mode = "path"
		else:
			self.mode = "inline"
	
	def _load_inline(self):
		"""Load file as base64 inline data."""
		if self.file_path and os.path.exists(self.file_path):
			with open(self.file_path, "rb") as f:
				self.inline_data = base64.b64encode(f.read()).decode("utf-8")
			self.encoding = "base64"
	
	def _load_path(self):
		"""Use file path reference."""
		self.encoding = "path"
	
	def to_dict(self):
		"""
		Convert to dictionary representation.
		
		Returns:
			dict: Container data
		"""
		result = {
			"file_type": self.file_type,
			"file_size": self.file_size,
			"mode": self.mode,
			"encoding": self.encoding,
			"metadata": self.metadata,
		}
		
		if self.mode == "inline":
			result["data"] = self.inline_data
		else:
			result["path"] = self.file_path
		
		return result
	
	def __repr__(self):
		return f"PyfficeBinaryContainer({self.file_type}, {self.file_size} bytes, {self.mode})"


# ====================================================================================================================||
# Helper functions
# ====================================================================================================================||

def get_limit_for_type(file_type):
	"""
	Get the inline size limit for a file type.
	
	Args:
		file_type: File extension (with or without dot)
		
	Returns:
		int: Size limit in bytes
	"""
	return PyfficeBinaryContainer().get_limit(file_type)


def set_limit_for_type(file_type, limit_mb):
	"""
	Set a custom inline size limit for a file type.
	
	Args:
		file_type: File extension (with or without dot)
		limit_mb: Limit in megabytes
	"""
	PyfficeBinaryContainer.set_limit(file_type, limit_mb * 1024 * 1024)


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
