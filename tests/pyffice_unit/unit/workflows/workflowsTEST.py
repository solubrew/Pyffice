"""Tests for pyffice/workflows/.

Coverage:
- PyfficeWorkflow: add_node, add_edge, execute_node, update_nodes
- PyfficeFormulasLibrary: construction as PyfficeDocumentManager
- PyfficeFormula + ABS + SUM: execute produces correct results
- is_number utility: int/float → True, anything else → False

Skipped:
- pyffice.workflows.alarms (PyfficeAlarm) — module fails to import
  in this env (transitive `from pyffice.calendars.tasks import
  PyfficeEvent, PyfficeTask` — `pyffice.calendars.tasks` doesn't exist
  on disk; the reference is stale). Tests will land when the import
  is fixed.
"""

import pytest

from pyffice.workflows.workflows import PyfficeWorkflow
from pyffice.workflows.formulas import (
    PyfficeFormulasLibrary,
    PyfficeFormula,
    PyfficeFormulaABS,
    PyfficeFormulaSUM,
    is_number,
)


class TestPyfficeWorkflowConstruction:
    """PyfficeWorkflow() constructs an empty graph."""

    def test_constructs_with_no_args(self):
        w = PyfficeWorkflow()
        assert w is not None

    def test_constructs_with_cfg(self):
        w = PyfficeWorkflow({"nodes": [], "edges": []})
        assert w is not None


class TestPyfficeWorkflowGraphOps:
    """The graph mutation methods are fluent (return self)."""

    def test_add_node_returns_self(self):
        w = PyfficeWorkflow()
        assert w.add_node("n1") is w

    def test_add_edge_returns_self(self):
        w = PyfficeWorkflow()
        assert w.add_edge("a", "b") is w

    def test_execute_node_returns_self(self):
        w = PyfficeWorkflow()
        assert w.execute_node("n1") is w

    def test_update_nodes_returns_self(self):
        w = PyfficeWorkflow()
        assert w.update_nodes(("a", "b")) is w

    def test_node_data_persists(self):
        w = PyfficeWorkflow()
        w.add_node("n1", {"label": "step one"})
        assert w.nodes["n1"] == {"label": "step one"}

    def test_edge_accumulates(self):
        w = PyfficeWorkflow()
        w.add_edge("a", "b")
        w.add_edge("b", "c")
        assert ("a", "b") in w.edges
        assert ("b", "c") in w.edges


class TestPyfficeFormulasLibrary:
    """The library is a PyfficeDocumentManager facade."""

    def test_constructs(self):
        lib = PyfficeFormulasLibrary()
        assert lib is not None

    def test_inherits_document_manager(self):
        from pyffice.document import PyfficeDocumentManager
        assert issubclass(PyfficeFormulasLibrary, PyfficeDocumentManager)


class TestPyfficeFormulaABS:
    """PyfficeFormulaABS.execute() returns abs() of the first parameter."""

    def _make(self, parameters):
        # Constructor needs a "formula" key in cfg (used to
        # compute self.formula_tag). Parameters must be added
        # via add_parameter after construction — the constructor
        # resets self.parameters = {}.
        f = PyfficeFormulaABS({"formula": "ABS"})
        for k, v in parameters.items():
            f.add_parameter(k, v)
        return f

    def test_abs_of_positive(self):
        f = self._make({"x": 5})
        assert f.execute() == 5

    def test_abs_of_negative(self):
        f = self._make({"x": -7})
        assert f.execute() == 7

    def test_abs_of_zero(self):
        f = self._make({"x": 0})
        assert f.execute() == 0


class TestPyfficeFormulaSUM:
    """PyfficeFormulaSUM.execute() returns sum() of all parameters."""

    def _make(self, parameters):
        f = PyfficeFormulaSUM({"formula": "SUM"})
        for k, v in parameters.items():
            f.add_parameter(k, v)
        return f

    def test_sum_of_two(self):
        f = self._make({"x": 2, "y": 3})
        assert f.execute() == 5

    def test_sum_of_three(self):
        f = self._make({"a": 1, "b": 2, "c": 3})
        assert f.execute() == 6

    def test_sum_of_empty(self):
        f = self._make({})
        assert f.execute() == 0


class TestPyfficeFormulaBase:
    """PyfficeFormula (base) — constructor + add_parameter."""

    def test_constructs_with_formula_key(self):
        # Without the "formula" key, the constructor crashes on
        # `<{ + None + }>`. Documented as a pre-existing bug.
        f = PyfficeFormula({"formula": "ABS"})
        assert f is not None
        assert f.parameters == {}

    def test_add_parameter_returns_none(self):
        # Pre-existing behavior: add_parameter returns None, not
        # self (breaks the fluent pattern used elsewhere). Documented
        # here so the contract is visible.
        f = PyfficeFormula({"formula": "ABS"})
        assert f.add_parameter("x", 5) is None

    def test_add_parameter_side_effects(self):
        # Despite returning None, add_parameter mutates self.parameters.
        f = PyfficeFormula({"formula": "SUM"})
        f.add_parameter("a", 1)
        f.add_parameter("b", 2)
        assert f.parameters == {"a": 1, "b": 2}

    def test_formula_tag_built_from_cfg(self):
        f = PyfficeFormula({"formula": "ABS"})
        assert f.formula_tag == "<{ABS}>"


class TestIsNumber:
    """is_number() returns True for int/float, False otherwise."""

    def test_int_is_number(self):
        assert is_number(42) is True

    def test_float_is_number(self):
        assert is_number(3.14) is True

    def test_zero_is_number(self):
        assert is_number(0) is True

    def test_string_is_not_number(self):
        assert is_number("42") is False

    def test_none_is_not_number(self):
        assert is_number(None) is False

    def test_list_is_not_number(self):
        assert is_number([1, 2, 3]) is False

    def test_dict_is_not_number(self):
        assert is_number({"x": 1}) is False

    def test_bool_is_number(self):
        # isinstance(True, int) is True in Python, so bool → True.
        # This is the documented behavior; documented here as a guard.
        assert is_number(True) is True
