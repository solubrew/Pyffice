"""
Pyffice Calendar Ports - External format converters for calendar data.
"""
import re
from datetime import datetime
from typing import Optional

from pyffice.calendars.calendars import PyfficeCalendar, PyfficeEvent
from pyffice.ports.ports import PyfficePort


class ICSPort(PyfficePort):
    """Port for iCalendar (.ics) format."""

    def read(self, file_path: str) -> PyfficeCalendar:
        """Read ICS file and convert to PyfficeCalendar."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return self._parse_ics(content)

    def _parse_ics(self, content: str) -> PyfficeCalendar:
        """Parse ICS content into PyfficeCalendar."""
        calendar = PyfficeCalendar()
        events = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', content, re.DOTALL)
        for event_data in events:
            event = self._parse_event(event_data)
            if event:
                calendar.events.append(event)
        return calendar

    def _parse_event(self, event_data: str) -> Optional[PyfficeEvent]:
        """Parse a single VEVENT block."""
        title = self._extract_field(event_data, 'SUMMARY')
        description = self._extract_field(event_data, 'DESCRIPTION')
        start = self._extract_field(event_data, 'DTSTART')
        end = self._extract_field(event_data, 'DTEND')
        
        if title:
            event = PyfficeEvent()
            event.set_event(title)
            event.set_start_dttm(start)
            event.set_end_dttm(end)
            return event
        return None

    def _extract_field(self, event_data: str, field: str) -> Optional[str]:
        """Extract a field from event data."""
        match = re.search(rf'{field}:(.*?)(?:\r?\n|$)', event_data)
        return match.group(1).strip() if match else None

    def write(self, calendar: PyfficeCalendar, file_path: str) -> None:
        """Write PyfficeCalendar to ICS file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("BEGIN:VCALENDAR\r\n")
            f.write("VERSION:2.0\r\n")
            f.write("PRODID:-//Pyffice//Calendar//EN\r\n")
            for event in calendar.events or []:
                f.write("BEGIN:VEVENT\r\n")
                f.write(f"SUMMARY:{event.event}\r\n")
                if event.start_dttm:
                    f.write(f"DTSTART:{event.start_dttm}\r\n")
                if event.end_dttm:
                    f.write(f"DTEND:{event.end_dttm}\r\n")
                f.write("END:VEVENT\r\n")
            f.write("END:VCALENDAR\r\n")


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
