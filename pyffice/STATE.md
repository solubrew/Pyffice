# Pyffice Project State

**Last Updated:** 2026-03-11  
**Version:** 0.0.1  
**Status:** Active Development

---

## Project Overview

Pyffice is a comprehensive document management system supporting 40+ document types across text, media, databases, CAD, and productivity formats.

| Metric | Count |
|--------|-------|
| Total Python Files | 156 |
| Total Classes | 86+ |
| Top-Level Modules | 37 |
| Test Files | 50+ |

---

## Core Architecture

### Base Classes

```
PyfficeUnit (base)
    └── PyfficeDocument (extends PyfficeUnit)
            ├── PyfficeDocumentManager (collection manager)
            └── [Document Type Classes]
```

| Class | File | Purpose |
|-------|------|---------|
| `PyfficeUnit` | document.py | Base unit with versioning, change tracking, metadata |
| `PyfficeDocument` | document.py | File-based documents with save/load, vector search |
| `PyfficeDocumentManager` | document.py | Collection of documents |
| `PyfficeDeque` | document.py | Document history with deque |

---

## Module Inventory

### Core Modules (pyffice/)

| Module | Classes | Status | Notes |
|--------|---------|--------|-------|
| `pyffice.py` | PyfficeCodex, Logma, Errors | ✅ Stable | Main entry point |
| `document.py` | PyfficeUnit, PyfficeDocument, etc | ✅ Stable | Core document classes |
| `cli.py` | CLI commands | ✅ Stable | Command-line interface |
| `agent.py` | PyfficeAgent | 🔶 WIP | Agent integration |

### Document Type Modules

| Module | Document Classes | Inherits | Status |
|--------|-----------------|----------|--------|
| **text/** | PyfficeScript | PyfficeDocument | ✅ |
| **spreadsheet/** | PyfficeSpreadSheet, PyfficeMatrix | PyfficeDocument/DocManager | ✅ |
| **images/** | PyfficeImage, PyfficeScreenShot, PyfficeImageManager | PyfficeDocument | ✅ |
| **presentation/** | PyfficePresentation, PyfficeSlideShow | PyfficeDocument | ✅ |
| **contacts/** | PyfficeContact, PyfficeRolodex | PyfficeDocument/DocManager | ✅ |
| **calendars/** | PyfficeCalendar | PyfficeDocumentManager | ⚠️ Incomplete |
| **charts/** | PyfficeChart, SankeyChart | PyfficeDocument | ✅ |
| **audio/** | PyfficeAudio, PyfficePlayList | PyfficeDocument/DocManager | ✅ |
| **video/** | PyfficeVideo | PyfficeDocument | ✅ |
| **reports/** | PyfficeReport | PyfficeDocument | ✅ |
| **databases/** | PyfficeDatabaseConnection, PyfficeDatabaseManager | PyfficeDocumentManager | ✅ |
| **notebooks/** | PyfficeNotebook | PyfficeDocument | ✅ |
| **email/** | PyfficeEmailMessage, PyfficeMailBox | PyfficeDocument/DocManager | ✅ |
| **socials/** | PyfficeSMS, PyfficeMMS, PyfficePostalMail | PyfficeDocument | ✅ |
| **forms/** | PyfficeForm, PyfficeFormsManager, PyfficeSurvey | PyfficeDocument/DocManager | ✅ |

### Container/Archive Modules

| Module | Classes | Status |
|--------|---------|--------|
| container/zip.py | PyfficeZip | ✅ |
| container/tar.py | PyfficeTar | ✅ |
| container/rar.py | PyfficeRAR | ✅ |
| container/sevenzip.py | Pyffice7Z | ✅ |
| container/binary.py | PyfficeBinaryContainer | ✅ |

### CAD/CAM Modules

| Module | Classes | Status |
|--------|---------|--------|
| cad/cad.py | PyfficeCADAssembly, PyfficeCADManager, PyfficeCADPart | ✅ |
| cad/stl.py | PyfficeSTL | ✅ |
| cad/obj.py | PyfficeOBJ | ✅ |
| cad/items.py | PyfficeShape | ✅ |
| cam/cam.py | PyfficeCAM, PyfficeCAMManager | ✅ |
| cam/gcode.py | PyfficeGCode | ✅ |
| cam/bom.py | PyfficeBOM, PyfficeSoftwareBOM | ✅ |

### Configuration/Port Modules (config/)

| Module | Classes | Status |
|--------|---------|--------|
| config/config.py | PyfficeConfig, PyfficeTOML, PyfficeHelp | ✅ |
| config/env.py | PyfficeENV | ✅ |
| config/ini.py | PyfficeINI | ✅ |
| config/toml.py | PyfficeTOML | ✅ |
| config/policies.py | PyfficePolicy | ✅ |
| config/ports.py | PyfficePort + 8 port implementations | ✅ |
| config/gports.py | Google Docs/Forms/Sheets ports | ✅ |
| config/msports.py | Excel/Word ports | ✅ |

### Data/Utility Modules

| Module | Classes | Status |
|--------|---------|--------|
| data/ | CSV, JSON, XML, YAML handlers | ✅ |
| tags/ | PyfficeTag, PyfficeTagsManager, PyfficeRating, PyfficeReference | ✅ |
| items/ | Cells, Colors, Shapes, Text, Tasks, Persona | ✅ |
| updates/ | Update tracking classes | ✅ |
| workflows/ | Automations, Formulas, Playlists, Alarms | ✅ |
| filesystems/ | PyfficeFileSystem | ✅ |
| diagrams/ | PyfficeSketch, Node, Edge, Layer | ✅ |
| analytics/ | PyfficeSources, DataSet, DataView | ✅ |
| web/ | Browser, Services, Prompts, URL | ✅ |

### Media Modules

| Module | Classes | Status |
|--------|---------|--------|
| media/heic.py | PyfficeHeic | ✅ |
| media/raw.py | PyfficeRaw | ✅ |
| media/video.py | PyfficeVideo | ✅ |

### Script/ebook Modules

| Module | Classes | Status |
|--------|---------|--------|
| script/ | LaTeX, ODT, RST, RTF, AsciiDoc | ✅ |
| ebook/ | EPUB, MOBI, AZW | ✅ |

---

## Known Issues

### Incomplete Implementations

1. **PyfficeCalendar** (`calendars/calendars.py`)
   - `set_events()` - stub only
   - `set_tasks()` - stub only
   - Missing: Event/task persistence

2. **PyfficeImageManager** (`images/images.py`)
   - Partial implementation
   - Needs: Batch operations, caching

3. **PyfficeScreenShot** (`images/images.py`)
   - Stub implementation
   - Needs: Screen capture integration

4. **Vector Search** (document.py)
   - `search_vector()` returns empty dict
   - Requires: sentence_transformers integration

5. **PyfficeCodex** (pyffice.py)
   - Many methods return None or raise NotImplementedError
   - Needs: Full implementation of document operations

---

## Dependencies

### Required
- Python 3.12+
- pyyaml
- ogma (logging)
- pycurity (hashing, time utilities)
- subtrix (UUID generation)

### Optional
- sentence_transformers (vector embeddings)
- condor (config management)

---

## Test Coverage

| Directory | Test Files | Status |
|-----------|------------|--------|
| test_pyffice/unit/ | 50+ test files | 🔶 Partial |
| pyffice/tests/ | 30+ test files | 🔶 Partial |

---

## File Structure

```
pyffice/
├── __init__.py           # Package init, exports
├── pyffice.py            # Main Codex class
├── document.py           # Base document classes
├── cli.py                # CLI interface
├── agent.py              # Agent integration
├── analytics/            # Data analytics
├── audio/                # Audio files
├── cad/                  # CAD formats (STL, OBJ, DWG, etc.)
├── calendars/            # Calendar/Event management ⚠️
├── cam/                  # CAM (G-code, BOM)
├── charts/               # Chart generation
├── config/               # Config formats & ports
├── contacts/             # Contact management
├── container/            # Archive formats
├── data/                 # Data file handlers
├── databases/            # Database connections
├── diagrams/             # Diagram/Sketch
├── ebook/                # E-book formats
├── email/                # Email handling
├── filesystems/          # FS abstraction
├── forms/                # Forms & surveys
├── images/               # Image handling ⚠️
├── items/                # Reusable document items
├── media/                # Media formats
├── notebooks/            # Jupyter notebooks
├── presentation/         # Presentations
├── reports/              # Report generation
├── script/               # Script formats
├── socials/              # Social media
├── spreadsheet/          # Spreadsheets
├── tags/                 # Tagging system
├── updates/              # Change tracking
├── video/                # Video handling
├── web/                  # Web utilities
└── workflows/            # Workflow automation
```

---

## Next Steps

1. ✅ Complete PyfficeCalendar event/task methods
2. 🔶 Implement vector search with sentence_transformers
3. 🔶 Expand test coverage
4. 🔶 Complete PyfficeImageManager
5. 🔶 Implement PyfficeScreenShot capture

---

*Generated by senbot - 2026-03-11*
