# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Spreadsheet Ports Module
	description: >
		External spreadsheet format ports - converts all external spreadsheet formats to/from
		PyfficeSpreadSheet. Includes XLSX, XLS, CSV, ODS, TSV and other formats.
	version: 0.0.1.0.1.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from typing import Dict, Any, Optional, List
from pathlib import Path
from abc import ABC, abstractmethod

# ======================================3rd Party Library Modules=====================================================||
from pandas import read_csv, read_excel, DataFrame, ExcelWriter

# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.spreadsheet.spreadsheet import PyfficeSpreadSheet
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class SpreadsheetPort(ABC):
    """Abstract base class for spreadsheet format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import spreadsheet file to PyfficeSpreadSheet"""
        pass
    
    @abstractmethod
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to spreadsheet file format"""
        pass


class XLSXPort(SpreadsheetPort):
    """Microsoft Excel XLSX format port"""
    
    EXTENSIONS = {'.xlsx', '.XLSX'}
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import XLSX to PyfficeSpreadSheet"""
        path = Path(file_path)
        
        # Read all sheets
        xls = ExcelFile(str(path))
        sheet_names = xls.sheet_names
        
        # Create PyfficeSpreadSheet (single sheet - workbook handled separately)
        spreadsheet = PyfficeSpreadSheet()
        spreadsheet.create_new_document(path.stem)
        
        # Read first sheet as primary data
        df = read_excel(path, sheet_name=0, engine='openpyxl')
        
        # Convert DataFrame to cells dict
        cells = {}
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                col = chr(65 + col_idx)  # A, B, C, ...
                row_num = idx + 1
                address = f"{col}|{row_num}"
                cells[address] = value
        
        spreadsheet.document['cells'] = cells
        spreadsheet.document['data'] = df.to_dict()
        spreadsheet.document['sheets'] = sheet_names
        spreadsheet.document['source_format'] = 'xlsx'
        
        return spreadsheet
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to XLSX"""
        path = Path(file_path)
        
        cells = spreadsheet.document.get('cells', {})
        
        # Convert cells dict to DataFrame
        data = []
        if cells:
            max_row = max(int(addr.split('|')[1]) for addr in cells.keys())
            max_col = max(ord(addr.split('|')[0]) for addr in cells.keys()) - 64
            
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    col_letter = chr(64 + col)
                    address = f"{col_letter}|{row}"
                    row_data.append(cells.get(address, None))
                data.append(row_data)
        
        df = DataFrame(data)
        
        with ExcelWriter(str(path), engine='openpyxl') as writer:
            df.to_excel(writer, index=False, header=False)


class XlsPort(SpreadsheetPort):
    """Microsoft Excel XLS (legacy) format port"""
    
    EXTENSIONS = {'.xls', '.XLS'}
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import XLS to PyfficeSpreadSheet"""
        path = Path(file_path)
        
        spreadsheet = PyfficeSpreadSheet()
        spreadsheet.create_new_document(path.stem)
        
        df = read_excel(path, sheet_name=0, engine='xlrd')
        
        cells = {}
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                col = chr(65 + col_idx)
                row_num = idx + 1
                address = f"{col}|{row_num}"
                cells[address] = value
        
        spreadsheet.document['cells'] = cells
        spreadsheet.document['data'] = df.to_dict()
        spreadsheet.document['source_format'] = 'xls'
        
        return spreadsheet
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to XLS"""
        path = Path(file_path)
        
        cells = spreadsheet.document.get('cells', {})
        
        data = []
        if cells:
            max_row = max(int(addr.split('|')[1]) for addr in cells.keys())
            max_col = max(ord(addr.split('|')[0]) for addr in cells.keys()) - 64
            
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    col_letter = chr(64 + col)
                    address = f"{col_letter}|{row}"
                    row_data.append(cells.get(address, None))
                data.append(row_data)
        
        df = DataFrame(data)
        
        with ExcelWriter(str(path), engine='xlwt') as writer:
            df.to_excel(writer, index=False, header=False)


class CSVPort(SpreadsheetPort):
    """Comma-Separated Values format port"""
    
    EXTENSIONS = {'.csv', '.CSV'}
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import CSV to PyfficeSpreadSheet"""
        path = Path(file_path)
        
        spreadsheet = PyfficeSpreadSheet()
        spreadsheet.create_new_document(path.stem)
        
        df = read_csv(path)
        
        cells = {}
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                col = chr(65 + col_idx)
                row_num = idx + 1
                address = f"{col}|{row_num}"
                cells[address] = value
        
        spreadsheet.document['cells'] = cells
        spreadsheet.document['data'] = df.to_dict()
        spreadsheet.document['source_format'] = 'csv'
        
        return spreadsheet
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to CSV"""
        path = Path(file_path)
        
        cells = spreadsheet.document.get('cells', {})
        
        data = []
        if cells:
            max_row = max(int(addr.split('|')[1]) for addr in cells.keys())
            max_col = max(ord(addr.split('|')[0]) for addr in cells.keys()) - 64
            
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    col_letter = chr(64 + col)
                    address = f"{col_letter}|{row}"
                    row_data.append(cells.get(address, None))
                data.append(row_data)
        
        df = DataFrame(data)
        df.to_csv(path, index=False, header=False)


class ODSPort(SpreadsheetPort):
    """OpenDocument Spreadsheet format port"""
    
    EXTENSIONS = {'.ods', '.ODS'}
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import ODS to PyfficeSpreadSheet"""
        path = Path(file_path)
        
        spreadsheet = PyfficeSpreadSheet()
        spreadsheet.create_new_document(path.stem)
        
        df = read_excel(path, sheet_name=0, engine='odf')
        
        cells = {}
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                col = chr(65 + col_idx)
                row_num = idx + 1
                address = f"{col}|{row_num}"
                cells[address] = value
        
        spreadsheet.document['cells'] = cells
        spreadsheet.document['data'] = df.to_dict()
        spreadsheet.document['source_format'] = 'ods'
        
        return spreadsheet
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to ODS"""
        path = Path(file_path)
        
        cells = spreadsheet.document.get('cells', {})
        
        data = []
        if cells:
            max_row = max(int(addr.split('|')[1]) for addr in cells.keys())
            max_col = max(ord(addr.split('|')[0]) for addr in cells.keys()) - 64
            
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    col_letter = chr(64 + col)
                    address = f"{col_letter}|{row}"
                    row_data.append(cells.get(address, None))
                data.append(row_data)
        
        df = DataFrame(data)
        
        with ExcelWriter(str(path), engine='odf') as writer:
            df.to_excel(writer, index=False, header=False)


class TSVPort(SpreadsheetPort):
    """Tab-Separated Values format port"""
    
    EXTENSIONS = {'.tsv', '.TSV'}
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import TSV to PyfficeSpreadSheet"""
        path = Path(file_path)
        
        spreadsheet = PyfficeSpreadSheet()
        spreadsheet.create_new_document(path.stem)
        
        df = read_csv(path, sep='\t')
        
        cells = {}
        for idx, row in df.iterrows():
            for col_idx, value in enumerate(row):
                col = chr(65 + col_idx)
                row_num = idx + 1
                address = f"{col}|{row_num}"
                cells[address] = value
        
        spreadsheet.document['cells'] = cells
        spreadsheet.document['data'] = df.to_dict()
        spreadsheet.document['source_format'] = 'tsv'
        
        return spreadsheet
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
        """Export PyfficeSpreadSheet to TSV"""
        path = Path(file_path)
        
        cells = spreadsheet.document.get('cells', {})
        
        data = []
        if cells:
            max_row = max(int(addr.split('|')[1]) for addr in cells.keys())
            max_col = max(ord(addr.split('|')[0]) for addr in cells.keys()) - 64
            
            for row in range(1, max_row + 1):
                row_data = []
                for col in range(1, max_col + 1):
                    col_letter = chr(64 + col)
                    address = f"{col_letter}|{row}"
                    row_data.append(cells.get(address, None))
                data.append(row_data)
        
        df = DataFrame(data)
        df.to_csv(path, sep='\t', index=False, header=False)


class SpreadsheetPortsManager:
    """Manages all spreadsheet format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, SpreadsheetPort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default spreadsheet ports"""
        self.ports['xlsx'] = XLSXPort()
        self.ports['xls'] = XlsPort()
        self.ports['csv'] = CSVPort()
        self.ports['ods'] = ODSPort()
        self.ports['tsv'] = TSVPort()
    
    def register_port(self, format_name: str, port: SpreadsheetPort) -> None:
        """Register a new spreadsheet format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[SpreadsheetPort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeSpreadSheet:
        """Import any supported spreadsheet file to PyfficeSpreadSheet"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported spreadsheet format: {ext}")
    
    def export_file(self, spreadsheet: PyfficeSpreadSheet, file_path: str, format_name: str = None) -> None:
        """Export PyfficeSpreadSheet to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported spreadsheet format: {format_name}")
        
        port.export_file(spreadsheet, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeSpreadSheet:
        """Convert between spreadsheet formats"""
        sheet = self.import_file(input_path)
        self.export_file(sheet, output_path)
        return sheet
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> SpreadsheetPortsManager:
    """Get global spreadsheet ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = SpreadsheetPortsManager()
    return _port_manager


def import_spreadsheet(file_path: str) -> PyfficeSpreadSheet:
    """Convenience function to import spreadsheet file"""
    return get_ports_manager().import_file(file_path)


def export_spreadsheet(spreadsheet: PyfficeSpreadSheet, file_path: str) -> None:
    """Convenience function to export spreadsheet file"""
    get_ports_manager().export_file(spreadsheet, file_path)


def convert_spreadsheet(input_path: str, output_path: str) -> PyfficeSpreadSheet:
    """Convenience function to convert between spreadsheet formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
