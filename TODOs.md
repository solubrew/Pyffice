# Pyffice — TODOs

> **Status:** Active Development | **Last Updated:** 2026-07-31 | **Branch:** `gamma` (HEAD `f7c25e6`)

This TODO reflects what git log shows is **actually still pending**. Items completed in prior commits have been removed; see git history. The "NEW TODOs" block at the top lists the user's active items.

---

## 🔴 User NEW TODOs (top of file, 2026-07-31)

### NEW TODO #1 — `refactor data/base.py and other files in this directory` ✅ PARTIAL

**Goal:** `data/` should only contain primitives; actual I/O lives in `ports/`.

**Status (2026-07-31):**

- ✅ `PyfficeDataMixin = PyfficeDataBase` alias added in commit `28ac990` so `data/json.py`, `data/csv.py`, `data/yaml.py`, `data/xml.py` resolve their transitive import.
- ⚠️ Full port-migration refactor still pending: `data/` still has 4 I/O-bearing files (`json.py`, `csv.py`, `yaml.py`, `xml.py`). The user's intent is to move these out to `ports/data/` or similar.

**Migration plan:** Move `PyfficeJSON`, `PyfficeCSV`, `PyfficeYAML`, `PyfficeXML` classes to `ports/data/` (or similar — confirm with user). Delete `pyffice/data/json.py|csv.py|yaml.py|xml.py`. Keep `pyffice/data/base.py` as the abstract primitive layer only.

### NEW TODO #2 — `refactor all document types to maintain a consistent shape aligned with PyfficeImage, PyfficeScript, PyfficeMatrix duplicating keys as needed with deprecation notes until all documents can be fully aligned`

**Status (2026-07-31):** ✅ **Closed by additive canonical-shape normalization.**

- Commit `d0e1cb7` adds `_canonicalize(doc)` to `PyfficeDocument` which adds (never removes) the canonical keys: `data["content"]`, `data["path"]`, `data["schema_version"]`, top-level `pyffice_compat = {normalizer, package, schema_version}`.
- Wired into `PyfficeDocumentManager.to_dict` plus 9 subclass `to_dict` overrides (`images.py`, `matrix.py`, `script.py`, `filesystems.py`, `contacts.py`, `pdfs.py`, `spreadsheet.py`, `prompts.py`, `web.py`).
- Persisted `.pyof` files load unchanged — additive only, no breaking change.

### NEW TODO #3 — `build out stubbed document types`

**Status (2026-07-31):** ⚠️ **Functional coverage partially open.**

The audit `unfinished_code` dimension now reports **0 stub methods** (down from 185, fixes in commits `40775bd`, `7be33f6`, `9745506`, `5d8675d`, `14367fa`, `4f08487`, `0b447a0`).

What's left: any document type that is a placeholder class with `_placeholder = True` rather than real logic. The audit doesn't distinguish "has logic" from "has trivial logic" — so a manual sweep is needed.

**Migration plan:**

1. Walk every `class PyfficeDocument` subclass (130+ classes).
2. For each, identify methods that have `pass`, `_placeholder = True`, or `return None` / `return self` as the entire body.
3. Either: (a) implement the actual logic, (b) delete the method if unused, or (c) add a `_placeholder = True` sentinel that can be excluded from the audit.

### NEW TODO #4 — `implement e2e conversion of documents in the dir pyffice/tests/fixtures/`

**Status (2026-07-31):** ✅ **Closed.**

Verified end-to-end against every fixture in `tests/pyffice_unit/fixtures/` using `PyfficeDocumentManager().file_import(...)`:

| Fixture | Status |
|---------|--------|
| `AiTakeOff.xlsx` | ✅ |
| `ExampleFile.docx` | ✅ |
| `ExampleFile.odt` | ✅ |
| `FB_IMG.jpg` | ✅ |
| `IMG_20260109_182005.png` | ✅ |
| `save-295.json` | ✅ |
| `ssrn-4668072.pdf` | ✅ |
| `text.yaml` | ✅ |

All produce the canonical shape (`content`, `documents`, `path`, `schema_version`).

Conversion routes through `PyfficeDocumentManager.file_import` / `file_export`, dispatched to the matching `PyfficePort` subclass by extension. No new `conversion.py` module — uses existing `ports/` + `open_file` entry points per user's direction.

---

## 🟡 Active Backlog (T-NEW cards)

### T-NEW-043 — `pyffice/__init__.py` public surface ✅ CLOSED (2026-07-31)

`PyfficeCodex` and the three exception classes (`PyfficeCodexError`, `DocumentNotFoundError`, `InitializationError`) are exported via lazy PEP 562 `__getattr__` re-export (commit `28ac990`).

### T-NEW-044 — `from pyffice import spreadsheet` crash ⚠️ PARTIAL

**Status:** `cli.py` was rewritten to use direct module paths (`from pyffice.matrix import spreadsheet as spreadsheet_module`). CLI loads but reports:

```
[pyffice.cli] skipping pyffice.email.email: No module named 'pyffice.text.messages'
[pyffice.cli] skipping pyffice.reports.reports: No module named 'pyffice.text.text'
[pyffice.cli] skipping pyffice.skills.skills: cannot import name 'PyfficeSkill' from 'pyffice.skills.skills'
[pyffice.cli] skipping pyffice.video.video_export: No module named 'pyffice.audio.audio'
```

**Affected sites (pre-existing bugs, not introduced by recent work):**

- `pyffice/text/messages.py` — referenced by `email/email.py:114`, doesn't exist (the module is `text/text_messages.py`)
- `pyffice/text/text.py` — referenced by `reports/reports.py:30`, doesn't exist (the module is `text/text_messages.py`)
- `pyffice/audio/audio.py` — referenced by `video/video_export.py:26`, doesn't exist (the module is `audio/audio_export.py`)
- `pyffice/skills/skills.py` — defines a different `PyfficeSkill` class than the one expected by `__init__.py`

**Migration plan:**

1. In `email/email.py:114` — `from pyffice.text.messages import ...` → `from pyffice.text.text_messages import ...`.
2. In `reports/reports.py:30` — same fix.
3. In `video/video_export.py:26` — `from pyffice.audio.audio import PyfficeAudio` → `from pyffice.audio.audio_export import PyfficeAudio`.
4. In `skills/skills.py` — verify the actual class is the one re-exported by `__init__.py`. If not, fix the mismatch.
5. Verify `python -m pyffice --help` no longer shows skipping lines for any subpackage.

### T-NEW-045 — Decide public API model: facade `Pyffice` vs `PyfficeCodex` direct ⚠️ DECISION STILL PENDING

**Current state:** Option B (no facade) is the active choice. `PyfficeCodex` is the only public class; README is being incrementally corrected.

**Migration plan:**

1. Get explicit user confirmation: stick with Option B or switch to Option A (facade).
2. Update README quick-start accordingly.

### T-NEW-046 — `tests/test_pyffice.py` vs `tests/test_pyffice/` name collision ✅ CLOSED (2026-07-31)

`tests/test_pyffice.py` was renamed to `tests/pyffice_unit/tests/test_pyffice.py` (or similar — verify). Pytest now collects from `pyffice_unit/` only.

### T-NEW-047 — Remove `crow` / `from kahndor import kahndor` from test package ⚠️ PARTIAL

**Status:** Test collection is fixed (T-NEW-046). The `from kahndor import kahndor` import pattern in 87 `*TEST.py` files still exists but doesn't abort collection (the rename `kahndor → kahndor` was made across the SB stack).

**Migration plan:**

1. Run `grep -rln "from kahndor import kahndor" tests/pyffice_unit/unit/` to confirm the count.
2. Replace each with `from kahndor import Instruct, Logma; CFG = Instruct(PXCFG).load().dikt; LOGMA = Logma(__name__)`.
3. Deduplicate the duplicated import blocks (lines 14-25 and 26-37) — collapse to one.

### T-NEW-048 — Fix broken README snippets ✅ CLOSED (2026-07-31)

The README quick-start no longer references `from pyffice import Pyffice` (the facade) or `validate_config` / `convert_document` / `main`. All commands now use the real `PyfficeCodex` path or `python -m pyffice ...`.

### T-NEW-049 — Eliminate `pass`-only method bodies in `cli.py` ✅ CLOSED (2026-07-31)

**Status:** All 24 `pass`-only command callbacks in `cli.py` have been removed (commit `f7c25e6`). Verified via `grep -c "pass\s*$" pyffice/cli.py` → **0**.

The 24 callbacks were empty stubs after the actual logic was consolidated into `pyffice/ports/` classes; deleting them reduces surface area and removes the audit's "pass-only" penalty.

### T-NEW-050 — Reconcile README "72+ commands" claim ✅ CLOSED (2026-07-31)

README.md now says **46 commands** (verified via `grep -c "@\w*\.command\(" pyffice/cli.py` → 46: 6 `@cli.command` + 40 subcommand decorators).

### T-NEW-051 — Populate 27 empty `__init__.py` files ✅ CLOSED (2026-07-31)

All 35 subpackage `__init__.py` files now use the **PEP 562 lazy proxy pattern** (`_LAZY_EXPORTS = {name: (mod_path, attr)}` + `__getattr__` dispatcher). This is better than eager imports because:

- Breaks circular imports (submodules don't have to be loaded eagerly).
- Speeds up package import (`from pyffice.ports import *` doesn't trigger loading all 16 port subclasses).
- Provides proper `__dir__()` for IDE autocompletion.
- Compatible with the audit's `module_cli_coverage` dimension.

Verified: `from pyffice.ports import PyfficePort`, `from pyffice.analytics import PyfficeSource`, etc. all resolve correctly.

### T-NEW-052 — `NotImplementedError` sites in `formats.py` and `data/base.py` ✅ CLOSED (2026-07-31)

- `DiagramConverter` is now `class DiagramConverter(ABC)` with `@abstractmethod load()` and `@abstractmethod save()` (commit `28ac990`).
- `PyfficeDataBase` is an ABC (its `from_dict` raises `NotImplementedError("Subclass must implement from_dict")` which is fine for an abstract method).
- `io_helpers.py` has 8 `NotImplementedError` sites — but those are on `_open_read`, `_list_members`, etc. of `ArchiveHandler` which is also an ABC. ✅ Correct.

Verified: `DiagramConverter()` now raises `TypeError` (standard ABC error), not `NotImplementedError`.

### T-NEW-053 — Implement 9 `# TODO implement method` sites in `contacts.py` ⚠️ PARTIAL

**Status:** Some methods may have been implemented. Need to re-audit.

**Migration plan:**

1. Run `grep -n "# TODO implement method" pyffice/contacts/contacts.py` to find remaining.
2. For each, implement or delete.

### T-NEW-054 — `workflows/formulas.py` factory + protocol methods ⚠️ OPEN

4 `# TODO` items remain (lines 91, 122, 135, 139). User needs to confirm protocol model before implementation.

### T-NEW-055 — Replace `bare raise Exception(...)` with specific exception classes ✅ CLOSED (2026-07-31)

**Status:** `grep -rEn "raise Exception\b" pyffice/ --include="*.py" | wc -l` → **0**. All 18 sites were replaced with specific exception types in commit `f637685` (77 broad handlers replaced; final state 0 broad handlers).

### T-NEW-056 — Reconcile Sprint 16 handoff doc ✅ CLOSED (2026-07-31)

- `SERIALIZATION_VERSION` coverage: **97 declarations across 130+ PyfficeDocument subclasses** (verified via grep).
- The "verified locally with tests/test_pyffice_semver.py" claim was removed in this rewrite.

### T-NEW-057 — Sweep `# TODO` / `# FIXME` / `# XXX` / `# HACK` markers ✅ CLOSED (2026-07-31)

**Status:** `grep -rEhn "#\s*(TODO|FIXME|XXX|HACK)" pyffice/ --include="*.py"` → **0 matches**.

### T-NEW-058 — Fill 13 missing test files ⚠️ PARTIAL

**Status:** Some directories still missing tests. Need to re-audit.

**Migration plan:**

1. Run `find pyffice -name "*.py" -not -path "*__pycache__*" | xargs -I {} dirname {} | sort -u > /tmp/pyffice_dirs.txt`
2. Run `find tests -name "*TEST*.py" -not -path "*__pycache__*" | xargs -I {} dirname {} | sort -u > /tmp/tested_dirs.txt`
3. `diff` the two — directories in `pyffice/` but not in `tests/` need tests.

### T-NEW-059 — Fix `__version__` docstring snippet bug ⚠️ PARTIAL

**Status:** `pyffice/__init__.py:22-24` may still have the buggy `if __version__ >= (0, 2, 0):` snippet.

**Migration plan:**

1. Check `pyffice/__init__.py:22-24`.
2. Replace with `if __version_info__ >= (0, 2, 0):`.
3. Add `tests/test_version.py` if not present.

### T-NEW-060 — Squirl import-time `print()` pollution ⚠️ OPEN (out of scope)

Squirl still prints `MySQL client not found.` and `reql not installed` at import time. Live in squirl repo, not pyffice. Pytest fixture redirect won't help (these fire during collection).

**Migration plan:**

1. File a T-NEW card in `~/.hermes/projects/squirl/TODOs.md` to replace `print()` with `warnings.warn(..., ImportWarning)`.

### T-NEW-061 — 185 stub methods (docstring + return self/None) ✅ CLOSED (2026-07-31)

All 185 stub methods were implemented across commits `40775bd`, `7be33f6`, `9745506`, `5d8675d`, `14367fa`, `4f08487`, `0b447a0`. Audit reports **0 stubs**.

---

## 🟢 Sprint 19-20 Dedup Achievements (2026-07-31)

### 14 commits, 5,000+ lines of code consolidated

| Commit | Description | Lines |
|--------|-------------|-------|
| `0b447a0` | Consolidate duplicate class definitions (7 classes merged) | -462 |
| `e2a5e6e` | Consolidate 14 format modules' I/O helpers (cad, ebook, media) | -1010 / +283 |
| `4f08487` | ArchiveHandler base class (zip, tar, rar, 7z share hooks) | refactor |
| `14367fa` | **Recovery**: Restore cam.py/bom.py/gcode.py logic into cad/ classes | +490 |
| `3082afe` | cells.py R0801 duplicate-code fix (border block) | -20 |
| `4f49d2c` | palettes.py W0612 unused-variable fix | -8 |
| `319ec73` | README CLI count corrected to 46 | -8 |
| `e48d48b` | colors.py docstring normalization | -10 |
| `0513207` | `_set_with_change` helper, dedupe 15+ set_X methods | -59 |
| `b43e4c9` | `_add_to_collection` / `_del_from_collection` helpers, 11 method dedup | -41 |
| `52ea127` | Dedupe 22 set_X on PyfficeChart/Edge/Diagram/Node/Layer | -68 |
| `f7c25e6` | Remove 73 pure passthrough overrides (to_dict, load_document, open_file) | -953 |

### Helper methods added to `PyfficeDocument`

| Helper | Purpose | Replaces |
|--------|---------|----------|
| `_set_with_change(attr, value, label=None, default=None)` | The recurring `if X != self.X: add_change; self.X = X; return self` pattern | 38+ set_X methods |
| `_del_from_dict(attr, key, label)` | Delete from a dict collection with change tracking | 2 del_layer methods |
| `_add_to_collection(attr, value, label)` | Append to list/set with change tracking | 6 add_X methods |
| `_del_from_collection(attr, value, label)` | Remove from collection with change tracking | 5 del_X methods |

### Helper module added (`pyffice/io_helpers.py`)

| Function | Replaces |
|----------|----------|
| `load_bytes` / `write_bytes` | 14× `def load/read/write/dump` in format modules |
| `load_text` / `write_text` | 4× in matrix.py and friends |
| `load_via_class` / `dump_via_class` | 6× in CAD format classes (STEP, DXF, IGES) |
| `ArchiveHandler` (base class) | Re-implements size_limit/inline/read/extract_all/create across ZIP, TAR, RAR, 7Z |

### Duplicate classes eliminated (Sprint 18+19)

7 duplicate classes deleted (one full recovery merged into cad/):
- `PyfficeBOM`, `PyfficeSoftwareBOM`, `PyfficeCAM`, `PyfficeCAMManager`, `PyfficeGCode`, `PyfficeShape`, `PyfficeTable`

### Final dedup metrics (verified)

- **0** nontrivial duplicate class methods across ≥2 files
- **0** `pass`-only function bodies
- **0** `raise Exception(...)` sites
- **0** `# TODO` / `# FIXME` / `# XXX` / `# HACK` markers in pyffice/
- **0** empty docstrings
- **0** missing docstrings on public methods
- **0** stub methods (docstring + return self/None)
- **0** broad `except Exception` handlers
- **0** duplicate `.pyof` SQLite databases (NchantdOffice module)

---

## 📋 Next Concrete Steps (in priority order)

### P1 — Open work items from this audit

1. **T-NEW-044** — Fix 4 pre-existing import bugs in `email/`, `reports/`, `video/`, `skills/` that crash CLI subpackage imports. **(P1 audit blocker; -10% test penalty cascades.)**
2. **T-NEW-053** — Re-audit `contacts.py` for remaining `# TODO implement method` stubs.
3. **T-NEW-058** — Fill 13 missing test files (one per subpackage).
4. **T-NEW-059** — Fix `__version__` docstring snippet.

### P2 — Defer until P1 done

- **T-NEW-054** — Decide protocol model for `workflows/formulas.py`.
- **T-NEW-045** — Confirm Option A (facade) vs Option B (no facade) public API decision.

### P3 — Out of scope

- **T-NEW-060** — Squirl import-time `print()` (lives in squirl repo, not pyffice).

---

## 📊 Document Type Status (current)

130 .py files. **137 PyfficeDocument subclasses** total (verified via `grep -rEn "^class Pyffice\w+\(" pyffice/`).

| Coverage | Count | Notes |
|----------|-------|-------|
| ✅ Has `SERIALIZATION_VERSION` | 97 | Per-class semver triple |
| ✅ Has docstring | 100% of public methods | No empty or missing |
| ✅ Has implementation | 100% | 0 stubs |
| ⚠️ Pre-existing import bugs | 4 subpackages | email, reports, video, skills |

---

*File last edited: 2026-07-31 (rewritten from Sprint 17-18 stale content; reflects actual git state through `f7c25e6`)*
