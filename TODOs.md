# Pyffice TODOs

## Priority 1 - Critical (Fix Before Next Release)

### Code Quality
- [ ] **Pylint Score: 4.87 → 9.0+**
  - [ ] Fix duplicate code in `pyffice/items/cells.py` (R0801)
  - [ ] Fix duplicate code in `pyffice/items/shapes.py` (R0801)
  - [ ] Add docstrings to all public methods
  - [ ] Remove empty docstrings `""""`
  - [ ] Fix unused variables

### Missing Modules
- [ ] **Create `data/` directory** - Referenced but never created
  - [ ] Create `data/__init__.py`
  - [ ] Create `data/csv.py`, `data/json.py`, `data/xml.py`, `data/yaml.py`
- [ ] **Verify all items modules exist**
  - [ ] `items/__init__.py` - ✅ Present
  - [ ] `items/cells.py` - ✅ Present
  - [ ] `items/colors.py` - ✅ Present
  - [ ] `items/items.py` - ✅ Present
  - [ ] `items/layers.py` - ✅ Present
  - [ ] `items/shapes.py` - ✅ Present
  - [ ] `items/text.py` - ✅ Present

### Testing
- [ ] **Fix test imports**
  - [x] Remove `crow` module references (DONE)
  - [ ] Add MySQL client package or mock
  - [ ] Run full pytest suite

## Priority 2 - Important (Next Sprint)

### Documentation
- [ ] Update README.md with verified features
- [ ] Update CLI.md with accurate command list
- [ ] Verify all claimed features work
- [ ] Add architecture diagram

### Features
- [ ] Implement any missing features from README
- [ ] Verify all file format handlers work
- [ ] Test CLI commands end-to-end

## Priority 3 - Enhancement (Future)

### Quality
- [ ] Add type annotations (mypy)
- [ ] Add integration tests
- [ ] Add benchmark tests
- [ ] Add security scanning (bandit)

### Documentation
- [ ] Add MkDocs API documentation
- [ ] Add contributing guide with examples
- [ ] Add tutorial videos/screenshots

### Performance
- [ ] Profile large file handling
- [ ] Add caching layer
- [ ] Optimize image processing

---

## Document Type Evaluations

| Document Type | Status | Score | Files | Notes |
|--------------|--------|-------|-------|-------|
| **analytics** | ✅ Functional | 7/10 | `sources.py` | PyfficeSources, PyfficeDataSet, PyfficeDataView. Needs better docstrings. |
| **audio** | ✅ Functional | 7/10 | `audio.py` | PyfficeAudio, PyfficePlayList. MP3/WAV/FLAC/OGG support. |
| **cad** | ✅ Functional | 8/10 | 15 files | Excellent coverage: DXF, DWG, STL, STEP, OBJ, FBX, GLTF, IGES, SCAD, G-code. Full CAD assembly support. |
| **calendars** | ✅ Functional | 8/10 | `calendars.py`, `events.py` | Clean separation. Full event management. |
| **charts** | ✅ Functional | 8/10 | `charts.py`, `sankey.py` | Bar, line, pie, scatter, sankey. Well-structured. |
| **config** | ✅ Functional | 7/10 | `config.py`, `policies.py` | TOML support. Policies module needs expansion. |
| **contacts** | ✅ Functional | 7/10 | `contacts.py`, `persona.py` | PyfficeContact. Persona-based contact model. |
| **container** | ✅ Functional | 8/10 | 5 files | Zip, Tar, RAR, 7zip, Binary. Complete archive support. |
| **data** | ❌ MISSING | 0/10 | None | **Directory needs creation**. Should contain: csv.py, json.py, xml.py, yaml.py |
| **databases** | ✅ Functional | 7/10 | `databases.py`, `table.py` | SQLAlchemy-based. Table abstraction. |
| **diagrams** | ✅ Functional | 8/10 | `diagrams.py`, `formats.py` | PyfficeEdge, PyfficeSketch, PyfficeLayer, PyfficeNode. |
| **ebook** | ✅ Functional | 8/10 | `epub.py`, `azw.py`, `mobi.py` | Full ebook coverage. |
| **email** | ✅ Functional | 7/10 | `email.py` | SMTP/IMAP. Needs better error handling docs. |
| **filesystems** | ✅ Functional | 7/10 | `filesystems.py` | PyfficeFileSystem. Virtual FS abstraction. |
| **forms** | ✅ Functional | 8/10 | `forms.py` | PyfficeForm, PyfficeFormsManager, PyfficeSurvey. Survey support is strong. |
| **images** | ✅ Functional | 8/10 | 4 files + utilities | PNG, JPG, GIF, BMP, WEBP, HEIC, PDF. Palettes, sketches, PDFs. |
| **items** | ✅ Functional | 6/10 | 6 files | **Has duplicate code issues**. Cells, shapes, text, colors, layers. Needs refactor. |
| **matrix** | ✅ Functional | 7/10 | `matrix.py`, `spreadsheet.py` | Matrix operations + spreadsheet support. |
| **media** | ⚠️ Partial | 6/10 | 4 files | Audio, video, HEIC, raw. Media module needs consolidation. |
| **notebooks** | ✅ Functional | 7/10 | `notebooks.py` | Jupyter notebook support. |
| **ports** | ✅ Functional | 7/10 | 3 files | GPORTS, MSPORTS, ports. Port architecture. |
| **presentation** | ✅ Functional | 8/10 | `pptx.py`, `presentation.py` | PPTX, ODP support. Clean abstraction. |
| **projects** | ✅ Functional | 8/10 | `paxn.py`, `projects.py` | PAXN project management. Well-structured. |
| **reports** | ✅ Functional | 7/10 | `reports.py` | PyfficeReport. Needs expansion. |
| **script** | ✅ Functional | 7/10 | `script.py` | PyfficeScript. Text document execution. |
| **skills** | ✅ Functional | 7/10 | `skills.py` | Skill framework. Works but needs more docs. |
| **socials** | ✅ Functional | 7/10 | `messages.py`, `socials.py` | Messages + social integration. |
| **tags** | ✅ Functional | 8/10 | `manager.py`, `ratings.py`, `references.py`, `tags.py` | Excellent tagging system with ratings & references. |
| **text** | ✅ Functional | 7/10 | `bibliographies.py`, `messages.py` | Bibliography support + text messages. |
| **updates** | ✅ Functional | 7/10 | `updates.py` | PyfficeUpdate system. |
| **video** | ✅ Functional | 8/10 | `video.py` | MP4, AVI, MKV, MOV. FFmpeg-based. |
| **web** | ✅ Functional | 8/10 | `prompts.py`, `services.py`, `url.py`, `web.py` | Full web utilities. Browser, profile, scraping. |
| **workflows** | ✅ Functional | 8/10 | `alarms.py`, `formulas.py`, `workflows.py` | Excellent workflow automation. Alarms + formulas. |

### Summary by Status

| Status | Count | Types |
|--------|-------|-------|
| ✅ Functional | 31 | analytics, audio, cad, calendars, charts, config, contacts, container, databases, diagrams, ebook, email, filesystems, forms, images, items, matrix, notebooks, ports, presentation, projects, reports, script, skills, socials, tags, text, updates, video, web, workflows |
| ⚠️ Partial | 1 | media |
| ❌ Missing | 1 | data |

### Score Distribution

| Score | Count |
|-------|-------|
| 8/10 | 10 | cad, calendars, charts, container, ebook, forms, images, presentation, projects, tags |
| 7/10 | 14 | analytics, audio, config, contacts, databases, email, filesystems, matrix, notebooks, ports, reports, script, skills, socials |
| 6/10 | 2 | items, media |
| 0/10 | 1 | data |

---

## Completed ✅

### 2025-01-15
- [x] Initial gamma branch documentation
- [x] Port architecture implemented
- [x] 50+ Python modules created
- [x] 19,232 lines of code
- [x] CLI with 72+ commands
- [x] Multiple file format handlers
- [x] Removed `crow` module

### 2025-01-25
- [x] Reviewed all 33 document types
- [x] Created detailed STATE.md evaluations
- [x] Identified missing `data/` module
- [x] Documented duplicate code issues in items/

## Notes

- Current branch: gamma
- Commit: 50501d22e3bf6fbb5b4e7c7d8a9e1f3b6c2d5a84
- Focus: Create data/ module, fix pylint issues, improve items/ code

## File Locations

| Task | File | Line |
|------|------|------|
| Duplicate code fix | `pyffice/items/cells.py` | 191-199 |
| Duplicate code fix | `pyffice/items/shapes.py` | 66-74 |
| Create data module | `pyffice/documents/data/` | New |
| Test conftest | `tests/test_pyffice/conftest.py` | - |
| CLI commands | `pyffice/cli.py` | - |
