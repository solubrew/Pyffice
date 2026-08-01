"""Cloud storage ports for Google Drive and Dropbox.

T-NEW-070: Cloud connection ports that let Pyffice import/export
documents directly from/to Google Drive and Dropbox.

Auth model: API key / service account (Option B from the card).
Rationale:
- Lower friction — user pastes a key or service account JSON, no
  browser consent flow.
- All secrets stored via pycurity (PyKeyStore) per SB-stack convention.
- The existing ``PyfficeService`` class already holds API keys
  via ``set_key()`` / ``set_service()`` — cloud ports read from
  a PyfficeService instance, not directly.

Each cloud port overrides the PyfficePort file I/O surface
(``file_open``, ``file_write``, ``file_export``, ``file_import``)
so the standard port API works transparently for cloud-hosted files.

Optional dependencies (guarded with try/except so the module loads
without them):
- ``google-auth`` + ``google-api-python-client`` for Google Drive
- ``dropbox`` for Dropbox
"""

from os.path import dirname, join
import datetime as dt
from io import BytesIO
from typing import Any, Optional

from kahndor import kahndor
from kahndor.logma import Logma

from pyffice.ports.ports import PyfficePort
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "../config/_data_", "cloud_services.yaml")


# -- Optional dependency probes ---------------------------------------------------

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build as gbuild
    from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False
    service_account = None
    gbuild = None
    MediaFileUpload = None
    MediaIoBaseDownload = None

try:
    import dropbox as dbx_pkg
    from dropbox.files import FileMetadata, FolderMetadata

    HAS_DROPBOX = True
except ImportError:
    HAS_DROPBOX = False
    dbx_pkg = None
    FileMetadata = None
    FolderMetadata = None


# ============================================================================================#
#  BASE CLOUD PORT
# ============================================================================================#

class PyfficeCloudPort(PyfficePort):
    """Base class for cloud-storage ports.

    Subclasses (GoogleDrive, Dropbox) implement the concrete API
    calls. The base provides the common auth/credential plumbing
    and the standard PyfficePort override surface.

    All secrets are held in ``self._credentials`` (a dict) and
    should be sourced from ``PyfficeService`` / pycurity — never
    from env vars.
    """

    SERIALIZATION_VERSION = (1, 0, 0)

    PROVIDER = "base"

    def __init__(self, cfg=None) -> None:
        """Initialize cloud port.

        Args:
            cfg: Optional config dict. May contain:
                - ``service_account_path``: path to a service account JSON.
                - ``access_token``: raw OAuth2 access token.
                - ``credentials``: pre-loaded credential dict.
        """
        logma.debug(f"PyfficeCloudPort.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeCloudPort")).override(cfg)
        self._credentials = None
        self._client = None
        self.authenticated = False

    # -- Auth surface -------------------------------------------------------------

    def authenticate(self, credentials: Optional[dict] = None) -> Self:
        """Authenticate with the cloud provider.

        Subclasses override this to build their specific client
        (googleapiclient discovery, dropbox.Dropbox, etc.).

        Args:
            credentials: Credential dict. Keys depend on provider:
                - Google: ``{"service_account_path": "..."}`` or
                  ``{"service_account_json": {...}}`` or
                  ``{"access_token": "..."}``.
                - Dropbox: ``{"access_token": "..."}`` or
                  ``{"app_key": "...", "app_secret": "...",
                     "refresh_token": "..."}``.

        Returns:
            Self for chaining.
        """
        if credentials is not None:
            self._credentials = credentials
        if self._credentials is None:
            raise ValueError(f"No credentials provided for {self.PROVIDER}")
        return self

    # -- Cloud file operations (subclass interface) -------------------------------

    def list_files(self, folder_id: Optional[str] = None) -> list[dict]:
        """List files in a cloud folder.

        Args:
            folder_id: Cloud-provider folder ID. ``None`` means root.

        Returns:
            List of ``{"id": ..., "name": ..., "mime_type": ...,
            "size": ...}`` dicts.
        """
        raise NotImplementedError("Subclass must implement list_files")

    def download_file(self, file_id: str, local_path: str) -> "PyfficeCloudPort":
        """Download a cloud file to a local path.

        Args:
            file_id: Cloud-provider file ID.
            local_path: Local filesystem path to write to.

        Returns:
            Self for chaining.
        """
        raise NotImplementedError("Subclass must implement download_file")

    def upload_file(self, local_path: str, parent_folder_id: Optional[str] = None) -> dict:
        """Upload a local file to the cloud.

        Args:
            local_path: Local filesystem path to read from.
            parent_folder_id: Cloud-provider folder ID to upload into.

        Returns:
            Dict with the uploaded file's cloud metadata (id, name, etc.).
        """
        raise NotImplementedError("Subclass must implement upload_file")

    def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> dict:
        """Create a folder in cloud storage.

        Args:
            name: Folder name.
            parent_folder_id: Parent folder ID (None for root).

        Returns:
            Dict with the new folder's cloud metadata.
        """
        raise NotImplementedError("Subclass must implement create_folder")

    def delete_file(self, file_id: str) -> "PyfficeCloudPort":
        """Delete a file from cloud storage.

        Args:
            file_id: Cloud-provider file ID.

        Returns:
            Self for chaining.
        """
        raise NotImplementedError("Subclass must implement delete_file")

    # -- PyfficePort override surface --------------------------------------------

    def cloud_download(self, file_id: str) -> bytes:
        """Download a cloud file and return raw bytes.

        Override of PyfficePort.file_open for cloud sources.
        Uses download_file to a temp path, then reads bytes.
        """
        import tempfile
        import os

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        try:
            self.download_file(file_id, tmp)
            with open(tmp, "rb") as f:
                return f.read()
        finally:
            os.unlink(tmp)

    def cloud_upload(self, data: bytes, name: str, parent_folder_id: Optional[str] = None) -> dict:
        """Upload raw bytes to cloud storage.

        Override of PyfficePort.file_write for cloud destinations.
        """
        import tempfile
        import os

        fd, tmp = tempfile.mkstemp()
        os.close(fd)
        try:
            with open(tmp, "wb") as f:
                f.write(data)
            return self.upload_file(tmp, parent_folder_id)
        finally:
            os.unlink(tmp)


# ============================================================================================#
#  GOOGLE DRIVE
# ============================================================================================#

class PyfficePortGoogleDrive(PyfficeCloudPort):
    """Google Drive cloud storage port.

    Requires ``google-auth`` and ``google-api-python-client``.
    Authenticate with a service account JSON or OAuth2 access token.

    Credentials (via PyfficeService / pycurity):
        ``{"service_account_path": "/path/to/service-account.json"}``
        or
        ``{"service_account_json": {...}}``
        or
        ``{"access_token": "ya29..."}``
    """

    SERIALIZATION_VERSION = (1, 0, 0)
    PROVIDER = "google_drive"

    def authenticate(self, credentials: Optional[dict] = None) -> Self:
        """Build the googleapiclient client.

        Args:
            credentials: See class docstring for accepted keys.

        Returns:
            Self for chaining.
        """
        super().authenticate(credentials)
        if not HAS_GOOGLE:
            raise ImportError(
                "google-auth and google-api-python-client are required. "
                "Install: pip install google-auth google-api-python-client"
            )
        creds = self._credentials
        scopes = ["https://www.googleapis.com/auth/drive.file"]

        if "service_account_path" in creds:
            self._client = service_account.ServiceAccountCredentials.from_service_account_file(
                creds["service_account_path"], scopes=scopes
            )
        elif "service_account_json" in creds:
            from io import BytesIO
            import json
            sa_info = creds["service_account_json"]
            if isinstance(sa_info, str):
                sa_info = json.loads(sa_info)
            self._client = service_account.ServiceAccountCredentials.from_service_account_info(
                sa_info, scopes=scopes
            )
        elif "access_token" in creds:
            import requests
            from google.oauth2.credentials import Credentials
            self._client = Credentials(token=creds["access_token"])
        else:
            raise ValueError(
                "Google credentials must contain 'service_account_path', "
                "'service_account_json', or 'access_token'"
            )

        self._service = gbuild("drive", "v3", credentials=self._client)
        self.authenticated = True
        logma.info(f"Google Drive authenticated ({self.PROVIDER})")
        return self

    def list_files(self, folder_id: Optional[str] = None) -> list[dict]:
        """List files in a Google Drive folder.

        Args:
            folder_id: Drive folder ID. ``None`` or ``"root"`` for root.

        Returns:
            List of ``{"id", "name", "mime_type", "size"}`` dicts.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        q = None
        if folder_id and folder_id != "root":
            q = f"'{folder_id}' in parents and trashed=false"
        else:
            q = "'root' in parents and trashed=false"
        results = self._service.files().list(
            q=q, pageSize=100, fields="files(id, name, mimeType, size)"
        ).execute()
        return [
            {"id": f["id"], "name": f["name"],
             "mime_type": f.get("mimeType", ""), "size": f.get("size", "0")}
            for f in results.get("files", [])
        ]

    def download_file(self, file_id: str, local_path: str) -> Self:
        """Download a file from Google Drive.

        Args:
            file_id: Drive file ID.
            local_path: Local path to save the file.

        Returns:
            Self for chaining.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        request = self._service.files().get_media(fileId=file_id)
        with open(local_path, "wb") as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                _, done = downloader.next_chunk()
        logma.info(f"Downloaded {file_id} -> {local_path}")
        return self

    def upload_file(self, local_path: str, parent_folder_id: Optional[str] = None) -> dict:
        """Upload a file to Google Drive.

        Args:
            local_path: Local file path.
            parent_folder_id: Parent folder ID (None for root).

        Returns:
            Dict with ``id`` and ``name`` of the uploaded file.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        import os
        media = MediaFileUpload(local_path, resumable=True)
        metadata = {"name": os.path.basename(local_path)}
        if parent_folder_id:
            metadata["parents"] = [parent_folder_id]
        result = self._service.files().create(
            body=metadata, media_body=media, fields="id,name"
        ).execute()
        logma.info(f"Uploaded {local_path} -> {result.get('id')}")
        return {"id": result.get("id"), "name": result.get("name")}

    def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> dict:
        """Create a folder on Google Drive.

        Args:
            name: Folder name.
            parent_folder_id: Parent folder ID.

        Returns:
            Dict with ``id`` and ``name`` of the new folder.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        metadata = {"name": name, "mimeType": "application/vnd.google-apps.folder"}
        if parent_folder_id:
            metadata["parents"] = [parent_folder_id]
        result = self._service.files().create(body=metadata, fields="id,name").execute()
        logma.info(f"Created folder '{name}' -> {result.get('id')}")
        return {"id": result.get("id"), "name": result.get("name")}

    def delete_file(self, file_id: str) -> Self:
        """Delete a file from Google Drive.

        Args:
            file_id: Drive file ID.

        Returns:
            Self for chaining.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        self._service.files().delete(fileId=file_id).execute()
        logma.info(f"Deleted {file_id}")
        return self


# ============================================================================================#
#  DROPBOX
# ============================================================================================#

class PyfficePortDropbox(PyfficeCloudPort):
    """Dropbox cloud storage port.

    Requires the ``dropbox`` package.
    Authenticate with an access token or app key/secret + refresh token.

    Credentials (via PyfficeService / pycurity):
        ``{"access_token": "sl.xxx"}``
        or
        ``{"app_key": "...", "app_secret": "...", "refresh_token": "..."}``
    """

    SERIALIZATION_VERSION = (1, 0, 0)
    PROVIDER = "dropbox"

    def authenticate(self, credentials: Optional[dict] = None) -> Self:
        """Build the Dropbox client.

        Args:
            credentials: See class docstring for accepted keys.

        Returns:
            Self for chaining.
        """
        super().authenticate(credentials)
        if not HAS_DROPBOX:
            raise ImportError(
                "dropbox package is required. Install: pip install dropbox"
            )
        creds = self._credentials
        if "access_token" in creds:
            self._client = dbx_pkg.Dropbox(oauth2_access_token=creds["access_token"])
        elif "app_key" in creds and "refresh_token" in creds:
            self._client = dbx_pkg.Dropbox(
                app_key=creds["app_key"],
                app_secret=creds.get("app_secret", ""),
                oauth2_refresh_token=creds["refresh_token"],
            )
        else:
            raise ValueError(
                "Dropbox credentials must contain 'access_token' or "
                "('app_key' + 'refresh_token')"
            )
        self.authenticated = True
        logma.info(f"Dropbox authenticated ({self.PROVIDER})")
        return self

    def list_files(self, folder_id: Optional[str] = None) -> list[dict]:
        """List files in a Dropbox folder.

        Args:
            folder_id: Dropbox path (e.g. ``"/Documents"``). ``None`` for root.

        Returns:
            List of ``{"id", "name", "mime_type", "size"}`` dicts.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        path = folder_id or ""
        result = self._client.files_list_folder(path)
        files = []
        for entry in result.entries:
            if isinstance(entry, FileMetadata):
                files.append({
                    "id": entry.id,
                    "name": entry.name,
                    "mime_type": "",
                    "size": str(entry.size),
                    "path": entry.path_display,
                })
            elif isinstance(entry, FolderMetadata):
                files.append({
                    "id": entry.id,
                    "name": entry.name,
                    "mime_type": "folder",
                    "size": "0",
                    "path": entry.path_display,
                })
        return files

    def download_file(self, file_id: str, local_path: str) -> Self:
        """Download a file from Dropbox.

        Args:
            file_id: Dropbox file path (e.g. ``"/file.pdf"``).
            local_path: Local path to save the file.

        Returns:
            Self for chaining.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        self._client.files_download_to_file(local_path, file_id)
        logma.info(f"Downloaded {file_id} -> {local_path}")
        return self

    def upload_file(self, local_path: str, parent_folder_id: Optional[str] = None) -> dict:
        """Upload a file to Dropbox.

        Args:
            local_path: Local file path.
            parent_folder_id: Dropbox folder path (e.g. ``"/uploads"``).

        Returns:
            Dict with ``id``, ``name``, and ``path`` of the uploaded file.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        import os
        dest = f"{parent_folder_id or ''}/{os.path.basename(local_path)}"
        with open(local_path, "rb") as f:
            result = self._client.files_upload(f.read(), dest)
        logma.info(f"Uploaded {local_path} -> {dest}")
        return {
            "id": result.id,
            "name": result.name,
            "path": result.path_display,
        }

    def create_folder(self, name: str, parent_folder_id: Optional[str] = None) -> dict:
        """Create a folder on Dropbox.

        Args:
            name: Folder name.
            parent_folder_id: Parent folder path.

        Returns:
            Dict with ``id``, ``name``, and ``path`` of the new folder.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        path = f"{parent_folder_id or ''}/{name}"
        result = self._client.files_create_folder_v2(path)
        logma.info(f"Created folder '{path}'")
        return {
            "id": result.metadata.id,
            "name": result.metadata.name,
            "path": result.metadata.path_display,
        }

    def delete_file(self, file_id: str) -> Self:
        """Delete a file from Dropbox.

        Args:
            file_id: Dropbox file path.

        Returns:
            Self for chaining.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        self._client.files_delete_v2(file_id)
        logma.info(f"Deleted {file_id}")
        return self
