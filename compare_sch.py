import sqlite3
import json
from typing import Dict, List, Tuple

class SchemaComparer:
    """
    一個用於比對 .sch 檔案和 SQLite 資料庫中結構定義的類別。
    A class to compare schema definitions between a .sch file and a SQLite database.
    """
    def __init__(self, schema_file: str, db_path: str = "schema.db"):
        """
        初始化 SchemaComparer。
        Initializes the SchemaComparer.

        :param schema_file: .sch 結構檔案的路徑。
        :param db_path: SQLite 資料庫檔案的路徑。
        """
        self.schema_file = schema_file
        self.db_path = db_path
        self.differences: List[Dict] = []  # 用於儲存差異的列表
        
    def parse_schema_line(self, line: str) -> Tuple[str, str, str, str, str]:
        """解析 .sch 檔案中的單一行。 (Parse a single line from schema file)"""
        parts = line.strip().split('^')
        if len(parts) != 6:
            return None
        table_name, column_name, type_id, size, position, _ = parts
        return table_name, column_name, type_id, size, position
        
    def get_db_column(self, table_name: str, column_name: str) -> Tuple[str, str, str]:
        """從資料庫中獲取指定欄位的資訊。 (Get column info from database)"""
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
        """比較 .sch 檔案和資料庫之間的結構差異。 (Compare schema file with database)"""
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
                    # 欄位在資料庫中不存在 (Column not found in database)
                    self._record_difference(table_name, column_name, {
                        "status": "missing_in_db",
                        "file_info": {"type": type_id, "size": size, "position": position},
                        "db_info": None
                    })
                    continue
                
                db_type, db_size, db_position = db_info
                
                # 檢查屬性是否有差異 (Check for differences)
                if db_type != type_id or db_size != size or db_position != position:
                    self._record_difference(table_name, column_name, {
                        "status": "different",
                        "file_info": {"type": type_id, "size": size, "position": position},
                        "db_info": {"type": db_type, "size": db_size, "position": db_position}
                    })
                    
    def _record_difference(self, table_name: str, column_name: str, diff_info: Dict):
        """將發現的差異記錄到列表中。 (Record a difference in the differences list)"""
        record = {
            "status": diff_info["status"],
            "table": table_name,
            "column": column_name,
            "file_info": diff_info["file_info"],
            "db_info": diff_info["db_info"]
        }
        self.differences.append(record)
        
    def export_json(self, output_file: str):
        """將差異匯出為 JSON 檔案。 (Export differences to JSON file)"""
        if not self.differences:
            print("未發現差異。 (No differences found)")
            return
            
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.differences, f, indent=2, ensure_ascii=False)
            
        print(f"差異已匯出至 (Differences exported to) {output_file}")

    def print_differences(self):
        """在主控台印出差異。 (Print differences to console)"""
        if not self.differences:
            print("未發現差異。 (No differences found)")
            return
            
        for diff in self.differences:
            print(f"\n資料表 (Table): {diff['table']}")
            print("-" * 80)
            print(f"欄位 (Column): {diff['column']}")
            
            if diff['status'] == 'missing_in_db':
                print("狀態 (Status): 資料庫中缺少 (Missing in database)")
                print("檔案中的值 (File values):", diff['file_info'])
            else:
                print("狀態 (Status): 值不符 (Different values)")
                print("檔案中的值 (File values):", diff['file_info'])
                print("資料庫中的值 (DB values):", diff['db_info'])
            print("-" * 40)

def main():
    """
    主函式，用於執行比對。
    Main function to run comparison.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Compare schema file with database. (比對 .sch 檔案與資料庫的結構)')
    parser.add_argument('schema_file', help='Path to schema file (e.g., ds.sch). (.sch 檔案的路徑)')
    parser.add_argument('--db', default='schema.db', help='SQLite database file name (default: schema.db). (SQLite 資料庫檔案名稱)')
    parser.add_argument('--json', help='Export differences to JSON file. (將差異匯出至 JSON 檔案)')
    
    args = parser.parse_args()
    
    comparer = SchemaComparer(args.schema_file, args.db)
    comparer.compare_schemas()
    
    if args.json:
        comparer.export_json(args.json)
    else:
        comparer.print_differences()

if __name__ == "__main__":
    main()
