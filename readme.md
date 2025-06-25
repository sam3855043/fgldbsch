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
```

# Schema Comparison Tool

A tool to compare table schemas between .sch files and SQLite databases.

## Usage

Basic comparison:
```bash
python compare_sch.py schema_file.sch --db database.db
```

Export differences to JSON:
```bash
python compare_sch.py schema_file.sch --db database.db --json differences.json
```

## JSON Output Format

The differences.json file contains an array of differences with the following structure:

```json
{
  "status": "different|missing_in_db",
  "table": "table_name",
  "column": "column_name", 
  "file_info": {
    "type": "type_id",
    "size": "size",
    "position": "position"
  },
  "db_info": {
    "type": "type_id",
    "size": "size", 
    "position": "position"
  }
}
```

Where:
- `status`: Indicates if column is missing or has different attributes
- `table`: Table name
- `column`: Column name
- `file_info`: Column attributes from schema file
- `db_info`: Column attributes from database (null if missing)


