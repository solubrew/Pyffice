# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Database Ports Module
	description: >
		External database format ports - converts all external database formats to/from
		PyfficeDatabase. Includes SQL, NoSQL, GraphDB, SQLite and other formats.
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
import sqlite3

# ======================================Solutions Brewer Library Modules==============================================||
from pyffice.databases.databases import PyfficeDatabaseConnection, PyfficeDatabaseManager
from pyffice.document import PyfficeDocument


# ====================================================================================================================||


class DatabasePort(ABC):
    """Abstract base class for database format ports"""
    
    EXTENSIONS: set = set()
    
    @abstractmethod
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import database file to PyfficeDatabaseConnection"""
        pass
    
    @abstractmethod
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str) -> None:
        """Export PyfficeDatabaseConnection to database file format"""
        pass


class SQLitePort(DatabasePort):
    """SQLite database format port"""
    
    EXTENSIONS = {'.sqlite', '.sqlite3', '.db', '.SQLITE', '.SQLITE3', '.DB'}
    
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import SQLite to PyfficeDatabaseConnection"""
        path = Path(file_path)
        
        conn = sqlite3.connect(str(path))
        cursor = conn.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        database = PyfficeDatabaseConnection(str(path))
        database.create_new_document(path.stem)
        
        database.document['tables'] = tables
        database.document['source_format'] = 'sqlite'
        
        # Get schema for each table
        schema = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = [{'name': row[1], 'type': row[2]} for row in cursor.fetchall()]
            schema[table] = columns
        
        database.document['schema'] = schema
        conn.close()
        
        return database
    
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str) -> None:
        """Export PyfficeDatabaseConnection to SQLite"""
        path = Path(file_path)
        
        schema = database.document.get('schema', {})
        
        conn = sqlite3.connect(str(path))
        cursor = conn.cursor()
        
        # Create tables based on schema
        for table_name, columns in schema.items():
            col_defs = ', '.join([f"{col['name']} {col['type']}" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs});")
        
        conn.commit()
        conn.close()


class SQLPort(DatabasePort):
    """SQL dump file format port"""
    
    EXTENSIONS = {'.sql', '.SQL'}
    
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import SQL dump to PyfficeDatabaseConnection"""
        path = Path(file_path)
        
        database = PyfficeDatabaseConnection(str(path))
        database.create_new_document(path.stem)
        
        with open(path, 'r') as f:
            sql_content = f.read()
        
        database.document['sql_content'] = sql_content
        database.document['source_format'] = 'sql'
        
        return database
    
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str) -> None:
        """Export PyfficeDatabaseConnection to SQL dump"""
        path = Path(file_path)
        
        sql_content = database.document.get('sql_content', '')
        with open(path, 'w') as f:
            f.write(sql_content)


class JSONDBPort(DatabasePort):
    """JSON database format port"""
    
    EXTENSIONS = {'.json', '.JSON'}
    
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import JSON database to PyfficeDatabaseConnection"""
        import json
        
        path = Path(file_path)
        
        database = PyfficeDatabaseConnection(str(path))
        database.create_new_document(path.stem)
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        database.document['data'] = data
        database.document['source_format'] = 'json'
        
        return database
    
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str) -> None:
        """Export PyfficeDatabaseConnection to JSON"""
        import json
        
        path = Path(file_path)
        
        data = database.document.get('data', {})
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)


class CSVDBPort(DatabasePort):
    """CSV database format port"""
    
    EXTENSIONS = {'.csv', '.CSV'}
    
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import CSV database to PyfficeDatabaseConnection"""
        from pandas import read_csv
        
        path = Path(file_path)
        
        database = PyfficeDatabaseConnection(str(path))
        database.create_new_document(path.stem)
        
        df = read_csv(path)
        
        database.document['data'] = df.to_dict()
        database.document['tables'] = [path.stem]
        database.document['source_format'] = 'csv'
        
        return database
    
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str) -> None:
        """Export PyfficeDatabaseConnection to CSV"""
        from pandas import DataFrame
        
        path = Path(file_path)
        
        data = database.document.get('data', {})
        df = DataFrame(data)
        
        df.to_csv(path, index=False)


class DatabasePortsManager:
    """Manages all database format ports and conversions"""
    
    def __init__(self):
        self.ports: Dict[str, DatabasePort] = {}
        self._register_default_ports()
    
    def _register_default_ports(self):
        """Register all default database ports"""
        self.ports['sqlite'] = SQLitePort()
        self.ports['sqlite3'] = SQLitePort()
        self.ports['db'] = SQLitePort()
        self.ports['sql'] = SQLPort()
        self.ports['json'] = JSONDBPort()
        self.ports['csv'] = CSVDBPort()
    
    def register_port(self, format_name: str, port: DatabasePort) -> None:
        """Register a new database format port"""
        self.ports[format_name] = port
    
    def get_port(self, format_name: str) -> Optional[DatabasePort]:
        """Get port for a specific format"""
        return self.ports.get(format_name.lower())
    
    def import_file(self, file_path: str) -> PyfficeDatabaseConnection:
        """Import any supported database file to PyfficeDatabaseConnection"""
        path = Path(file_path)
        ext = path.suffix.lower()
        
        for port in self.ports.values():
            if ext in port.EXTENSIONS:
                return port.import_file(str(path))
        
        raise ValueError(f"Unsupported database format: {ext}")
    
    def export_file(self, database: PyfficeDatabaseConnection, file_path: str, format_name: str = None) -> None:
        """Export PyfficeDatabaseConnection to specified format"""
        path = Path(file_path)
        
        if format_name is None:
            format_name = path.suffix.lower().lstrip('.')
        
        port = self.ports.get(format_name.lower())
        if port is None:
            raise ValueError(f"Unsupported database format: {format_name}")
        
        port.export_file(database, str(path))
    
    def convert(self, input_path: str, output_path: str) -> PyfficeDatabaseConnection:
        """Convert between database formats"""
        db = self.import_file(input_path)
        self.export_file(db, output_path)
        return db
    
    def get_supported_formats(self) -> List[str]:
        """Get list of supported format extensions"""
        formats = set()
        for port in self.ports.values():
            formats.update(port.EXTENSIONS)
        return sorted(list(formats))


# Global port manager instance
_port_manager = None

def get_ports_manager() -> DatabasePortsManager:
    """Get global database ports manager instance"""
    global _port_manager
    if _port_manager is None:
        _port_manager = DatabasePortsManager()
    return _port_manager


def import_database(file_path: str) -> PyfficeDatabaseConnection:
    """Convenience function to import database file"""
    return get_ports_manager().import_file(file_path)


def export_database(database: PyfficeDatabaseConnection, file_path: str) -> None:
    """Convenience function to export database file"""
    get_ports_manager().export_file(database, file_path)


def convert_database(input_path: str, output_path: str) -> PyfficeDatabaseConnection:
    """Convenience function to convert between database formats"""
    return get_ports_manager().convert(input_path, output_path)


# ====================================================================================================================||
