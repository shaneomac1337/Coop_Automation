#!/usr/bin/env python3
"""
Service Cards Excel to JSON Converter

This script converts the service-cards.xlsx file into a JSON format
that can be used by the configuration generator.

Usage:
    python convert_service_cards_to_json.py
"""

import pandas as pd
import json
from typing import Dict, List


def convert_excel_to_json(excel_file: str = "service-cards.xlsx", 
                          output_file: str = "service_cards_mapping.json") -> None:
    """Convert service cards Excel file to JSON format."""
    
    print(f"📖 Reading Excel file: {excel_file}")
    
    # Read the Excel file
    df = pd.read_excel(excel_file)
    
    # Group by SiteID (store)
    stores_dict: Dict[str, List[str]] = {}
    
    for _, row in df.iterrows():
        site_id = str(int(row['SiteID'])) if pd.notna(row['SiteID']) else None
        admin_card = str(int(row['Admin cards'])) if pd.notna(row['Admin cards']) else None
        
        if site_id and admin_card:
            if site_id not in stores_dict:
                stores_dict[site_id] = []
            stores_dict[site_id].append(admin_card)
    
    # Create the JSON structure
    service_cards_data = {
        "metadata": {
            "description": "Store to service card mapping for WDM configuration",
            "version": "1.0",
            "source": excel_file,
            "total_stores": len(stores_dict),
            "total_cards": sum(len(cards) for cards in stores_dict.values())
        },
        "stores": {}
    }
    
    # Add each store's cards
    for store_id in sorted(stores_dict.keys(), key=int):
        cards = stores_dict[store_id]
        service_cards_data["stores"][store_id] = {
            "cards": cards,
            "card_count": len(cards)
        }
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(service_cards_data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Converted {len(stores_dict)} stores with {service_cards_data['metadata']['total_cards']} service cards")
    print(f"📁 Saved to: {output_file}")
    
    # Print summary
    print(f"\n📊 Summary:")
    print(f"   Total stores: {len(stores_dict)}")
    print(f"   Total cards: {service_cards_data['metadata']['total_cards']}")
    print(f"   Stores with most cards:")
    
    top_stores = sorted(stores_dict.items(), key=lambda x: len(x[1]), reverse=True)[:5]
    for store_id, cards in top_stores:
        print(f"      Store {store_id}: {len(cards)} cards")


if __name__ == "__main__":
    convert_excel_to_json()
