# Pyffice — TODOs

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
- ``pyffice.__version__`` is ``"0.1.0"`` and
  ``pyffice.__version_info__`` is ``(0, 1, 0)`` — exposed
  for callers who want the package-level version.
