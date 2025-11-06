# Store Manager Configuration Import Automation

This solution automates the generation of store manager configuration files for WDM (Wall Display Management) systems, similar to the existing printer configuration approach but focused on wall configurations, web-UI server settings, and service card management.

## Overview

The automation solution consists of:

1. **Store Mapping Configuration** (`store_wall_mapping.json`) - Defines stores and their wall IP addresses
2. **Service Cards Mapping** (`service_cards_mapping.json`) - Defines service cards for each store
3. **Configuration Generator** (`generate_store_config.py`) - Creates structure XML files
4. **Configuration Validator** (`validate_config.py`) - Validates generated configurations
5. **Excel to JSON Converter** (`convert_service_cards_to_json.py`) - Converts service cards Excel to JSON
6. **Implementation Plan** (`store_configuration_automation_plan.md`) - Detailed technical documentation

## Quick Start

### 1. Generate Configuration for a Single Store

```bash
python generate_store_config.py --store 9999
```

### 2. Generate Configurations for All Stores (Separate Files)

```bash
python generate_store_config.py --all
```

### 3. Generate Combined Configuration for All Stores (Single File)

```bash
python generate_store_config.py --all --combined
```

### 4. Validate Generated Configuration

```bash
python validate_config.py --file output/store_9999_config.xml
```

### 5. Validate All Generated Configurations

```bash
python validate_config.py --directory output
```

## Generated Files

The solution can generate structure XML files in two formats:

### Separate Files (Default)
- `output/store_9999_config.xml` - Installation Test Store configuration
- `output/store_1674_config.xml` - Store 1674 configuration
- `output/store_1655_config.xml` - Store 1655 configuration

### Combined File (With --combined flag)
- `output/all_stores_config.xml` - All stores in a single configuration file

## Configuration Structure

Each generated configuration includes:

### Wall Configuration Changes

The key feature is the addition of wall configuration changes to the CSE-wdm node:

```xml
<node alias="CSE-wdm" country="SE" name="WDM" unique-name="9999.WDM">
    <change file="wall-config.xml" url="wall-config.walls.1.clientId" value="192.168.99.101"/>
    <change file="wall-config.xml" url="wall-config.walls.2.clientId" value="192.168.99.102"/>
    <change file="wall-config.xml" url="wall-config.walls.3.clientId" value="192.168.99.103"/>
    <change file="wall-config.xml" url="wall-config.walls.100.clientId" value="192.168.99.200"/>
    <change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://192.168.26.213:8080/app-wdm"/>
    <change file="service-cards.xml" url="service-cards-config.service-cards.service-card" value="9903215"/>
    <change file="service-cards.xml" url="service-cards-config.service-cards.service-card:2" value="9903183"/>
    <change file="service-cards.xml" url="service-cards-config.service-cards.service-card:3" value="9903292"/>
</node>
```

### Web-UI Configuration Changes

The solution also supports web-ui-config changes based on a simple store IP mapping properties file (`store_ip_mapping.properties`):

**Format of store_ip_mapping.properties:**
```
# Store IP Mapping Properties File
# Format: StoreID:IPAddress
9999:192.168.26.213
1674:10.1.0.20
1655:192.168.55.100
```

**Generated web-ui-config change:**
```xml
<change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://192.168.26.213:8080/app-wdm"/>
```

### Service Cards Configuration Changes

The solution also supports service-cards.xml changes based on service cards mapping JSON file (`service_cards_mapping.json`):

**Service Cards Mapping Structure:**
```json
{
  "stores": {
    "1038": {
      "cards": ["9903215", "9903183", "9903292", "9903184"],
      "card_count": 4
    }
  }
}
```

**Generated service-cards changes:**
```xml
<change file="service-cards.xml" url="service-cards-config.service-cards.service-card" value="9903215"/>
<change file="service-cards.xml" url="service-cards-config.service-cards.service-card:2" value="9903183"/>
<change file="service-cards.xml" url="service-cards-config.service-cards.service-card:3" value="9903292"/>
<change file="service-cards.xml" url="service-cards-config.service-cards.service-card:4" value="9903184"/>
```

**Note**: The first service card has no index suffix, while subsequent cards use `:2`, `:3`, `:4`, etc.

**Converting Excel to JSON:**
If you have service cards in Excel format (`service-cards.xlsx`), convert it to JSON:
```bash
python convert_service_cards_to_json.py
```

### Wall Types

- **Wall 1**: Dispensing wall (mandatory)
- **Wall 2, 3**: Additional dispensing walls (optional)
- **Wall 100**: Disposal wall (mandatory)

## Store Mapping Configuration

The `store_wall_mapping.json` file defines:

```json
{
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
    }
  }
}
```

## Key Features

### ✅ Automated Generation
- Single command generates all store configurations
- Template-based approach ensures consistency
- Proper XML formatting and structure

### ✅ Flexible Wall Configuration
- Support for variable number of walls per store
- Mandatory walls: 1 (dispense) and 100 (disposal)
- Optional walls: 2, 3, etc.

### ✅ Service Cards Management
- Support for multiple service cards per store
- Automatic conversion from Excel to JSON format
- First card uses base URL, subsequent cards use indexed URLs (`:2`, `:3`, etc.)
- Optional feature - stores without service cards work fine

### ✅ IP Address Management
- Unique IP per wall per store
- IP address format validation
- Duplicate IP detection

### ✅ Validation & Quality Assurance
- XML schema validation
- Wall configuration validation
- Comprehensive error reporting

### ✅ Easy Maintenance
- JSON-based store mapping
- Template-driven generation
- Clear separation of concerns

## Command Line Options

### Generator Script

```bash
python generate_store_config.py [OPTIONS]

Options:
  --all                    Generate configurations for all stores
  --store STORE_ID         Generate configuration for specific store
  --combined               Generate all stores in a single combined file (use with --all)
  --output OUTPUT_DIR      Output directory (default: output)
  --mapping MAPPING_FILE   Store mapping file (default: store_wall_mapping.json)
  --template TEMPLATE_FILE Template file (default: template.xml)
  --ip-mapping IP_FILE     Store IP mapping file for web-ui-config (default: store_ip_mapping.properties)
  --service-cards CARDS_FILE Service cards mapping file (default: service_cards_mapping.json)
  --help                   Show help message
```

### Validator Script

```bash
python validate_config.py [OPTIONS]

Options:
  --file FILE_PATH         Validate specific configuration file
  --directory DIRECTORY    Validate all XML files in directory
  --summary                Show only summary for directory validation
  --help                   Show help message
```

## Adding New Stores

To add a new store:

1. Edit `store_wall_mapping.json`
2. Add new store entry with required walls and IP addresses
3. Run the generator to create the configuration

Example:
```json
"1234": {
  "name": "New Store",
  "country": "SE",
  "parent_node": "ENTERPRISE.TENANT.SWEDEN",
  "walls": {
    "1": "192.168.12.101",
    "100": "192.168.12.200"
  }
}
```

For stores that should keep the template unchanged (no WDM or web UI changes), set `"skip_wdm": true` and omit the `walls` block (or leave it empty).

## Integration with Store Manager

The generated XML files can be imported directly into the store manager application, similar to how the GKStores configurations were imported. The wall configuration changes will be applied to the target `wall-config.xml` file during import.

## Technical Details

- **Base Template**: `template.xml`
- **Target Configurations**:
  - `wall-config.xml` - Wall IP configurations
  - `web-ui-config.xml` - Web UI server configurations
- **URL Patterns**:
  - `wall-config.walls.X.clientId` - Wall configurations
  - `webUiConfig.system.serverAddress` - Web UI server address
- **Similar to**: Printer configuration pattern from GKStores example

## Validation Rules

The validator checks for:

- ✅ Valid XML structure
- ✅ Required sections (systems, nodes, etc.)
- ✅ Mandatory walls (1 and 100)
- ✅ Valid IP address format
- ✅ No duplicate IP addresses
- ✅ Proper CSE-wdm node configuration
- ✅ Web-UI configuration URL format validation
- ✅ Server address format (http://ip:8080/app-wdm)
- ✅ Service card number format validation
- ✅ Service card URL pattern validation

## Files Generated

```
automation/
├── store_wall_mapping.json              # Store to wall IP mapping (JSON)
├── store_ip_mapping.properties          # Store to server IP mapping (properties format)
├── service_cards_mapping.json           # Store to service cards mapping (JSON)
├── service-cards.xlsx                   # Original service cards Excel file
├── template.xml                         # Base structure template
├── generate_store_config.py             # Configuration generator
├── validate_config.py                   # Configuration validator
├── convert_service_cards_to_json.py     # Excel to JSON converter for service cards
├── store_configuration_automation_plan.md # Technical documentation
├── README.md                            # This file
└── output/                              # Generated configurations
    ├── store_9999_config.xml            # Individual store files
    ├── store_1674_config.xml
    ├── store_1655_config.xml
    └── all_stores_config.xml             # Combined file (with --combined)
```

## Output Options

### 🔄 **Separate Files Mode** (Default)
```bash
python generate_store_config.py --all
```
- Generates individual XML files for each store
- Easier to manage individual store configurations
- Suitable for selective imports

### 📦 **Combined File Mode** (New Feature)
```bash
python generate_store_config.py --all --combined
```
- Generates single XML file containing all stores
- Similar to GKStores configuration format
- Suitable for bulk imports
- All stores in one file: `output/all_stores_config.xml`

## Success Indicators

✅ **Generated 3 store configurations successfully**
✅ **Wall configuration changes properly added to CSE-wdm nodes**
✅ **Web-UI configuration changes added based on IP mapping**
✅ **Unique IP addresses assigned per wall per store**
✅ **Server IP addresses configured for web-ui-config**
✅ **Mandatory walls (1, 100) included for all stores**
✅ **Optional walls (2, 3) included where specified**
✅ **Proper XML structure and formatting**
✅ **Template-based approach ensures consistency**
✅ **Support for both separate and combined output formats**
✅ **Dual configuration system (wall + web-ui) working seamlessly**
✅ **Service cards configuration system integrated**
✅ **Excel to JSON conversion tool for service cards**
✅ **Automatic indexed URL generation for multiple service cards**

The solution is ready for production use and can be easily extended for additional stores or modified wall configurations. Wall management, web-UI server configurations, and service cards management are all fully automated.