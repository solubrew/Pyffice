# Pyffice Import/Export Testing Plan

## Overview
Comprehensive testing plan for all pyffice document format import/export functionality.

## Current Test Results (2026-03-02)

### Config Formats (pyffice/config/)
| Format | Module | read() | write() | load() | Status |
|--------|--------|--------|---------|--------|--------|
| INI | ini.py | ❌ | ❌ | ✅ | Needs read/write aliases |
| TOML | toml.py | ❌ | ❌ | ❌ | **SYNTAX ERROR line 46** |
| ENV | env.py | ❌ | ❌ | ✅ | Needs read/write aliases |

### Container Formats (pyffice/container/)
| Format | Module | read() | write() | Status |
|--------|--------|--------|---------|--------|
| ZIP | zip.py | ❌ | ❌ | Not implemented |
| TAR | tar.py | ❌ | ❌ | Not implemented |
| RAR | rar.py | ❌ | ❌ | Stub |
| 7Z | sevenzip.py | ❌ | ❌ | Stub |

### eBook Formats (pyffice/ebook/)
| Format | Module | read() | write() | load() | Status |
|--------|--------|--------|---------|--------|--------|
| EPUB | epub.py | ✅ | ❌ | ❌ | Needs write/load aliases |
| MOBI | mobi.py | ❌ | ❌ | ❌ | Stub |
| AZW | azw.py | ❌ | ❌ | ❌ | Stub |

### CAD Formats (pyffice/cad/)
| Format | Module | read() | write() | load() | Status |
|--------|--------|--------|---------|--------|--------|
| OBJ | obj.py | ❌ | ❌ | ❌ | Needs all methods |
| STL | stl.py | ❌ | ❌ | ❌ | Needs all methods |
| GLTF | gltf.py | ❌ | ❌ | ❌ | Stub |
| DXF | dxf.py | ❌ | ❌ | ❌ | Stub |
| DWG | dwg.py | ❌ | ❌ | ❌ | Stub |
| STEP | step.py | ❌ | ❌ | ❌ | Stub |
| IGES | iges.py | ❌ | ❌ | ❌ | Stub |
| BLEND | blend.py | ❌ | ❌ | ❌ | Stub |
| FBX | fbx.py | ❌ | ❌ | ❌ | Stub |
| SCAD | scad.py | ❌ | ❌ | ❌ | Stub |

### Script Formats (pyffice/script/)
| Format | Module | read() | write() | Status |
|--------|--------|--------|---------|--------|
| RTF | rtf.py | ❌ | ❌ | Stub |
| ODT | odt.py | ❌ | ❌ | Stub |
| LaTeX | latex.py | ❌ | ❌ | Stub |
| RST | rst.py | ❌ | ❌ | Stub |
| ASCII | asciidoc.py | ❌ | ❌ | Stub |

### Presentation (pyffice/presentation/)
| Format | Module | read() | write() | Status |
|--------|--------|--------|---------|--------|
| PPTX | pptx.py | ❌ | ❌ | Stub |

### Media (pyffice/media/)
| Format | Module | read() | write() | Status |
|--------|--------|--------|---------|--------|
| Video | video.py | ❌ | ❌ | Stub |
| Audio | audio.py | ❌ | ❌ | Stub |

## Implementation Checklist

### Priority 1 - Fix Syntax Errors
- [ ] Fix config/toml.py - Syntax error line 46

### Priority 2 - Add Aliases (quick wins)
- [ ] Fix config/ini.py - Add `read` and `write` aliases
- [ ] Fix config/env.py - Add `read` and `write` aliases  
- [ ] Fix ebook/epub.py - Add `write` and `load` aliases

### Priority 3 - Implement Container Formats
- [ ] Implement container/zip.py - read/write methods
- [ ] Implement container/tar.py - read/write methods

### Priority 4 - Implement CAD Formats
- [ ] Implement cad/obj.py - read/write/load methods
- [ ] Implement cad/stl.py - read/write/load methods
- [ ] Implement cad/gltf.py - read/write methods

### Priority 5 - Stubs (lower priority)
- [ ] container/rar.py, sevenzip.py
- [ ] ebook/mobi.py, azw.py
- [ ] cad/dxf.py, dwg.py, step.py, iges.py, blend.py, fbx.py, scad.py
- [ ] script/rtf.py, odt.py, latex.py, rst.py, asciidoc.py
- [ ] presentation/pptx.py
- [ ] media/video.py, audio.py

## Test Execution
```bash
cd /home/solubrew/.orin/workspace/projects/pyffice
source /home/solubrew/ENVs/tuh/bin/activate
python -m pytest test_pyffice/unit/ -v
```

## Status: IN PROGRESS
