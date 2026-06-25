# Pyffice TODOs

## Priority 1 - Critical (Fix Before Next Release)

### Code Quality
- [ ] **Pylint Score: 4.87 → 9.0+**
  - [ ] Fix duplicate code in `pyffice/items/cells.py` (R0801)
  - [ ] Fix duplicate code in `pyffice/items/shapes.py` (R0801)
  - [ ] Add docstrings to all public methods
  - [ ] Remove empty docstrings `"""""`
  - [ ] Fix unused variables

### Testing
- [ ] **Fix test imports**
  - [ ] Add missing `crow` module or remove import
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

## Completed ✅

### 2025-01-15
- [x] Initial gamma branch documentation
- [x] Port architecture implemented
- [x] 50+ Python modules created
- [x] 19,232 lines of code
- [x] CLI with 72+ commands
- [x] Multiple file format handlers

## Notes

- Current branch: gamma
- Commit: f48afe72eaad77ad3b8424a156a94f4c266d6d63
- Focus: Get pylint score to 9.0+, fix tests

## File Locations

| Task | File | Line |
|------|------|------|
| Duplicate code fix | `pyffice/items/cells.py` | 191-199 |
| Duplicate code fix | `pyffice/items/shapes.py` | 66-74 |
| Test conftest | `tests/test_pyffice/conftest.py` | 15 |
| CLI commands | `pyffice/cli.py` | - |
