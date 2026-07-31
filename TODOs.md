# Pyffice — TODOs

# New TODOs:
- refactor data/base.py and other files in this directory as they are all covered by document types elsewhere in the package and any actual import/export work needs to be in the ports/ path
- refactor all document types to maintain a consistent shape aligned with PyfficeImage, PyfficeScript, PyfficeMatrix duplicating keys as needed with deprication notes until all documents can be fully aligned
- build out stubbed document types







> **Status:** Active Development | **Last Updated:** 2026-07-06 | **Branch:** `gamma` (HEAD `08815ee`)

This TODO reflects what git log shows is **actually still pending**. Items completed in prior commits have been removed; see git history.

---

## 🔴 Priority 1 — Critical

### Pylint Score: 4.87 → 9.0+

- [ ] **R0801 — Duplicate code in `pyffice/items/cells.py`** (lines ~191–199)
- [ ] **R0801 — Duplicate code in `pyffice/items/shapes.py`** (lines ~66–74)
- [ ] Add docstrings to public methods missing them
- [ ] Remove empty docstrings (`""""`)
- [ ] Fix unused variables

### Testing

- [ ] Add MySQL client package or mock — tests can't connect to a DB
- [ ] Run full pytest suite once DB issue is resolved

---

## 🟡 Priority 2 — Next Sprint

### Documentation

- [ ] Update `README.md` with verified features only
- [ ] Update `CLI.md` with accurate command list
- [ ] Add architecture diagram

### Features

- [ ] Verify all file-format handlers actually work (not just `__init__.py`)
- [ ] Test CLI commands end-to-end

---

## 🟢 Priority 3 — Enhancement

### Quality

- [ ] Add type annotations (mypy)
- [ ] Add integration tests
- [ ] Add benchmark tests
- [ ] Add security scanning (bandit)

### Documentation

- [ ] Add MkDocs API documentation
- [ ] Add contributing guide with examples

### Performance

- [ ] Profile large file handling
- [ ] Add caching layer
- [ ] Optimize image processing

---

## ✅ Recently Completed (git history)

| Commit | Description |
|--------|-------------|
| `4d5a8ca` | Add missing `__init__.py` for `data/` module |
| `5ada534` | Add `cam` and `spreadsheet` modules (resolves CLI import errors) |
| `e44f89a` | Add missing `__init__.py` for `charts/` and `skills/` modules |
| `1d4d0fb` | Complete `__init__.py` files, CLI imports, `subtrix` dep, duplicate code |
| `e2155ef` | Docstrings on all module `__init__.py` files |
| `93996b5` | Add `items`, `skills`, `media` modules for Pylint compliance |
| `08815ee` | Continue implementing remaining pyffice document types |
| `87a0e16` | Expanded file types |
| `50501d2` | Update documentation to reflect current state |
| `34f22f6` | Update `ogma` and `condor` to `kahndor` |

---

## 📊 Document Type Status (current)

33 types total. **All 33 have directory/module presence** (no longer "missing"). The "data" type row in the previous TODO is now stale — `data/` exists.

| Status | Count | Notes |
|--------|-------|-------|
| ✅ Functional | 31 | Full implementation |
| ⚠️ Partial | 1 | media (consolidation pending) |
| ❌ Missing | 0 | All present — need quality verification |

**Open quality items:** `items/` cells.py + shapes.py duplicates; `media/` consolidation; need end-to-end CLI + format-handler verification.

---

## 📋 Next Concrete Steps

1. **P1**: Fix `cells.py` and `shapes.py` R0801 duplicates (low risk, mechanical)
2. **P1**: Resolve test-suite DB dependency (mock or real client)
3. **P2**: Walk every CLI command + file-format handler end-to-end against the gamma tree
4. **P2**: Trim `README.md` to only documented features
5. Defer P3 until P1+P2 done

---

*File last edited: 2026-07-06 (rewritten from prior stale contents reflecting actual git state)*


---

## Session handoff — Sprint 16 (2026-07-29)

Upstream ``pyffice/gamma`` already has Sprint 16 work
(commit ``5b858c2 feat(pyffice): per-class SERIALIZATION_VERSION
+ record schema_version``): each PyfficeDocument subclass
declares ``SERIALIZATION_VERSION = (1, 0, 0)`` and
``to_dict()`` records both ``"semver"`` (package-level,
from ``pyffice.__version__``) and ``"schema_version"``
(per-class, ``list(self.SERIALIZATION_VERSION)``) into
``meta_data``. This was driven by user correction
(2026-07-29): "it isn't the package version each
PyfficeDocument type needs its own version control as
each can have a different to_dict() schema".

The change applies to ``PyfficeUnit``, ``PyfficeDocument``,
``PyfficeDocumentManager``, ``PyfficeDeque``. Was verified
locally with the registered tests in
``tests/test_pyffice_semver.py``.

**Open items (unchanged from before Sprint 16):** the
existing R0801 dedup work plus the docstring cleanup
items above are the live backlog.

**Architectural facts to remember for the next session:**

- Each PyfficeDocument subclass declares
  ``SERIALIZATION_VERSION = (1, 0, 0)`` independently.
- The receiving side reads both ``semver`` (what Pyffice
  produced this blob) and ``schema_version`` (how to
  deserialize THIS class). Subclasses can move schema
  versions independently.
| ``pyffice.__version__`` is ``"0.1.0"`` and
  ``pyffice.__version_info__`` is ``(0, 1, 0)`` — exposed
  for callers who want the package-level version.

---

## Sprint 17 T-NEW Backlog — audit-driven + source-scanned (2026-07-31)

Source sweep: `sasquatch analyze -p .` (sasquatch@4d9f66f, pre-test score
86.81%, final 76.81% with -10% test penalty) plus a source scan for
`NotImplementedError`, `# TODO`/`# FIXME`, `pass`-only bodies, bare
`raise Exception(...)`, empty `__init__.py`, and module-vs-test
mirror coverage. Each card below is grounded in concrete file:line
evidence.

### T-NEW-043 — Fix `pyffice/__init__.py` public surface so `import pyffice` exposes what the README claims (2026-07-31)

`pyffice/__init__.py` is 25 lines: only `__version_info__` /
`__version__` are exported. The README and `cli.py` import
`from pyffice import Pyffice` and `from pyffice import spreadsheet`
which both fail. The actual class is `PyfficeCodex` and lives in
`pyffice/pyffice.py`. Without a public surface fix, every CLI invocation
crashes and every doc snippet that says `import pyffice` is a lie.

**Affected sites:**

- `pyffice/__init__.py:23` — only exports `__version__` /
  `__version_info__`; no class re-exports.
- `pyffice/__init__.py:22-24` — docstring snippet
  `if __version__ >= (0, 2, 0):` is a `str` vs `int` tuple compare
  and raises `TypeError` if a user copies it.
- `pyffice/cli.py:11-19` — does `from pyffice import (..., spreadsheet, ...)`
  and `from pyffice.pyffice import Pyffice`; both break.
- `README.md:107-131` — facade snippet uses `app.document.convert(...)`,
  `app.email.send(...)`; `PyfficeCodex` has no `document.convert` or
  `email.send` (verified: `p.document` is an `Instruct` config object,
  not a manager).
- `tests/test_pyffice.py:10-30` — imports `validate_config`,
  `convert_document`, `main` from `pyffice`; none exist.

**Migration plan:**

No priority tier — design decision first (see T-NEW-045). Pick
ONE of the following before any code change:

1. **Shrink README + tests to the truth.** Re-export
   `PyfficeCodex` (and `PyfficeCodexError`, `DocumentNotFoundError`,
   `InitializationError`) from `pyffice/__init__.py`. Rewrite
   `README.md` quick-start to use `PyfficeCodex`. Rewrite
   `tests/unit/test_pyffice.py` to call the real method names.
   `cli.py` switches from `from pyffice.pyffice import Pyffice` to
   `from pyffice.pyffice import PyfficeCodex as Pyffice`.
2. **Build the facade.** Create a `pyffice/api.py` with a `Pyffice`
   class that holds `document`, `image`, `video`, `email`,
   `calendar`, `workflow` sub-managers (each with the methods
   the README documents), wired to the existing
   `PyfficeDocumentManager`, `PyfficeImage`, etc. classes. Re-export
   `Pyffice` from `pyffice/__init__.py`.

Default to option 1 unless the user wants the facade.

1. Add the docstring snippet fix: replace
   `if __version__ >= (0, 2, 0):` with
   `if __version_info__ >= (0, 2, 0):` in `__init__.py:22-24`.
2. Re-export the three public exception classes + `PyfficeCodex`
   from `pyffice/__init__.py`.
3. Update `cli.py:11-19` to use the real paths (see T-NEW-046 for
   the `spreadsheet` cleanup that overlaps).
4. Update README quick-start and `tests/unit/test_pyffice.py` to
   use `PyfficeCodex`.
5. Add a smoke test
   `tests/unit/test_package_public_api.py` asserting each
   documented `from pyffice import X` resolves.

### T-NEW-044 — Fix `cli.py` crash: `from pyffice import spreadsheet` is unrecoverable (2026-07-31)

`python -m pyffice --help` raises `ImportError: cannot import name
'spreadsheet' from 'pyffice'`. `pyffice/__init__.py` does not expose
any submodules — it only exports `__version__` / `__version_info__`.
There is no `pyffice/spreadsheet.py` at the project root; the
spreadsheet implementation lives in `pyffice/matrix/spreadsheet.py`
as `PyfficeSpreadSheet`.

**Affected sites:**

- `pyffice/cli.py:11-19` — `from pyffice import (analytics, audio,
  cad, calendars, cam, charts, contacts, databases, diagrams, email,
  filesystems, forms, images, items, notebooks, presentation,
  projects, reports, socials, spreadsheet, tags, text, updates,
  video, web, workflows,)`. Of these 25 names, exactly zero are
  exported by `pyffice/__init__.py` (it's empty).
- `pyffice/cli.py:20` — `from pyffice.pyffice import Pyffice` —
  fails (no `Pyffice` class; the class is `PyfficeCodex`).

**Migration plan:**

No priority tier — the CLI cannot start without this. P1 blocker
for any audit >80% since the test penalty cascades.

1. Replace the `from pyffice import (...)` block in `cli.py:11-19`
   with the real module paths:
   ```python
   from pyffice.analytics import sources as analytics
   from pyffice.audio import audio as audio_module
   from pyffice.calendars import calendars as calendars_module
   from pyffice.charts import charts as charts_module
   from pyffice.contacts import contacts as contacts_module
   from pyffice.databases import databases as databases_module
   from pyffice.diagrams import diagrams as diagrams_module
   from pyffice.email import email as email_module
   from pyffice.filesystems import filesystems as filesystems_module
   from pyffice.forms import forms as forms_module
   from pyffice.images import images as images_module
   from pyffice.items import items as items_module
   from pyffice.matrix import spreadsheet as spreadsheet_module
   from pyffice.notebooks import notebooks as notebooks_module
   from pyffice.ports import ports as ports_module
   from pyffice.presentation import presentation as presentation_module
   from pyffice.projects import projects as projects_module
   from pyffice.reports import reports as reports_module
   from pyffice.script import script as script_module
   from pyffice.skills import skills as skills_module
   from pyffice.tags import tags as tags_module
   from pyffice.text import text as text_module
   from pyffice.updates import updates as updates_module
   from pyffice.video import video as video_module
   from pyffice.web import web as web_module
   from pyffice.workflows import workflows as workflows_module
   ```
2. Replace `from pyffice.pyffice import Pyffice` with
   `from pyffice.pyffice import PyfficeCodex as Pyffice` (matches
   the alias convention used elsewhere; pairs with T-NEW-043).
3. Verify `python -m pyffice --help` returns the click help text
   without traceback. Verify `python -m pyffice --help | head -5`
   shows the group description.
4. Smoke test
   `tests/test_cli_help.py` that invokes the click group via
   `CliRunner.invoke(cli, ["--help"])` and asserts exit code 0
   and a non-empty output.

### T-NEW-045 — Decide the public API model: facade `Pyffice` or expose `PyfficeCodex` directly (2026-07-31)

The README and `cli.py` both reference a `Pyffice` facade with
sub-managers (`app.document`, `app.image`, `app.email`, etc.) that
do not exist. The actual class hierarchy is `PyfficeCodex`
extends `PyfficeDocumentManager` and exposes `document` as an
`Instruct` config object — not a manager with a `.convert()`
method. Without a decision, every doc/example/test will be wrong
in different ways.

**Affected sites:**

- `pyffice/pyffice.py:75` — `class PyfficeCodex(PyfficeDocumentManager)`.
- `pyffice/pyffice.py:114-119` — `PyfficeCodex.__init__` wires up
  `url_library`, `contacts`, `documents`, `forms_manager`, `imports`,
  `source`. No `image`, `video`, `audio`, `email`, `calendar`,
  `workflow` sub-managers.
- `pyffice/document.py:PyfficeDocumentManager` — base class. Already
  exposes `document`, `change_limit`, `changes`, `add_change`,
  `add_document`. Does NOT have `.convert(path_in, path_out)`.
- `pyffice/charts/charts.py:PyfficeChart`,
  `pyffice/images/images.py:PyfficeImage`,
  `pyffice/email/email.py:PyfficeEmail`,
  `pyffice/workflow_formulas/...`, etc. — each exists as a
  standalone class but is not wired into `PyfficeCodex.__init__`.
- `README.md:104-131` — quick-start assumes the facade exists.
- `pyffice/cli.py:20` — `from pyffice.pyffice import Pyffice`.

**Migration plan:**

Design decision FIRST. Two valid options:

- **Option A (façade, more work):** Build `pyffice/api.py` with a
  `Pyffice` class whose `__init__` constructs every sub-manager
  from the existing modules and exposes the README's documented
  surface. This is what the README already promises; everything
  else (CLI, tests, examples) starts working once it exists.
- **Option B (no facade, rewrite README):** Keep `PyfficeCodex` as
  the only public class. Rewrite README quick-start to
  demonstrate the actual surface (`PyfficeCodex().add_document(...)`,
  `PyfficeCodex().add_change(...)`, etc.). Update `cli.py` to
  reference `PyfficeCodex`. Simpler; no new code in pyffice.

Default: **Option B**. The 6 `@cli.command` decorators don't
actually expose `app.document.convert(...)`-style operations
either, so the facade would need to be built for the CLI to
work end-to-end regardless. Pick B for the first cut; revisit
the facade if a downstream consumer explicitly asks for it.

1. Get the user's explicit choice between A and B before any
   code change (decision block in T-NEW-043 also asks).
2. After decision, the chosen path is captured in T-NEW-043
   (option 1 = B; option 2 = A).

### T-NEW-046 — Fix `tests/test_pyffice.py` vs `tests/test_pyffice/` name collision (2026-07-31)

Pytest aborts collection with
`import file mismatch: imported module 'tests.test_pyffice' has
this __file__ attribute ... tests/test_pyffice ... which is not
the same as the test file we want to collect:
tests/test_pyffice.py`. The directory `tests/test_pyffice/`
is a package; the file `tests/test_pyffice.py` cannot be
collected because of the collision. Effect: every `pytest`
run aborts before any test executes. Effect on the audit: the
audit's -10% test penalty kicks in unconditionally.

**Affected sites:**

- `tests/test_pyffice.py` — the colliding file. Contents are
  five tests that import `from pyffice import main`,
  `validate_config`, `convert_document` — all non-existent
  (see T-NEW-043).
- `tests/test_pyffice/` — the package directory containing
  `conftest.py`, `unit/`, `fixtures/`, `tests/` (with 87
  `*TEST.py` files), `integration/`.
- `pyproject.toml:[tool.pytest.ini_options] testpaths = ["tests"]`
  — does NOT exclude either path, so pytest tries both.

**Migration plan:**

No priority tier — P1 audit blocker.

1. Delete `tests/test_pyffice.py` (the colliding file). Its
   contents reference functions that don't exist (T-NEW-043)
   and are superseded by `tests/test_pyffice/unit/*TEST.py`
   files.
2. OR: rename `tests/test_pyffice/` to `tests/pyffice_unit/`
   (and `tests/test_pyffice/conftest.py` accordingly) and keep
   the file. Default to the rename — the `*TEST.py` files in
   the package reference each other via
   `from pyffice.items.cells import PyfficeCell` etc., so the
   directory IS a real package; the file is the duplicate.
3. Verify `pytest tests/ --collect-only -q` no longer aborts.
4. Smoke test `pytest tests/integration/ -q` should report at
   least the 2 integration tests it currently collects
   (`test_import_pyffice`, `test_cli_entry_point` — the latter
   fails for the import reasons in T-NEW-043 and -044).

### T-NEW-047 — Remove `crow` / `from kahndor import kahndor` from the `tests/test_pyffice/` package (2026-07-31)

`tests/test_pyffice/conftest.py` does `import crow;
crow.crowLoad("Subtrix", "DELTA")`. The `crow` package does not
exist in any SB venv (only in the `condor` rename history).
Every `*TEST.py` file in `tests/test_pyffice/unit/` does
`from kahndor import kahndor; CFG = kahndor.Instruct(PXCFG).load().dikt`,
which fails with `ModuleNotFoundError: No module named
'kahndor.kahndor'` because the local `kahndor` package doesn't
have a `kahndor` submodule (`kahndor.kahndor` is the file
`kahndor/kahndor.py` accessed via the package init). All 87
`*TEST.py` files are blocked from collection by this single
import.

**Affected sites:**

- `tests/test_pyffice/conftest.py:11` — `import crow`.
- `tests/test_pyffice/conftest.py:13` —
  `crow.crowLoad("Subtrix", "DELTA")`.
- `tests/test_pyffice/unit/filesystems/filesystemsTEST.py:24-25`
  — `from kahndor.logma import Logma` (line 25) + duplicate
  imports from line 14 onwards.
- Same pattern in all 87 `tests/test_pyffice/unit/*TEST.py`
  files — duplicate import blocks (lines 14-25 and 25-37 are
  identical across the suite).
- `tests/test_pyffice/unit/items/textTEST.py` (and others) —
  reference non-existent `_data_/<file>TEST.yaml` config files.

**Migration plan:**

No priority tier — P1 audit blocker (no test collection until
this is fixed).

1. Delete the `crow` import in `conftest.py:11-13`. Replace
   with a no-op or a comment noting the rename history.
2. In every `*TEST.py`, replace
   `from kahndor import kahndor; CFG = kahndor.Instruct(PXCFG).load().dikt`
   with `from kahndor import Instruct, Logma; CFG = Instruct(PXCFG).load().dikt`
   and `LOGMA = Logma(__name__)`.
3. Deduplicate the import blocks: each `*TEST.py` has the same
   12-line block twice (lines 14-25 and lines 26-37); collapse
   to one.
4. For each missing `_data_/<file>TEST.yaml` referenced by
   `PXCFG = join(HERE, "_data_", "<file>TEST.yaml")`, either
   create a minimal valid YAML or wrap the `Instruct().load()`
   in `try/except` with a sentinel empty dict.
5. Add `--continue-on-collection-errors` to
   `pyproject.toml [tool.pytest.ini_options] addopts` so
   individual broken tests don't abort collection.
6. Verify `pytest tests/test_pyffice/unit/filesystems/ -q`
   reports N>0 tests collected (was 0).
7. Smoke test
   `tests/test_pyffice_smoke.py` that imports `from kahndor
   import Instruct` and constructs an empty dict.

### T-NEW-048 — Fix the 8 documented broken READMEs: `validate_config`, `convert_document`, `main`, etc. are not in the package (2026-07-31)

The `tests/unit/test_pyffice.py` file (and the colliding file at
`tests/test_pyffice.py`) import symbols that the package does
not export: `validate_config`, `convert_document`, `main`. The
`README.md` quick-start also uses
`from pyffice import Pyffice` which doesn't exist (T-NEW-043).
None of these will be repaired by T-NEW-043 unless we
explicitly add (or remove) each one.

**Affected sites:**

- `tests/unit/test_pyffice.py:4` —
  `from pyffice import __version__, validate_config, convert_document`.
- `tests/test_pyffice.py:10` — `from pyffice import validate_config`.
- `tests/test_pyffice.py:16` —
  `from pyffice import convert_document`.
- `tests/test_pyffice.py:23` — `from pyffice import main`.
- `tests/integration/test_integration.py:21` —
  `from pyffice import main`.

**Migration plan:**

No priority tier — covered by T-NEW-043 (Option B).

1. After T-NEW-043 Option B is chosen, delete
   `tests/unit/test_pyffice.py` and `tests/test_pyffice.py`.
   The integration test in
   `tests/integration/test_integration.py:21` should also
   drop the `from pyffice import main` import — the CLI
   smoke check is `python -m pyffice --help` once T-NEW-044
   lands.
2. Replace with one focused integration test
   `tests/integration/test_package_imports.py`:
   ```python
   import pyffice
   from pyffice import PyfficeCodex, __version__, __version_info__
   from pyffice.pyffice import (
       PyfficeCodexError, DocumentNotFoundError, InitializationError,
   )

   def test_version_is_string():
       assert pyffice.__version__ == "0.1.0"
       assert pyffice.__version_info__ == (0, 1, 0)

   def test_codex_constructs():
       c = PyfficeCodex()
       assert c.config is not None

   def test_subclasses_are_exceptions():
       for cls in (PyfficeCodexError, DocumentNotFoundError, InitializationError):
           assert issubclass(cls, Exception)
   ```
3. Verify `pytest tests/integration/ -v` reports 3+ tests, all
   pass.

### T-NEW-049 — Eliminate `pass`-only method bodies in `pyffice/cli.py` (2026-07-31)

`pyffice/cli.py` has **24** `pass`-only lines (verified via
`grep -cEn "^\s+pass\s*$" pyffice/cli.py` → `24`). Most are
inside click command callbacks decorated with `@cli.command`.
With only 6 actual `@cli.command` decorators in the file (vs
the "72+" the README claims), most of the visible CLI surface
is empty stubs. The audit's `module_cli_coverage: 85%` is
measuring presence (not behavior), so empty callbacks pass
muster.

**Affected sites:**

- `pyffice/cli.py` — 24 `^\s+pass\s*$` matches (lines include
  162, 230, 304, 355, 406, 455, 488, 520 + 16 others). Run
  `grep -nE "^\s+pass\s*$" pyffice/cli.py` for the full list.
- `pyffice/diagrams/formats.py:502, 651` — `pass` in
  `try/except` blocks (different pattern, but same flavor of
  swallowed-error stub).

**Migration plan:**

No priority tier — covered partially by T-NEW-050 (CLI count
discrepancy). The actionable part is:

1. Inventory all `@cli.command` / click callback `pass` bodies
   in `pyffice/cli.py` (run
   `grep -nE "@cli\.command|def [a-z_]+\(.*\) ->.*:$" pyffice/cli.py`
   to enumerate).
2. For each, either:
   - implement the documented behavior (preferred when
     behavior is obvious from the decorator name), or
   - raise `NotImplementedError` with a TODO message, or
   - delete the decorator + body entirely.
3. Never leave a `pass`-only callback that pretends to be a
   command.

### T-NEW-050 — Reconcile README's "72+ command-line operations" with the actual 6 commands (2026-07-31)

`pyffice/cli.py` has exactly **6** `@cli.command()` decorators
(verified via `grep -cE "@cli\.command" pyffice/cli.py` →
`6`). The README claims "72+ command-line operations". The
discrepancy is 66 commands. Either the CLI grew plans that
were never built, or the README was copied from a different
project.

**Affected sites:**

- `README.md:33` — "**CLI**: 72+ command-line operations".
- `README.md:78-102` — 8 documented `pyffice <subcmd> ...`
  examples (document, spreadsheet, image, video, audio, email,
  calendar, workflow).
- `pyffice/cli.py:41, 63, 88, 109, 133, 1161` — actual
  `@cli.command` decorators (6 total).
- `CLI.md` (root) — should describe the real 6 commands, not
  phantom ones.

**Migration plan:**

No priority tier — docs/CLI hygiene. Document the truth, then
grow the CLI.

1. Change `README.md:33` from "72+" to the actual count after
   T-NEW-049 + T-NEW-051 are complete. Until then, change to
   "6 (in-progress)" so the README is not a lie.
2. Replace each `pyffice <subcmd> ...` example in
   `README.md:78-102` with a `python -c "..."` example using
   `PyfficeCodex` (per T-NEW-045 Option B).
3. Audit `CLI.md` for the same phantom commands. Remove any
   example that doesn't have a backing `@cli.command` in
   `pyffice/cli.py`.
4. Add `pyffice/cli.py` smoke test
   `tests/test_cli_count.py` asserting the count of
   `@cli.command` decorators matches a constant in
   `pyffice/cli.py:__all__` so the README and CLI cannot drift
   silently.

### T-NEW-051 — Populate the 27 functionally-empty subpackage `__init__.py` files (2026-07-31)

Of 35 subpackage `__init__.py` files, only **7** actually re-export
the public surface when `from pyffice.<x> import *` runs:

| Subpackage | `from <x> import *` exports |
|---|---|
| `cam` | `PyfficeBOM, PyfficeCAM, PyfficeCAMManager, PyfficeGCode, PyfficeSoftwareBOM` |
| `container` | (verified file has re-exports) |
| `data` | (verified file has re-exports) |
| `diagrams` | (verified file has re-exports) |
| `items` | `Item, ItemType, Document` |
| `projects` | (verified file has re-exports) |
| `skills` | `PyfficeSkill, PyfficeSkillManager, PyfficeCapability, SkillRegistry` |

The remaining **27** subpackages have `__init__.py` files that
either (a) are zero bytes (`filesystems`, `forms`, `reports`,
`script`, `updates`) or (b) contain only a `<(META)>` header and
section banner noise with no `from ... import` or `__all__` lines.
Verified by running `from pyffice.<x> import *` — every one of
the 27 returns `[]`:

- `analytics`, `audio`, `cad`, `calendars`, `charts`, `config`,
  `contacts`, `databases`, `ebook`, `email`, `filesystems`,
  `forms`, `images`, `matrix`, `media`, `notebooks`, `ports`,
  `presentation`, `reports`, `script`, `socials`, `tags`,
  `text`, `updates`, `video`, `web`, `workflows`

Note: `ports/__init__.py` is 1128 bytes but contains zero
re-exports — the size comes entirely from `<(META)>` headers
and section banners. The audit's `module_cli_coverage: 85%`
hides this gap because it checks for the *presence* of
`__init__.py`, not for re-exports.

**Affected sites:** the 27 functionally-empty `__init__.py`
files. Verified via `wc -c` and `from pyffice.<x> import *`:

- 5 zero-byte files (truly empty):
  - `pyffice/filesystems/__init__.py` (0 bytes)
  - `pyffice/forms/__init__.py` (0 bytes)
  - `pyffice/reports/__init__.py` (0 bytes)
  - `pyffice/script/__init__.py` (0 bytes)
  - `pyffice/updates/__init__.py` (0 bytes)
- 22 docstring-only / META-only files (33–69 bytes, no
  re-exports):
  - `pyffice/contacts/__init__.py` (35 bytes)
  - `pyffice/config/__init__.py` (33 bytes)
  - `pyffice/tags/__init__.py` (48 bytes)
  - `pyffice/audio/__init__.py` (51 bytes)
  - `pyffice/email/__init__.py` (51 bytes)
  - `pyffice/video/__init__.py` (51 bytes)
  - `pyffice/ebook/__init__.py` (52 bytes)
  - `pyffice/cad/__init__.py` (54 bytes)
  - `pyffice/media/__init__.py` (54 bytes)
  - `pyffice/web/__init__.py` (54 bytes)
  - `pyffice/analytics/__init__.py` (58 bytes)
  - `pyffice/calendars/__init__.py` (58 bytes)
  - `pyffice/databases/__init__.py` (58 bytes)
  - `pyffice/matrix/__init__.py` (58 bytes)
  - `pyffice/workflows/__init__.py` (58 bytes)
  - `pyffice/text/__init__.py` (59 bytes)
  - `pyffice/presentation/__init__.py` (61 bytes)
  - `pyffice/socials/__init__.py` (62 bytes)
  - `pyffice/charts/__init__.py` (62 bytes)
  - `pyffice/notebooks/__init__.py` (63 bytes)
  - `pyffice/images/__init__.py` (69 bytes)
- 1 large-but-functionally-empty file (`ports`):
  - `pyffice/ports/__init__.py` (1128 bytes — `<(META)>`
    header + section banners + comments, no `from ... import`
    or `__all__`)

All 27 verified to return `[]` when
`from pyffice.<x> import *` is run.

**Migration plan:**

No priority tier — API completeness.

For each empty `__init__.py`:

1. Identify the public classes in the subpackage's
   `*.py` files (e.g. `pyffice.audio.audio.PyfficeAudio`,
   `PyfficePlayList`).
2. Add `from <module> import <Class1>, <Class2>` lines.
3. Define `__all__ = [<Class1>, <Class2>, ...]`.
4. Add a 1-paragraph module docstring describing the
   subpackage (matches the existing `diagrams/__init__.py`
   style).
5. Verify `from pyffice.audio import PyfficeAudio,
   PyfficePlayList` succeeds (was: `from pyffice.audio
   import audio as audio_module` works; direct class import
   fails today).

Reference implementation: `pyffice/skills/__init__.py`
(already does this correctly).

### T-NEW-052 — Fix `NotImplementedError` sites in `pyffice/diagrams/formats.py` and `pyffice/data/base.py` (2026-07-31)

Three sites raise `NotImplementedError`. Verified by
`grep -rEn "raise NotImplementedError" pyffice/ --include="*.py"`:

**Affected sites:**

- `pyffice/diagrams/formats.py:84` —
  `raise NotImplementedError` in
  `DiagramConverter.load(self, file_path)` (no message).
- `pyffice/diagrams/formats.py:88` —
  `raise NotImplementedError` in
  `DiagramConverter.save(self, diagram, file_path)` (no message).
- `pyffice/data/base.py:174` —
  `raise NotImplementedError("Subclass must implement from_dict")`
  in `PyfficeDataBase.from_dict(data)`.

The two `DiagramConverter` sites (lines 84, 88) are on an
abstract base class (`DiagramConverter` — confirmed: the class
defines `__init__`, `load`, `save`, `detect_format`; `DiaConverter`
and other concrete converters inherit from it). The base is
**not** declared `abc.ABC` — `DiagramConverter()` can be
instantiated and `load()` will raise `NotImplementedError`
without a message.

The `PyfficeDataBase.from_dict` site (line 174) is also
abstract but uses a message string.

**Migration plan:**

No priority tier — completion work.

1. `pyffice/diagrams/formats.py` — mark `DiagramConverter`
   abstract by adding `from abc import ABC, abstractmethod`
   and changing the class declaration to
   `class DiagramConverter(ABC):`. Decorate `load` and `save`
   with `@abstractmethod`. The bare `raise NotImplementedError`
   on lines 84 and 88 should be replaced with `@abstractmethod`
   decorators (Python uses the decorator's presence, not the
   raise, to block instantiation).
2. `pyffice/data/base.py:174` — verify `PyfficeDataBase` is
   also abstract. If yes, apply the same `@abstractmethod` +
   `ABC` metaclass treatment. If no, implement `from_dict` or
   raise a more specific error.
3. Add a smoke test
   `tests/test_abstract_diagram_converter.py` asserting
   `DiagramConverter()` raises `TypeError` (Python's standard
   abstract-method error, not `NotImplementedError`).
4. Verify `grep -rEn "raise NotImplementedError" pyffice/
   --include="*.py"` returns 0 matches.

### T-NEW-053 — Implement the 9 `# TODO implement method` sites in `pyffice/contacts/contacts.py` (2026-07-31)

`pyffice/contacts/contacts.py` has 9 consecutive `# TODO
implement method` markers (lines 153, 158, 163, 168, 173,
178, 188, 193, 280). Each is a method body that returns
nothing or passes after the TODO. This is the largest
concentration of `# TODO` in the project.

**Affected sites:**

- `pyffice/contacts/contacts.py:153` — method TODO.
- `pyffice/contacts/contacts.py:158` — method TODO.
- `pyffice/contacts/contacts.py:163` — method TODO.
- `pyffice/contacts/contacts.py:168` — method TODO.
- `pyffice/contacts/contacts.py:173` — method TODO.
- `pyffice/contacts/contacts.py:178` — method TODO.
- `pyffice/contacts/contacts.py:188` — method TODO.
- `pyffice/contacts/contacts.py:193` — method TODO.
- `pyffice/contacts/contacts.py:280` — method TODO.

**Migration plan:**

No priority tier — finish the contact manager surface.

1. Inventory each method (name + signature) and determine the
   intended behavior from the surrounding context (docstring,
   adjacent methods, tests in
   `tests/test_pyffice/unit/items/personaTEST.py` which
   exercises some of them).
2. Implement each method, or delete it if it's truly unused.
3. Add tests for each implemented method (parameterized via
   `@pytest.mark.parametrize` for setter pairs).
4. Verify `grep -n "# TODO" pyffice/contacts/contacts.py`
   reports 0 matches.

### T-NEW-054 — Decide and implement `pyffice/workflows/formulas.py` factory + protocol methods (2026-07-31)

`pyffice/workflows/formulas.py` has 4 distinct `# TODO` items
that together describe a "execute a formula via a protocol"
subsystem that doesn't exist yet:

- `pyffice/workflows/formulas.py:91` —
  `# TODO implement factory methods for execution, etc for
  each formula using the config file`.
- `pyffice/workflows/formulas.py:122` —
  `# TODO convert the formula to be compatability with a
  specific protocol`.
- `pyffice/workflows/formulas.py:135` —
  `# TODO separate string formula into its defined
  attributes`.
- `pyffice/workflows/formulas.py:139` —
  `# TODO execute the formula and return the result`.

**Affected sites:** as above (all four lines in
`pyffice/workflows/formulas.py`).

**Migration plan:**

No priority tier — needs a design pass first.

1. Read `pyffice/workflows/formulas.py` end-to-end. Identify
   the existing `PyfficeFormula` class surface and what
   "protocol" means here (Excel? SQL? YAML? custom?).
2. Decide the protocol model (recommend: keep it
   config-driven via `config.dikt["protocols"]` like the rest
   of the codebase, no new dependency).
3. Implement the 4 TODOs as a coherent `Formula.parse` /
   `Formula.compile` / `Formula.execute` triplet.
4. Add `tests/test_pyffice/unit/workflows/formulasTEST.py` (it
   doesn't exist today — see T-NEW-058) covering each method.

### T-NEW-055 — Replace `bare raise Exception(...)` with specific exception classes (2026-07-31)

**18** sites raise the base `Exception` class with a string
message instead of a specific exception type. Verified via
`grep -rEn "raise Exception\b" pyffice/ --include="*.py" | wc -l`
→ 18. Effect: callers can't `except pyffice.X` to recover
from known errors; they have to match on the message string.

**Affected sites (full list):**

- `pyffice/filesystems/filesystems.py:128` —
  `raise Exception(f"Unknown Location {self.location}")`.
- `pyffice/tags/references.py:113` —
  `raise Exception(f"Media Type Unknown {media_type}")`.
- `pyffice/script/script.py:295` —
  `raise Exception(f"File format not supported {file_}")`.
- `pyffice/document.py:467` —
  `raise Exception(f"Tags not properly formated {self.tags}")`.
- `pyffice/document.py:576` —
  `raise Exception(f"No path provided")`.
- `pyffice/document.py:820` — `raise Exception("")` (empty
  message — definitely a bug).
- `pyffice/ports/ports.py:606` —
  `raise Exception(f"No File Provided {file_}")`.
- `pyffice/ports/ports.py:621` —
  `raise Exception(f"Unknown File Type {file_}")`.
- `pyffice/images/images.py:257` —
  `raise Exception(f"Unknown Location {self.location}")`.
- `pyffice/images/pdfs.py:264` —
  `raise Exception(f"Unknown Location {self.location}")`.
- `pyffice/workflows/formulas.py:165` —
  `raise Exception("Too Many Parameters")`.
- `pyffice/workflows/formulas.py:186` —
  `raise Exception("Non Number Values in Parameters")`.
- `pyffice/matrix/matrix.py:149` —
  `raise Exception(f"No File Provided {file_}")`.
- `pyffice/matrix/matrix.py:157` —
  `raise Exception(f"File Type Unknown {file_}")`.
- `pyffice/matrix/matrix.py:392` —
  `raise Exception(f"Unknown File Type {file_type} for file
  {file}")`.
- `pyffice/matrix/spreadsheet.py:93` —
  `raise Exception(f"Unknown Syntax {syntax}")`.
- `pyffice/matrix/spreadsheet.py:122` —
  `raise Exception(f"Unknown Return Format {return_format}")`.
- `pyffice/matrix/spreadsheet.py:184` —
  `raise Exception(f"Column {column} not found")`.

**Migration plan:**

No priority tier — API quality.

1. Add 6 new exception classes to
   `pyffice/pyffice.py` (next to `PyfficeCodexError`):
   - `UnknownLocationError` (filesystems, images, pdfs)
   - `UnknownFileTypeError` (ports, script, matrix)
   - `UnknownMediaTypeError` (tags)
   - `UnknownSyntaxError` (spreadsheet)
   - `UnknownReturnFormatError` (spreadsheet)
   - `ColumnNotFoundError` (spreadsheet)
   - `TooManyParametersError` (formulas)
   - `InvalidParameterTypeError` (formulas)
   - `InvalidConfigurationError` (document tags)
   - `MissingPathError` (document, matrix)
2. Replace each `raise Exception(...)` with the specific
   class. For `document.py:820` (empty message), either
   implement the missing behavior or raise
   `NotImplementedError("describe the missing branch")`.
3. Add a smoke test
   `tests/test_exception_types.py` that catches each new
   exception class by name and asserts the message is
   preserved.

### T-NEW-056 — Reconcile the Sprint 16 session-handoff doc with reality (2026-07-31)

`TODOs.md` lines 108-142 contain a "Session handoff — Sprint
16 (2026-07-29)" block that claims:

- Per-class `SERIALIZATION_VERSION = (1, 0, 0)` was added to
  `PyfficeUnit`, `PyfficeDocument`,
  `PyfficeDocumentManager`, `PyfficeDeque`.
- A test file `tests/test_pyffice_semver.py` was registered
  and verified locally.

`git log --all -- 'tests/test_pyffice_semver.py'` returns
zero commits. The file does not exist. The Sprint 16 commits
(`5b858c2`, `9946acc`) added `SERIALIZATION_VERSION` to 12+
modules but the handoff overstates the coverage
(`pyffice/databases/databases.py` has zero `SERIALIZATION_VERSION`
hits despite being a `PyfficeDocumentManager` user).

**Affected sites:**

- `TODOs.md:108-142` — the handoff block. The "Was verified
  locally with the registered tests in
  `tests/test_pyffice_semver.py`" claim is false.
- `pyffice/databases/databases.py` — no
  `SERIALIZATION_VERSION` declared despite being a manager.
- `pyffice/databases/table.py` — partial coverage (5 hits).
- `pyffice/items/items.py`, `pyffice/calendars/calendars.py`,
  `pyffice/contacts/contacts.py` — unknown coverage.

**Migration plan:**

No priority tier — docs honesty.

1. Inventory all `PyfficeDocument` subclasses (search for
   `class .*PyfficeDocument\b` and direct subclasses). For
   each, verify `SERIALIZATION_VERSION = (1, 0, 0)` (or
   another tuple) is declared. Add it where missing,
   starting with `pyffice/databases/databases.py`.
2. Either:
   - (a) commit `tests/test_pyffice_semver.py` with at least
     one test per subclass asserting
     `SERIALIZATION_VERSION` exists and is a 3-tuple of
     ints; or
   - (b) remove the "verified locally" claim from the handoff
     and replace with "needs verification; see T-NEW-056".
3. Rewrite `TODOs.md:108-142` to match reality: replace the
   claim "tests/test_pyffice_semver.py" with the real test
   path once (a) or (b) is done.

### T-NEW-057 — Sweep `# TODO` / `# FIXME` / `# XXX` / `# HACK` markers from `pyffice/` source (2026-07-31)

**20** inline TODO-style markers in `pyffice/` source (verified
via
`grep -rEhn "#\s*(TODO|FIXME|XXX|HACK)" pyffice/ --include="*.py"`
→ 20 matches: 19 `# TODO` plus 1 `#TODO`). Each should either
be implemented, deleted, or promoted to a tracked card in
`TODOs.md`. The audit's `embedded_todos: 60%` dimension
penalizes inline `# TODO` comments.

**Affected sites (full list):**

- `pyffice/calendars/calendars.py:115` — `# TODO needs rewrite`.
- `pyffice/pyffice.py:134` — `# TODO implement method`.
- `pyffice/document.py:171` —
  `# need to fix version` (note: missing `# TODO` prefix but
  same intent).
- `pyffice/contacts/contacts.py:153,158,163,168,173,178,188,193,280`
  — 9× `# TODO implement method` (covered by T-NEW-053).
- `pyffice/workflows/formulas.py:91,122,135,139` — 4× (covered
  by T-NEW-054).
- `pyffice/matrix/matrix.py:117` —
  `# TODO build out determination/compability method`.
- `pyffice/matrix/spreadsheet.py:29` —
  `# TODO need replace with functional system`.
- `pyffice/matrix/spreadsheet.py:139` —
  `# TODO: implement method`.
- `pyffice/skills/skills.py:37` — bare `# TODO:` (no message).

**Migration plan:**

No priority tier — completion + doc hygiene.

1. For each `# TODO` site: decide (implement | delete |
   promote to T-NEW card).
2. Run the sweep AFTER T-NEW-053, T-NEW-054, and the 3
   standalone matrix/calendar/skills sites.
3. After sweep, `grep -rE "#\s*(TODO|FIXME|XXX|HACK)"
   pyffice/ --include="*.py"` should return only items that
   have a corresponding T-NEW card in `TODOs.md`.

### T-NEW-058 — Fill in the 13 missing test files in `tests/test_pyffice/unit/` (2026-07-31)

The audit's `testing: 100%` is misleading — it's 100% on
file presence (every existing test dir has at least one
`*TEST.py`), but **13** test files are missing entirely.
Verified via two grep passes:

**10 subpackages have NO test directory at all** (the test
dir doesn't exist under `tests/test_pyffice/unit/`):

- `container` — no `tests/test_pyffice/unit/container/`
- `data` — no `tests/test_pyffice/unit/data/`
- `ebook` — no `tests/test_pyffice/unit/ebook/`
- `matrix` — no `tests/test_pyffice/unit/matrix/`
- `media` — no `tests/test_pyffice/unit/media/`
- `ports` — no `tests/test_pyffice/unit/ports/`
- `projects` — no `tests/test_pyffice/unit/projects/`
- `script` — no `tests/test_pyffice/unit/script/`
- `skills` — no `tests/test_pyffice/unit/skills/`
- `updates` — no `tests/test_pyffice/unit/updates/`

**3 root-level modules have no test directory at all**
(stray `documentTEST.py` and `pyfficeTEST.py` exist in the
wrong location — at `tests/test_pyffice/unit/` root — but
there is no proper `document/` or `pyffice/` directory):

- `pyffice/cli.py` — no `tests/test_pyffice/unit/cli/` (or
  `cli.pyTEST.py` at the dir root).
- `pyffice/document.py` — has a stray
  `tests/test_pyffice/unit/documentTEST.py` but no
  `tests/test_pyffice/unit/document/` directory.
- `pyffice/pyffice.py` — has a stray
  `tests/test_pyffice/unit/pyfficeTEST.py` but no
  `tests/test_pyffice/unit/pyffice/` directory.

The subpkg-with-existing-dir list (verified: each has ≥2
`*TEST.py` files): `analytics, audio, cad, calendars, cam,
charts, config, contacts, databases, diagrams, email,
filesystems, forms, images, items, notebooks, presentation,
reports, socials, spreadsheet, tags, text, video, web,
workflows` — 25 subpackages with tests present.

**Affected sites:** the 13 missing test files / directories.

**Migration plan:**

No priority tier — test coverage.

For each missing subpkg (10 listed above):

1. Create `tests/test_pyffice/unit/<subpkg>/`.
2. Identify the public surface of the module (classes,
   functions, public methods).
3. Write a `*TEST.py` skeleton following the existing pattern
   (`tests/test_pyffice/unit/items/cellsTEST.py` is the
   reference — has a `Test_PyfficeBackground` class with
   `setup_class`, `teardown_class`, one test per method).
4. Use `unittest.TestCase` if the existing suite uses it; use
   `pytest.mark.parametrize` for input/output matrices.
5. Each test must assert on real behavior, not on log lines
   or import success.

For the 3 root-level modules:

1. Move the stray `documentTEST.py` and `pyfficeTEST.py` into
   the proper `document/` and `pyffice/` directories (or
   leave them at the dir root if that's the convention).
2. Create `tests/test_pyffice/unit/cli/` for `pyffice/cli.py`.

Verify the new tests are collected:
`pytest tests/test_pyffice/unit/<subpkg>/ -v --collect-only`.

### T-NEW-059 — Fix the `__version__`/`__version_info__` docstring snippet bug in `pyffice/__init__.py` (2026-07-31)

`pyffice/__init__.py:22-24` documents:
```python
from pyffice import __version__
if __version__ >= (0, 2, 0):
    ...
```
`__version__` is the string `"0.1.0"` (set at line 25 of the
same file). A `str >= tuple` comparison raises `TypeError`.
The docstring actively misleads users.

**Affected sites:**

- `pyffice/__init__.py:22-24` — the snippet.
- `pyffice/__init__.py:24` — `__version__` assignment.
- `pyffice/__init__.py:23` — `__version_info__` assignment.

**Migration plan:**

No priority tier — quick fix.

1. Replace the snippet in `__init__.py:22-24` with:
   ```python
   from pyffice import __version_info__
   if __version_info__ >= (0, 2, 0):
       ...
   ```
   (uses the tuple, which supports the comparison).
2. Add a test `tests/test_version.py`:
   ```python
   import pyffice
   def test_version_string_format():
       assert pyffice.__version__ == ".".join(
           str(p) for p in pyffice.__version_info__
       )
   def test_version_info_is_3tuple():
       assert isinstance(pyffice.__version_info__, tuple)
       assert len(pyffice.__version_info__) == 3
       assert all(isinstance(p, int) for p in pyffice.__version_info__)
   ```
3. Verify `pytest tests/test_version.py -v` passes.

### T-NEW-060 — Quash the import-time stdout pollution from `squirl` during `pyffice` import (2026-07-31)

`import pyffice` transitively imports `squirl`, which calls
`print()` at module load time on two code paths. Verified
sources (file:line):

- `squirl/squirl/orgnql/yonql.py:63` —
  `print(f"reql not installed")`.
- `squirl/squirl/orgnql/sonql.py:39` —
  `print(f"MySQL client not found. Please install the
  'mysqlclient' package.")`.

(`pycurity` does NOT print these — I claimed it did in an
earlier draft; correct attribution is `squirl` only.)

Effect: every pytest run prints those two lines during
collection; the audit's `-10% test penalty` output gets these
lines mixed in; downstream tools that parse pytest output
break.

This card lives in pyffice because **pyffice's test suite is
the consumer that suffers**, not because pyffice is the
source. The fix in `squirl` is the right place; pyffice can
also suppress at the pytest layer if `squirl` isn't
immediately fixable.

**Affected sites:**

- `squirl/squirl/orgnql/yonql.py:63` — `print(f"reql not
  installed")`.
- `squirl/squirl/orgnql/sonql.py:39` —
  `print(f"MySQL client not found. Please install the
  'mysqlclient' package.")`.
- All transitive callers via `import pyffice`, `import
  pyffice.pyffice`, etc.

**Migration plan:**

No priority tier — output hygiene.

1. **Proper fix (upstream, preferred):** file a T-NEW card in
   `~/.hermes/projects/squirl/TODOs.md` to replace the
   `print()` calls with `warnings.warn(..., ImportWarning)`
   or `logger.debug(...)`. The prints are deprecation-style
   messages; `warnings` is the right channel.
2. **Quick win (pyffice-side pytest workaround):** add a
   conftest fixture in `tests/conftest.py` (currently 0
   bytes) that redirects stdout during test execution. Note
   that pytest hooks can't suppress module-level `print()`
   calls during collection, so this only helps for prints
   emitted during test execution, not during import. The
   real fix is upstream.
3. Verify `pytest tests/integration/ -q 2>&1` no longer
   contains the `MySQL client` or `reql` lines after the
   upstream fix.

---

## Cross-references

- T-NEW-043 covers the top-level public-surface decision
  (drives T-NEW-044, T-NEW-045, T-NEW-048).
- T-NEW-044 unblocks `python -m pyffice --help` (drives
  T-NEW-049, T-NEW-050).
- T-NEW-046 + T-NEW-047 unblock pytest collection (drives
  T-NEW-058).
- T-NEW-051 is independent and the largest single API
  completeness gain.
- T-NEW-053 + T-NEW-054 + T-NEW-057 sweep the `# TODO`
  backlog.
- T-NEW-056 reconciles the Sprint 16 handoff with the
  actual git state.
- T-NEW-060 is the last 10% — output hygiene that doesn't
  affect scores but does affect every audit run.
