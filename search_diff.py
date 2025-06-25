import json
from typing import List, Dict

def search_different_size(json_file: str, target_size: str = "3594") -> List[Dict]:
    """Search for records where file_info.size is not equal to target_size"""
    with open(json_file, 'r') as f:
        differences = json.load(f)
    
    # Filter records where file_info.size != target_size
    filtered_records = [
        record for record in differences
        if record.get('file_info', {}).get('size') != target_size
    ]
    
    return filtered_records

def print_results(records: List[Dict]):
    """Print filtered records in a formatted way"""
    if not records:
        print("No records found with different size")
        return
        
    print(f"Found {len(records)} records with different size:")
    print("-" * 80)
    
    for record in records:
        print(f"Table: {record['table']}")
        print(f"Column: {record['column']}")
        print(f"Size in file: {record['file_info'].get('size', 'N/A')}")
        if record['db_info']:
            print(f"Size in DB: {record['db_info'].get('size', 'N/A')}")
        print("-" * 40)

def export_results(records: List[Dict], output_file: str):
    """Export filtered records to JSON file"""
    with open(output_file, 'w') as f:
        json.dump(records, f, indent=2)
    print(f"Results exported to {output_file}")

def main():
    # Search for records with size != "3594"
    different_size_records = search_different_size("schema_differences.json")
    
    # Print results
    print_results(different_size_records)
    
    # Export filtered results
    export_results(different_size_records, "size_differences.json")

if __name__ == "__main__":
    main()
