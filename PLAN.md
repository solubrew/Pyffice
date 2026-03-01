# Pyffice AI Agent Enhancement Plan

**Date**: 2026-03-01  
**Branch**: `orin-ws`  
**Goal**: Make Pyffice AI-agent friendly while preserving existing functionality

---

## 🎯 Objectives

1. **AI Agent Friendly**: Create clear, callable interfaces for LLM agents
2. **Preserve Functionality**: Don't break any existing features
3. **Production Ready**: Move from prototype toward production quality
4. **Bidirectional YAML**: Ensure seamless Office ↔ YAML conversion

---

## 📊 Current State Analysis

### Strengths (Keep)
- ✅ YAML-based configuration system (AI-friendly serialization)
- ✅ Change tracking with undo/redo
- ✅ Document versioning
- ✅ Tag system with UUID-based IDs
- ✅ Comprehensive metadata (author, timestamps, hashes)
- ✅ Core classes: `PyfficeCodex`, `PyfficeDocument`, `PyfficeUnit`

### Weaknesses (Fix)
- ⚠️ Many placeholder methods with empty implementations
- ⚠️ Missing imports (e.g., `SentenceTransformer`)
- ⚠️ Inconsistent error handling
- ⚠️ Template placeholders not resolved
- ⚠️ No AI agent tooling/interface layer

---

## 🗓️ Phased Implementation Plan

### Phase 1: Foundation & Core Stabilization
**Goal**: Fix broken imports, add error handling, document APIs

| Task | Description | Priority |
|------|-------------|----------|
| 1.1 | Fix missing imports (`SentenceTransformer`, `utils` from condor) | P0 |
| 1.2 | Add proper error handling to all public methods | P0 |
| 1.3 | Fill in docstrings with parameters and return types | P1 |
| 1.4 | Add type hints throughout codebase | P1 |
| 1.5 | Create `__all__` exports for each module | P2 |

### Phase 2: AI Agent Interface Layer
**Goal**: Create LLM-friendly tool interfaces

| Task | Description | Priority |
|------|-------------|----------|
| 2.1 | Create `PyfficeAgent` class with tool definitions | P0 |
| 2.2 | Implement `to_json_schema()` for all document types | P0 |
| 2.3 | Add `from_yaml_string()` / `to_yaml_string()` to all docs | P0 |
| 2.4 | Create tool-ready functions (docstrings for LLMs) | P0 |
| 2.5 | Add token-efficient summary methods for long documents | P1 |
| 2.6 | Implement embedding-ready `to_chunks()` method | P1 |

### Phase 3: Core Module Implementation
**Goal**: Complete spreadsheet, text, presentation modules

| Module | Tasks | Priority |
|--------|-------|----------|
| **spreadsheet** | Complete cell formulas, charts, pandas integration | P0 |
| **text** | Implement docx import/export, bibliography handling | P0 |
| **presentation** | Implement pptx import/export, shapes | P0 |
| **PDF** | Complete PDF extraction and export | P1 |

### Phase 4: Testing & Documentation
**Goal**: Production-ready quality

| Task | Description |
|------|-------------|
| 4.1 | Add pytest coverage for core modules |
| 4.2 | Create usage examples for each document type |
| 4.3 | Add AI agent usage examples |
| 4.4 | Generate API documentation |

### Phase 5: Integration & Deployment
**Goal**: Make it usable in production

| Task | Description |
|------|-------------|
| 5.1 | Set up CI/CD pipeline |
| 5.2 | Create Docker container |
| 5.3 | Add logging and monitoring |
| 5.4 | Performance optimization |

---

## 🔧 AI Agent Tool Interface Design

### Example: Agent-Friendly API

```python
# Tool-ready function (LLM can call this directly)
def read_spreadsheet(path: str, sheet: str = None) -> dict:
    """Read an Excel file and return as YAML-compatible dict.
    
    Args:
        path: Path to Excel file (.xlsx, .csv)
        sheet: Optional sheet name (default: first sheet)
    
    Returns:
        Dict with 'metadata' and 'data' keys
    """
    matrix = PyfficeMatrix()
    matrix.file_import(path)
    return matrix.to_dict()

def create_spreadsheet(data: dict, output_path: str):
    """Create Excel from YAML-compatible dict.
    
    Args:
        data: Dict with 'metadata' and 'data' keys
        output_path: Path to save Excel file
    """
    matrix = PyfficeMatrix()
    matrix.load_document(data)
    matrix.save(output_path, "excel")
```

### Structured Output Support

```python
# For LLM output parsing
matrix.to_json_schema()  # Returns JSON Schema for validation
matrix.to_yaml_string()   # Returns YAML for LLM consumption
matrix.to_summary()       # Token-efficient summary
```

---

## 📁 File Structure (Post-Enhancement)

```
pyffice/
├── __init__.py           # Exports: PyfficeCodex, PyfficeMatrix, etc.
├── pyffice.py            # Main entry point
├── document.py           # Base classes
├── agent.py              # NEW: AI Agent interface layer
├── tools.py              # NEW: Tool-ready functions
├── spreadsheet/
│   ├── spreadsheet.py    # PyfficeMatrix, PyfficeSpreadSheet
│   └── ports/            # Import/export handlers
├── text/
│   ├── text.py           # PyfficeScript
│   └── bibliographies.py
├── presentation/
│   └── presentation.py   # PyfficeDeck
├── pdf/
│   └── pdfs.py           # PyfficePDF
├── images/
│   └── images.py         # PyfficeImage
└── _data_/               # YAML configs
```

---

## 🔄 Backward Compatibility

- All existing public methods preserved
- YAML format remains compatible
- CLI interface unchanged
- Import paths may add new aliases but old ones work

---

## 🚀 Quick Start (AI Agent)

```python
from pyffice import PyfficeCodex, PyfficeMatrix

# Read Office file → YAML
doc = PyfficeMatrix()
doc.file_import("report.xlsx")
yaml_output = doc.to_yaml_string()

# Modify (AI agent can edit YAML)
# ... edit yaml_output ...

# Write YAML → Office file
doc2 = PyfficeMatrix()
doc2.load_document(yaml_output)
doc2.save("report_modified.xlsx", "excel")
```

---

## ✅ Success Metrics

1. All core document types (spreadsheet, text, presentation) fully operational
2. AI agent can read/modify/write Office files via YAML
3. JSON Schema available for all document types
4. 80%+ test coverage on core modules
5. Documentation complete with AI agent examples

---

## 📝 Notes

- **Token Efficiency**: Use `to_summary()` for large docs to reduce LLM tokens
- **Embedding**: Use `to_chunks()` for vector database ingestion
- **Validation**: Use `to_json_schema()` to validate LLM-generated YAML
