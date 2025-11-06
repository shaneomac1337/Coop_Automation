# Store Manager Configuration Import Automation

This solution automates the generation of store manager configuration files for WDM (Wall Display Management) systems, similar to the existing printer configuration approach but focused on wall configurations, web-UI server settings, and service card management.

## Features

✨ **Graphical User Interface (GUI)** - Simple, user-friendly interface for all operations
🤖 **Automated Generation** - Single command generates all store configurations
🎯 **Flexible Configuration** - Support for variable number of walls per store
💳 **Service Cards Management** - Automatic service card configuration
📊 **Excel to JSON Converter** - Built-in conversion tool in GUI (requires pandas)
🌐 **Web-UI Integration** - Server address configuration
✅ **Built-in Validation** - Comprehensive error checking
📊 **Real-time Feedback** - Progress logging and status updates
🔄 **Multiple Modes** - Separate or combined output files

## Overview

The automation solution consists of:

1. **Graphical User Interface** (`src/gui.py`) - Simple GUI for all operations
2. **Store Mapping Configuration** (`config/mappings/store_wall_mapping.json`) - Defines stores and their wall IP addresses
3. **Service Cards Mapping** (`config/mappings/service_cards_mapping.json`) - Defines service cards for each store
4. **Configuration Generator** (`src/generate_store_config.py`) - Creates structure XML files
5. **Configuration Validator** (`src/validate_config.py`) - Validates generated configurations
6. **Excel to JSON Converter** (`src/convert_service_cards_to_json.py`) - Converts service cards Excel to JSON
7. **Implementation Plan** (`docs/store_configuration_automation_plan.md`) - Detailed technical documentation

## 📁 Project Structure

```
Coop_Automation/
├── README.md                      # Main documentation (you are here)
├── .gitignore                     # Git ignore rules
├── start_gui.bat                  # Windows launcher for GUI
│
├── src/                           # Source code
│   ├── gui.py                     # Graphical user interface
│   ├── generate_store_config.py   # Configuration generator
│   ├── validate_config.py         # Configuration validator
│   └── convert_service_cards_to_json.py  # Excel converter
│
├── config/                        # Configuration files
│   ├── templates/                 # XML templates
│   │   ├── template.xml
│   │   ├── web-ui-config.xml
│   │   └── wall-config.xml
│   ├── mappings/                  # Store and service mappings
│   │   ├── store_wall_mapping.json
│   │   ├── service_cards_mapping.json
│   │   └── store_ip_mapping.properties
│   └── examples/                  # Example configurations
│
├── docs/                          # Documentation
│   ├── GUI_QUICKSTART.md
│   ├── GUI_VISUAL_GUIDE.md
│   ├── GUI_IMPLEMENTATION.md
│   ├── BUILD_EXECUTABLE_GUIDE.md
│   └── ... (more docs)
│
├── scripts/                       # Build and utility scripts
│   └── build_exe.py               # PyInstaller build script
│
└── output/                        # Generated configurations
    └── store_*.xml                # Generated store configs
```

## Quick Start

### Option 1: Using the GUI (Recommended for Beginners)

```bash
python src/gui.py
```

Or use the Windows launcher:
```bash
start_gui.bat
```

The GUI provides an easy-to-use interface with:
- 🎯 Store selection dropdown
- 🚀 One-click configuration generation
- ✓ Built-in validation
- 📁 Direct access to output folder
- 📊 Real-time log output
- 📑 Excel to JSON conversion (for service cards)

### Option 2: Using Command Line

#### 1. Generate Configuration for a Single Store

```bash
python src/generate_store_config.py --store 9999
```

#### 2. Generate Configurations for All Stores (Separate Files)

```bash
python src/generate_store_config.py --all
```

#### 3. Generate Combined Configuration for All Stores (Single File)

```bash
python src/generate_store_config.py --all --combined
```

#### 4. Validate Generated Configuration

```bash
python src/validate_config.py --file output/store_9999_config.xml
```

#### 5. Validate All Generated Configurations

```bash
python src/validate_config.py --directory output
```

## Generated Files

The solution can generate structure XML files in two formats:

### Separate Files (Default)
- `output/store_9999_config.xml` - Installation Test Store configuration
- `output/store_1674_config.xml` - Store 1674 configuration
- `output/store_1655_config.xml` - Store 1655 configuration

### Combined File (With --combined flag)
- `output/all_stores_config.xml` - All stores in a single configuration file

## Using the GUI

### Starting the GUI

Simply run:
```bash
python src/gui.py
```

Or double-click: `start_gui.bat`

### GUI Features

The GUI provides an intuitive interface with the following sections:

#### 1. **Configuration Files Section**
- Set paths for store mapping, template, and output directory
- Default values work out of the box

#### 2. **Service Cards Conversion Section**
- Convert Excel files (`service-cards.xlsx`) to JSON format
- Browse button to select Excel file
- Specify output JSON filename
- One-click conversion with detailed feedback
- **Note:** Requires `pandas` library: `pip install pandas openpyxl`

#### 3. **Store Selection Section**
- **Generate All Stores (Separate Files)** - Creates individual XML files for each store
- **Generate All Stores (Combined File)** - Creates a single XML with all stores
- **Generate Single Store** - Select and generate one store from the dropdown

#### 4. **Action Buttons**
- **🚀 Generate Configuration** - Starts the generation process
- **✓ Validate Output** - Validates all generated files
- **📁 Open Output Folder** - Opens the output directory in file explorer
- **🔄 Reload Stores** - Refreshes the store list from mapping file

#### 5. **Output Log**
- Real-time feedback during generation and validation
- Shows progress, errors, and success messages
- Clear log button to start fresh

#### 6. **Status Bar**
- Shows current operation status at the bottom

### GUI Workflow

#### Standard Workflow:
1. **Launch GUI**: Run `python src/gui.py` or double-click `start_gui.bat`
2. **Select Mode**: Choose generation mode (all stores, combined, or single)
3. **Select Store** (if single mode): Pick from dropdown
4. **Generate**: Click "Generate Configuration" button
5. **Validate**: Click "Validate Output" to check generated files
6. **Open Folder**: Click "Open Output Folder" to view results

#### Excel Conversion Workflow (For Service Cards):
1. **Launch GUI**: Run `python src/gui.py` or double-click `start_gui.bat`
2. **Locate Excel Section**: "Service Cards Conversion" section
3. **Select File**: Click "Browse..." or enter path to `service-cards.xlsx`
4. **Convert**: Click "📊 Convert Excel to JSON" button
5. **Check Log**: See conversion results and statistics
6. **Use JSON**: The generated `service_cards_mapping.json` is ready to use

**Note:** Excel conversion requires pandas: `pip install pandas openpyxl`

### GUI Benefits

✅ **No Command Line Required** - Perfect for non-technical users
✅ **Visual Feedback** - See exactly what's happening
✅ **Error Prevention** - Clear options prevent mistakes
✅ **Quick Access** - Open output folder directly
✅ **Integrated Validation** - Test configurations immediately
✅ **Store Browser** - See all available stores at a glance

### GUI Documentation

- **[GUI Quick Start Guide](docs/GUI_QUICKSTART.md)** - Step-by-step getting started
- **[GUI Visual Guide](docs/GUI_VISUAL_GUIDE.md)** - Visual interface walkthrough
- **[GUI Implementation Details](docs/GUI_IMPLEMENTATION.md)** - Technical documentation
- **[Build Executable Guide](docs/BUILD_EXECUTABLE_GUIDE.md)** - Create standalone .exe file

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
python src/convert_service_cards_to_json.py
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
python src/generate_store_config.py [OPTIONS]

Options:
  --all                    Generate configurations for all stores
  --store STORE_ID         Generate configuration for specific store
  --combined               Generate all stores in a single combined file (use with --all)
  --output OUTPUT_DIR      Output directory (default: output)
  --mapping MAPPING_FILE   Store mapping file (default: config/mappings/store_wall_mapping.json)
  --template TEMPLATE_FILE Template file (default: config/templates/template.xml)
  --ip-mapping IP_FILE     Store IP mapping file (default: config/mappings/store_ip_mapping.properties)
  --service-cards CARDS    Service cards mapping file (default: config/mappings/service_cards_mapping.json)
  --help                   Show help message
```

### Validator Script

```bash
python src/validate_config.py [OPTIONS]

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
Coop_Automation/
├── src/                                 # Source code
│   ├── gui.py                           # Graphical User Interface
│   ├── generate_store_config.py         # Configuration generator
│   ├── validate_config.py               # Configuration validator
│   └── convert_service_cards_to_json.py # Excel to JSON converter
│
├── config/                              # Configuration files
│   ├── templates/                       # XML templates
│   │   ├── template.xml
│   │   ├── web-ui-config.xml
│   │   └── wall-config.xml
│   ├── mappings/                        # Mappings
│   │   ├── store_wall_mapping.json      # Store to wall IP mapping
│   │   ├── store_ip_mapping.properties  # Store to server IP mapping
│   │   └── service_cards_mapping.json   # Store to service cards mapping
│   └── examples/                        # Example files
│
├── docs/                                # Documentation
│   ├── GUI_QUICKSTART.md
│   ├── BUILD_EXECUTABLE_GUIDE.md
│   ├── SERVICE_CARDS_IMPLEMENTATION.md
│   └── ... (more documentation)
│
├── scripts/                             # Build scripts
│   └── build_exe.py                     # PyInstaller build script
│
├── output/                              # Generated configurations
│   ├── store_9999_config.xml            # Individual store files
│   ├── store_1674_config.xml
│   ├── store_1655_config.xml
│   └── all_stores_config.xml            # Combined file (with --combined)
│
├── README.md                            # This file
├── .gitignore                           # Git ignore rules
└── start_gui.bat                        # Windows launcher
```

## Output Options

### 🔄 **Separate Files Mode** (Default)
```bash
python src/generate_store_config.py --all
```
- Generates individual XML files for each store
- Easier to manage individual store configurations
- Suitable for selective imports

### 📦 **Combined File Mode** (New Feature)
```bash
python src/generate_store_config.py --all --combined
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