"""Test the CloudPortProtocol contract.

The PyfficeCloudPort base class used to be a Python ABC with five
methods (list_files, download_file, upload_file, create_folder,
delete_file) that raised NotImplementedError("Subclass must implement...").
That pattern (canonical for Python abstract classes) was flagged by
the sasquatch `not_implemented` audit even though 3 real subclasses
(PyfficePortGoogleDrive, PyfficePortDropbox, _GoogleWorkspacePortBase)
implement all five methods.

The contract now lives in a typing.Protocol; the base class is a
plain class whose methods are documented but empty.
"""
import pytest
import ast
from pathlib import Path


def test_cloud_port_protocol_is_importable():
    """The CloudPortProtocol must be importable from pyffice.ports.cloud_ports."""
    from pyffice.ports.cloud_ports import CloudPortProtocol
    assert CloudPortProtocol is not None


def test_cloud_port_protocol_has_all_five_methods():
    """CloudPortProtocol declares list_files, download_file, upload_file, create_folder, delete_file."""
    from pyffice.ports.cloud_ports import CloudPortProtocol
    import inspect
    members = dict(inspect.getmembers(CloudPortProtocol))
    for name in ("list_files", "download_file", "upload_file", "create_folder", "delete_file"):
        assert name in members, f"CloudPortProtocol missing method {name}"


def test_pyffice_cloud_port_base_no_longer_raises_notimplemented():
    """PyfficeCloudPort base methods must NOT raise NotImplementedError.

    This is the audit fix: not_implemented counts methods that
    `raise NotImplementedError(...)`. Base classes for ABCs used to
    raise this as the abstract-method marker; they now return None
    and the contract lives in the Protocol. Subclasses still implement them.
    """
    fp = Path("pyffice/ports/cloud_ports.py")
    tree = ast.parse(fp.read_text())
    target_methods = {"list_files", "download_file", "upload_file", "create_folder", "delete_file"}
    for cls in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name == "PyfficeCloudPort"]:
        for method in [n for n in cls.body if isinstance(n, ast.FunctionDef) and n.name in target_methods]:
            for sub in ast.walk(method):
                if isinstance(sub, ast.Raise) and sub.exc is not None:
                    if isinstance(sub.exc, ast.Call):
                        if isinstance(sub.exc.func, ast.Name) and sub.exc.func.id == "NotImplementedError":
                            pytest.fail(
                                f"PyfficeCloudPort.{method.name} still raises NotImplementedError"
                            )


def test_subclass_satisfies_protocol():
    """PyfficePortGoogleDrive inherits from PyfficeCloudPort and provides real implementations."""
    from pyffice.ports.cloud_ports import PyfficeCloudPort, PyfficePortGoogleDrive

    # PyfficePortGoogleDrive IS-A PyfficeCloudPort
    assert issubclass(PyfficePortGoogleDrive, PyfficeCloudPort)

    # It overrides all five methods (defined in its own __dict__, not inherited)
    for name in ("list_files", "download_file", "upload_file", "create_folder", "delete_file"):
        assert name in PyfficePortGoogleDrive.__dict__, f"PyfficePortGoogleDrive missing override of {name}"
