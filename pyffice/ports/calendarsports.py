"""
Pyffice Calendar Ports - External format converters for calendar data.
"""
from pyffice.calendars.calendars import PyfficeCalendar
from pyffice.ports.ports import PyfficePort


class ICSPort(PyfficePort):
    """Port for iCalendar (.ics) format."""

    def read(self, file_path: str) -> PyfficeCalendar:
        """Read ICS file and convert to PyfficeCalendar."""
        # TODO: Implement ICS parsing
        pass

    def write(self, calendar: PyfficeCalendar, file_path: str) -> None:
        """Write PyfficeCalendar to ICS file."""
        # TODO: Implement ICS writing
        pass


class CalDAVPort(PyfficePort):
    """Port for CalDAV protocol."""

    def read(self, url: str) -> PyfficeCalendar:
        """Read calendar from CalDAV server."""
        pass

    def write(self, calendar: PyfficeCalendar, url: str) -> None:
        """Write calendar to CalDAV server."""
        pass


class OutlookPort(PyfficePort):
    """Port for Microsoft Outlook format."""

    def read(self, file_path: str) -> PyfficeCalendar:
        """Read Outlook file and convert to PyfficeCalendar."""
        pass

    def write(self, calendar: PyfficeCalendar, file_path: str) -> None:
        """Write PyfficeCalendar to Outlook format."""
        pass
