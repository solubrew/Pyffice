# External Tools Needed

Pyffice can handle most formats natively. The following require external tools or libraries:

## CRITICAL: Broken Import Chain
**All modules fail to import due to**: `from condor import condor` - this module does not exist in the condor package.

Files affected (30+):
- pyffice/tags/tags.py
- pyffice/diagrams/diagrams.py
- pyffice/audio/audio.py
- pyffice/config/*.py
- pyffice/updates/updates.py
- pyffice/cad/*.py
- pyffice/cam/*.py
- pyffice/video/video.py
- pyffice/spreadsheet/spreadsheet.py
- pyffice/items/*.py
- pyffice/calendars/*.py
- pyffice/contacts/contacts.py
- pyffice/databases/*.py
- pyffice/email/email.py
- pyffice/presentation/presentation.py
- pyffice/document.py
- pyffice/__init__.py

**Solution**: Either:
1. Create a stub `condor/condor.py` module, OR
2. Replace all `from condor import condor` with direct condor usage

## Container Formats
- **rar**: `unar` or `unrar` CLI tool
- **sevenzip**: `p7zip` or `7-zip` CLI tool

## eBook Formats
- **epub**: Works natively (tested directly, not through pyffice)
- **mobi**: Requires `kindleunpack` or `mobi_unpack`
- **azw/azw3**: Requires `calibre` (`ebook-convert`)

## CAD Formats
- **obj/stl/scad**: Work natively
- **dxf**: Requires `dxfpy` or `ezdxf`
- **dwg**: Requires `opencascade` or `ezdxf` (limited)
- **step/iges**: Requires `occ` (OpenCASCADE)
- **blend**: Requires `bpy` (Blender Python)
- **fbx/gltf**: Work natively

## Document Formats
- **pptx**: Requires `python-pptx` (`pip install python-pptx`)
- **rtf**: Works natively
- **odt**: Requires `odfpy` (`pip install odfpy`)
- **latex**: Requires `pdflatex`/XeLaTeX system install

## Media Formats
- **video**: Requires `ffmpeg` system install
- **audio**: Requires `ffmpeg` or `pydub` (`pip install pydub`)

## Currently Working (Direct Import, Not Through pyffice.__init__)
- csv, json, yaml, xml, ini, toml, env, zip, tar, epub
