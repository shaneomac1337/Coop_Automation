#!/usr/bin/env python3
"""
Configuration Validator

This script validates generated store configuration files to ensure
they meet the required standards and contain proper wall configurations.

Usage:
    python validate_config.py --file output/store_9999_config.xml
    python validate_config.py --directory output
    python validate_config.py --help
"""

import xml.etree.ElementTree as ET
import argparse
import sys
import ipaddress
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional, Set


class ConfigValidator:
    """Validator for store configuration files."""
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def reset(self) -> None:
        """Reset error and warning lists."""
        self.errors = []
        self.warnings = []
    
    def validate_ip_address(self, ip: str) -> bool:
        """Validate IP address format."""
        try:
            ipaddress.IPv4Address(ip)
            return True
        except ipaddress.AddressValueError:
            return False
    
    def validate_xml_structure(self, file_path: str) -> Tuple[bool, Optional[ET.Element]]:
        """Validate XML file structure and return root element."""
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            if root.tag != "structure":
                self.errors.append(f"Root element should be 'structure', found '{root.tag}'")
                return False, root
            
            # Check required sections
            required_sections = ["systems", "time-regimes", "central-is", "nodes"]
            for section in required_sections:
                if root.find(section) is None:
                    self.errors.append(f"Missing required section: {section}")
            
            return len(self.errors) == 0, root
            
        except ET.ParseError as e:
            self.errors.append(f"XML parsing error: {e}")
            return False, None
        except FileNotFoundError:
            self.errors.append(f"File not found: {file_path}")
            return False, None
    
    def validate_wall_configurations(self, root: ET.Element) -> bool:
        """Validate wall configuration changes in the XML."""
        wall_changes = root.findall(".//change[@file='wall-config.xml']")
        
        if not wall_changes:
            self.errors.append("No wall configuration changes found")
            return False
        
        # Track wall IDs and IP addresses
        wall_ips: Dict[str, str] = {}
        mandatory_walls: Set[str] = {"1"}
        found_walls: Set[str] = set()
        
        for change in wall_changes:
            url = change.get("url", "")
            value = change.get("value", "")
            
            # Extract wall ID from URL (format: wall-config.walls.X.clientId)
            if "wall-config.walls." in url and ".clientId" in url:
                # Extract wall ID between "walls." and ".clientId"
                start = url.find("wall-config.walls.") + 18
                end = url.find(".clientId")
                wall_id = url[start:end]
                found_walls.add(wall_id)
                
                # Validate IP address
                if not self.validate_ip_address(value):
                    self.errors.append(f"Invalid IP address '{value}' for wall {wall_id}")
                else:
                    if value in wall_ips.values():
                        self.errors.append(f"Duplicate IP address '{value}' found")
                    wall_ips[wall_id] = value
            else:
                self.errors.append(f"Invalid wall configuration URL: {url}")
        
        # Check mandatory walls
        missing_walls = mandatory_walls - found_walls
        if missing_walls:
            self.errors.append(f"Missing mandatory walls: {', '.join(missing_walls)}")
        
        # Validate wall ID sequence
        wall_ids = [int(w) for w in found_walls if w.isdigit()]
        if wall_ids:
            wall_ids.sort()
            if wall_ids[0] != 1:
                self.warnings.append("Wall IDs should start with 1")
            
            # Check for gaps (except between regular walls and disposal wall 100)
            regular_walls = [w for w in wall_ids if w < 100]
            if len(regular_walls) > 1:
                for i in range(1, len(regular_walls)):
                    if regular_walls[i] - regular_walls[i-1] > 1:
                        self.warnings.append(f"Gap in wall ID sequence: {regular_walls[i-1]} to {regular_walls[i]}")
        
        return len(self.errors) == 0
    
    def validate_webui_configurations(self, root: ET.Element) -> bool:
        """Validate web-ui-config changes in the XML."""
        webui_changes = root.findall(".//change[@file='web-ui-config.xml']")
        
        for change in webui_changes:
            url = change.get("url", "")
            value = change.get("value", "")
            
            # Check if it's the expected web-ui-config URL
            if url == "webUiConfig.system.serverAddress":
                # Validate URL format
                if not value.startswith("http://") or ":8080/app-wdm" not in value:
                    self.errors.append(f"Invalid web-ui-config URL format: {value}")
            else:
                self.warnings.append(f"Unexpected web-ui-config URL: {url}")
        
        return len(self.errors) == 0
    
    def validate_store_node(self, root: ET.Element) -> bool:
        """Validate store node configuration."""
        store_nodes = root.findall(".//node[@alias='GKR-Store']")
        
        if not store_nodes:
            self.errors.append("No store node found")
            return False
        
        # For combined configurations, multiple store nodes are expected
        # For individual configurations, only one store node should exist
        is_combined = len(store_nodes) > 1
        
        if is_combined:
            print(f"   📦 Detected combined configuration with {len(store_nodes)} stores")
        
        # Validate each store node individually
        for i, store_node in enumerate(store_nodes):
            store_id = store_node.get("rsid", f"store_{i}")
            
            # Check required attributes
            required_attrs = ["country", "name", "rsid", "unique-name"]
            for attr in required_attrs:
                if not store_node.get(attr):
                    self.errors.append(f"Store node {store_id} missing required attribute: {attr}")
            
            # Check for CSE-wdm node
            wdm_nodes = store_node.findall(".//node[@alias='CSE-wdm']")
            if not wdm_nodes:
                self.errors.append(f"No CSE-wdm node found in store {store_id}")
            elif len(wdm_nodes) > 1:
                self.warnings.append(f"Multiple CSE-wdm nodes found in store {store_id}")
        
        return len(self.errors) == 0
    
    def validate_systems(self, root: ET.Element) -> bool:
        """Validate systems section."""
        systems = root.find("systems")
        if systems is None:
            return False
        
        required_systems = [
            "GKR-Store", "CSE-sdc-store_SE", "CSE-pos-server-STORE_SE",
            "GKR-mwb-store", "CSE-lps-store", "CSE-wdm"
        ]
        
        found_systems = [system.get("alias") for system in systems.findall("system")]
        
        for req_system in required_systems:
            if req_system not in found_systems:
                self.errors.append(f"Missing required system: {req_system}")
        
        return len(self.errors) == 0
    
    def validate_file(self, file_path: str) -> Dict[str, Any]:
        """Validate a single configuration file."""
        self.reset()
        
        print(f"🔍 Validating: {file_path}")
        
        # Validate XML structure
        is_valid_xml, root = self.validate_xml_structure(file_path)
        if not is_valid_xml or root is None:
            return {
                "file": file_path,
                "valid": False,
                "errors": self.errors.copy(),
                "warnings": self.warnings.copy()
            }
        
        # Validate components
        self.validate_systems(root)
        self.validate_store_node(root)
        self.validate_wall_configurations(root)
        self.validate_webui_configurations(root)
        
        is_valid = len(self.errors) == 0
        
        # Print results
        if is_valid:
            print(f"   ✅ Valid configuration")
        else:
            print(f"   ❌ Invalid configuration")
        
        if self.errors:
            print(f"   🚨 Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"      - {error}")
        
        if self.warnings:
            print(f"   ⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"      - {warning}")
        
        return {
            "file": file_path,
            "valid": is_valid,
            "errors": self.errors.copy(),
            "warnings": self.warnings.copy()
        }
    
    def validate_directory(self, directory: str) -> List[Dict[str, Any]]:
        """Validate all XML files in a directory."""
        dir_path = Path(directory)
        
        if not dir_path.exists():
            print(f"❌ Directory not found: {directory}")
            return []
        
        xml_files = list(dir_path.glob("*.xml"))
        
        if not xml_files:
            print(f"⚠️  No XML files found in: {directory}")
            return []
        
        print(f"🔍 Validating {len(xml_files)} files in: {directory}")
        
        results: List[Dict[str, Any]] = []
        for xml_file in xml_files:
            result = self.validate_file(str(xml_file))
            results.append(result)
        
        # Summary
        valid_count = sum(1 for r in results if r["valid"])
        invalid_count = len(results) - valid_count
        
        print(f"\n📊 Validation Summary:")
        print(f"   ✅ Valid files: {valid_count}")
        print(f"   ❌ Invalid files: {invalid_count}")
        print(f"   📁 Total files: {len(results)}")
        
        return results


def main() -> None:
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Validate store configuration files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python validate_config.py --file output/store_9999_config.xml
  python validate_config.py --directory output
  python validate_config.py --directory output --summary
        """
    )
    
    parser.add_argument("--file", type=str, 
                       help="Validate a specific configuration file")
    parser.add_argument("--directory", type=str, 
                       help="Validate all XML files in a directory")
    parser.add_argument("--summary", action="store_true",
                       help="Show only summary for directory validation")
    
    args = parser.parse_args()
    
    if not args.file and not args.directory:
        parser.print_help()
        sys.exit(1)
    
    validator = ConfigValidator()
    
    try:
        if args.file:
            result = validator.validate_file(args.file)
            if not result["valid"]:
                sys.exit(1)
                
        elif args.directory:
            results = validator.validate_directory(args.directory)
            
            if not args.summary:
                # Show detailed results
                invalid_files = [r for r in results if not r["valid"]]
                if invalid_files:
                    print(f"\n❌ Invalid files:")
                    for result in invalid_files:
                        print(f"   {result['file']}")
                        for error in result['errors']:
                            print(f"      - {error}")
            
            # Exit with error code if any files are invalid
            if any(not r["valid"] for r in results):
                sys.exit(1)
        
        print("\n✅ All validations passed!")
        
    except Exception as e:
        print(f"\n❌ Validation error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()