# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository automates the generation of store manager configuration files for WDM (Wall Display Management) systems. It creates XML structure files with wall configuration changes, web-UI server configurations, service card mappings, and wdm-config.properties settings for multiple stores across Sweden.

## Essential Commands

### Using the GUI (Recommended)
```bash
# Launch graphical user interface
python src/gui.py

# Or use Windows launcher
start_gui.bat
```

The GUI provides store selection, one-click generation for all stores or single store, integrated validation, real-time log output, direct access to output folder, and Excel to JSON conversion for service cards (requires pandas).

### Generate Configurations (Command Line)
```bash
# Generate all store configurations (separate files)
python src/generate_store_config.py --all

# Generate combined configuration file for all stores
python src/generate_store_config.py --all --combined

# Generate configuration for specific store
python src/generate_store_config.py --store 1038

# Specify custom paths
python src/generate_store_config.py --store 1038 --output custom_output --mapping config/mappings/store_wall_mapping.json
```

### Validate Configurations
```bash
# Validate specific configuration file
python src/validate_config.py --file output/store_1038_config.xml

# Validate all configurations in output directory
python src/validate_config.py --directory output

# Validate with summary only
python src/validate_config.py --directory output --summary
```

### Excel to JSON Conversion (Service Cards)
```bash
# Convert service cards Excel to JSON
python src/convert_service_cards_to_json.py
```

### Build Standalone Executable
```bash
# Build Windows executable with all dependencies
python scripts/build_exe.py
```

## Architecture Overview

### Core Components

**src/gui.py**: tkinter-based GUI for all operations. Handles threaded execution to keep UI responsive. Integrates generation, validation, and Excel conversion in one interface.

**src/generate_store_config.py**: Main configuration generator. Processes JSON mappings and creates XML structure files. Key class is `StoreConfigGenerator` with methods:
- `load_store_mapping()`: Loads store_wall_mapping.json, validates mandatory walls, and parses wall types metadata
- `load_store_ip_mapping()`: Loads store_ip_mapping.properties for web-UI configuration
- `load_service_cards_mapping()`: Loads service_cards_mapping.json
- `generate_wall_changes()`: Creates wall-config.xml change elements for clientId and wallType
- `generate_wall_type_description_changes()`: Creates wall-config.xml change elements for wall type descriptions
- `generate_webui_changes()`: Creates web-ui-config.xml change elements
- `generate_service_card_changes()`: Creates service-cards.xml change elements
- `generate_wdm_config_changes()`: Creates wdm-config.properties change elements
- `create_store_structure()`: Builds complete store structure from template
- `generate_all_stores()`: Generates separate or combined configuration files

**src/validate_config.py**: Configuration validator that ensures XML structure, wall configurations, IP addresses, and URL patterns are valid. Uses `ConfigValidator` class.

**src/convert_service_cards_to_json.py**: Converts Excel files with service card data to JSON format expected by the generator. Uses pandas to read Excel and groups by SiteID.

### Configuration Files

**config/mappings/store_wall_mapping.json**: Primary mapping file. Structure:
- `metadata`: Contains mandatory_walls list and wall_types_example (just documentation/example, not used by generator)
- `stores`: Object with store_id as key, containing name, country, parent_node, walls object, optional skip_wdm flag, and optional wall_type_descriptions to enable wall type features per store

**config/mappings/store_ip_mapping.properties**: Simple store-to-server IP mapping for web-UI configuration. Format: `StoreID:IPAddress` (one per line, supports comments with # or !)

**config/mappings/service_cards_mapping.json**: Store-to-service-cards mapping. Structure contains stores object with card arrays and card_count.

**config/templates/template.xml**: Base structure template containing systems, time-regimes, central-is, and nodes sections. Contains placeholder store node with alias "GKR-Store" and child nodes including CSE-wdm where changes are injected.

### Configuration Flow

1. Store mapping files define stores and their wall/server IP addresses and service cards
2. Generator loads template.xml and all mapping files
3. For each store, generator creates store node structure from template
4. Generator finds CSE-wdm child node and injects configuration changes:
   - Wall changes: `wall-config.walls.X.clientId` → IP address
   - Wall type changes: `wall-config.walls.X.wallType` → WALL_TYPE_X (or WALL_TYPE_DISPOSAL for wall 100)
   - Wall type descriptions: `wall-config.wall-types.WALL_TYPE_X.description` → description text
   - Web-UI changes: `webUiConfig.system.serverAddress` → `http://IP:8080/app-wdm`
   - Service card changes: `service-cards-config.service-cards.service-card[:N]` → card number
   - WDM config changes: `remote-services.businessUnitId` → store_id
5. Generator formats XML with proper indentation using minidom
6. Output saved to separate files or combined file
7. Validator checks XML structure, mandatory walls, wall types, descriptions, IP format, and URL patterns

### Wall Types
- **Wall 1**: Dispensing wall (WALL_TYPE_1) - mandatory for all stores
- **Wall 2**: Additional dispensing wall (WALL_TYPE_2) - optional
- **Wall 3**: Additional dispensing wall (WALL_TYPE_3) - optional
- **Wall 100**: Disposal wall (WALL_TYPE_DISPOSAL) - optional but commonly used

Wall type naming follows the pattern: Wall ID X → WALL_TYPE_X, except wall 100 which always uses WALL_TYPE_DISPOSAL.

### Output Modes
- **Separate files**: Individual XML per store (store_9999_config.xml)
- **Combined file**: All stores in single XML (all_stores_config.xml)

## Key Implementation Details

### Generated Change Elements

Wall configurations and other settings are injected into the CSE-wdm node.

**With wall_type_descriptions enabled** (opt-in):
```xml
<node alias="CSE-wdm" country="SE" name="WDM" unique-name="1346.WDM">
    <change file="wall-config.xml" url="wall-config.walls.1.clientId" value="10.23.131.22"/>
    <change file="wall-config.xml" url="wall-config.walls.1.wallType" value="WALL_TYPE_1"/>
    <change file="wall-config.xml" url="wall-config.walls.2.clientId" value="10.23.131.21"/>
    <change file="wall-config.xml" url="wall-config.walls.100.clientId" value="10.23.131.23"/>
    <change file="wall-config.xml" url="wall-config.walls.100.wallType" value="WALL_TYPE_DISPOSAL"/>
    <change file="wall-config.xml" url="wall-config.wall-types.WALL_TYPE_1.description" value="Main dispensing wall with 50 devices"/>
    <change file="wall-config.xml" url="wall-config.wall-types.WALL_TYPE_DISPOSAL.description" value="Disposal wall for returns"/>
    <change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://10.23.131.22:8080/app-wdm"/>
    <change file="service-cards.xml" url="service-cards-config.service-cards.service-card" value="9903215"/>
    <change file="wdm-config.properties" url="remote-services.businessUnitId" value="1346"/>
</node>
```
Note: Wall 2 only has clientId (no wallType/description) because it wasn't in wall_type_descriptions.

**Without wall_type_descriptions** (default/legacy behavior):
```xml
<node alias="CSE-wdm" country="SE" name="WDM" unique-name="1038.WDM">
    <change file="wall-config.xml" url="wall-config.walls.1.clientId" value="10.31.99.32"/>
    <change file="wall-config.xml" url="wall-config.walls.100.clientId" value="10.31.99.31"/>
    <change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://10.31.99.32:8080/app-wdm"/>
    <change file="wdm-config.properties" url="remote-services.businessUnitId" value="1038"/>
</node>
```

### Store Mapping Structure

Each store requires: name, country, parent_node, walls object (unless skip_wdm is true). Wall IDs map to IP addresses. Store IDs become rsid attributes in generated XML. Unique names are generated by combining parent_node with normalized store name.

### Text Normalization

The `normalize_identifier()` function in generate_store_config.py handles Swedish characters (Å, Ä, Ö, É, Ü) by converting to ASCII equivalents, replacing special characters with underscores, and removing consecutive/leading/trailing underscores. This ensures XML identifiers are valid.

### Service Card URL Pattern

First service card uses base URL without index suffix. Subsequent cards use :2, :3, :4, etc. Example:
- Card 1: `service-cards-config.service-cards.service-card`
- Card 2: `service-cards-config.service-cards.service-card:2`
- Card 3: `service-cards-config.service-cards.service-card:3`

### Wall Type Descriptions (Opt-in Feature)

Wall type and description features are **opt-in per store**. Only stores with `wall_type_descriptions` defined will generate wallType and description changes. Stores without this field work exactly like before (only clientId changes).

**Example in metadata (for reference only)**:
```json
"wall_types_example": {
  "_comment": "This is just an EXAMPLE. To enable for a store, add wall_type_descriptions to that store.",
  "1": "Dispensing wall for 50 devices with handicap rows 5-6.",
  "2": "Additional dispensing wall.",
  "100": "Disposal wall."
}
```

**Enable for a specific store** (defines wall ID to description mapping):
```json
"1346": {
  "name": "Väst - 1346 Coop Mellerud",
  "walls": { "1": "10.23.131.22", "2": "10.23.131.21", "100": "10.23.131.23" },
  "wall_type_descriptions": {
    "1": "Main dispensing wall with 50 devices",
    "100": "Disposal wall for returns"
  }
}
```

**Behavior**:
- Wall types are auto-derived: wall 1 → WALL_TYPE_1, wall 100 → WALL_TYPE_DISPOSAL, etc.
- Partial configuration is supported - only walls with descriptions get wallType/description changes
- In the example above, wall 2 would only have clientId change (no wallType or description)
- Stores without `wall_type_descriptions` get no wallType or description changes (backward compatible)

### Skip Flags

Stores can have `skip_wdm: true` to skip wall and web-UI configuration (keeps template unchanged). Stores can have `skip_webui: true` to skip only web-UI configuration while keeping wall configuration.

## Adding New Stores

1. Edit `config/mappings/store_wall_mapping.json` to add new store entry with required fields
2. Optionally add entry to `config/mappings/store_ip_mapping.properties` for web-UI configuration
3. Optionally add service cards to `config/mappings/service_cards_mapping.json`
4. Run generator to create configuration files
5. Validate generated configurations

For stores that should keep the template unchanged (no WDM or web UI changes), set `"skip_wdm": true` and omit the walls block.

## Development Workflow

When modifying the generator logic, test with both single store generation and combined file generation to ensure both code paths work. When changing validation rules, update both the validator and the corresponding documentation. When adding new configuration types, update generate_store_config.py to add new change generation methods, update validation rules, and document the new configuration format.

## Building Distribution

The project includes a build script at `scripts/build_exe.py` that uses PyInstaller to create a standalone Windows executable. The build process creates a complete distribution folder with the executable, configuration files, documentation, and an empty output folder. Detailed instructions are in `docs/BUILD_EXECUTABLE_GUIDE.md`.
