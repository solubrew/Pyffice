"""
Pyffice Workflows Ports - External format converters for workflow data.
"""
from pyffice.workflows.workflows import PyfficeWorkflow
from pyffice.ports.ports import PyfficePort


class BPMNPort(PyfficePort):
    """Port for BPMN (.bpmn, .xml) format."""

    def read(self, file_path: str) -> PyfficeWorkflow:
        """Read BPMN file and convert to PyfficeWorkflow."""
        pass

    def write(self, workflow: PyfficeWorkflow, file_path: str) -> None:
        """Write PyfficeWorkflow to BPMN format."""
        pass


class XESPort(PyfficePort):
    """Port for XES (eXtensible Event Stream) format."""

    def read(self, file_path: str) -> PyfficeWorkflow:
        """Read XES file and convert to PyfficeWorkflow."""
        pass

    def write(self, workflow: PyfficeWorkflow, file_path: str) -> None:
        """Write PyfficeWorkflow to XES format."""
        pass


class JSONFlowPort(PyfficePort):
    """Port for JSON workflow format."""

    def read(self, file_path: str) -> PyfficeWorkflow:
        """Read JSON file and convert to PyfficeWorkflow."""
        pass

    def write(self, workflow: PyfficeWorkflow, file_path: str) -> None:
        """Write PyfficeWorkflow to JSON format."""
        pass


class YAMLFlowPort(PyfficePort):
    """Port for YAML workflow format."""

    def read(self, file_path: str) -> PyfficeWorkflow:
        """Read YAML file and convert to PyfficeWorkflow."""
        pass

    def write(self, workflow: PyfficeWorkflow, file_path: str) -> None:
        """Write PyfficeWorkflow to YAML format."""
        pass
