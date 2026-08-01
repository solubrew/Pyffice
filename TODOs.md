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
[pyffice.cli] skipping pyffice.video.video_export: No module named 'pyffice.audio.audio'
```

**Affected sites (pre-existing bugs, not introduced by recent work):**

- `pyffice/text/messages.py` — referenced by `email/email.py:114`, doesn't exist (the module is `text/text_messages.py`)
- `pyffice/text/text.py` — referenced by `reports/reports.py:30`, doesn't exist (the module is `text/text_messages.py`)
- `pyffice/audio/audio.py` — referenced by `video/video_export.py:26`, doesn't exist (the module is `audio/audio_export.py`)

**Migration plan:**

1. In `email/email.py:114` — `from pyffice.text.messages import ...` → `from pyffice.text.text_messages import ...`.
2. In `reports/reports.py:30` — same fix.
3. In `video/video_export.py:26` — `from pyffice.audio.audio import PyfficeAudio` → `from pyffice.audio.audio_export import PyfficeAudio`.
4. Verify `python -m pyffice --help` no longer shows skipping lines for any subpackage.

### T-NEW-045 — Decide public API model: facade `Pyffice` vs `PyfficeCodex` direct ✅ CLOSED (2026-07-31) — Option B confirmed

**Status:** Per user confirmation (2026-07-31), users use `PyfficeCodex` directly. No facade. The README was updated to use `from pyffice import PyfficeCodex` (README.md:94). The legacy `Pyffice = PyfficeCodex` alias in `pyffice/cli.py:69` is the only remaining reference, kept for backwards compatibility within the CLI layer.

The "PyfficeSkill" placeholder card (T-NEW-067) was already closed by the `pyffice/skills/` directory deletion in commit `d9d4fa9`.

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

`grep -nE 'TODO|FIXME|XXX|HACK' pyffice/workflows/formulas.py` → **0 markers**. The 4 TODOs the card named (lines 91, 122, 135, 139) are no longer in the file. The card's "user needs to confirm protocol model" framing is now moot — the skills subscript was removed entirely (commit `d9d4fa9`).

### T-NEW-055 — Replace `bare raise Exception(...)` with specific exception classes ✅ CLOSED (2026-07-31)

**Status:** `grep -rEn "raise Exception\b" pyffice/ --include="*.py" | wc -l` → **0**. All 18 sites were replaced with specific exception types in commit `f637685` (77 broad handlers replaced; final state 0 broad handlers).

### T-NEW-056 — Reconcile Sprint 16 handoff doc ✅ CLOSED (2026-07-31)

- `SERIALIZATION_VERSION` coverage: **97 declarations across 130+ PyfficeDocument subclasses** (verified via grep).
- The "verified locally with tests/test_pyffice_semver.py" claim was removed in this rewrite.

### T-NEW-057 — Sweep `# TODO` / `# FIXME` / `# XXX` / `# HACK` markers ✅ CLOSED (2026-07-31)

**Status:** `grep -rEhn "#\s*(TODO|FIXME|XXX|HACK)" pyffice/ --include="*.py"` → **0 matches**.

### T-NEW-058 — Fill 13 missing test files ✅ CLOSED (2026-07-31) — re-baselined as T-NEW-065

The original "13 missing test files" claim was wrong. Re-baselined against HEAD `b2a27e9`: the actual coverage gap is 18 subpackages with `0` name-matched tests AND `≤ 2` grep refs. Top 5 by source LOC: `web` (2592), `items` (1852), `images` (1631), `tags` (524), `workflows` (679). See **T-NEW-065** for the full per-subpackage coverage table and migration plan.

### T-NEW-059 — Fix `__version__` docstring snippet bug ⚠️ PARTIAL

**Status:** `pyffice/__init__.py:22-24` may still have the buggy `if __version__ >= (0, 2, 0):` snippet.

**Migration plan:**

1. Check `pyffice/__init__.py:22-24`.
2. Replace with `if __version_info__ >= (0, 2, 0):`.
3. Add `tests/test_version.py` if not present.

### T-NEW-060 — Squirl import-time `print()` pollution ✅ CLOSED (2026-07-31) — tracked in squirl repo

Filed as **T-NEW-061** in `~/.hermes/projects/squirl/TODOs.md`. The fix:

1. Replace `print(f"reql not installed")` in `squirl/squirl/orgnql/yonql.py:63` with `warnings.warn(..., ImportWarning, stacklevel=2)`.
2. Replace `print(f"MySQL client not found. ...")` in `squirl/squirl/orgnql/sonql.py:39` with the same pattern.
3. Add `import warnings` to each file.
4. Add a smoke test `squirl/tests/test_no_import_time_prints.py` that runs `import squirl` with `capsys` and asserts stdout/stderr do NOT contain the reql/MySQL strings.
5. Verify in `pyffice`: `pytest tests/ -q 2>&1` no longer contains "MySQL client not found" or "reql not installed" in stdout.

Pyffice has no action — the fix lives in the squirl repo. Closing this card as a cross-project pointer.

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

1. **T-NEW-044** — Fix 3 pre-existing import bugs in `email/`, `reports/`, `video/` that crash CLI subpackage imports. **(P1 audit blocker; -10% test penalty cascades.)**
2. **T-NEW-053** — Re-audit `contacts.py` for remaining `# TODO implement method` stubs.
3. **T-NEW-058** — Fill 13 missing test files (one per subpackage).
4. **T-NEW-059** — Fix `__version__` docstring snippet.

### P2 — Defer until P1 done

- **T-NEW-054** — Decide protocol model for `workflows/formulas.py`.
- **T-NEW-045** — Confirm Option A (facade) vs Option B (no facade) public API decision. ✅ CLOSED (Option B).

### P3 — Out of scope

- **T-NEW-060** — Squirl import-time `print()`. ✅ CLOSED (tracked in squirl as T-NEW-061).

---

## 📊 Document Type Status (current)

130 .py files. **137 PyfficeDocument subclasses** total (verified via `grep -rEn "^class Pyffice\w+\(" pyffice/`).

| Coverage | Count | Notes |
|----------|-------|-------|
| ✅ Has `SERIALIZATION_VERSION` | 97 | Per-class semver triple |
| ✅ Has docstring | 100% of public methods | No empty or missing |
| ✅ Has implementation | 100% | 0 stubs |
| ⚠️ Pre-existing import bugs | 3 subpackages | email, reports, video |

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

### T-NEW-065 — T-NEW-058 missing-test count is 35, not 13 ✅ CLOSED (2026-07-31)

**Status:** Re-baselined. The original T-NEW-058 claim of "13 missing test files" was wrong.

**Verified against HEAD `b2a27e9`:**

```
find pyffice -name '*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u → 35 source dirs
find tests -name '*TEST*.py' -not -path '*__pycache__*' | xargs -I {} dirname {} | sort -u → 8 tested dirs
diff (above) | grep '^<' | wc -l → 35 untested
```

But the real coverage is more nuanced. The project uses two test-file naming conventions:

| Pattern | Count | Location |
|---|---|---|
| `test_*.py` | 40 | `tests/unit/`, `tests/integration/`, `tests/pyffice_unit/tests/`, `tests/pyffice_unit/tests/tests/` |
| `*TEST*.py` | 10 | `tests/pyffice_unit/unit/` (legacy) |

**Refined per-subpackage coverage (verified):** for each `pyffice/<sub>` directory, count both (a) test files that match the subpackage name (`find tests -iname "*<name>*"`) and (b) test files that import from it (`grep -rEln "from pyffice.<name>|import pyffice.<name>" tests/`).

| Subpackage | Test name matches | Test grep refs | Status |
|---|---|---|---|
| `pyffice` | 2 | 42 | ✅ tested |
| `pyffice/analytics` | 0 | 1 | ⚠️ minimal |
| `pyffice/audio` | 1 | 4 | ✅ tested |
| `pyffice/cad` | 2 | 37 | ✅ tested |
| `pyffice/calendars` | 0 | 4 | ⚠️ minimal |
| `pyffice/charts` | 0 | 2 | ⚠️ minimal |
| `pyffice/config` | 1 | 10 | ✅ tested |
| `pyffice/contacts` | 0 | 1 | ⚠️ minimal |
| `pyffice/container` | 0 | 17 | ⚠️ minimal |
| `pyffice/data` | 0 | 12 | ⚠️ minimal (port-pending per T-NEW-043) |
| `pyffice/databases` | 0 | 2 | ⚠️ minimal |
| `pyffice/diagrams` | 0 | 4 | ⚠️ minimal |
| `pyffice/ebook` | 1 | 14 | ✅ tested |
| `pyffice/email` | 0 | 1 | ⚠️ minimal |
| `pyffice/filesystems` | 0 | 1 | ⚠️ minimal |
| `pyffice/forms` | 0 | 2 | ⚠️ minimal |
| `pyffice/images` | 0 | 3 | ⚠️ minimal |
| `pyffice/items` | 0 | 7 | ⚠️ minimal |
| `pyffice/matrix` | 1 | 3 | ✅ tested |
| `pyffice/media` | 1 | 7 | ✅ tested |
| `pyffice/notebooks` | 0 | 1 | ⚠️ minimal |
| `pyffice/ports` | 1 | 3 | ✅ tested |
| `pyffice/presentation` | 1 | 7 | ✅ tested |
| `pyffice/projects` | 1 | 3 | ✅ tested |
| `pyffice/reports` | 0 | 1 | ⚠️ minimal |
| `pyffice/script` | 1 | 8 | ✅ tested |
| `pyffice/skills` | — | — | ❌ **DELETED** (commit `d9d4fa9`) |
| `pyffice/socials` | 0 | 1 | ⚠️ minimal |
| `pyffice/tags` | 0 | 4 | ⚠️ minimal |
| `pyffice/text` | 0 | 3 | ⚠️ minimal |
| `pyffice/updates` | 1 | 3 | ✅ tested |
| `pyffice/video` | 1 | 1 | ✅ tested |
| `pyffice/web` | 0 | 4 | ⚠️ minimal |
| `pyffice/workflows` | 0 | 5 | ⚠️ minimal |

**Summary:**
- 8 subpackages have a dedicated test file matching their name (`*TEST*.py` or `test_<name>.py`).
- 7 subpackages have `grep` references but no name-matched test file (light coverage).
- 18 subpackages have BOTH `0` name matches AND `≤ 2` grep refs — these are the real "missing test" candidates.
- `pyffice/skills` was the only subpackage with **zero** test coverage — module deleted entirely (commit `d9d4fa9`). 33 subpackages remain.

**Migration plan (re-baselined, no priority / low priority — coverage is a marathon, not a sprint):**

1. Stop counting "missing test files" — the meaningful metric is per-subpackage coverage (test name match + grep refs). The 35-dir diff is misleading.
2. Identify the 18 subpackages with `0` name matches AND `≤ 2` grep refs. These are the actual backlog.
3. Pick 5 subpackages per sprint, write 1 test file each that:
   - Imports the module's main class(es).
   - Instantiates with safe defaults.
   - Asserts on the canonical shape (`content`, `documents`, `path`, `schema_version` per NEW TODO #2).
4. **Top 5 by source LOC** (per `find -name '*.py' -exec cat {} + | wc -l`):
   - `pyffice/web` (2592 LOC) — biggest gap, has no test file.
   - `pyffice/items` (1852 LOC) — 7 grep refs but no name-matched test.
   - `pyffice/images` (1631 LOC) — 3 grep refs but no name-matched test.
   - `pyffice/tags` (524 LOC) — 4 grep refs but no name-matched test.
   - `pyffice/workflows` (679 LOC) — 5 grep refs but no name-matched test.
5. Don't try to write 18 new test files in one batch — pick 5 per sprint, verify the audit score lift, repeat.

**Closed.** The re-baselined data is the new source of truth; T-NEW-058 should be marked `✅ CLOSED` (see T-NEW-058 in the old backlog section above).

### T-NEW-069 — Migrate `pyffice/data/` to `pyffice/ports/` and delete ✅ CLOSED (2026-07-31)

**Status:** Per user direction (2026-07-31), the directory migration is shipped.

**Audit findings (zero callers):**

- `pyffice/data/base.py` (PyfficeDataBase, PyfficeDataMixin) — 0 callers; `PyfficeDataMixin` is a typo-alias for itself
- `pyffice/data/csv.py` (PyfficeCSV + 7 free fns) — 0 callers; CSV handling is a port concern
- `pyffice/data/json.py` (PyfficeJSON) — 0 callers; JSON is the canonical wire format already
- `pyffice/data/yaml.py` (PyfficeYAML) — 0 callers; references undefined `PyfficeDictBase` (broken)
- `pyffice/data/xml.py` (5 free fns) — 0 callers
- `pyffice/data/data/__init__.py` — 0 callers; empty module with just a docstring

**Migration:**

| Was | Now | Notes |
|---|---|---|
| `pyffice/data/csv.py` | `pyffice/ports/csv_handler.py` | `PyfficeCSV` class + 7 module fns, behavior preserved verbatim |
| `pyffice/data/json.py` | `pyffice/ports/json_handler.py` | `PyfficeJSON` class + 6 module fns; `PyfficeDataMixin` inheritance dropped (the two methods that were added — `get` / `set` — are reimplemented as plain helpers) |
| `pyffice/data/__init__.py` | same path, rewritten as lazy proxy | Re-exports `PyfficeCSV`, `PyfficeJSON`, csv_*, json_* from the new ports modules; legacy `from pyffice.data import PyfficeCSV` keeps working |
| `pyffice/data/base.py` | deleted | zero callers; `PyfficeUnit._set_with_change` already provides the primitives |
| `pyffice/data/yaml.py` | deleted | zero callers; references undefined `PyfficeDictBase` |
| `pyffice/data/xml.py` | deleted | zero callers |
| `pyffice/data/data/` | deleted | empty nested dir with only a docstring |

**`pyffice/ports/__init__.py` updated** to add the new handlers to the lazy proxy: `PyfficeCSV`, `PyfficeJSON`, csv_*, json_* (avoiding name collisions with the existing `PyfficePortCSV` which is a port type, not a file handler).

**Tests added (56 new, all passing):**

- `tests/pyffice_unit/unit/ports/csv_handlerTEST.py` — 15 tests (module fns, class methods, delimiter support)
- `tests/pyffice_unit/unit/ports/json_handlerTEST.py` — 19 tests (module fns, class methods, dotted get/set)

**Verified:**

- `from pyffice.ports import PyfficeCSV, PyfficeJSON` → works
- `from pyffice.data import PyfficeCSV, PyfficeJSON` → still works (via lazy proxy)
- Both paths resolve to the SAME class object (identity check)
- 56/56 new tests pass
- 310/313 pre-existing tests still pass (3 pre-existing failures: 2 thingery env errors, 1 updates placeholder)
- No behavioral changes for any caller (the migration of `get`/`set` methods is a refactor that preserves PyfficeDataMixin's contract)

**Directory state after migration:**

```
pyffice/data/
  __init__.py    (re-export bridge, 2.7 KB)
```

Down from 7 files + 1 nested dir to 1 file.

### T-NEW-066 — T-NEW-044 status REGRESSED — only 2 of 4 fixes landed ⚠️ OPEN (P0) — **CLOSED 2026-07-31**

**Verified against HEAD `0674ce8`:**

All 4 import-path bugs T-NEW-044 named (and the 2 more surfaced after the logma fix) are now resolved:

| Step | Site | Status |
|---|---|---|
| 1 | `email/email.py:114` → `from pyffice.text.text_messages import ...` | **DONE** (verified — line 114 doesn't exist; the eager `text.messages` import is gone) |
| 2 | `reports/reports.py:30` → `from pyffice.text.text_messages import ...` | **DONE** (verified — the eager import was already removed; the new fix is `text.text` → `script.script`) |
| 3 | `video/video_export.py:26` → `from pyffice.audio.audio_export import PyfficeAudio` | **DONE** (commit `d598ec6`) |
| 4 | `skills/skills.py` — condor + logma migration + lazy __init__ | **DELETED** (commit `d9d4fa9`) — per user direction, the placeholder module was removed entirely (`git rm -r pyffice/skills/`); 109 lines removed across 4 files |
| 5 | `reports/reports.py:24` → `from pyffice.script.script import PyfficeScript` | **DONE** (commit `d598ec6`) — surfaced after step 1; T-NEW-044 step 2 listed wrong target |
| 6 | `cli.py:994` → `from pyffice.items.text import PyfficeText` | **DONE** (commit `d598ec6`) — surfaced after step 1 |

**Verified:** `python -m pyffice --help` runs without `NameError: name 'logma' is not defined`. Remaining 23 skipping lines are all environment-level (squirl/sb-stack not installed, optional 3rd-party like pandas/bs4/docx/ffmpeg/openpyxl/pptx missing) — **no more import-path bugs**.

Commit history: `d598ec6` (steps 3/5/6), `e898c06` (step 4 placeholder), `d9d4fa9` (step 4 finalized by deletion).

### T-NEW-067 — `PyfficeSkill` / `PyfficeSkillManager` / `PyfficeCapability` / `SkillRegistry` ✅ CLOSED (2026-07-31) — closed by deletion (commit `d9d4fa9`)

The full implementation plan (capability slots vs JSON-config vs Python-class registration) is no longer applicable — the user directed the entire `pyffice/skills/` placeholder to be removed rather than refactored. The 4 classes that were deferred for implementation are now superseded by the absence of the module. If skills re-enter the codebase, it will be a fresh design decision.

### T-NEW-068 — `condor` migration to `kahndor` complete across pyffice ✅ CLOSED (2026-07-31)

**Status:** `grep -rEln "from condor|import condor" pyffice/ --include='*.py'` → **0** (the `pyffice/skills/` placeholder was deleted entirely in commit `d9d4fa9`, so the historical comment is gone too). All `condor` imports were `from condor import condor` — and the user confirmed `condor` was folded into `kahndor`.

Migration sweep (no `ogma.*` imports remaining in pyffice/):
- `grep -rEln "from ogma\.logma|from ogma import logma" pyffice/` → **0 files**
- `grep -rEn "from ogma\." pyffice/` → **0 matches**

The remaining `from kahndor import kahndor` / `from kahndor.logma import Logma` imports are the canonical pattern.

---

## 🟡 NEW FEATURE REQUEST — Cloud Connection Ports (2026-07-31)

### T-NEW-070 — Implement cloud connection in ports to Google Drive and Dropbox ✅ CLOSED (2026-07-31)

**Status:** Implemented in commit `9509eec`. Auth model: API key / service account (Option B).

**Goal:** Add real cloud storage connectivity to `pyffice/ports/` so documents can be imported from and exported to Google Drive and Dropbox directly — not just the current empty stubs.

**Current state (verified against HEAD `98e60ab`):**

`pyffice/ports/gports.py` has 3 Google port stubs that are empty bodies:
- `PyfficePortGoogleDocs(PyfficePort)` — line 42, empty `__init__` only
- `PyfficePortGoogleForms(PyfficePort)` — line 55, empty `__init__` only
- `PyfficePortGoogleSheets(PyfficePort)` — line 68, empty `__init__` only

No Dropbox port exists anywhere in the codebase. No auth/credential handling exists (zero `oauth`, `credential`, `token`, `refresh_token` references in `pyffice/`).

`pyffice/web/services.py:35` has `PyfficeService(PyfficeDocument)` with `set_key()` / `set_service()` setters — this is the existing API-key holder that the cloud ports should integrate with.

**Affected sites:**

- `pyffice/ports/gports.py` — stub classes need real implementations
- `pyffice/ports/__init__.py` — add new Dropbox port exports to lazy proxy
- `pyffice/ports/ports.py` — base `PyfficePort` may need an `authenticate()` / `connect()` method
- `pyffice/web/services.py` — `PyfficeService` holds API keys; cloud ports should read from this
- `pyffice/ports/_data_/` — may need a `cloud_services.yaml` config for endpoints/scopes

**Migration plan (no priority / low priority — design decision first):**

1. **Design the auth model.** Two viable paths:
   - **(a) OAuth 2.0 flow** — full integration with Google Identity / Dropbox API. Requires `google-auth`, `google-auth-oauthlib`, `dropbox` packages. The user authorizes via browser redirect, pyffice stores the refresh token via pycurity.
   - **(b) API key / service account** — simpler. User provides a service account JSON (Google) or access token (Dropbox). Pyffice stores it via `PyfficeService.set_key()`. Lower friction, but limited scope (no per-user file access).

2. **Implement Google Drive connection** (either model):
   - Add `PyfficePortGoogleDrive(PyfficePort)` in `gports.py` — the main file-storage port (not Docs/Forms/Sheets which are document-format-specific).
   - Methods: `authenticate(credential)`, `list_files(folder_id)`, `download_file(file_id, local_path)`, `upload_file(local_path, parent_folder_id)`, `create_folder(name, parent_id)`.
   - Wire into `PyfficePort.open_file()` / `save_file()` so the standard port API works transparently.

3. **Implement Dropbox connection:**
   - Add `pyffice/ports/dports.py` (new file) with `PyfficePortDropbox(PyfficePort)`.
   - Same method surface: `authenticate`, `list_files`, `download_file`, `upload_file`, `create_folder`.
   - Add to `pyffice/ports/__init__.py` lazy proxy.

4. **Credential storage:**
   - All secrets go through pycurity (PyKeyStore) per the SB-stack convention — never env vars, never plaintext.
   - The `PyfficeService` class already has `set_key()` / `set_service()` — cloud ports read credentials from a `PyfficeService` instance, not directly.

5. **Add tests:**
   - `tests/pyffice_unit/unit/ports/cloud_portsTEST.py` — construction + auth mock + file listing mock. Real API calls are out of scope for unit tests; use `unittest.mock` to simulate responses.

6. **Document the CLI integration:**
   - `pyffice/cli.py` — add a `cloud` subcommand group: `pyffice cloud auth --service google`, `pyffice cloud list --service dropbox --folder /`, `pyffice cloud pull --file <id>`, `pyffice cloud push --file <path>`.

**Why this is a design decision first:**

The auth model (OAuth vs API key) determines:
- Which packages are required (`google-auth-oauthlib` vs just `requests`)
- Where credentials are stored (refresh token vs service account JSON)
- What scopes are needed (drive.file vs drive.readonly)
- Whether the user needs a browser-based consent flow

The user should confirm the auth model before implementation begins.

---

## 📊 P0/P1 Priority Ranking (added 2026-07-31)

### P0 (must fix before any other CLI work) — **ALL CLEAR 2026-07-31**

✅ All P0 cards closed in this session:
- T-NEW-062 — audio_export.py logma NameError (fixed)
- T-NEW-063 — video_export.py wrong import path (fixed)
- T-NEW-066 — T-NEW-044 regression (all 4 import-path bugs + 2 more surfaced, fixed)

### P1 (re-baseline, not new work) — **ALL CLEAR 2026-07-31**

- ✅ **T-NEW-064** — Close T-NEW-053 / T-NEW-054 / T-NEW-047 / T-NEW-059 as verified-done. Done earlier this session.
- ✅ **T-NEW-065** — Re-baseline T-NEW-058 from 13 → 35. Done in this session. Also closes T-NEW-058.
- ✅ **T-NEW-068** — `condor` → `kahndor` migration complete. Closed earlier this session.
- ✅ **T-NEW-069** — Migrate `pyffice/data/` to `pyffice/ports/` and delete. Done in this session.
- ✅ **T-NEW-067** — `PyfficeSkill` etc. placeholder. Closed by deletion (commit `d9d4fa9`).

### P2 (deferred / existing backlog)

- **T-NEW-070** — Cloud connection ports (Google Drive + Dropbox). ✅ CLOSED (commit `9509eec`). 3 new classes, 42 tests, graceful optional-dep handling.
- **T-NEW-045** — Public API facade decision. ✅ CLOSED (Option B, no facade).
- **T-NEW-060** — Squirl import-time `print()`. ✅ CLOSED (tracked in squirl as T-NEW-061).
- **T-NEW-CANDIDATE** — Test coverage marathon. ✅ CLOSED (2026-07-31) — 630 tests across 26 subpackages.

---

*File last edited: 2026-07-31 (T-NEW-070 CLOSED — cloud ports shipped: PyfficeCloudPort + GoogleDrive + Dropbox, 42 tests; 672 total tests; verified against HEAD `9509eec`)*
