"""
Pyffice Projects Ports - External format converters for project data.
"""
from pyffice.projects.projects import PyfficeProject
from pyffice.ports.ports import PyfficePort


class MSProjectPort(PyfficePort):
    """Port for Microsoft Project (.mpp) format."""

    def read(self, file_path: str) -> PyfficeProject:
        """Read MS Project file and convert to PyfficeProject."""
        pass

    def write(self, project: PyfficeProject, file_path: str) -> None:
        """Write PyfficeProject to MS Project format."""
        pass


class GanttPort(PyfficePort):
    """Port for Gantt chart format."""

    def read(self, file_path: str) -> PyfficeProject:
        """Read Gantt file and convert to PyfficeProject."""
        pass

    def write(self, project: PyfficeProject, file_path: str) -> None:
        """Write PyfficeProject to Gantt format."""
        pass


class JSONProjectPort(PyfficePort):
    """Port for JSON project format."""

    def read(self, file_path: str) -> PyfficeProject:
        """Read JSON file and convert to PyfficeProject."""
        pass

    def write(self, project: PyfficeProject, file_path: str) -> None:
        """Write PyfficeProject to JSON format."""
        pass


class XMLProjectPort(PyfficePort):
    """Port for XML project format."""

    def read(self, file_path: str) -> PyfficeProject:
        """Read XML file and convert to PyfficeProject."""
        pass

    def write(self, project: PyfficeProject, file_path: str) -> None:
        """Write PyfficeProject to XML format."""
        pass
