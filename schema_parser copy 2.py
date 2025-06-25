import re
import json
import sqlite3
from typing import Dict, List, Tuple

class SchemaParser:
    def __init__(self, file_path: str, db_path: str = "schema.db"):
        self.file_path = file_path
        self.tables: Dict[str, List[Tuple[str, str, str, str, str]]] = {}
        self.db_path = db_path
        
    def parse(self):
        """Parse the schema file and store table definitions"""
        with open(self.file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                    
                # Parse line format: table^column^type^size^position^
                parts = line.strip().split('^')
                if len(parts) != 6:
                    continue
                    
                table, column, type_id, size, position, _ = parts
                
                if table not in self.tables:
                    self.tables[table] = []
                    
                self.tables[table].append((column, type_id, size, position))

    def get_table_definition(self, table_name: str) -> List[Tuple[str, str, str, str]]:
        """Get column definitions for a specific table"""
        return self.tables.get(table_name, [])
        
    def get_all_tables(self) -> List[str]:
        """Get list of all table names"""
        return sorted(list(self.tables.keys()))
        
    def export_json(self, output_file: str):
        """Export schema to JSON format"""
        schema_dict = {}
        for table, columns in self.tables.items():
            schema_dict[table] = [
                {
                    "column": col[0],
                    "type": col[1],
                    "size": col[2],
                    "position": col[3]
                }
                for col in columns
            ]
            
        with open(output_file, 'w') as f:
            json.dump(schema_dict, f, indent=2)

    def print_table_info(self, table_name: str = None):
        """Print table structure information"""
        if table_name and table_name in self.tables:
            self._print_single_table(table_name)
        elif not table_name:
            for tbl in sorted(self.tables.keys()):
                self._print_single_table(tbl)
                print()
        else:
            print(f"Table {table_name} not found")

    def _print_single_table(self, table_name: str):
        """Helper method to print a single table's structure"""
        print(f"Table: {table_name}")
        print("-" * 80)
        print("Column".ljust(30), "Type".ljust(10), "Size".ljust(10), "Position")
        print("-" * 80)
        
        for col, type_id, size, pos in self.tables[table_name]:
            print(f"{col.ljust(30)} {type_id.ljust(10)} {size.ljust(10)} {pos}")

    def create_db_schema(self):
        """Create SQLite database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_name TEXT UNIQUE NOT NULL
        )
        ''')
        
        # Create columns table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS columns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_id INTEGER NOT NULL,
            column_name TEXT NOT NULL,
            type_id TEXT NOT NULL,
            size TEXT NOT NULL,
            position TEXT NOT NULL,
            FOREIGN KEY (table_id) REFERENCES tables (id),
            UNIQUE(table_id, column_name)
        )
        ''')
        
        conn.commit()
        conn.close()

    def export_to_sqlite(self):
        """Export schema to SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create schema if not exists
        self.create_db_schema()
        
        # Clear existing data
        cursor.execute('DELETE FROM columns')
        cursor.execute('DELETE FROM tables')
        
        try:
            # Insert tables and their columns
            for table_name, columns in self.tables.items():
                cursor.execute('INSERT INTO tables (table_name) VALUES (?)', (table_name,))
                table_id = cursor.lastrowid
                
                # Insert columns for this table
                column_data = [
                    (table_id, col[0], col[1], col[2], col[3])
                    for col in columns
                ]
                cursor.executemany(
                    'INSERT INTO columns (table_id, column_name, type_id, size, position) VALUES (?, ?, ?, ?, ?)',
                    column_data
                )
            
            conn.commit()
            print(f"Successfully exported schema to {self.db_path}")
            
        except Exception as e:
            conn.rollback()
            print(f"Error exporting to database: {e}")
            
        finally:
            conn.close()

    def load_from_sqlite(self):
        """Load schema from SQLite database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get all tables and their columns
            cursor.execute('''
                SELECT t.table_name, c.column_name, c.type_id, c.size, c.position
                FROM tables t
                JOIN columns c ON t.id = c.table_id
                ORDER BY t.table_name, c.position
            ''')
            
            self.tables = {}
            for row in cursor.fetchall():
                table_name, column_name, type_id, size, position = row
                if table_name not in self.tables:
                    self.tables[table_name] = []
                self.tables[table_name].append((column_name, type_id, size, position))
                
        finally:
            conn.close()

def main():
    """Main function to demonstrate usage"""
    parser = SchemaParser("/Users/samuel/program/fgldbsch/ds.sch", "schema.db")
    parser.parse()
    
    # Export to SQLite
    parser.export_to_sqlite()
    
    # Test loading from SQLite
    new_parser = SchemaParser("/Users/samuel/program/fgldbsch/ds.sch", "schema.db")
    new_parser.load_from_sqlite()
    
    # Print all tables from loaded data
    new_parser.print_table_info()
    
if __name__ == "__main__":
    main()
