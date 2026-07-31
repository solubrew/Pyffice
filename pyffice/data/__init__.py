"""
Pyffice Data Module

Data file handling: CSV, JSON, XML, YAML, and related formats.

T-NEW-051 / T-NEW-052: many of these modules have pre-existing
broken transitive imports (pyffice.data.json expects a
PyfficeDataMixin that doesn't exist in base.py, etc.). Each
import below is wrapped in try/except so one broken submodule
doesn't crash the whole package init.
"""

from pyffice.data.base import PyfficeDataBase

try:
    from pyffice.data.csv import (
        PyfficeCSV,
        read as csv_read,
        write as csv_write,
        read_rows,
        write_rows,
        append,
        append_row,
    )
except ImportError:
    PyfficeCSV = csv_read = csv_write = read_rows = write_rows = append = append_row = None

try:
    from pyffice.data.json import (
        PyfficeJSON,
        parse as json_parse,
        read as json_read,
        write as json_write,
        create,
        add_child,
    )
except ImportError:
    PyfficeJSON = json_parse = json_read = json_write = create = add_child = None

try:
    from pyffice.data.yaml import PyfficeYAML
except ImportError:
    PyfficeYAML = None

__all__ = [
    "PyfficeCSV",
    "PyfficeJSON",
    "PyfficeYAML",
    "PyfficeDataBase",
    "csv_read",
    "csv_write",
    "read_rows",
    "write_rows",
    "append",
    "append_row",
    "json_parse",
    "json_read",
    "json_write",
    "create",
    "add_child",
]
