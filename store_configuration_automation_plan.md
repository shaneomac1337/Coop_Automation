# Store Manager Configuration Import Automation Plan

## Overview
This document outlines the detailed plan for automating the configuration import solution for the store manager application, specifically focusing on WDM (Wall Display Management) configurations.

## Current Situation Analysis

### Existing Files
- **GKStoresConfig_Prod_001only_updated_capital_S.xml**: Example configuration from previous customer showing printer configuration changes
- **structure_Installation_Test_Store_202505280610.xml**: Base structure for new customer (simpler, without HybridInfoservers)
- **wall-config.xml**: Template showing wall configuration structure

### Key Requirements
- Modify WDM configuration similar to printer configuration approach
- Support multiple stores: 9999, 1674, 1655
- Each wall gets unique IP address
- Mandatory walls: 1 (dispense) and 100 (disposal)
- Optional walls: 2, 3, etc.

## Implementation Plan

### Phase 1: Data Structure Design

#### 1.1 Store-to-IP Mapping File (`store_wall_mapping.json`)
```json
{
  "metadata": {
    "description": "Store to wall IP address mapping for WDM configuration",
    "version": "1.0",
    "created": "2025-05-29",
    "mandatory_walls": [1, 100],
    "wall_types": {
      "1": "WALL_TYPE_1 (Dispensing)",
      "2": "WALL_TYPE_1 (Dispensing)", 
      "3": "WALL_TYPE_1 (Dispensing)",
      "100": "WALL_TYPE_DISPOSAL (Disposal)"
    }
  },
  "stores": {
    "9999": {
      "name": "Installation Test Store",
      "country": "SE",
      "parent_node": "ENTERPRISE.TENANT.SWEDEN",
      "walls": {
        "1": "192.168.99.101",
        "2": "192.168.99.102", 
        "3": "192.168.99.103",
        "100": "192.168.99.200"
      }
    },
    "1674": {
      "name": "Store 1674",
      "country": "SE",
      "parent_node": "ENTERPRISE.TENANT.SWEDEN", 
      "walls": {
        "1": "192.168.74.101",
        "100": "192.168.74.200"
      }
    },
    "1655": {
      "name": "Store 1655",
      "country": "SE",
      "parent_node": "ENTERPRISE.TENANT.SWEDEN",
      "walls": {
        "1": "192.168.55.101",
        "2": "192.168.55.102",
        "100": "192.168.55.200"
      }
    }
  }
}
```

### Phase 2: Configuration Generator Script

#### 2.1 Script Structure (`generate_store_config.py`)
```python
# Main components:
# 1. JSON loader for store mapping
# 2. XML template processor
# 3. Change element generator
# 4. Output file generator
# 5. Validation utilities
```

#### 2.2 Key Functions
- `load_store_mapping()`: Load and validate JSON mapping
- `generate_wall_changes()`: Create wall configuration change elements
- `create_store_structure()`: Generate complete store structure
- `validate_configuration()`: Validate generated XML
- `export_structure_file()`: Save final configuration

### Phase 3: Change Element Generation

#### 3.1 Wall Configuration Changes
For each store, generate change elements targeting the CSE-wdm node:

```xml
<node alias="CSE-wdm" country="SE" name="WDM" unique-name="9999.WDM">
    <change file="wall-config.xml" url="wall-config.walls.wall[wallId='1'].clientId" value="192.168.99.101"/>
    <change file="wall-config.xml" url="wall-config.walls.wall[wallId='2'].clientId" value="192.168.99.102"/>
    <change file="wall-config.xml" url="wall-config.walls.wall[wallId='3'].clientId" value="192.168.99.103"/>
    <change file="wall-config.xml" url="wall-config.walls.wall[wallId='100'].clientId" value="192.168.99.200"/>
</node>
```

#### 3.2 XPath Pattern
- Target: `wall-config.walls.wall[wallId='X'].clientId`
- Similar to printer pattern: `printers.physicalPrinterList.physicalPrinter.uniqueName`

### Phase 4: File Structure Organization

```
automation/
├── config/
│   └── store_wall_mapping.json
├── templates/
│   ├── base_structure_template.xml
│   └── wall_config_template.xml
├── scripts/
│   ├── generate_store_config.py
│   ├── validate_config.py
│   └── utils/
│       ├── xml_processor.py
│       └── ip_validator.py
├── output/
│   └── generated_configs/
│       ├── store_9999_config.xml
│       ├── store_1674_config.xml
│       └── store_1655_config.xml
└── docs/
    ├── configuration_guide.md
    └── usage_examples.md
```

### Phase 5: Validation and Quality Assurance

#### 5.1 Validation Rules
- XML schema validation
- IP address format validation (IPv4)
- Store ID uniqueness
- Mandatory wall presence (1 and 100)
- Wall ID consistency
- XPath syntax validation

#### 5.2 Error Handling
- Invalid IP addresses
- Missing mandatory walls
- Duplicate store IDs
- Malformed XML structure
- File I/O errors

### Phase 6: Usage and Automation

#### 6.1 Command Line Interface
```bash
# Generate all store configurations
python generate_store_config.py --all

# Generate specific store
python generate_store_config.py --store 9999

# Validate configuration
python validate_config.py --file output/store_9999_config.xml

# Batch validation
python validate_config.py --directory output/generated_configs/
```

#### 6.2 Integration Points
- Input: Store mapping JSON + Base template
- Processing: Configuration generator
- Output: Ready-to-import structure XML files
- Validation: Automated quality checks

## Expected Outcomes

### Generated Structure Files
Each store will have a complete structure XML file containing:
- All required system definitions
- Store-specific node configuration
- CSE-wdm node with wall configuration changes
- Proper XML formatting and validation

### Example Output for Store 9999
```xml
<node alias="GKR-Store" country="SE" name="Installation Test Store" 
      parent-node-ident="ENTERPRISE.TENANT.SWEDEN" rsid="9999" 
      unique-name="ENTERPRISE.TENANT.SWEDEN.INSTALLATION_TEST_STORE">
    <!-- Other nodes... -->
    <node alias="CSE-wdm" country="SE" name="WDM" unique-name="9999.WDM">
        <change file="wall-config.xml" url="wall-config.walls.wall[wallId='1'].clientId" value="192.168.99.101"/>
        <change file="wall-config.xml" url="wall-config.walls.wall[wallId='2'].clientId" value="192.168.99.102"/>
        <change file="wall-config.xml" url="wall-config.walls.wall[wallId='3'].clientId" value="192.168.99.103"/>
        <change file="wall-config.xml" url="wall-config.walls.wall[wallId='100'].clientId" value="192.168.99.200"/>
    </node>
</node>
```

## Benefits

1. **Automation**: Eliminates manual configuration for multiple stores
2. **Consistency**: Ensures uniform configuration patterns
3. **Scalability**: Easy to add new stores or modify existing ones
4. **Validation**: Built-in quality checks prevent configuration errors
5. **Maintainability**: Template-based approach for easy updates
6. **Documentation**: Clear mapping between stores and configurations

## Next Steps

1. Create the store mapping JSON file
2. Develop the configuration generator script
3. Implement validation utilities
4. Test with example stores (9999, 1674, 1655)
5. Generate and validate output files
6. Create usage documentation

## Technical Notes

- Based on existing GKStores configuration pattern
- Uses XPath-style targeting for wall configuration
- Supports variable number of walls per store
- Maintains compatibility with existing wall-config.xml structure
- Follows XML best practices for structure files