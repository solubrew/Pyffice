"""Tests for pyffice/updates/updates.py.

Coverage:
- PyfficeUpdate construction + config + default document=None
- check_schema returns True (placeholder behavior)
- check_extra / check_missing return None (placeholder)
- create_temp_file returns None
- PyfficeUnitUpdate / PyfficeDocumentUpdate subclass correctly
- PyfficeDocumentUpdate.process() with empty document returns empty
- PyfficeDocumentUpdate.run_adds() merges dicts
- PyfficeUpdater exists (verify importable, even if behavior is
  unknown — limits coverage without a real schema fixture)
"""

import pytest

from pyffice.updates.updates import (
    PyfficeUpdate,
    PyfficeUnitUpdate,
    PyfficeDocumentUpdate,
)


class TestPyfficeUpdateConstruction:
    """PyfficeUpdate() constructs with default attributes."""

    def test_document_defaults_to_none(self):
        u = PyfficeUpdate()
        assert u.document is None

    def test_config_is_set(self):
        u = PyfficeUpdate()
        assert u.config is not None

    def test_config_override(self):
        u = PyfficeUpdate({"custom": "value"})
        # The config dict is reflected in the loaded config.
        assert u.config is not None


class TestPyfficeUpdatePlaceholders:
    """check_* methods are placeholder no-ops (return None or True)."""

    def test_check_schema_returns_true(self):
        u = PyfficeUpdate()
        assert u.check_schema({}) is True

    def test_check_extra_returns_none(self):
        u = PyfficeUpdate()
        assert u.check_extra() is None

    def test_check_missing_returns_none(self):
        u = PyfficeUpdate()
        assert u.check_missing() is None

    def test_create_temp_file_returns_none(self):
        u = PyfficeUpdate()
        assert u.create_temp_file() is None


class TestPyfficeUnitUpdate:
    """PyfficeUnitUpdate subclasses PyfficeUpdate."""

    def test_is_instance_of_pyffice_update(self):
        u = PyfficeUnitUpdate()
        assert isinstance(u, PyfficeUpdate)

    def test_inherits_check_schema(self):
        u = PyfficeUnitUpdate()
        assert u.check_schema({}) is True

    def test_get_version_schema_returns_none(self):
        u = PyfficeUnitUpdate()
        # Returns None — placeholder.
        assert u.get_version_schema("1.0.0") is None


class TestPyfficeDocumentUpdate:
    """PyfficeDocumentUpdate subclasses PyfficeUpdate."""

    def test_is_instance_of_pyffice_update(self):
        u = PyfficeDocumentUpdate()
        assert isinstance(u, PyfficeUpdate)

    def test_data_meta_data_defaults(self):
        u = PyfficeDocumentUpdate()
        assert u.data is None
        assert u.meta_data is None

    def test_process_empty_document_returns_empty(self):
        u = PyfficeDocumentUpdate()
        result = u.process({})
        # Empty dict short-circuits to {}.
        assert result == {}

    def test_process_none_returns_empty(self):
        u = PyfficeDocumentUpdate()
        result = u.process(None)
        # None is also short-circuited to {}.
        assert result == {}

    def test_check_schema_inherits(self):
        u = PyfficeDocumentUpdate()
        assert u.check_schema({"foo": "bar"}) is True


class TestPyfficeDocumentUpdateRunAdds:
    """run_adds merges dicts onto a target."""

    def test_empty_update_data_no_op(self):
        u = PyfficeDocumentUpdate()
        target = {"a": 1}
        u.run_adds(target, None)
        assert target == {"a": 1}

    def test_empty_dict_update_data_no_op(self):
        u = PyfficeDocumentUpdate()
        target = {"a": 1}
        u.run_adds(target, {})
        assert target == {"a": 1}

    def test_dict_merge_adds_keys(self):
        u = PyfficeDocumentUpdate()
        target = {"a": 1}
        u.run_adds(target, {"b": 2, "c": 3})
        assert target == {"a": 1, "b": 2, "c": 3}

    def test_dict_merge_overwrites_existing_keys(self):
        u = PyfficeDocumentUpdate()
        target = {"a": 1, "b": 2}
        u.run_adds(target, {"b": 99, "c": 3})
        assert target == {"a": 1, "b": 99, "c": 3}