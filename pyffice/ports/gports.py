"""Google Workspace ports for Google Docs, Sheets, Slides, and Forms.

T-NEW-070: Builds out the empty stubs in the original gports.py
into real Google Workspace API integrations. Each port inherits
from PyfficeCloudPort and uses the googleapiclient to interact
with the specific Google Workspace service.

All ports share the same auth surface as PyfficePortGoogleDrive
(service account JSON, service account dict, or OAuth2 access token).
The scopes differ per service.

Optional deps: google-auth, google-api-python-client (guarded
with try/except so the module loads without them).
"""

from os.path import dirname, join
from typing import Any, Optional

from kahndor import kahndor
from kahndor.logma import Logma

from pyffice.ports.cloud_ports import PyfficeCloudPort, HAS_GOOGLE

# ====================================================================================================================||
here = join(dirname(__file__), "")
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "../config/_data_", "imports.yaml")


class _GoogleWorkspacePortBase(PyfficeCloudPort):
    """Shared base for Google Workspace service ports.

    Provides the common ``_build_service`` helper that all
    Workspace ports use to create their googleapiclient discovery
    object. Each subclass sets ``API_NAME``, ``API_VERSION``, and
    ``SCOPES``.
    """

    SERIALIZATION_VERSION = (1, 0, 0)

    API_NAME = ""
    API_VERSION = ""
    SCOPES = []

    def authenticate(self, credentials: Optional[dict] = None) -> "_GoogleWorkspacePortBase":
        """Authenticate and build the googleapiclient service.

        Args:
            credentials: Same shape as PyfficePortGoogleDrive.

        Returns:
            Self for chaining.
        """
        super().authenticate(credentials)
        if not HAS_GOOGLE:
            raise ImportError(
                "google-auth and google-api-python-client are required. "
                "Install: pip install google-auth google-api-python-client"
            )
        from google.oauth2 import service_account
        from googleapiclient.discovery import build as gbuild
        from google.oauth2.credentials import Credentials

        creds = self._credentials

        if "service_account_path" in creds:
            gc = service_account.ServiceAccountCredentials.from_service_account_file(
                creds["service_account_path"], scopes=self.SCOPES
            )
        elif "service_account_json" in creds:
            import json
            sa_info = creds["service_account_json"]
            if isinstance(sa_info, str):
                sa_info = json.loads(sa_info)
            gc = service_account.ServiceAccountCredentials.from_service_account_info(
                sa_info, scopes=self.SCOPES
            )
        elif "access_token" in creds:
            gc = Credentials(token=creds["access_token"])
        else:
            raise ValueError(
                f"Google credentials must contain 'service_account_path', "
                f"'service_account_json', or 'access_token'"
            )

        self._client = gc
        self._service = gbuild(self.API_NAME, self.API_VERSION, credentials=gc)
        self.authenticated = True
        logma.info(f"{self.API_NAME} v{self.API_VERSION} authenticated")
        return self


# ============================================================================================#
#  GOOGLE SHEETS
# ============================================================================================#

class PyfficePortGoogleSheets(_GoogleWorkspacePortBase):
    """Google Sheets port for reading and writing spreadsheet data.

    Requires ``google-auth`` and ``google-api-python-client``.

    Scopes: ``https://www.googleapis.com/auth/spreadsheets``

    Usage::

        port = PyfficePortGoogleSheets()
        port.authenticate({"service_account_path": "sa.json"})
        values = port.read_range("sheet_id", "A1:D10")
        port.write_range("sheet_id", "A1", [["hello", "world"]])
    """

    API_NAME = "sheets"
    API_VERSION = "v4"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    def read_range(self, spreadsheet_id: str, range_name: str) -> list[list]:
        """Read values from a spreadsheet range.

        Args:
            spreadsheet_id: The Google Sheets document ID.
            range_name: A1 notation range (e.g. ``"Sheet1!A1:D10"``).

        Returns:
            2D list of cell values.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name
        ).execute()
        return result.get("values", [])

    def write_range(self, spreadsheet_id: str, range_name: str,
                    values: list[list]) -> dict:
        """Write values to a spreadsheet range.

        Args:
            spreadsheet_id: The Google Sheets document ID.
            range_name: A1 notation range (e.g. ``"Sheet1!A1"``).
            values: 2D list of cell values.

        Returns:
            Response dict from the API (updatedCells, etc.).
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        body = {"values": values}
        result = self._service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", body=body
        ).execute()
        logma.info(f"Updated {result.get('updatedCells', 0)} cells")
        return result

    def append_range(self, spreadsheet_id: str, range_name: str,
                     values: list[list]) -> dict:
        """Append values after the last row of data in a range.

        Args:
            spreadsheet_id: The Google Sheets document ID.
            range_name: A1 notation range to append after.
            values: 2D list of cell values.

        Returns:
            Response dict from the API.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        body = {"values": values}
        result = self._service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption="RAW", insertDataOption="INSERT_ROWS", body=body
        ).execute()
        return result

    def clear_range(self, spreadsheet_id: str, range_name: str) -> dict:
        """Clear values from a spreadsheet range.

        Args:
            spreadsheet_id: The Google Sheets document ID.
            range_name: A1 notation range to clear.

        Returns:
            Response dict from the API.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id, range=range_name
        ).execute()
        return result

    def create_spreadsheet(self, title: str) -> dict:
        """Create a new spreadsheet.

        Args:
            title: Title of the new spreadsheet.

        Returns:
            Dict with ``spreadsheetId`` and ``properties``.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.spreadsheets().create(
            body={"properties": {"title": title}}
        ).execute()
        return {"spreadsheetId": result.get("spreadsheetId"),
                "properties": result.get("properties", {})}

    def list_sheets(self, spreadsheet_id: str) -> list[dict]:
        """List all sheet tabs in a spreadsheet.

        Args:
            spreadsheet_id: The Google Sheets document ID.

        Returns:
            List of ``{"sheetId", "title", "index"}`` dicts.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        metadata = self._service.spreadsheets().get(
            spreadsheetId=spreadsheet_id
        ).execute()
        return [
            {"sheetId": s["properties"].get("sheetId"),
             "title": s["properties"].get("title"),
             "index": s["properties"].get("index", 0)}
            for s in metadata.get("sheets", [])
        ]


# ============================================================================================#
#  GOOGLE DOCS
# ============================================================================================#

class PyfficePortGoogleDocs(_GoogleWorkspacePortBase):
    """Google Docs port for reading and writing document content.

    Requires ``google-auth`` and ``google-api-python-client``.

    Scopes: ``https://www.googleapis.com/auth/documents``

    Usage::

        port = PyfficePortGoogleDocs()
        port.authenticate({"service_account_path": "sa.json"})
        doc = port.get_document("doc_id")
        port.insert_text("doc_id", "Hello, World!")
    """

    API_NAME = "docs"
    API_VERSION = "v1"
    SCOPES = ["https://www.googleapis.com/auth/documents"]

    def get_document(self, document_id: str) -> dict:
        """Fetch the full document structure.

        Args:
            document_id: The Google Docs document ID.

        Returns:
            Full document JSON (body, inlineObjects, etc.).
        """
        logma.debug(f"PyfficePortGoogleDocs.get_document called")
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.documents().get(documentId=document_id).execute()

    def create_document(self, title: str) -> dict:
        """Create a new Google Doc.

        Args:
            title: Title of the new document.

        Returns:
            Dict with ``documentId`` and ``title``.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.documents().create(
            body={"title": title}
        ).execute()
        return {"documentId": result.get("documentId"),
                "title": result.get("title", "")}

    def insert_text(self, document_id: str, text: str,
                    index: Optional[int] = None) -> dict:
        """Insert text into a document.

        Args:
            document_id: The Google Docs document ID.
            text: Text to insert.
            index: Position to insert at (1 = beginning). If None,
                appends to end of document.

        Returns:
            Response dict with write results.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        if index is None:
            # Append: find the last element's end index
            doc = self._service.documents().get(documentId=document_id).execute()
            elements = doc.get("body", {}).get("content", [])
            index = elements[-1]["endIndex"] - 1 if elements else 1
        requests = [{"insertText": {"location": {"index": index}, "content": text}}]
        return self._service.documents().batchUpdate(
            documentId=document_id, body={"requests": requests}
        ).execute()

    def replace_text(self, document_id: str, find: str, replace: str) -> dict:
        """Find and replace text in a document.

        Args:
            document_id: The Google Docs document ID.
            find: Text to search for.
            replace: Replacement text.

        Returns:
            Response dict.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        requests = [{
            "replaceAllText": {
                "containsText": {"text": find, "matchCase": True},
                "replaceText": replace,
            }
        }]
        return self._service.documents().batchUpdate(
            documentId=document_id, body={"requests": requests}
        ).execute()

    def batch_update(self, document_id: str, requests: list[dict]) -> dict:
        """Apply a batch of document update requests.

        Args:
            document_id: The Google Docs document ID.
            requests: List of Google Docs API request objects.

        Returns:
            Response dict.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.documents().batchUpdate(
            documentId=document_id, body={"requests": requests}
        ).execute()


# ============================================================================================#
#  GOOGLE SLIDES
# ============================================================================================#

class PyfficePortGoogleSlides(_GoogleWorkspacePortBase):
    """Google Slides port for reading and writing presentation data.

    Requires ``google-auth`` and ``google-api-python-client``.

    Scopes: ``https://www.googleapis.com/auth/presentations``

    Usage::

        port = PyfficePortGoogleSlides()
        port.authenticate({"service_account_path": "sa.json"})
        deck = port.get_presentation("pres_id")
        port.create_presentation("My Deck")
    """

    API_NAME = "slides"
    API_VERSION = "v1"
    SCOPES = ["https://www.googleapis.com/auth/presentations"]

    def get_presentation(self, presentation_id: str) -> dict:
        """Fetch the full presentation structure.

        Args:
            presentation_id: The Google Slides presentation ID.

        Returns:
            Full presentation JSON (slides, layouts, etc.).
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.presentations().get(
            presentationId=presentation_id
        ).execute()

    def create_presentation(self, title: str) -> dict:
        """Create a new presentation.

        Args:
            title: Title of the new presentation.

        Returns:
            Dict with ``presentationId``.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.presentations().create(
            body={"title": title}
        ).execute()
        return {"presentationId": result.get("presentationId"),
                "title": title}

    def add_slide(self, presentation_id: str,
                  layout: str = "BLANK") -> dict:
        """Add a slide to a presentation.

        Args:
            presentation_id: The Google Slides presentation ID.
            layout: Layout reference (e.g. "TITLE", "BLANK",
                "TITLE_AND_BODY").

        Returns:
            Response dict with the new slide's objectId.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        requests = [{"createSlide": {"slideLayoutReference": {"predefinedLayout": layout}}}]
        result = self._service.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests}
        ).execute()
        return result

    def batch_update(self, presentation_id: str, requests: list[dict]) -> dict:
        """Apply a batch of presentation update requests.

        Args:
            presentation_id: The Google Slides presentation ID.
            requests: List of Google Slides API request objects.

        Returns:
            Response dict.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.presentations().batchUpdate(
            presentationId=presentation_id, body={"requests": requests}
        ).execute()


# ============================================================================================#
#  GOOGLE FORMS
# ============================================================================================#

class PyfficePortGoogleForms(_GoogleWorkspacePortBase):
    """Google Forms port for reading and writing form data.

    Requires ``google-auth`` and ``google-api-python-client``.

    Scopes: ``https://www.googleapis.com/auth/forms.body``

    Note: The Google Forms API is relatively new and has limited
    operations compared to Sheets/Docs/Slides. This port covers
    the core CRUD: create, get, update, and list responses.

    Usage::

        port = PyfficePortGoogleForms()
        port.authenticate({"service_account_path": "sa.json"})
        form = port.get_form("form_id")
        responses = port.list_responses("form_id")
    """

    API_NAME = "forms"
    API_VERSION = "v1"
    SCOPES = [
        "https://www.googleapis.com/auth/forms.body",
        "https://www.googleapis.com/auth/forms.responses.readonly",
    ]

    def get_form(self, form_id: str) -> dict:
        """Fetch the form structure.

        Args:
            form_id: The Google Forms form ID.

        Returns:
            Full form JSON (info, items, etc.).
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.forms().get(formId=form_id).execute()

    def create_form(self, title: str, description: str = "") -> dict:
        """Create a new form.

        Args:
            title: Form title.
            description: Optional form description.

        Returns:
            Dict with ``formId`` and ``responderUri``.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        info = {"title": title}
        if description:
            info["documentTitle"] = description
        result = self._service.forms().create(body={"info": info}).execute()
        return {"formId": result.get("formId"),
                "responderUri": result.get("responderUri", "")}

    def batch_update(self, form_id: str, requests: list[dict]) -> dict:
        """Apply batch updates to a form (add questions, etc.).

        Args:
            form_id: The Google Forms form ID.
            requests: List of Google Forms API request objects.

        Returns:
            Response dict.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        return self._service.forms().batchUpdate(
            formId=form_id, body={"requests": requests}
        ).execute()

    def list_responses(self, form_id: str) -> list[dict]:
        """List form responses.

        Args:
            form_id: The Google Forms form ID.

        Returns:
            List of response dicts.
        """
        if not self.authenticated:
            raise RuntimeError("Not authenticated. Call authenticate() first.")
        result = self._service.forms().responses().list(
            formId=form_id
        ).execute()
        return result.get("responses", [])
