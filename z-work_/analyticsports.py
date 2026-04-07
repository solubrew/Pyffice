"""
Pyffice Analytics Ports - Import/Export converters for analytics formats.
"""

from pyffice.analytics.sources import PyfficeAnalytics
from pyffice.items.items import PyfficeTable


class JSONPort:
    """Port for JSON analytics data."""
    
    @staticmethod
    def to_pyffice(data: dict) -> PyfficeAnalytics:
        return PyfficeAnalytics(data=data)
    
    @staticmethod
    def from_pyffice(analytics: PyfficeAnalytics) -> dict:
        return analytics.to_dict()


class CSVPort:
    """Port for CSV analytics data."""
    
    @staticmethod
    def to_pyffice(csv_data: str) -> PyfficeAnalytics:
        lines = csv_data.strip().split('\n')
        if len(lines) < 2:
            return PyfficeAnalytics(data={})
        headers = lines[0].split(',')
        data = []
        for line in lines[1:]:
            values = line.split(',')
            data.append(dict(zip(headers, values)))
        return PyfficeAnalytics(data={'rows': data})
    
    @staticmethod
    def from_pyffice(analytics: PyfficeAnalytics) -> str:
        data = analytics.to_dict()
        if not data or 'rows' not in data:
            return ""
        rows = data['rows']
        if not rows:
            return ""
        headers = list(rows[0].keys())
        lines = [','.join(headers)]
        for row in rows:
            lines.append(','.join(str(row.get(h, '')) for h in headers))
        return '\n'.join(lines)


class ParquetPort:
    """Port for Parquet analytics data."""
    
    @staticmethod
    def to_pyffice(parquet_data: bytes) -> PyfficeAnalytics:
        return PyfficeAnalytics(data={'format': 'parquet', 'size': len(parquet_data)})
    
    @staticmethod
    def from_pyffice(analytics: PyfficeAnalytics) -> bytes:
        return b''


class ExcelAnalyticsPort:
    """Port for Excel analytics workbooks."""
    
    @staticmethod
    def to_pyffice(excel_data: bytes) -> PyfficeAnalytics:
        return PyfficeAnalytics(data={'format': 'xlsx', 'size': len(excel_data)})
    
    @staticmethod
    def from_pyffice(analytics: PyfficeAnalytics) -> bytes:
        return b''


class PortRegistry:
    """Registry of all analytics ports."""
    
    PORTS = {
        'json': JSONPort,
        'csv': CSVPort,
        'parquet': ParquetPort,
        'xlsx': ExcelAnalyticsPort,
    }
    
    @classmethod
    def get_port(cls, format: str):
        return cls.PORTS.get(format.lower())
    
    @classmethod
    def list_formats(cls):
        return list(cls.PORTS.keys())
