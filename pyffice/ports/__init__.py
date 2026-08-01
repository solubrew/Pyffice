"""
Ports module for pyffice.
"""

# Lazy __getattr__ proxy to break circular imports when
# subpkg modules are partially initialized (PEP 562).
_LAZY_EXPORTS = {
    # T-NEW-070: Google Workspace ports (built out from stubs)
    "PyfficePortGoogleDocs": ("pyffice.ports.gports", "PyfficePortGoogleDocs"),
    "PyfficePortGoogleForms": ("pyffice.ports.gports", "PyfficePortGoogleForms"),
    "PyfficePortGoogleSheets": ("pyffice.ports.gports", "PyfficePortGoogleSheets"),
    "PyfficePortGoogleSlides": ("pyffice.ports.gports", "PyfficePortGoogleSlides"),
    "PyfficePortExcel": ("pyffice.ports.msports", "PyfficePortExcel"),
    "PyfficePortWord": ("pyffice.ports.msports", "PyfficePortWord"),
    "read_docx_tables": ("pyffice.ports.msports", "read_docx_tables"),
    "PyfficePort": ("pyffice.ports.ports", "PyfficePort"),
    "PyfficePortCherryTree": ("pyffice.ports.ports", "PyfficePortCherryTree"),
    "PyfficePortOffice": ("pyffice.ports.ports", "PyfficePortOffice"),
    "PyfficePortCSV": ("pyffice.ports.ports", "PyfficePortCSV"),
    "PyfficePortDia": ("pyffice.ports.ports", "PyfficePortDia"),
    "PyfficePortFileSystem": ("pyffice.ports.ports", "PyfficePortFileSystem"),
    "PyfficePortImage": ("pyffice.ports.ports", "PyfficePortImage"),
    "PyfficePortJupyter": ("pyffice.ports.ports", "PyfficePortJupyter"),
    "PyfficePortText": ("pyffice.ports.ports", "PyfficePortText"),
    "PyfficePortWebSession": ("pyffice.ports.ports", "PyfficePortWebSession"),
    # T-NEW-069: file format handlers migrated from pyffice/data/
    "PyfficeCSV": ("pyffice.ports.csv_handler", "PyfficeCSV"),
    "PyfficeJSON": ("pyffice.ports.json_handler", "PyfficeJSON"),
    # T-NEW-070: cloud storage ports
    "PyfficeCloudPort": ("pyffice.ports.cloud_ports", "PyfficeCloudPort"),
    "PyfficePortGoogleDrive": ("pyffice.ports.cloud_ports", "PyfficePortGoogleDrive"),
    "PyfficePortDropbox": ("pyffice.ports.cloud_ports", "PyfficePortDropbox"),
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
}

def __getattr__(name: str) -> None:
    if name in _LAZY_EXPORTS:
        mod_path, attr = _LAZY_EXPORTS[name]
        mod = __import__(mod_path, fromlist=[attr])
        value = getattr(mod, attr)
        globals()[name] = value  # cache for next access
        return value
    raise AttributeError(
        "module 'pyffice.ports' has no attribute " + repr(name)
    )


def __dir__():
    return sorted(list(globals().keys()) + list(_LAZY_EXPORTS.keys()))

__all__ = [
    "PyfficePortGoogleDocs",
    "PyfficePortGoogleForms",
    "PyfficePortGoogleSheets",
    "PyfficePortGoogleSlides",
    "PyfficePortExcel",
    "PyfficePortWord",
    "read_docx_tables",
    "PyfficePort",
    "PyfficePortCherryTree",
    "PyfficePortOffice",
    "PyfficePortCSV",
    "PyfficePortDia",
    "PyfficePortFileSystem",
    "PyfficePortImage",
    "PyfficePortJupyter",
    "PyfficePortText",
    "PyfficePortWebSession",
    # T-NEW-069: file format handlers (migrated from pyffice/data/)
    "PyfficeCSV",
    "PyfficeJSON",
    # T-NEW-070: cloud storage ports
    "PyfficeCloudPort",
    "PyfficePortGoogleDrive",
    "PyfficePortDropbox",
    "csv_read",
    "csv_write",
    "csv_read_rows",
    "csv_write_rows",
    "csv_append",
    "csv_append_row",
    "json_read",
    "json_write",
    "json_parse",
    "json_to_string",
]
