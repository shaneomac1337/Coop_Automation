#!/usr/bin/env python3
"""
SFTP Endpoint Excel to JSON Converter

This script converts the SFTP endpoint Excel file into a JSON format
that can be used by the configuration generator.

Usage:
    python convert_sftp_endpoint_to_json.py
    python convert_sftp_endpoint_to_json.py --input "SFTP endpoint_Import 2.0.xlsx" --output config/mappings/sftp_endpoint_mapping.json
"""

import pandas as pd
import json
import argparse
from typing import Dict


def convert_excel_to_json(excel_file: str = "SFTP endpoint_Import 2.0.xlsx",
                          output_file: str = "config/mappings/sftp_endpoint_mapping.json") -> None:
    """Convert SFTP endpoint Excel file to JSON format."""

    print(f"Reading Excel file: {excel_file}")

    # Read the Excel file
    df = pd.read_excel(excel_file)

    # Build stores dict from Site ID and SFTP endpoint columns
    stores_dict: Dict[str, str] = {}

    for _, row in df.iterrows():
        site_id = str(int(row['Site ID'])) if pd.notna(row['Site ID']) else None
        sftp_endpoint = str(row['SFTP endpoint']).strip() if pd.notna(row['SFTP endpoint']) else None

        if site_id and sftp_endpoint:
            stores_dict[site_id] = sftp_endpoint

    # Create the JSON structure
    sftp_endpoint_data = {
        "metadata": {
            "description": "Store to SFTP endpoint mapping for POS Server configuration",
            "version": "1.0",
            "source": excel_file,
            "total_stores": len(stores_dict)
        },
        "stores": {}
    }

    # Add each store's SFTP endpoint (sorted by store ID)
    for store_id in sorted(stores_dict.keys(), key=int):
        sftp_endpoint_data["stores"][store_id] = stores_dict[store_id]

    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(sftp_endpoint_data, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(stores_dict)} stores with SFTP endpoints")
    print(f"Saved to: {output_file}")

    # Print summary
    print(f"\nSummary:")
    print(f"   Total stores: {len(stores_dict)}")
    print(f"   First 5 entries:")

    sample_stores = list(stores_dict.items())[:5]
    for store_id, endpoint in sample_stores:
        print(f"      Store {store_id}: {endpoint}")


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert SFTP endpoint Excel file to JSON format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python convert_sftp_endpoint_to_json.py
  python convert_sftp_endpoint_to_json.py --input "SFTP endpoint_Import 2.0.xlsx" --output config/mappings/sftp_endpoint_mapping.json
        """
    )

    parser.add_argument("--input", type=str, default="SFTP endpoint_Import 2.0.xlsx",
                       help="Input Excel file (default: SFTP endpoint_Import 2.0.xlsx)")
    parser.add_argument("--output", type=str, default="config/mappings/sftp_endpoint_mapping.json",
                       help="Output JSON file (default: config/mappings/sftp_endpoint_mapping.json)")

    args = parser.parse_args()

    convert_excel_to_json(args.input, args.output)


if __name__ == "__main__":
    main()
