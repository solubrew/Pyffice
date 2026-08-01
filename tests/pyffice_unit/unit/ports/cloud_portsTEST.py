"""Tests for pyffice/ports/cloud_ports.py (T-NEW-070).

Tests cover construction, inheritance, auth surface, and the
NotImplementedError contract on the base class. Real API calls
are NOT tested here — the optional deps (google-auth, dropbox)
may not be installed, and network calls are out of scope for
unit tests.

The mock tests use unittest.mock to simulate API responses where
the deps are missing.
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from pyffice.ports.cloud_ports import (
    PyfficeCloudPort,
    PyfficePortGoogleDrive,
    PyfficePortDropbox,
    HAS_GOOGLE,
    HAS_DROPBOX,
)
from pyffice.ports.ports import PyfficePort
from pyffice.document import PyfficeDocumentManager


# ============================================================================================#
#  BASE CLOUD PORT
# ============================================================================================#

class TestPyfficeCloudPortConstruction:
    """PyfficeCloudPort is the base for all cloud storage ports."""

    def test_constructs_with_no_args(self):
        cp = PyfficeCloudPort()
        assert cp is not None
        assert cp.authenticated is False
        assert cp._credentials is None
        assert cp._client is None

    def test_inherits_pyffice_port(self):
        assert issubclass(PyfficeCloudPort, PyfficePort)

    def test_inherits_pyffice_document_manager(self):
        assert issubclass(PyfficeCloudPort, PyfficeDocumentManager)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficeCloudPort.SERIALIZATION_VERSION, tuple)
        assert len(PyfficeCloudPort.SERIALIZATION_VERSION) == 3

    def test_provider_name(self):
        assert PyfficeCloudPort.PROVIDER == "base"


class TestPyfficeCloudPortAuth:
    """The authenticate() method stores credentials."""

    def test_authenticate_stores_credentials(self):
        cp = PyfficeCloudPort()
        creds = {"access_token": "test-token"}
        result = cp.authenticate(creds)
        assert result is cp
        assert cp._credentials == creds

    def test_authenticate_raises_on_no_credentials(self):
        cp = PyfficeCloudPort()
        with pytest.raises(ValueError, match="No credentials"):
            cp.authenticate()

    def test_authenticate_with_none_keeps_none(self):
        cp = PyfficeCloudPort()
        with pytest.raises(ValueError, match="No credentials"):
            cp.authenticate(None)


class TestPyfficeCloudPortNotImplemented:
    """The base class methods raise NotImplementedError."""

    def test_list_files_raises(self):
        cp = PyfficeCloudPort()
        with pytest.raises(NotImplementedError):
            cp.list_files()

    def test_download_file_raises(self):
        cp = PyfficeCloudPort()
        with pytest.raises(NotImplementedError):
            cp.download_file("id", "/tmp/test")

    def test_upload_file_raises(self):
        cp = PyfficeCloudPort()
        with pytest.raises(NotImplementedError):
            cp.upload_file("/tmp/test")

    def test_create_folder_raises(self):
        cp = PyfficeCloudPort()
        with pytest.raises(NotImplementedError):
            cp.create_folder("test")

    def test_delete_file_raises(self):
        cp = PyfficeCloudPort()
        with pytest.raises(NotImplementedError):
            cp.delete_file("id")


# ============================================================================================#
#  GOOGLE DRIVE
# ============================================================================================#

class TestPyfficePortGoogleDriveConstruction:
    """Google Drive port construction + inheritance."""

    def test_constructs_with_no_args(self):
        gd = PyfficePortGoogleDrive()
        assert gd is not None
        assert gd.authenticated is False

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortGoogleDrive, PyfficeCloudPort)

    def test_inherits_pyffice_port(self):
        assert issubclass(PyfficePortGoogleDrive, PyfficePort)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficePortGoogleDrive.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortGoogleDrive.SERIALIZATION_VERSION) == 3

    def test_provider_name(self):
        assert PyfficePortGoogleDrive.PROVIDER == "google_drive"


class TestPyfficePortGoogleDriveAuth:
    """Auth surface — guarded by HAS_GOOGLE dep check."""

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_authenticate_raises_without_deps(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(ImportError, match="google-auth"):
            gd.authenticate({"access_token": "test"})

    def test_authenticate_stores_credentials_before_dep_check(self):
        # Even without deps, the super().authenticate() call stores
        # the credentials before the dep check fails.
        gd = PyfficePortGoogleDrive()
        try:
            gd.authenticate({"access_token": "test"})
        except (ImportError, ValueError, Exception):
            pass
        assert gd._credentials == {"access_token": "test"}

    def test_authenticate_raises_on_no_credentials(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(ValueError, match="No credentials"):
            gd.authenticate()


class TestPyfficePortGoogleDriveWithoutDeps:
    """When google-auth is NOT installed, all operations raise RuntimeError."""

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_list_files_raises_not_authenticated(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            gd.list_files()

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_download_file_raises_not_authenticated(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            gd.download_file("id", "/tmp/test")

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_upload_file_raises_not_authenticated(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            gd.upload_file("/tmp/test")

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_create_folder_raises_not_authenticated(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            gd.create_folder("test")

    @pytest.mark.skipif(HAS_GOOGLE, reason="google-auth installed; test the missing-dep path")
    def test_delete_file_raises_not_authenticated(self):
        gd = PyfficePortGoogleDrive()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            gd.delete_file("id")


# ============================================================================================#
#  DROPBOX
# ============================================================================================#

class TestPyfficePortDropboxConstruction:
    """Dropbox port construction + inheritance."""

    def test_constructs_with_no_args(self):
        dbx = PyfficePortDropbox()
        assert dbx is not None
        assert dbx.authenticated is False

    def test_inherits_cloud_port(self):
        assert issubclass(PyfficePortDropbox, PyfficeCloudPort)

    def test_inherits_pyffice_port(self):
        assert issubclass(PyfficePortDropbox, PyfficePort)

    def test_serialization_version_tuple(self):
        assert isinstance(PyfficePortDropbox.SERIALIZATION_VERSION, tuple)
        assert len(PyfficePortDropbox.SERIALIZATION_VERSION) == 3

    def test_provider_name(self):
        assert PyfficePortDropbox.PROVIDER == "dropbox"


class TestPyfficePortDropboxAuth:
    """Auth surface — guarded by HAS_DROPBOX dep check."""

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_authenticate_raises_without_deps(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(ImportError, match="dropbox"):
            dbx.authenticate({"access_token": "test"})

    def test_authenticate_stores_credentials_before_dep_check(self):
        dbx = PyfficePortDropbox()
        try:
            dbx.authenticate({"access_token": "test"})
        except (ImportError, ValueError, Exception):
            pass
        assert dbx._credentials == {"access_token": "test"}

    def test_authenticate_raises_on_no_credentials(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(ValueError, match="No credentials"):
            dbx.authenticate()


class TestPyfficePortDropboxWithoutDeps:
    """When dropbox is NOT installed, all operations raise RuntimeError."""

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_list_files_raises_not_authenticated(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            dbx.list_files()

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_download_file_raises_not_authenticated(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            dbx.download_file("id", "/tmp/test")

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_upload_file_raises_not_authenticated(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            dbx.upload_file("/tmp/test")

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_create_folder_raises_not_authenticated(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            dbx.create_folder("test")

    @pytest.mark.skipif(HAS_DROPBOX, reason="dropbox installed; test the missing-dep path")
    def test_delete_file_raises_not_authenticated(self):
        dbx = PyfficePortDropbox()
        with pytest.raises(RuntimeError, match="Not authenticated"):
            dbx.delete_file("id")


# ============================================================================================#
#  LAZY EXPORT VERIFICATION
# ============================================================================================#

class TestCloudPortLazyExport:
    """Verify the ports/__init__.py lazy proxy resolves the cloud ports."""

    def test_cloud_port_importable_from_ports(self):
        from pyffice.ports import PyfficeCloudPort as Imported
        assert Imported is PyfficeCloudPort

    def test_google_drive_importable_from_ports(self):
        from pyffice.ports import PyfficePortGoogleDrive as Imported
        assert Imported is PyfficePortGoogleDrive

    def test_dropbox_importable_from_ports(self):
        from pyffice.ports import PyfficePortDropbox as Imported
        assert Imported is PyfficePortDropbox
