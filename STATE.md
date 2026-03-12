# pyffice STATE.md

## Project Overview
- **Project**: pyffice - Document framework for various file types
- **Location**: `/home/solubrew/.orin/workspace/projects/pyffice`
- **Total Classes**: 119 Pyffice-prefixed classes
- **GitVein**: `file:///mnt/overse/SBST01/vein/GitVein/pyffice` (branch: `orin-ws`)

---

## Class Inheritance Analysis

### ✅ Classes Properly Subclassing PyfficeDocument (34 classes)

These are correct and need no changes:

| Class | File | Status |
|-------|------|--------|
| PyfficeAudio | audio/audio.py | ✅ |
| PyfficeBibliography | text/text.py | ✅ |
| PyfficeCAM | cam/cam.py | ✅ |
| PyfficeChart | charts/charts.py | ✅ |
| PyfficeColorPalette | items/colors.py | ✅ |
| PyfficeConfig | config/config.py | ✅ |
| PyfficeContact | contacts/contacts.py | ✅ |
| PyfficeContext | web/prompts.py | ✅ |
| PyfficeDataView | analytics/sources.py | ✅ |
| PyfficeDeque | document.py | ✅ (also deque) |
| PyfficeDocumentManager | document.py | ✅ |
| PyfficeForm | forms/forms.py | ✅ |
| PyfficeGCode | cam/gcode.py | ✅ |
| PyfficeImage | images/images.py | ✅ |
| PyfficeMessage | socials/messages.py | ✅ |
| PyfficeNotebook | notebooks/notebooks.py | ✅ |
| PyfficeOBJ | cad/obj.py | ✅ |
| PyfficePDF | images/pdfs.py | ✅ |
| PyfficePersona | items/persona.py | ✅ |
| PyfficePlaylist | workflows/playlists.py | ✅ |
| PyfficePresentation | presentation/presentation.py | ✅ |
| PyfficePrompt | web/prompts.py | ✅ |
| PyfficeResponse | forms/surveys.py | ✅ |
| PyfficeScreenShot | images/images.py | ✅ |
| PyfficeScript | text/text.py | ✅ |
| PyfficeService | web/services.py | ✅ |
| PyfficeShape | cad/items.py | ✅ |
| PyfficeSpreadSheet | spreadsheet/spreadsheet.py | ✅ |
| PyfficeSurvey | forms/surveys.py | ✅ |
| PyfficeVideo | video/video.py | ✅ |
| PyfficeWebBrowser | web/web.py | ✅ |
| PyfficeWebPage | web/web.py | ✅ |
| PyfficeWork | items/tasks.py | ✅ |

---

### ⚠️ Classes Subclassing PyfficeUnit (but NOT PyfficeDocument)

These are component/item classes that may or may not need to be documents:

| Class | File | Current Base | Notes |
|-------|------|--------------|-------|
| PyfficeBackground | items/cells.py | PyfficeUnit | Component - likely OK |
| PyfficeCell | items/cells.py | PyfficeUnit | Component - likely OK |
| PyfficeColor | items/colors.py | PyfficeUnit | Component - likely OK |
| PyfficeEdge | diagrams/diagrams.py | PyfficeUnit | Component - likely OK |
| PyfficeEvent | calendars/tasks.py | PyfficeUnit | ⚠️ Should be PyfficeDocument? |
| PyfficeFormula | workflows/formulas.py | PyfficeUnit | Component - likely OK |
| PyfficeLayer | diagrams/diagrams.py | PyfficeUnit | Component - likely OK |
| PyfficeNode | diagrams/diagrams.py | PyfficeUnit | Component - likely OK |
| PyfficePage | items/text.py | PyfficeUnit | ⚠️ Should be PyfficeDocument? |
| PyfficeParagraph | items/text.py | PyfficeUnit | Component - likely OK |
| PyfficePart | items/items.py | PyfficeUnit | Component - likely OK |
| PyfficePolicy | config/policies.py | PyfficeUnit | ⚠️ Should be PyfficeDocument? |
| PyfficeSketchConnection | diagrams/diagrams.py | PyfficeUnit | Component - likely OK |
| PyfficeTable | databases/table.py | PyfficeUnit | ⚠️ Also in items/items.py - check |
| PyfficeTask | calendars/tasks.py | PyfficeUnit | ⚠️ Should be PyfficeDocument? |
| PyfficeText | items/text.py | PyfficeUnit | Component - likely OK |
| PyfficeTimeUnit | calendars/tasks.py | PyfficeUnit | Component - likely OK |
| PyfficeURL | web/url.py | PyfficeUnit | ⚠️ Should be PyfficeDocument? |

---

### ❌ Classes With Non-Standard Inheritance

| Class | File | Current Base | Issue | Recommendation |
|-------|------|--------------|-------|----------------|
| PyfficeAlarm | workflows/alarms.py | PyfficeEvent | Event→Unit | Change to PyfficeDocument |
| PyfficeAutomationManager | workflows/automations.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeBOM | cam/bom.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeBinaryContainer | container/binary.py | object | Container | OK as utility class |
| PyfficeCADAssembly | cad/cad.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeCADManager | cad/cad.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeCADPart | cad/cad.py | PyfficePart→PyfficeUnit | Part is Unit | OK as component |
| PyfficeCAMManager | cam/cam.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeCalendar | calendars/calendars.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeCodex | pyffice.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeCodexError | pyffice.py | Exception | Exception | OK (exception class) |
| PyfficeDataSet | analytics/sources.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeDatabaseConnection | databases/databases.py | sonql.Doc | ⚠️ External base | Change to PyfficeDocument |
| PyfficeDatabaseManager | databases/databases.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeDocumentUpdate | updates/updates.py | PyfficeUpdate | Update class | OK (utility) |
| PyfficeENV | config/env.py | object | Config utility | OK (utility class) |
| PyfficeEmailMessage | email/email.py | PyfficeMessage→PyfficeDocument | ✅ OK | - |
| PyfficeFileSystem | filesystems/filesystems.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeFormulasLibrary | workflows/formulas.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeGanttChart | calendars/gantt.py | object | ⚠️ Should be PyfficeDocument | Change to PyfficeDocument |
| PyfficeHTML | items/text.py | PyfficeText→PyfficeUnit | ⚠️ Should be PyfficeDocument | Change to PyfficeDocument |
| PyfficeHeic | media/heic.py | object | Media utility | OK as utility class |
| PyfficeHelp | config/config.py | PyfficeConfig→PyfficeDocument | ✅ OK | - |
| PyfficeINI | config/ini.py | object | Config utility | OK (utility class) |
| PyfficeImageManager | images/images.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeMMS | socials/messages.py | PyfficeMessage→PyfficeDocument | ✅ OK | - |
| PyfficeMailBox | email/email.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeMatrix | spreadsheet/spreadsheet.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficePlayList | workflows/playlists.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficePort | config/ports.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficePostalMail | socials/messages.py | PyfficeMessage→PyfficeDocument | ✅ OK | - |
| PyfficeProject | items/tasks.py | PyfficeTasksManager→PyfficeDocumentManager | ✅ OK | - |
| PyfficeProjectsManager | items/tasks.py | PyfficeTasksManager→PyfficeDocumentManager | ✅ OK | - |
| PyfficePromptsManager | web/prompts.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeRAR | container/rar.py | object | Container | OK as utility class |
| PyfficeRating | tags/ratings.py | PyfficeTag→object | Tag utility | OK (utility) |
| PyfficeRaw | media/raw.py | object | Media utility | OK as utility class |
| PyfficeRecurrenceManager | items/tasks.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeReference | tags/references.py | PyfficeTag→object | Tag utility | OK (utility) |
| PyfficeReport | reports/reports.py | PyfficeScript→PyfficeDocument | ✅ OK | - |
| PyfficeRolodex | contacts/contacts.py | PyfficeDocumentManager | ✅ OK | - |
| Pyffice7Z | container/sevenzip.py | object | Container | OK as utility class |
| PyfficeShape | items/shapes.py | PyfficeUnit | Component | OK as component |
| PyfficeSMS | socials/messages.py | PyfficeMessage→PyfficeDocument | ✅ OK | - |
| PyfficeSketch | diagrams/diagrams.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeSlideShow | presentation/presentation.py | object | ⚠️ Should be PyfficeDocument | Change to PyfficeDocument |
| PyfficeSoftwareBOM | cam/bom.py | PyfficeBOM→PyfficeDocumentManager | ✅ OK | - |
| PyfficeSources | analytics/sources.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeSTL | cad/stl.py | object | CAD utility | OK as utility class |
| PyfficeSurveyManager | forms/surveys.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeTagsManager | tags/manager.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeTar | container/tar.py | object | Container | OK as utility class |
| PyfficeTaskFrame | items/tasks.py | PyfficeTask→PyfficeUnit | Task component | OK as component |
| PyfficeTasksManager | items/tasks.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeTOML | config/config.py | PyfficeConfig→PyfficeDocument | ✅ OK | - |
| PyfficeTag | tags/tags.py | object | Tag utility | OK (utility) |
| PyfficeUnitUpdate | updates/updates.py | PyfficeUpdate | Update class | OK (utility) |
| PyfficeUpdate | updates/updates.py | object | Update base | OK (utility) |
| PyfficeURLLibrary | web/url.py | PyfficeDocumentManager | ✅ OK | - |
| PyfficeWebProfile | web/web.py | PyfficeContact→PyfficeDocument | ✅ OK | - |
| PyfficeWebProfileManager | web/web.py | PyfficeRolodex→PyfficeDocumentManager | ✅ OK | - |
| PyfficeZip | container/zip.py | object | Container | OK as utility class |

---

## Module Structure (33 folders)

| Module | Classes | Document Classes | Component Classes |
|--------|---------|------------------|-------------------|
| analytics | 3 | 2 (DataView, Sources) | 1 (DataSet manager) |
| audio | 1 | 1 (Audio) | 0 |
| cad | 9 | 2 (OBJ, CAM) | 7 (parts, STL, etc.) |
| calendars | 4 | 1 (Calendar) | 3 (Event, Task, Gantt) |
| cam | 4 | 2 (CAM, GCode) | 2 (BOM, Manager) |
| charts | 1 | 1 (Chart) | 0 |
| config | 14 | 3 (Config, TOML, Help) | 11 (ports, env, etc.) |
| contacts | 2 | 2 (Contact, Rolodex) | 0 |
| container | 6 | 0 | 6 (all utility) |
| databases | 3 | 2 (Manager, Connection*) | 1 (Table*) |
| diagrams | 5 | 1 (Sketch) | 4 (Node, Edge, Layer, Connection) |
| ebook | 0 | 0 | 0 |
| email | 2 | 2 (Message, MailBox) | 0 |
| filesystems | 1 | 1 (FileSystem) | 0 |
| forms | 5 | 4 (Form, Survey, Response, Manager) | 1 (SurveyManager) |
| images | 4 | 3 (Image, PDF, ScreenShot) | 1 (Manager) |
| items | 12 | 2 (Persona, Work) | 10 (cells, colors, shapes, etc.) |
| matrix | 0 | 0 | 0 |
| media | 3 | 0 | 3 (all utility) |
| notebooks | 1 | 1 (Notebook) | 0 |
| presentation | 2 | 1 (Presentation) | 1 (SlideShow*) |
| reports | 1 | 1 (Report→Script→Document) | 0 |
| script | 0 | 0 | 0 |
| socials | 4 | 4 (Message, SMS, MMS, Postal) | 0 |
| spreadsheet | 2 | 2 (SpreadSheet, Matrix) | 0 |
| tags | 5 | 1 (Manager) | 4 (Tag, Rating, Reference) |
| tests | 0 | 0 | 0 |
| text | 4 | 2 (Script, Bibliography) | 2 (Text*, Page*, HTML*) |
| updates | 3 | 0 | 3 (all utility) |
| video | 1 | 1 (Video) | 0 |
| web | 8 | 6 (Browser, Page, Service, Prompt, Context, URL*) | 2 (Profile, ProfileManager) |
| workflows | 5 | 2 (Playlist, Formula*) | 3 (Workflow, Alarm*, Automation) |

*Marked items need review

---

## Changes Required

### High Priority (Should be PyfficeDocument)

1. **PyfficeGanttChart** (`calendars/gantt.py`) - Currently `object`
   - Should subclass `PyfficeDocument`

2. **PyfficeHTML** (`items/text.py`) - Currently `PyfficeText→PyfficeUnit`
   - Should subclass `PyfficeDocument`

3. **PyfficeSlideShow** (`presentation/presentation.py`) - Currently `object`
   - Should subclass `PyfficeDocument`

4. **PyfficeAlarm** (`workflows/alarms.py`) - Currently `PyfficeEvent→PyfficeUnit`
   - Should subclass `PyfficeDocument`

5. **PyfficeDatabaseConnection** (`databases/databases.py`) - Currently `sonql.Doc`
   - Should subclass `PyfficeDocument`

6. **PyfficeURL** (`web/url.py`) - Currently `PyfficeUnit`
   - Should subclass `PyfficeDocument`

### Medium Priority (Review Needed)

1. **PyfficeEvent**, **PyfficeTask** - Calendar events/tasks - consider if they need document capabilities
2. **PyfficePolicy** - Config policy - may need document capabilities
3. **PyfficePage** - Text page - may need document capabilities

### Low Priority (OK as-is)

- Container classes (Zip, Tar, RAR, 7Z, Binary) - Utility classes, don't need document inheritance
- Media classes (Heic, Raw, STL) - Utility classes
- Tag/Rating classes - Utility classes
- Exception classes - OK

---

## Summary

| Category | Count |
|----------|-------|
| Total Pyffice classes | 119 |
| ✅ Properly subclass PyfficeDocument | 34 |
| ⚠️ Subclass PyfficeUnit (review) | 18 |
| ❌ Need to be changed to PyfficeDocument | 6 |
| ✅ OK as utility/component classes | ~61 |

---

## Version History

| Date | Change | Author |
|------|--------|--------|
| 2026-03-11 | Initial STATE.md created | senbot |
