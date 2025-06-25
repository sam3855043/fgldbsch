# Schema Management Tools

Tools for managing and comparing database schema definitions.

## Scripts

- `schema_parser.py`: Parse and store schema definitions
- `compare_py.py`: Compare schema files with database
- `search_diff.py`: Search for specific differences in schemas

## Usage

### Schema Parser

Parse schema file and store in SQLite database:

```bash
# Basic usage
python schema_parser.py schema_file.sch

# Specify custom database
python schema_parser.py schema_file.sch --db custom.db

# Reset database and save new schema
python schema_parser.py schema_file.sch --reset
```

### Schema Comparer

Compare schema file with database:

```bash
# Compare schema file with database
python compare_py.py schema_file.sch

# Export differences to JSON
python compare_py.py schema_file.sch --json output.json
```

### Difference Searcher

Search for specific differences:

```bash
# Search for size differences
python search_diff.py

# Search and export results
python search_diff.py --output size_differences.json
```

## Data Formats

### Schema File Format


