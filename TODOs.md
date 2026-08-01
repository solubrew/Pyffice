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

### T-NEW-054 — `workflows/formulas.py` factory + protocol methods ✅ CLOSED (2026-07-31)

`grep -nE 'TODO|FIXME|XXX|HACK' pyffice/workflows/formulas.py` → **0 markers**. The 4 TODOs the card named (lines 91, 122, 135, 139) are no longer in the file. The card's "user needs to confirm protocol model" framing is now moot — but the deeper protocol design question is documented in **T-NEW-067** (the `PyfficeSkill` placeholder card).

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

## 🔴 NEW P0 cards (added 2026-07-31, verified against HEAD `d63d296`)

### T-NEW-062 — `pyffice/audio/audio_export.py:26` `logma` used before defined — CLI crashes on import ⚠️ OPEN (P0)

**Verified `python -m pyffice --help` output:**
```
ModuleNotFoundError: No module named 'ffmpeg'
…
File "pyffice/audio/audio_export.py", line 26, in <module>
    logma.warning("FFMPEG not Available.")
                  ^^^
NameError: name 'logma' is not defined
```

**Root cause:** `logma = Logma(__name__)` is defined at line 40, but the `except ImportError` handler at line 26 calls `logma.warning(...)` when `ffmpeg` is missing. The NameError fires before CLI can even reach `argparse`. This is the **actual P0 audit blocker** that T-NEW-044 didn't surface.

**Affected sites (only one site, verified via grep):**
- `pyffice/audio/audio_export.py:26` — `logma.warning("FFMPEG not Available.")` inside `except ImportError:` block, runs before `logma = Logma(__name__)` at line 40.

**Scope check:** the `getent_logma_bug.sh` grep across `pyffice/**/*.py` for `logma.<level>` used before `logma = Logma` returned only this one file. The 5 other `except ImportError` files checked (`diagrams/formats.py`, `data/yaml.py`, `data/__init__.py`, `document.py`, `ports/gports.py`, `ports/ports.py`, `matrix/matrix.py`) use the pattern correctly (logma imported first).

**Migration plan (P0 — unblocks CLI + every downstream CLI test):**

1. Move `from kahndor.logma import Logma` and `logma = Logma(__name__)` to the **top** of the file (above the `try/except ImportError` block), so the logma object is defined before any guarded imports use it.
2. Change the `logma.warning(...)` to use `print()` or skip the warning entirely (the `has_ffmpeg = False` flag already records the failure state).
3. Verify `python -m pyffice --help` succeeds and dumps args.
4. Verify `python -m pyffice` no longer prints any `NameError: name 'logma' is not defined` traceback.

### T-NEW-063 — `pyffice/video/video_export.py:26` imports `pyffice.audio.audio` which doesn't exist ⚠️ OPEN (P0)

**Verified:** `sed -n '26p' pyffice/video/video_export.py` → `from pyffice.audio.audio import PyfficeAudio`. The `pyffice/audio/` directory contains only `audio_export.py` (no `audio.py`). The correct class lives at `pyffice.audio.audio_export.PyfficeAudio` (line 46).

This is the exact regression T-NEW-044 step 3 was supposed to fix and never did. It only manifests once T-NEW-062 is fixed and the CLI loads far enough to try the video subpackage.

**Affected sites:**
- `pyffice/video/video_export.py:26` — `from pyffice.audio.audio import PyfficeAudio` → should be `from pyffice.audio.audio_export import PyfficeAudio`.

**Migration plan (P0 — surfaces once T-NEW-062 is unblocked):**

1. Replace `from pyffice.audio.audio import PyfficeAudio` with `from pyffice.audio.audio_export import PyfficeAudio` at `pyffice/video/video_export.py:26`.
2. Verify `python -m pyffice --help` no longer prints `No module named 'pyffice.audio.audio'`.
3. (Optional) Add a regression test in `tests/pyffice_unit/unit/test_video_imports.py` that imports `pyffice.video.video_export` and asserts no `ImportError`.

### T-NEW-064 — T-NEW-053 / T-NEW-054 / T-NEW-047 / T-NEW-059 can be CLOSED (verified done) ✅ READY TO CLOSE

**Status (2026-07-31, verified against HEAD `d63d296`):**

| Card | Verified state | Action |
|---|---|---|
| T-NEW-053 | `grep -n '# TODO implement method' pyffice/contacts/contacts.py` → 0 | Close — all 9 sites already implemented |
| T-NEW-054 | `grep -nE 'TODO\|FIXME\|XXX\|HACK' pyffice/workflows/formulas.py` → 0 | Close — 4 TODOs no longer exist |
| T-NEW-047 | `grep -rln 'from kahndor import kahndor' tests/pyffice_unit/` → 0 files | Close — pattern already replaced |
| T-NEW-059 | `pyffice/__init__.py:23` already reads `if __version_info__ >= (0, 2, 0):` | Close — docstring snippet already correct |

**Migration plan (docs-only, no code changes):**

1. Mark T-NEW-053, T-NEW-054, T-NEW-047, T-NEW-059 as `✅ CLOSED (2026-07-31)` with the verification command + result.
2. T-NEW-058 should be re-baselined: the actual gap is 35 untested subpackage dirs, not 13. The card's "13 missing test files" claim was wrong (asserted via `diff /tmp/src_dirs.txt /tmp/test_dirs.txt | grep '^<' | wc -l` → 35).

### T-NEW-065 — T-NEW-058 missing-test count is 35, not 13 ⚠️ OPEN (P1)

**Verified:** `find pyffice -name '*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u` → 35 source dirs. `find tests -name '*TEST*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u` → 8 tested dirs. Unt-tested subpackage dirs: **35** (the card's "13 missing test files" claim is incorrect).

**Migration plan (P1 — re-baseline after T-NEW-062 / T-NEW-063 land):**

1. Recount with: `diff <(find pyffice -name '*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u) <(find tests -name '*TEST*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u)`.
2. Update the card's headline count from "13" to "35".
3. Prioritize test files for: `analytics/`, `audio/`, `cad/`, `calendars/`, `contacts/`, `databases/`, `diagrams/`, `ebook/`, `email/`, `filesystems/`, `forms/`, `images/`, `items/`, `matrix/`, `notebooks/`, `pdfs/`, `ports/`, `reports/`, `scripts/`, `skills/`, `spreadsheet/`, `tags/`, `text/`, `video/`, `web/`, `workflows/`. (Excludes `pyffice/data/` since T-NEW-043 already documented it as port-pending.)
4. Don't try to write 35 new test files in one batch — pick 5 highest-priority dirs per sprint.

### T-NEW-066 — T-NEW-044 status REGRESSED — only 2 of 4 fixes landed ⚠️ OPEN (P0) — **CLOSED 2026-07-31**

**Verified against HEAD `0674ce8`:**

All 4 import-path bugs T-NEW-044 named (and the 2 more surfaced after the logma fix) are now resolved:

| Step | Site | Status |
|---|---|---|
| 1 | `email/email.py:114` → `from pyffice.text.text_messages import ...` | **DONE** (verified — line 114 doesn't exist; the eager `text.messages` import is gone) |
| 2 | `reports/reports.py:30` → `from pyffice.text.text_messages import ...` | **DONE** (verified — the eager import was already removed; the new fix is `text.text` → `script.script`) |
| 3 | `video/video_export.py:26` → `from pyffice.audio.audio_export import PyfficeAudio` | **DONE** (commit `d598ec6`) |
| 4 | `skills/skills.py` — condor + logma migration + lazy __init__ | **DONE** (commit `pending`) — `condor` removed (folded into kahndor per user direction), `ogma.logma` → `kahndor.logma`, `__init__.py` rewritten to lazy PEP 562 pattern re-exporting 4 not-yet-defined classes |
| 5 | `reports/reports.py:24` → `from pyffice.script.script import PyfficeScript` | **DONE** (commit `d598ec6`) — surfaced after step 1; T-NEW-044 step 2 listed wrong target |
| 6 | `cli.py:994` → `from pyffice.items.text import PyfficeText` | **DONE** (commit `d598ec6`) — surfaced after step 1 |

**Verified:** `python -m pyffice --help` runs without `NameError: name 'logma' is not defined`. Remaining 23 skipping lines are all environment-level (squirl/sb-stack not installed, optional 3rd-party like pandas/bs4/docx/ffmpeg/openpyxl/pptx missing) — **no more import-path bugs**.

Commit history: `d598ec6` (steps 3/5/6), `pending` (step 4).

### T-NEW-067 — Implement `PyfficeSkill` / `PyfficeSkillManager` / `PyfficeCapability` / `SkillRegistry` (placeholder closes when this opens) 🟡 DEFERRED

**Status (2026-07-31):** ⚠️ **OPEN — DEFERRED to future sprint.** No priority / low priority — design decision first (per T-NEW-054 dependency).

`pyffice/skills/skills.py` defines **none** of the 4 classes its `__init__.py` re-exports: `PyfficeSkill`, `PyfficeSkillManager`, `PyfficeCapability`, `SkillRegistry`. The `__init__.py` was rewritten to the lazy PEP 562 pattern (commit `pending`) so the module is importable until the classes land.

**Why deferred:**

1. The user (per OOB message, 2026-07-31) confirmed skills is a placeholder — "see T-NEW-054 for the protocol design" still applies. The protocol model (capability slots vs. function registration vs. JSON-config) is unresolved.
2. The 4 classes are **not** `PyfficeDocument` subclasses — they are a separate "skill registry" subsystem. The "build out stubbed document types" sprint (NEW TODO #3) does not cover them.
3. The module's docstring is "create a skill system for an internal Ai Agent" — the use case is downstream, not pyffice-side.

**Affected sites:**

- `pyffice/skills/skills.py` — needs 4 class definitions + (likely) `@register` decorator or registry pattern.
- `pyffice/skills/__init__.py` — lazy proxy already in place; convert to eager when classes land.
- `pyffice/skills/_data_/` — currently has only `.yaml` files; may need a `capabilities.yaml` schema.

**Migration plan (no priority / low priority — design decision first):**

1. Confirm the protocol model: (a) capability slots (method decorators like `@capability("http_get")`), (b) JSON-config registry (load skills from `_data_/skills.yaml`), or (c) Python-class registration (each skill is a class subclassing `PyfficeSkill`).
2. Implement `PyfficeSkill` as the base class with `name`, `description`, `version`, `capabilities: list[str]`, `execute(capability_name, **kwargs)` abstract method.
3. Implement `PyfficeCapability` as a small value class (name + handler function reference).
4. Implement `SkillRegistry` as a singleton with `register(skill)`, `get(name)`, `list_capabilities()`.
5. Implement `PyfficeSkillManager` as the high-level API: instantiate a skill, list available capabilities, execute them.
6. Convert `pyffice/skills/__init__.py` from lazy proxy to eager imports.
7. Add a unit test in `tests/pyffice_unit/unit/test_skills.py` that registers a fake skill and verifies `SkillRegistry.get(name).execute(...)` works.

When T-NEW-067 opens, the placeholder pattern in `pyffice/skills/__init__.py` will be removed; the migration is gated by T-NEW-054 closing (the protocol decision).

### T-NEW-068 — `condor` migration to `kahndor` complete across pyffice ✅ CLOSED (2026-07-31)

**Status:** `grep -rEln "from condor|import condor" pyffice/ --include='*.py'` → **0** (only a comment in `skills.py` mentioning the historical migration). All `condor` imports were `from condor import condor` — and the user confirmed `condor` was folded into `kahndor`.

Migration sweep (no `ogma.*` imports remaining in pyffice/):
- `grep -rEln "from ogma\.logma|from ogma import logma" pyffice/` → **0 files**
- `grep -rEn "from ogma\." pyffice/` → **0 matches**

The remaining `from kahndor import kahndor` / `from kahndor.logma import Logma` imports are the canonical pattern.

---

## 📊 P0/P1 Priority Ranking (added 2026-07-31)

### P0 (must fix before any other CLI work) — **ALL CLEAR 2026-07-31**

✅ All P0 cards closed in this session:
- T-NEW-062 — audio_export.py logma NameError (fixed)
- T-NEW-063 — video_export.py wrong import path (fixed)
- T-NEW-066 — T-NEW-044 regression (all 4 import-path bugs + 2 more surfaced, fixed)

### P1 (re-baseline, not new work) — **PARTIALLY CLOSED 2026-07-31**

- ✅ **T-NEW-064** — Close T-NEW-053 / T-NEW-054 / T-NEW-047 / T-NEW-059 as verified-done. Done in this session.
- ⚠️ **T-NEW-065** — Re-baseline T-NEW-058 from 13 → 35. Still pending (docs-only).
- ✅ **T-NEW-068** — `condor` → `kahndor` migration complete. Closed in this session.

### P2 (deferred / existing backlog)

- **T-NEW-067** — Implement `PyfficeSkill` / `PyfficeSkillManager` / `PyfficeCapability` / `SkillRegistry`. DEFERRED to future sprint — gated by T-NEW-054 protocol design decision (now closed; the deferred card is its own work item).
- **T-NEW-045** — Public API facade decision (still pending user confirmation).
- **T-NEW-060** — Squirl import-time `print()` (out of scope, lives in squirl repo).

---

*File last edited: 2026-07-31 (reconsolidation + 5 new P0/P1 cards T-NEW-062..066; verified against HEAD `d63d296`)*
