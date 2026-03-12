"""
Pyffice Matrix Ports - External format converters for matrix data.
"""
from pyffice.matrix.matrix import PyfficeMatrix
from pyffice.ports.ports import PyfficePort


class NumPyPort(PyfficePort):
    """Port for NumPy (.npy, .npz) format."""

    def read(self, file_path: str) -> PyfficeMatrix:
        """Read NumPy file and convert to PyfficeMatrix."""
        pass

    def write(self, matrix: PyfficeMatrix, file_path: str) -> None:
        """Write PyfficeMatrix to NumPy file."""
        pass


class MatlabPort(PyfficePort):
    """Port for MATLAB (.mat) format."""

    def read(self, file_path: str) -> PyfficeMatrix:
        """Read MATLAB file and convert to PyfficeMatrix."""
        pass

    def write(self, matrix: PyfficeMatrix, file_path: str) -> None:
        """Write PyfficeMatrix to MATLAB file."""
        pass


class CSVPort(PyfficePort):
    """Port for CSV format."""

    def read(self, file_path: str) -> PyfficeMatrix:
        """Read CSV file and convert to PyfficeMatrix."""
        pass

    def write(self, matrix: PyfficeMatrix, file_path: str) -> None:
        """Write PyfficeMatrix to CSV file."""
        pass


class HDF5Port(PyfficePort):
    """Port for HDF5 (.h5, .hdf5) format."""

    def read(self, file_path: str) -> PyfficeMatrix:
        """Read HDF5 file and convert to PyfficeMatrix."""
        pass

    def write(self, matrix: PyfficeMatrix, file_path: str) -> None:
        """Write PyfficeMatrix to HDF5 file."""
        pass
