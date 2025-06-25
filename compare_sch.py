import sqlite3
import json
from typing import Dict, List, Tuple

class SchemaComparer:
    def __init__(self, schema_file: str, db_path: str = "schema.db"):
        self.schema_file = schema_file
        self.db_path = db_path
        self.differences: List[Dict] = []  # Changed from Dict to List
        
    def parse_schema_line(self, line: str) -> Tuple[str, str, str, str, str]:
        """Parse a single line from schema file"""
        parts = line.strip().split('^')
        if len(parts) != 6:
            return None
        table_name, column_name, type_id, size, position, _ = parts
        return table_name, column_name, type_id, size, position
        
    def get_db_column(self, table_name: str, column_name: str) -> Tuple[str, str, str]:
        """Get column info from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT type_id, size, position 
            FROM schema_def 
            WHERE table_name = ? AND column_name = ?
        ''', (table_name, column_name))
        
        result = cursor.fetchone()
        conn.close()
        
        return result if result else None
        
    def compare_schemas(self):
        """Compare schema file with database"""
        with open(self.schema_file, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                    
                parsed = self.parse_schema_line(line)
                if not parsed:
                    continue
                    
                table_name, column_name, type_id, size, position = parsed
                db_info = self.get_db_column(table_name, column_name)
                
                if not db_info:
                    # Column not found in database
                    self._record_difference(table_name, column_name, {
                        "status": "missing_in_db",
                        "file_info": {"type": type_id, "size": size, "position": position},
                        "db_info": None
                    })
                    continue
                
                db_type, db_size, db_position = db_info
                
                # Check for differences
                if db_type != type_id or db_size != size or db_position != position:
                    self._record_difference(table_name, column_name, {
                        "status": "different",
                        "file_info": {"type": type_id, "size": size, "position": position},
                        "db_info": {"type": db_type, "size": db_size, "position": db_position}
                    })
                    
    def _record_difference(self, table_name: str, column_name: str, diff_info: Dict):
        """Record a difference in the differences list"""
        record = {
            "status": diff_info["status"],
            "table": table_name,
            "column": column_name,
            "file_info": diff_info["file_info"],
            "db_info": diff_info["db_info"]
        }
        self.differences.append(record)
        
    def export_json(self, output_file: str):
        """Export differences to JSON file"""
        if not self.differences:
            print("No differences found")
            return
            
        with open(output_file, 'w') as f:
            json.dump(self.differences, f, indent=2)
            
        print(f"Differences exported to {output_file}")

    def print_differences(self):
        """Print differences to console"""
        if not self.differences:
            print("No differences found")
            return
            
        for diff in self.differences:  # 有格式化的輸出每個差異項目
            print(f"\nTable: {diff['table']}")
            print("-" * 80)
            print(f"Column: {diff['column']}")
            
            if diff['status'] == 'missing_in_db':
                print("Status: Missing in database")
                print("File values:", diff['file_info'])
            else:
                print("Status: Different values")
                print("File values:", diff['file_info'])
                print("DB values:", diff['db_info'])
            print("-" * 40)

def main():
    """Main function to run comparison"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare schema file with database')
    parser.add_argument('schema_file', help='Path to schema file (e.g., ds.sch)')
    parser.add_argument('--db', default='schema.db', help='SQLite database file name (default: schema.db)')
    parser.add_argument('--json', help='Export differences to JSON file')
    
    args = parser.parse_args()
    
    comparer = SchemaComparer(args.schema_file, args.db)
    comparer.compare_schemas()
    
    if args.json:
        comparer.export_json(args.json)
    else:
        comparer.print_differences()

if __name__ == "__main__":
    main()
