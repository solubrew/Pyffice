# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
        docid:
        name:
        description: >
        version: 0.0.0.0.0.0
        authority: filesystem
        security: seclvl2
        <(WT)>: -32
"""

# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
import datetime as dt

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||
from kahndor import kahndor
from kahndor.logma import Logma
from pyffice.document import PyfficeUnit
from typing import Any
from typing_extensions import Self

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "events.yaml")


class PyfficeTimeUnit(PyfficeUnit):
    SERIALIZATION_VERSION = (1, 0, 0)
    """"""

    def __init__(self, cfg=None) -> None:
        """"""
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeScaleUnit")).override(cfg)
        self.start_time = None
        self.end_time = None
        self.days = None
        self.hours = None
        self.minutes = None
        self.months = None
        self.scale_unit = None
        self.seconds = None
        self.weeks = None
        self.years = None
        self.decades = None
        self.centuries = None

    def get_centuries(self) -> Any:
        """Return the centuries.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        centuries = self.end_time - self.start_time
        if centuries != self.centuries:
            self.add_change("centuries", self.centuries, centuries)
            self.centuries = centuries
        return self.centuries

    def get_days(self) -> Any:
        """Return the days.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        days = self.end_time - self.start_time
        if days != self.days:
            self.add_change("days", self.days, days)
            self.days = days
        return self.days

    def get_decades(self) -> Any:
        """Return the decades.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        decades = self.end_time - self.start_time
        if decades != self.decades:
            self.add_change("decades", self.decades, decades)
            self.decades = decades
        return self.decades

    def get_hours(self) -> Any:
        """Return the hours.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        hours = self.end_time - self.start_time
        if hours != self.hours:
            self.add_change("hours", self.hours, hours)
            self.hours = hours
        return self.hours

    def get_minutes(self) -> Any:
        """Return the minutes.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        minutes = self.end_time - self.start_time
        if minutes != self.minutes:
            self.add_change("minutes", self.minutes, minutes)
            self.minutes = minutes
        return self.minutes

    def get_months(self) -> Any:
        """Return the months.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        months = self.end_time - self.start_time
        if months != self.months:
            self.add_change("months", self.months, months)
            self.months = months
        return self.months

    def get_seconds(self) -> Any:
        """Return the seconds.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        seconds = self.end_time - self.start_time
        if seconds != self.seconds:
            self.add_change("seconds", self.seconds, seconds)
            self.seconds = seconds
        return self.seconds

    def get_weeks(self) -> Any:
        """Return the weeks.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        weeks = self.end_time - self.start_time
        if weeks != self.weeks:
            self.add_change("weeks", self.weeks, weeks)
            self.weeks = weeks
        return self.weeks

    def get_years(self) -> Any:
        """Return the years.
        
        Returns:
            Self for chaining.
        """
        if self.start_time is None or self.end_time is None:
            return None
        years = self.end_time - self.start_time
        if years != self.years:
            self.add_change("years", self.years, years)
            self.years = years
        return self.years

    def load_unit(self, unit) -> Self:
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        logma.info(f"Load Unit {unit}")
        if unit is None:
            unit = self.config.dikt.get("unit", {})
        super().load_unit(unit)
        self.set_scale_unit(unit.get("scale_unit", None))
        self.set_time_start(unit.get("start_time", None))
        self.set_time_end(unit.get("end_time", None))
        self.get_seconds()
        self.get_minutes()
        self.get_hours()
        self.get_days()
        self.get_weeks()
        self.get_months()
        self.get_years()
        self.get_decades()
        self.get_centuries()
        return self

    def set_scale_unit(self, scale_unit) -> Self:
        """Set the scale unit.
        
        Args:
            scale_unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        cfg = {}
        match scale_unit:
            case "day":
                self.scale_unit = "day"
            case "hour":
                self.scale_unit = "hour"
            case "minute":
                self.scale_unit = "minute"
            case "month":
                self.scale_unit = "month"
            case "second":
                self.scale_unit = "second"
            case "quarter_hour":
                self.scale_unit = "quarter_hour"
            case "quarter_year":
                self.scale_unit = "quarter_year"
            case "year":
                self.scale_unit = "year"
            case _:
                raise ValueError(f"tframe {scale_unit} is not supported")
        return self

    def set_time_end(self, end_time) -> Self:
        """Set the time end.
        
        Args:
            end_time: Parameter.
        
        Returns:
            Self for chaining.
        """
        if end_time != self.end_time:
            self.add_change("end_time", self.end_time, end_time)
            self.end_time = end_time
        return self

    def set_time_start(self, start_time) -> Self:
        """Set the time start.
        
        Args:
            start_time: Parameter.
        
        Returns:
            Self for chaining.
        """
        if start_time != self.start_time:
            self.add_change("start_time", self.start_time, start_time)
            self.start_time = start_time
        return self

class PyfficeEvent(PyfficeUnit):
    """"""
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """"""
        logma.debug(f"PyfficeEvent.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeEvent")).override(cfg)
        self.event = None
        self.end_dttm = None
        self.location_attendance = None
        self.start_dttm = None

    def load_unit(self, unit) -> Self:
        """Load a unit dict into this document.
        
        Args:
            unit: Parameter.
        
        Returns:
            Self for chaining.
        """
        if unit is None:
            unit = {}
        super().load_unit(unit)
        self.set_event(unit.get("event", None))
        self.set_start_dttm(unit.get("start_dttm", None))
        self.set_end_dttm(unit.get("end_dttm", None))
        self.set_location(unit.get("location", None))
        return self

    def set_end_dttm(self, end_dttm) -> Self:
        """Set the end dttm.
        
        Args:
            end_dttm: Parameter.
        
        Returns:
            Self for chaining.
        """
        if end_dttm != self.end_dttm:
            self.add_change("start_dttm", self.end_dttm, end_dttm)
            self.end_dttm = end_dttm
        return self

    def set_event(self, event) -> Self:
        """Set the event.
        
        Args:
            event: Parameter.
        
        Returns:
            Self for chaining.
        """
        if event != self.event:
            self.add_change("event", self.event, event)
            self.event = event
        return self

    def set_attendance_location(self, location) -> Self:
        """Set the attendance location.
        
        Args:
            location: Parameter.
        
        Returns:
            Self for chaining.
        """
        if location != self.location:
            self.add_change("location", self.location, location)
            self.location_attendance = location
        return self

    def set_start_dttm(self, start_dttm) -> Self:
        """Set the start dttm.
        
        Args:
            start_dttm: Parameter.
        
        Returns:
            Self for chaining.
        """
        if start_dttm != self.start_dttm:
            self.add_change("start_dttm", self.start_dttm, start_dttm)
            self.start_dttm = start_dttm
        return self


class PyfficeTask(PyfficeUnit):
    """A single task attached to an alarm or event.

    Holds a dict-shaped payload (cfg) and tracks its own change history.
    Constructed as ``PyfficeTask(payload)`` — used by PyfficeAlarm to
    wrap acknowledge / notify / postpone / postpone-list payloads.
    """
    SERIALIZATION_VERSION = (1, 0, 0)

    def __init__(self, cfg=None) -> None:
        """Initialize a task with an optional dict-shaped payload."""
        logma.debug(f"PyfficeTask.__init__ called")
        super().__init__(cfg)
        self.config.override(kahndor.Instruct(pxcfg).select("PyfficeTask")).override(cfg)
        self.payload = cfg

    def get_payload(self) -> Any:
        """Return the stored payload dict (or None if constructed empty)."""
        return self.payload

    def set_payload(self, payload) -> "PyfficeTask":
        """Replace the stored payload, returning self for chaining."""
        if payload != self.payload:
            self.add_change("payload", self.payload, payload)
            self.payload = payload
        return self


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
