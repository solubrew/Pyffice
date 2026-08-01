"""Tests for pyffice/projects/.

Coverage:
- PyfficeProject construction defaults (tasks/resources/milestones/dependencies)
- SUPPORTED_FORMATS class attribute covers 7 formats
- SERIALIZATION_VERSION tuple
- PyfficeProjectAssignment / Task / Resource / Milestone construction
- create_project_from_file dispatches on extension
- PAXNTask / PAXNProject / PAXNConverter construction
- load_paxn returns PAXNProject (or raises for nonexistent file)
"""

import pytest

from pyffice.projects.projects import (
    PyfficeProject,
    PyfficeProjectAssignment,
    PyfficeProjectTask,
    PyfficeProjectResource,
    PyfficeProjectMilestone,
    create_project_from_file,
)
from pyffice.projects.paxn import (
    PAXNTask,
    PAXNProject,
    PAXNConverter,
    load_paxn,
)


class TestPyfficeProjectConstruction:
    """PyfficeProject() constructs with empty collections."""

    def test_default_attributes(self):
        p = PyfficeProject()
        assert p.tasks == []
        assert p.resources == []
        assert p.milestones == []
        assert p.dependencies == []

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeProject.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeProject.SERIALIZATION_VERSION) == 3

    def test_supported_formats_covers_seven(self):
        assert len(PyfficeProject.SUPPORTED_FORMATS) == 7

    def test_supported_formats_includes_microsoft(self):
        assert "microsoft" in PyfficeProject.SUPPORTED_FORMATS
        assert ".mpp" in PyfficeProject.SUPPORTED_FORMATS["microsoft"]

    def test_supported_formats_includes_csv(self):
        assert "csv" in PyfficeProject.SUPPORTED_FORMATS
        assert ".csv" in PyfficeProject.SUPPORTED_FORMATS["csv"]


class TestPyfficeProjectSubclasses:
    """The 4 PyfficeProject unit subclasses construct."""

    def test_assignment_constructs(self):
        a = PyfficeProjectAssignment()
        assert a is not None

    def test_task_constructs(self):
        t = PyfficeProjectTask()
        assert t is not None

    def test_resource_constructs(self):
        r = PyfficeProjectResource()
        assert r is not None

    def test_milestone_constructs(self):
        m = PyfficeProjectMilestone()
        assert m is not None


class TestCreateProjectFromFile:
    """create_project_from_file dispatches on extension."""

    def test_unsupported_extension_raises(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("not a project file")
        # Dispatcher raises ValueError on unsupported extensions
        # (csv/yml/etc. are listed in SUPPORTED_FORMATS but the
        # dispatch chain only handles mpp/mpx/xml/gan).
        with pytest.raises((ValueError, AttributeError, Exception)):
            create_project_from_file(str(f))

    def test_microsoft_dispatch_calls_from_microsoft_project(self, tmp_path, monkeypatch):
        f = tmp_path / "project.mpp"
        f.write_bytes(b"fake mpp data")
        called = []
        def fake_from_mp(cls, path, cfg=None):
            called.append(path)
            return PyfficeProject()
        # Stub the classmethod at the PyfficeProject class level.
        monkeypatch.setattr(
            PyfficeProject, "from_microsoft_project",
            classmethod(fake_from_mp),
        )
        create_project_from_file(str(f))
        assert called == [str(f)]


class TestPAXNTask:
    """PAXNTask dataclass construction."""

    def test_constructs_with_defaults(self):
        t = PAXNTask(id="1", title="T1")
        assert t is not None

    def test_constructs_with_fields(self):
        t = PAXNTask(id="1", title="T1", description="hello", status="done")
        assert t.id == "1"
        assert t.title == "T1"
        assert t.description == "hello"
        assert t.status == "done"

    def test_defaults(self):
        t = PAXNTask(id="1", title="T1")
        assert t.priority == "medium"
        assert t.tags == []
        assert t.dependencies == []


class TestPAXNProject:
    """PAXNProject dataclass construction."""

    def test_constructs_with_defaults(self):
        p = PAXNProject(id="1", name="P1")
        assert p is not None

    def test_constructs_with_fields(self):
        p = PAXNProject(id="1", name="P1", description="hello")
        assert p.name == "P1"
        assert p.description == "hello"


class TestPAXNConverter:
    """PAXNConverter dataclass construction."""

    def test_constructs(self):
        c = PAXNConverter()
        assert c is not None


class TestLoadPaxn:
    """load_paxn opens a .paxn file."""

    def test_missing_file_raises(self, tmp_path):
        with pytest.raises((FileNotFoundError, OSError, Exception)):
            load_paxn(str(tmp_path / "nonexistent.paxn"))

class TestCanonicalToDictShape:
    """The 4 to_dict() overrides in projects.py produce the canonical
    additive envelope (data, did, meta_data, pyffice_compat) and
    preserve the original class-specific keys under doc["data"].

    See R4 in TODOs.md. The PAXNTask/PAXNProject classes are
    intentionally NOT converted — their flat shape is the YAML
    contract for load_paxn (see paxn.py:188, 199).
    """

    def test_pyffice_project_to_dict_has_canonical_shape(self):
        p = PyfficeProject()
        p.tasks = [PyfficeProjectTask({'name': 'T1'})]
        d = p.to_dict()
        # Canonical envelope keys are present.
        assert 'data' in d
        assert 'did' in d
        assert 'meta_data' in d
        assert 'pyffice_compat' in d
        # schema_version is mirrored.
        assert d['meta_data']['schema_version'] == [1, 0, 0]
        # Original keys preserved under data.
        assert 'version' in d['data']
        assert 'tasks' in d['data']
        assert 'resources' in d['data']
        assert 'milestones' in d['data']
        assert 'dependencies' in d['data']

    def test_pyffice_project_task_to_dict_has_canonical_shape(self):
        t = PyfficeProjectTask({'name': 'T1', 'progress': 50})
        d = t.to_dict()
        assert 'data' in d
        assert 'did' in d
        assert 'meta_data' in d
        assert 'pyffice_compat' in d
        # Original keys preserved under data.
        assert d['data']['name'] == 'T1'
        assert d['data']['progress'] == 50
        for k in ('name', 'start_date', 'end_date', 'duration',
                  'progress', 'assignee'):
            assert k in d['data']

    def test_pyffice_project_resource_to_dict_has_canonical_shape(self):
        r = PyfficeProjectResource({'name': 'R1', 'type': 'human'})
        d = r.to_dict()
        assert 'data' in d
        assert 'pyffice_compat' in d
        assert d['data']['name'] == 'R1'
        assert d['data']['type'] == 'human'
        for k in ('name', 'type', 'email'):
            assert k in d['data']

    def test_pyffice_project_milestone_to_dict_has_canonical_shape(self):
        m = PyfficeProjectMilestone({'name': 'M1', 'date': '2026-08-01'})
        d = m.to_dict()
        assert 'data' in d
        assert 'pyffice_compat' in d
        assert d['data']['name'] == 'M1'
        assert d['data']['date'] == '2026-08-01'
        for k in ('name', 'date'):
            assert k in d['data']

    def test_to_dict_is_additive_at_nested_level(self):
        """Tasks called from PyfficeProject.to_dict() also carry
        the canonical shape — the additive contract applies to
        nested objects, not just the top level."""
        task = PyfficeProjectTask({'name': 'N', 'progress': 25})
        p = PyfficeProject()
        p.tasks.append(task)
        d = p.to_dict()
        nested = d['data']['tasks'][0]
        assert 'data' in nested
        assert 'pyffice_compat' in nested
        assert nested['data']['name'] == 'N'
