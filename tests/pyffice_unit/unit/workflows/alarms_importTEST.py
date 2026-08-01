"""Test pyffice.workflows.alarms import chain + PyfficeAlarm behaviour.

The alarms module previously imported
    from pyffice.calendars.tasks import PyfficeEvent, PyfficeTask
but pyffice/calendars/tasks.py does not exist on disk and PyfficeTask
is not defined anywhere. PyfficeEvent lives at
pyffice.calendars.events.PyfficeEvent.

The fix moves the import to pyffice.calendars.events (for PyfficeEvent)
and adds a minimal PyfficeTask stub so the alarm chain can construct.
Tests assert on real instantiation behaviour, not on log lines.
"""
import pytest

import pyffice.workflows.alarms as alarms
from pyffice.workflows.alarms import PyfficeAlarm


def test_alarms_module_imports():
    """pyffice.workflows.alarms must import without ModuleNotFoundError or NameError."""
    assert alarms is not None


def test_pyffice_alarm_class_exists():
    """PyfficeAlarm is the documented class on the alarms module."""
    assert hasattr(alarms, "PyfficeAlarm")


def test_pyffice_task_is_resolvable():
    """The alarms module must surface a usable PyfficeTask (or alias)."""
    # The module uses PyfficeTask() inside PyfficeAlarm.add_postpone / setters;
    # the import must therefore either re-export PyfficeTask or fail-fast.
    assert hasattr(alarms, "PyfficeTask")


def test_pyffice_task_payload_roundtrip():
    """PyfficeTask(payload) stores payload and get_payload() returns it."""
    from pyffice.calendars.events import PyfficeTask as _PT
    payload = {"action": "send_email", "to": "u_1"}
    t = _PT(payload)
    assert t.get_payload() == payload
    # set_payload replaces it and returns self (chainable)
    new_payload = {"action": "send_sms"}
    result = t.set_payload(new_payload)
    assert result is t
    assert t.get_payload() == new_payload


def test_pyffice_task_serializes_canonical_shape():
    """PyfficeTask carries SERIALIZATION_VERSION like other PyfficeUnit subclasses."""
    from pyffice.calendars.events import PyfficeTask as _PT
    assert hasattr(_PT, "SERIALIZATION_VERSION")
    version = _PT.SERIALIZATION_VERSION
    assert isinstance(version, tuple)
    assert all(isinstance(part, int) for part in version)


def test_pyffice_alarm_instantiates_with_defaults():
    """PyfficeAlarm() returns an instance with documented initial state."""
    a = PyfficeAlarm()
    assert a is not None
    assert a.acknowledge_task is None
    assert a.notify_task is None
    assert a.postpone_task is None
    assert a.postpones == []
    assert a.tasks is None


def test_pyffice_alarm_inherits_pyffice_event():
    """PyfficeAlarm is a subclass of PyfficeEvent (it extends the event model)."""
    from pyffice.calendars.events import PyfficeEvent
    assert issubclass(PyfficeAlarm, PyfficeEvent)


def test_pyffice_alarm_set_postpone_returns_self():
    """set_postpone(postpone) is documented as chainable — must return self."""
    a = PyfficeAlarm()
    result = a.set_postpone({"delay": 5})
    assert result is a


def test_pyffice_alarm_set_tasks_stores_value():
    """set_tasks(tasks) must store the {notify, acknowledge} task envelope on self.tasks."""
    a = PyfficeAlarm()
    payload = {
        "notify": {"channel": "email"},
        "acknowledge": {"user": "u_1"},
        "postpone": {"delay": 5},
    }
    a.set_tasks(payload)
    # The stored envelope is the {notify_task, acknowledge_task} pair, NOT the input
    assert isinstance(a.tasks, dict)
    assert "notify" in a.tasks
    assert "acknowledge" in a.tasks
    # The notify_task and acknowledge_task were each wrapped in a PyfficeTask
    assert a.notify_task is not None
    assert a.acknowledge_task is not None
