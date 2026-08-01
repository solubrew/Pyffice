"""
Pyffice Data Module — re-export bridge.

T-NEW-069: The CSV/JSON handlers have moved to pyffice.ports
(csv_handler.py, json_handler.py). The remaining files in this
directory (base.py, yaml.py, xml.py, data/data/) have been deleted as
dead code with zero callers.

This module is kept as a backwards-compatibility re-export bridge:
any code that still does `from pyffice.data import PyfficeCSV` or
similar will continue to work via the lazy proxy below. The prefer
path is now `from pyffice.ports import PyfficeCSV` (and likewise
for the JSON handler).
"""

# Lazy __getattr__ proxy to the new ports handlers (PEP 562).
# Preserves the historical `pyffice.data` import path while the
# canonical location moves to pyffice.ports.
_LAZY_EXPORTS = {
    "PyfficeCSV": ("pyffice.ports.csv_handler", "PyfficeCSV"),
    "PyfficeJSON": ("pyffice.ports.json_handler", "PyfficeJSON"),
    "csv_read": ("pyffice.ports.csv_handler", "read"),
    "csv_write": ("pyffice.ports.csv_handler", "write"),
    "csv_read_rows": ("pyffice.ports.csv_handler", "read_rows"),
    "csv_write_rows": ("pyffice.ports.csv_handler", "write_rows"),
    "csv_append": ("pyffice.ports.csv_handler", "append"),
    "csv_append_row": ("pyffice.ports.csv_handler", "append_row"),
    "json_read": ("pyffice.ports.json_handler", "read"),
    "json_write": ("pyffice.ports.json_handler", "write"),
    "json_parse": ("pyffice.ports.json_handler", "parse"),
    "json_to_string": ("pyffice.ports.json_handler", "to_string"),
    # Legacy aliases kept for transitional callers; remove once
    # any third-party docs reference these names.
    "read_rows": ("pyffice.ports.csv_handler", "read_rows"),
    "write_rows": ("pyffice.ports.csv_handler", "write_rows"),
    "append": ("pyffice.ports.csv_handler", "append"),
    "append_row": ("pyffice.ports.csv_handler", "append_row"),
    "create": ("pyffice.ports.json_handler", "create"),
    "add_child": ("pyffice.ports.json_handler", "add_child"),
}


def __getattr__(name: str):
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache
        return value
    raise AttributeError(
        "module 'pyffice.data' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))


__all__ = [
    "PyfficeCSV",
    "PyfficeJSON",
    "csv_read", "csv_write", "csv_read_rows", "csv_write_rows",
    "csv_append", "csv_append_row",
    "json_read", "json_write", "json_parse", "json_to_string",
    # Legacy aliases
    "read_rows", "write_rows", "append", "append_row",
    "create", "add_child",
]
