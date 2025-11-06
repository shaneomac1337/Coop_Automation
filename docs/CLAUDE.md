# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This repository automates the generation of store manager configuration files for WDM (Wall Display Management) systems. It creates structure XML files with wall configuration changes and web-UI server configurations for multiple stores.

## Essential Commands

### Using the GUI (Recommended)
```bash
# Launch graphical user interface
python gui.py
```

The GUI provides:
- Store selection dropdown with all available stores
- One-click generation (all stores or single store)
- Integrated validation
- Real-time log output
- Direct access to output folder
- Excel to JSON conversion for service cards (requires pandas)

### Generate Configurations (Command Line)
```bash
# Generate all store configurations (separate files)
python generate_store_config.py --all

# Generate combined configuration file for all stores
python generate_store_config.py --all --combined

# Generate configuration for specific store
python generate_store_config.py --store 9999
```

### Validate Configurations
```bash
# Validate specific configuration file
python validate_config.py --file output/store_9999_config.xml

# Validate all configurations in output directory
python validate_config.py --directory output

# Validate with summary only
python validate_config.py --directory output --summary
```

## Architecture Overview

### Core Components
- **`gui.py`**: Simple tkinter-based GUI for all operations (NEW)
- **`generate_store_config.py`**: Main configuration generator that processes JSON mappings and creates XML structure files
- **`validate_config.py`**: Configuration validator that ensures XML structure, wall configurations, and IP addresses are valid
- **`store_wall_mapping.json`**: Store-to-wall IP address mapping with metadata and wall types
- **`store_ip_mapping.properties`**: Simple store-to-server IP mapping for web-UI configuration
- **`template.xml`**: Base structure template containing systems, nodes, and store hierarchy

### Configuration Flow
1. Store mapping files define stores and their wall/server IP addresses
2. Generator processes mappings against template to create store-specific XML structures
3. Wall changes are added to CSE-wdm nodes with format: `wall-config.walls.X.clientId`
4. Web-UI changes are added with format: `webUiConfig.system.serverAddress`
5. Validator ensures mandatory walls (1), IP format, and XML structure compliance

### Wall Types
- **Wall 1**: Dispensing wall (mandatory)
- **Walls 2, 3**: Additional dispensing walls (optional)
- **Wall 100**: Disposal wall (optional)

### Output Modes
- **Separate files**: Individual XML per store (`store_9999_config.xml`)
- **Combined file**: All stores in single XML (`all_stores_config.xml`)

## Key Configuration Elements

### Generated Change Elements
Wall configurations target the CSE-wdm node:
```xml
<change file="wall-config.xml" url="wall-config.walls.1.clientId" value="192.168.99.101"/>
<change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://192.168.26.213:8080/app-wdm"/>
```

### Store Mapping Structure
- Each store requires: name, country, parent_node, walls object
- Mandatory walls: 1 (dispense only)
- IP addresses must be valid IPv4 format
- Store IDs become rsid attributes in generated XML

## Adding New Stores

1. Edit `store_wall_mapping.json` to add new store entry
2. Optionally add entry to `store_ip_mapping.properties` for web-UI configuration
3. Run generator to create configuration files
4. Validate generated configurations

The system automatically handles unique-name generation, wall change creation, and XML structure validation.