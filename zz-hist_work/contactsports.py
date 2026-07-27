"""
Pyffice Contacts Ports - External format converters for contact data.
"""
from pyffice.contacts.contacts import PyfficeContact
from pyffice.ports.ports import PyfficePort


class VCardPort(PyfficePort):
    """Port for vCard (.vcf) format."""

    def read(self, file_path: str) -> PyfficeContact:
        """Read vCard file and convert to PyfficeContact."""
        pass

    def write(self, contact: PyfficeContact, file_path: str) -> None:
        """Write PyfficeContact to vCard file."""
        pass


class CSVContactPort(PyfficePort):
    """Port for CSV contact format."""

    def read(self, file_path: str) -> PyfficeContact:
        """Read CSV file and convert to PyfficeContact."""
        pass

    def write(self, contact: PyfficeContact, file_path: str) -> None:
        """Write PyfficeContact to CSV file."""
        pass


class LDIFPort(PyfficePort):
    """Port for LDIF (LDAP) format."""

    def read(self, file_path: str) -> PyfficeContact:
        """Read LDIF file and convert to PyfficeContact."""
        pass

    def write(self, contact: PyfficeContact, file_path: str) -> None:
        """Write PyfficeContact to LDIF file."""
        pass
