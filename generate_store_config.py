#!/usr/bin/env python3
"""
Store Configuration Generator

This script generates store manager configuration files by processing
store-to-wall IP mappings and creating structure XML files with
appropriate wall configuration changes.

Usage:
    python generate_store_config.py --all
    python generate_store_config.py --store 9999
    python generate_store_config.py --help
"""

import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
import sys
from pathlib import Path
import ipaddress
import re
from typing import Dict, List, Any, Optional


def normalize_identifier(text: str) -> str:
    """
    Normalize text for use in XML identifiers by replacing Swedish characters
    and other special characters with ASCII equivalents.
    """
    # Swedish character mappings
    char_map = {
        'Å': 'A', 'å': 'a',
        'Ä': 'A', 'ä': 'a',
        'Ö': 'O', 'ö': 'o',
        'É': 'E', 'é': 'e',
        'Ü': 'U', 'ü': 'u'
    }

    # Replace Swedish characters
    normalized = text
    for swedish_char, ascii_char in char_map.items():
        normalized = normalized.replace(swedish_char, ascii_char)

    # Replace spaces and other special characters with underscores
    normalized = re.sub(r'[^A-Za-z0-9._-]', '_', normalized)

    # Remove multiple consecutive underscores
    normalized = re.sub(r'_+', '_', normalized)

    # Remove leading/trailing underscores
    normalized = normalized.strip('_')

    return normalized


class StoreConfigGenerator:
    """Main class for generating store configurations."""
    
    def __init__(self, mapping_file: str = "store_wall_mapping.json",
                 template_file: str = "template.xml",
                 ip_mapping_file: str = "store_ip_mapping.properties",
                 service_cards_file: str = "service_cards_mapping.json"):
        self.mapping_file = mapping_file
        self.template_file = template_file
        self.ip_mapping_file = ip_mapping_file
        self.service_cards_file = service_cards_file
        self.store_mapping: Optional[Dict[str, Any]] = None
        self.template_root: Optional[ET.Element] = None
        self.store_ip_mapping: Optional[Dict[str, str]] = None
        self.service_cards_mapping: Optional[Dict[str, Any]] = None
        
    def load_store_mapping(self) -> Dict[str, Any]:
        """Load and validate the store mapping JSON file."""
        try:
            with open(self.mapping_file, 'r', encoding='utf-8') as f:
                self.store_mapping = json.load(f)
            
            # Validate mandatory walls
            if self.store_mapping and 'metadata' in self.store_mapping:
                mandatory_walls = self.store_mapping['metadata'].get('mandatory_walls', [])
                for store_id, store_data in self.store_mapping['stores'].items():
                    if store_data.get('skip_wdm', False):
                        continue
                    walls = store_data.get('walls')
                    if walls is None:
                        raise ValueError(f"Store {store_id} missing 'walls' definition")
                    if not isinstance(walls, dict):
                        raise ValueError(f"Store {store_id} has invalid walls definition (expected object)")
                    for wall_id in mandatory_walls:
                        if str(wall_id) not in walls:
                            raise ValueError(f"Store {store_id} missing mandatory wall {wall_id}")
            if self.store_mapping is not None:
                print(f"✓ Loaded mapping for {len(self.store_mapping['stores'])} stores")
                return self.store_mapping
            else:
                raise ValueError("Failed to load store mapping")
            
        except FileNotFoundError:
            print(f"❌ Error: Mapping file '{self.mapping_file}' not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in mapping file: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading mapping: {e}")
            sys.exit(1)
    
    def load_store_ip_mapping(self) -> Dict[str, str]:
        """Load the store IP mapping properties file."""
        try:
            store_ip_mapping = {}
            
            with open(self.ip_mapping_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#') or line.startswith('!'):
                        continue
                    
                    # Parse store_id:ip_address format
                    if ':' in line:
                        parts = line.split(':', 1)
                        if len(parts) == 2:
                            store_id = parts[0].strip()
                            ip_address = parts[1].strip()
                            
                            # Validate IP address
                            if self.validate_ip_address(ip_address):
                                store_ip_mapping[store_id] = ip_address
                            else:
                                print(f"⚠️  Warning: Invalid IP address '{ip_address}' for store {store_id} on line {line_num}")
                        else:
                            print(f"⚠️  Warning: Invalid format on line {line_num}: {line}")
                    else:
                        print(f"⚠️  Warning: Invalid format on line {line_num}: {line}")
            
            self.store_ip_mapping = store_ip_mapping
            print(f"✓ Loaded IP mapping for {len(store_ip_mapping)} stores from '{self.ip_mapping_file}'")
            return store_ip_mapping
            
        except FileNotFoundError:
            print(f"⚠️  Warning: IP mapping file '{self.ip_mapping_file}' not found - web-ui-config changes will be skipped")
            self.store_ip_mapping = {}
            return {}
        except Exception as e:
            print(f"⚠️  Warning: Error loading IP mapping: {e} - web-ui-config changes will be skipped")
            self.store_ip_mapping = {}
            return {}
    
    def load_service_cards_mapping(self) -> Dict[str, Any]:
        """Load the service cards mapping JSON file."""
        try:
            with open(self.service_cards_file, 'r', encoding='utf-8') as f:
                self.service_cards_mapping = json.load(f)
            
            if self.service_cards_mapping and 'stores' in self.service_cards_mapping:
                total_stores = len(self.service_cards_mapping['stores'])
                total_cards = sum(store_data['card_count'] for store_data in self.service_cards_mapping['stores'].values())
                print(f"✓ Loaded service cards mapping: {total_stores} stores, {total_cards} cards from '{self.service_cards_file}'")
                return self.service_cards_mapping
            else:
                raise ValueError("Invalid service cards mapping structure")
            
        except FileNotFoundError:
            print(f"⚠️  Warning: Service cards file '{self.service_cards_file}' not found - service card changes will be skipped")
            self.service_cards_mapping = {"stores": {}}
            return self.service_cards_mapping
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Invalid JSON in service cards file: {e} - service card changes will be skipped")
            self.service_cards_mapping = {"stores": {}}
            return self.service_cards_mapping
        except Exception as e:
            print(f"⚠️  Warning: Error loading service cards mapping: {e} - service card changes will be skipped")
            self.service_cards_mapping = {"stores": {}}
            return self.service_cards_mapping
    
    def load_template(self) -> ET.Element:
        """Load the base structure template XML file."""
        try:
            tree = ET.parse(self.template_file)
            self.template_root = tree.getroot()
            print(f"✓ Loaded template from '{self.template_file}'")
            return self.template_root
            
        except FileNotFoundError:
            print(f"❌ Error: Template file '{self.template_file}' not found")
            sys.exit(1)
        except ET.ParseError as e:
            print(f"❌ Error: Invalid XML in template file: {e}")
            sys.exit(1)
    
    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format."""
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    def generate_wall_changes(self, store_id: str, store_data: Dict[str, Any]) -> List[ET.Element]:
        """Generate wall configuration change elements for a store."""
        if store_data.get("skip_wdm", False):
            print(f"   Skipping wall changes for store {store_id} (skip_wdm set)")
            return []

        walls = store_data.get("walls") or {}
        if not walls:
            raise ValueError(f"No wall definitions found for store {store_id}")

        changes: List[ET.Element] = []

        for wall_id, ip_address in walls.items():
            if not self.validate_ip_address(ip_address):
                raise ValueError(f"Invalid IP address '{ip_address}' for store {store_id}, wall {wall_id}")

            change = ET.Element("change")
            change.set("file", "wall-config.xml")
            change.set("url", f"wall-config.walls.{wall_id}.clientId")
            change.set("value", ip_address)
            changes.append(change)

        return changes

    def generate_webui_changes(self, store_id: str, store_data: Dict[str, Any]) -> List[ET.Element]:
        """Generate web-ui-config changes for a store based on IP mapping."""
        if store_data.get("skip_wdm", False) or store_data.get("skip_webui", False):
            reason = "skip_wdm set" if store_data.get("skip_wdm", False) else "skip_webui set"
            print(f"   Skipping web-ui-config change for store {store_id} ({reason})")
            return []

        changes: List[ET.Element] = []

        # Load IP mapping if not already loaded
        if self.store_ip_mapping is None:
            self.load_store_ip_mapping()

        # Check if store has IP mapping
        if self.store_ip_mapping and store_id in self.store_ip_mapping:
            ip_address = self.store_ip_mapping[store_id]

            # Create web-ui-config change
            change = ET.Element("change")
            change.set("file", "web-ui-config.xml")
            change.set("url", "webUiConfig.system.serverAddress")
            change.set("value", f"http://{ip_address}:8080/app-wdm")
            changes.append(change)

            print(f"   Added web-ui-config change for store {store_id}: http://{ip_address}:8080/app-wdm")

        return changes
<<<<<<< HEAD

=======
    
    def generate_service_card_changes(self, store_id: str) -> List[ET.Element]:
        """Generate service-cards-config changes for a store based on service cards mapping."""
        changes: List[ET.Element] = []
        
        # Load service cards mapping if not already loaded
        if self.service_cards_mapping is None:
            self.load_service_cards_mapping()
        
        # Check if store has service cards
        if self.service_cards_mapping and store_id in self.service_cards_mapping.get('stores', {}):
            cards = self.service_cards_mapping['stores'][store_id]['cards']
            
            for idx, card_number in enumerate(cards):
                change = ET.Element("change")
                change.set("file", "service-cards.xml")
                
                # First card has no index suffix, subsequent cards have :2, :3, etc.
                if idx == 0:
                    change.set("url", "service-cards-config.service-cards.service-card")
                else:
                    change.set("url", f"service-cards-config.service-cards.service-card:{idx + 1}")
                
                change.set("value", card_number)
                changes.append(change)
            
            print(f"   Added {len(cards)} service card(s) for store {store_id}")
        
        return changes
    
    def generate_wdm_config_changes(self, store_id: str) -> List[ET.Element]:
        """Generate wdm-config.properties changes for a store."""
        changes: List[ET.Element] = []
        
        # Create wdm-config.properties change for businessUnitId
        change = ET.Element("change")
        change.set("file", "wdm-config.properties")
        change.set("url", "remote-services.businessUnitId")
        change.set("value", store_id)
        changes.append(change)
        
        print(f"   Added wdm-config change for store {store_id}: businessUnitId={store_id}")
        
        return changes
    
>>>>>>> c97cb17 (feat: Add service cards and wdm-config.properties support)
    def create_store_structure(self, store_id: str, store_data: Dict[str, Any]) -> ET.Element:
        """Create a complete store structure based on template."""
        # Create a deep copy of the template
        structure = ET.Element("structure")
        
        # Copy systems section
        systems = ET.SubElement(structure, "systems")
        if self.template_root is not None:
            template_systems = self.template_root.find("systems")
            if template_systems is not None:
                for system in template_systems:
                    systems.append(ET.fromstring(ET.tostring(system)))
        
        # Copy time-regimes section
        time_regimes = ET.SubElement(structure, "time-regimes")
        if self.template_root is not None:
            template_time_regimes = self.template_root.find("time-regimes")
            if template_time_regimes is not None:
                for child in template_time_regimes:
                    time_regimes.append(ET.fromstring(ET.tostring(child)))
        
        # Copy central-is section
        central_is = ET.SubElement(structure, "central-is")
        if self.template_root is not None:
            template_central_is = self.template_root.find("central-is")
            if template_central_is is not None:
                for child in template_central_is:
                    central_is.append(ET.fromstring(ET.tostring(child)))
        
        # Create nodes section with store-specific data
        nodes = ET.SubElement(structure, "nodes")
        
        # Create main store node
        store_node = ET.SubElement(nodes, "node")
        store_node.set("alias", "GKR-Store")
        store_node.set("country", store_data["country"])
        store_node.set("name", store_data["name"])
        store_node.set("parent-node-ident", store_data["parent_node"])
        store_node.set("rsid", store_id)
        store_node.set("unique-name", f"{store_data['parent_node']}.{normalize_identifier(store_data['name']).upper()}")
        
        # Add child nodes from template
        if self.template_root is not None:
            template_store_node = self.template_root.find(".//node[@alias='GKR-Store']")
            if template_store_node is not None:
                for child_node in template_store_node:
                    if child_node.tag == "node":
                        new_child = ET.fromstring(ET.tostring(child_node))
                        # Update unique names with store ID
                        if "unique-name" in new_child.attrib:
                            unique_name = new_child.get("unique-name")
                            if unique_name:
                                new_child.set("unique-name", unique_name.replace("9999", store_id))
                        
                        # Add wall changes to CSE-wdm node
                        if new_child.get("alias") == "CSE-wdm":
                            wall_changes = self.generate_wall_changes(store_id, store_data)
                            for change in wall_changes:
                                new_child.append(change)
                            
                            # Add web-ui-config changes to CSE-wdm node
                            webui_changes = self.generate_webui_changes(store_id, store_data)
                            for change in webui_changes:
                                new_child.append(change)
                            
                            # Add service card changes to CSE-wdm node
                            service_card_changes = self.generate_service_card_changes(store_id)
                            for change in service_card_changes:
                                new_child.append(change)
                            
                            # Add wdm-config.properties changes to CSE-wdm node
                            wdm_config_changes = self.generate_wdm_config_changes(store_id)
                            for change in wdm_config_changes:
                                new_child.append(change)
                        
                        store_node.append(new_child)
        
        return structure
    
    def format_xml(self, element: ET.Element) -> str:
        """Format XML with proper indentation."""
        rough_string = ET.tostring(element, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="    ")[23:]  # Remove XML declaration
    
    def generate_store_config(self, store_id: str) -> str:
        """Generate configuration for a specific store."""
        if self.store_mapping is None:
            self.load_store_mapping()
        
        if self.template_root is None:
            self.load_template()
        
        if self.store_mapping is None:
            raise ValueError("Store mapping not loaded")
            
        if store_id not in self.store_mapping["stores"]:
            raise ValueError(f"Store {store_id} not found in mapping")
        
        store_data = self.store_mapping["stores"][store_id]
        structure = self.create_store_structure(store_id, store_data)
        
        # Add XML declaration
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += self.format_xml(structure)
        
        return xml_content
    
    def save_store_config(self, store_id: str, output_dir: str = "output") -> str:
        """Generate and save configuration for a specific store."""
        try:
            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(exist_ok=True)
            
            # Generate configuration
            config_xml = self.generate_store_config(store_id)
            
            # Save to file
            output_file = f"{output_dir}/store_{store_id}_config.xml"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(config_xml)
            
            print(f"✓ Generated configuration for store {store_id}: {output_file}")
            return output_file
            
        except Exception as e:
            print(f"❌ Error generating config for store {store_id}: {e}")
            raise
    
    def generate_combined_config(self, output_dir: str = "output") -> str:
        """Generate a single configuration file containing all stores."""
        if self.store_mapping is None:
            self.load_store_mapping()
        
        if self.template_root is None:
            self.load_template()
        
        if self.store_mapping is None:
            raise ValueError("Store mapping not loaded")
        
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(exist_ok=True)
        
        # Create combined structure
        structure = ET.Element("structure")
        
        # Copy systems section from template
        systems = ET.SubElement(structure, "systems")
        if self.template_root is not None:
            template_systems = self.template_root.find("systems")
            if template_systems is not None:
                for system in template_systems:
                    systems.append(ET.fromstring(ET.tostring(system)))
        
        # Copy time-regimes section
        time_regimes = ET.SubElement(structure, "time-regimes")
        if self.template_root is not None:
            template_time_regimes = self.template_root.find("time-regimes")
            if template_time_regimes is not None:
                for child in template_time_regimes:
                    time_regimes.append(ET.fromstring(ET.tostring(child)))
        
        # Copy central-is section
        central_is = ET.SubElement(structure, "central-is")
        if self.template_root is not None:
            template_central_is = self.template_root.find("central-is")
            if template_central_is is not None:
                for child in template_central_is:
                    central_is.append(ET.fromstring(ET.tostring(child)))
        
        # Create nodes section with all stores
        nodes = ET.SubElement(structure, "nodes")
        
        # Add each store as a separate node
        for store_id, store_data in self.store_mapping["stores"].items():
            print(f"   Adding store {store_id} to combined configuration...")
            
            # Create store node
            store_node = ET.SubElement(nodes, "node")
            store_node.set("alias", "GKR-Store")
            store_node.set("country", store_data["country"])
            store_node.set("name", store_data["name"])
            store_node.set("parent-node-ident", store_data["parent_node"])
            store_node.set("rsid", store_id)
            store_node.set("unique-name", f"{store_data['parent_node']}.{normalize_identifier(store_data['name']).upper()}")
            
            # Add child nodes from template
            if self.template_root is not None:
                template_store_node = self.template_root.find(".//node[@alias='GKR-Store']")
                if template_store_node is not None:
                    for child_node in template_store_node:
                        if child_node.tag == "node":
                            new_child = ET.fromstring(ET.tostring(child_node))
                            # Update unique names with store ID
                            if "unique-name" in new_child.attrib:
                                unique_name = new_child.get("unique-name")
                                if unique_name:
                                    new_child.set("unique-name", unique_name.replace("9999", store_id))
                            
                            # Add wall changes to CSE-wdm node
                            if new_child.get("alias") == "CSE-wdm":
                                wall_changes = self.generate_wall_changes(store_id, store_data)
                                for change in wall_changes:
                                    new_child.append(change)
                                
                                # Add web-ui-config changes to CSE-wdm node
                                webui_changes = self.generate_webui_changes(store_id, store_data)
                                for change in webui_changes:
                                    new_child.append(change)
                                
                                # Add service card changes to CSE-wdm node
                                service_card_changes = self.generate_service_card_changes(store_id)
                                for change in service_card_changes:
                                    new_child.append(change)
                                
                                # Add wdm-config.properties changes to CSE-wdm node
                                wdm_config_changes = self.generate_wdm_config_changes(store_id)
                                for change in wdm_config_changes:
                                    new_child.append(change)
                            
                            store_node.append(new_child)
        
        # Generate XML content
        xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
        xml_content += self.format_xml(structure)
        
        # Save to file
        output_file = f"{output_dir}/all_stores_config.xml"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✓ Generated combined configuration: {output_file}")
        return output_file

    def generate_all_stores(self, output_dir: str = "output", combined: bool = False) -> List[str]:
        """Generate configurations for all stores in the mapping."""
        if combined:
            # Generate single combined file
            combined_file = self.generate_combined_config(output_dir)
            return [combined_file]
        else:
            # Generate separate files for each store
            if self.store_mapping is None:
                self.load_store_mapping()
            
            generated_files: List[str] = []
            
            if self.store_mapping is not None:
                for store_id in self.store_mapping["stores"]:
                    try:
                        output_file = self.save_store_config(store_id, output_dir)
                        generated_files.append(output_file)
                    except Exception as e:
                        print(f"❌ Failed to generate config for store {store_id}: {e}")
            
            print(f"\n✓ Generated {len(generated_files)} store configurations")
            return generated_files


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Generate store manager configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_store_config.py --all
  python generate_store_config.py --all --combined
  python generate_store_config.py --store 9999
  python generate_store_config.py --store 1674 --output custom_output
        """
    )
    
    parser.add_argument("--all", action="store_true",
                       help="Generate configurations for all stores")
    parser.add_argument("--store", type=str,
                       help="Generate configuration for specific store ID")
    parser.add_argument("--combined", action="store_true",
                       help="Generate all stores in a single combined file (use with --all)")
    parser.add_argument("--output", type=str, default="output",
                       help="Output directory (default: output)")
    parser.add_argument("--mapping", type=str, default="store_wall_mapping.json",
                       help="Store mapping file (default: store_wall_mapping.json)")
    parser.add_argument("--template", type=str,
                       default="template.xml",
                       help="Template file (default: template.xml)")
    parser.add_argument("--ip-mapping", type=str, default="store_ip_mapping.properties",
                       help="Store IP mapping file for web-ui-config (default: store_ip_mapping.properties)")
    parser.add_argument("--service-cards", type=str, default="service_cards_mapping.json",
                       help="Service cards mapping file (default: service_cards_mapping.json)")
    
    args = parser.parse_args()
    
    if not args.all and not args.store:
        parser.print_help()
        sys.exit(1)
    
    # Initialize generator
    generator = StoreConfigGenerator(args.mapping, args.template, args.ip_mapping, args.service_cards)
    
    try:
        if args.all:
            if args.combined:
                print("🚀 Generating combined configuration for all stores...")
                generated_files = generator.generate_all_stores(args.output, combined=True)
                print(f"\n📁 Generated combined file: {generated_files[0]}")
            else:
                print("🚀 Generating separate configurations for all stores...")
                generated_files = generator.generate_all_stores(args.output, combined=False)
                print("\n📁 Generated files:")
                for file_path in generated_files:
                    print(f"   {file_path}")
                
        elif args.store:
            print(f"🚀 Generating configuration for store {args.store}...")
            output_file = generator.save_store_config(args.store, args.output)
            
            print(f"\n📁 Generated file: {output_file}")
        
        print("\n✅ Configuration generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()