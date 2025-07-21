# Schema Management Tools

Tools for managing and comparing database schema definitions.

## Scripts

### schema_parser.py

Parse and store schema definitions in SQLite database:

```bash
# Basic usage
python schema_parser.py schema_file.sch

# Specify custom database
python schema_parser.py schema_file.sch --db custom.db

# Reset database and save new schema
python schema_parser.py schema_file.sch --reset
```

### compare_sch.py

Compare schema file with database to find differences:

```bash
# Compare schema with database
python compare_sch.py schema_file.sch

# Compare using custom database
python compare_sch.py schema_file.sch --db custom.db
```

Output will show:
- Missing columns in database
- Different column types
- Different column sizes
- Different column positions

Example output:

# Schema Comparison Tool
# 數據庫結構比對工具

A tool to compare table schemas between .sch files and SQLite databases.
一個用於比對 .sch 檔案和 SQLite 資料庫表結構的工具。

## Usage
## 使用方式

Basic comparison:

基本使用
```bash
python schema_parser.py schema_file.sch
```
基本比對：
```bash
python compare_sch.py schema_file.sch --db database.db
```

Export differences to JSON:
匯出差異到 JSON 檔案：
```bash
python compare_sch.py schema_file.sch --json differences.json
```

```bash
python compare_sch.py schema_file.sch --db database.db --json differences.json
```

## JSON Output Format
## JSON 輸出格式

The differences.json file contains an array of differences with the following structure:
differences.json 檔案包含一個差異陣列，結構如下：

```json
{
  "status": "different|missing_in_db",  // 狀態：不同|資料庫中缺少
  "table": "table_name",                // 資料表名稱
  "column": "column_name",              // 欄位名稱
  "file_info": {                        // 檔案中的資訊
    "type": "type_id",                  // 型別
    "size": "size",                     // 大小
    "position": "position"              // 位置
  },
  "db_info": {                          // 資料庫中的資訊
    "type": "type_id",                  // 型別
    "size": "size",                     // 大小
    "position": "position"              // 位置
  }
}
```

Where:
說明：
- `status`: Indicates if column is missing or has different attributes
  表示欄位是否缺少或屬性不同
- `table`: Table name
  資料表名稱
- `column`: Column name
  欄位名稱
- `file_info`: Column attributes from schema file
  來自結構檔案的欄位屬性
- `db_info`: Column attributes from database (null if missing)
  來自資料庫的欄位屬性（如果缺少則為 null）


