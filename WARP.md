# WARP.md - Coop_Automation Project

This file provides comprehensive guidance for AI agents working with the Coop_Automation codebase. It describes the project's purpose, architecture, conventions, and common workflows.

---

## 🎯 Project Purpose

The **Coop_Automation** project automates the generation of store manager configuration files for **WDM (Wall Display Management)** systems. It processes store-to-wall IP mappings and generates properly formatted XML structure files that can be imported into store management systems.

### Key Capabilities
- Generate XML configuration files for individual stores or all stores at once
- Support for both separate and combined output modes
- Dual configuration system: wall management + web-UI server configurations
- Built-in validation to ensure XML structure, wall configurations, and IP addresses are correct
- Flexible wall configuration (mandatory and optional walls)

---

## 📁 Project Structure

```
Coop_Automation/
├── generate_store_config.py          # Main configuration generator
├── validate_config.py                # Configuration validator
├── store_wall_mapping.json           # Store-to-wall IP mappings (JSON)
├── store_ip_mapping.properties       # Store-to-server IP mappings (properties format)
├── template.xml                      # Base structure template
├── wall-config.xml                   # Wall configuration template reference
├── web-ui-config.xml                 # Web-UI configuration template reference
├── GKStoresConfig_Prod_001only_updated_capital_S.xml  # Reference example from previous customer
├── README.md                         # User-facing documentation
├── CLAUDE.md                         # Legacy AI assistant guidance (less comprehensive than WARP.md)
├── store_configuration_automation_plan.md  # Detailed technical documentation
└── output/                           # Generated configuration files
    ├── store_<ID>_config.xml         # Individual store configurations
    └── all_stores_config.xml         # Combined configuration (all stores)
```

---

## 🛠️ Technology Stack

### Languages & Frameworks
- **Python 3.x**: Core language
- **Standard Library**: `xml.etree.ElementTree`, `xml.dom.minidom`, `argparse`, `json`, `ipaddress`, `pathlib`
- **XML Processing**: Native Python XML libraries for parsing and generation

### Key Libraries
- `xml.etree.ElementTree`: XML parsing and manipulation
- `xml.dom.minidom`: Pretty-printing XML output
- `ipaddress`: IP address validation
- `argparse`: Command-line interface
- `json`: Store mapping configuration parsing

### Development Environment
- **OS**: Windows (PowerShell 7.5.3)
- **Python Version**: 3.x (specific version not specified but modern features used)
- **No external dependencies**: Uses only Python standard library

---

## 🏗️ Architecture & Core Components

### 1. Configuration Generator (`generate_store_config.py`)

**Purpose**: Main script that processes JSON mappings and creates XML structure files

**Key Classes**:
- `StoreConfigGenerator`: Core generator class with methods for:
  - Loading store mappings from JSON
  - Loading store IP mappings from properties file
  - Loading base XML template
  - Generating wall configuration changes
  - Generating web-UI configuration changes
  - Creating complete store structures
  - Formatting XML output
  - Saving configurations to files

**Important Methods**:
- `load_store_mapping()`: Validates JSON structure and mandatory walls
- `load_store_ip_mapping()`: Parses properties file for web-UI server IPs
- `load_template()`: Loads base structure template
- `generate_wall_changes()`: Creates wall configuration change elements
- `generate_webui_changes()`: Creates web-UI configuration change elements
- `create_store_structure()`: Builds complete store XML structure
- `normalize_identifier()`: Converts Swedish characters to ASCII for XML identifiers
- `generate_all_stores()`: Batch generation for all stores
- `generate_combined_config()`: Creates single file with all stores

**Command-Line Options**:
```bash
--all                    # Generate configurations for all stores
--store STORE_ID         # Generate configuration for specific store
--combined               # Generate all stores in single file (use with --all)
--output OUTPUT_DIR      # Output directory (default: output)
--mapping MAPPING_FILE   # Store mapping file (default: store_wall_mapping.json)
--template TEMPLATE_FILE # Template file (default: template.xml)
--ip-mapping IP_FILE     # Store IP mapping file (default: store_ip_mapping.properties)
```

### 2. Configuration Validator (`validate_config.py`)

**Purpose**: Validates generated configuration files for correctness and compliance

**Key Classes**:
- `ConfigValidator`: Validation engine with methods for:
  - XML structure validation
  - Wall configuration validation
  - Web-UI configuration validation
  - Store node validation
  - Systems section validation
  - IP address format validation

**Validation Rules**:
- ✅ Valid XML structure with required sections (systems, time-regimes, central-is, nodes)
- ✅ Mandatory wall 1 (dispensing) present for non-skipped stores
- ✅ Valid IPv4 address format
- ✅ No duplicate IP addresses
- ✅ Proper CSE-wdm node configuration
- ✅ Web-UI configuration URL format (`http://ip:8080/app-wdm`)
- ✅ Required systems present (GKR-Store, CSE-sdc-store_SE, CSE-pos-server-STORE_SE, etc.)

**Command-Line Options**:
```bash
--file FILE_PATH         # Validate specific configuration file
--directory DIRECTORY    # Validate all XML files in directory
--summary                # Show only summary for directory validation
```

### 3. Store Mapping Configuration (`store_wall_mapping.json`)

**Purpose**: Defines stores and their wall IP addresses

**Structure**:
```json
{
  "metadata": {
    "description": "Store to wall IP address mapping for WDM configuration",
    "version": "1.0",
    "mandatory_walls": [1],
    "wall_types": {
      "1": "WALL_TYPE_1 (Dispensing)",
      "2": "WALL_TYPE_1 (Dispensing)",
      "3": "WALL_TYPE_1 (Dispensing)",
      "100": "WALL_TYPE_DISPOSAL (Disposal)"
    }
  },
  "stores": {
    "STORE_ID": {
      "name": "Store Name",
      "country": "SE",
      "parent_node": "ENTERPRISE.TENANT.SWEDEN",
      "walls": {
        "1": "10.x.x.x",
        "2": "10.x.x.x",      // Optional
        "100": "10.x.x.x"     // Optional
      },
      "skip_wdm": false       // Optional: skip wall configurations
    }
  }
}
```

**Key Fields**:
- `name`: Store display name (can contain Swedish characters)
- `country`: Two-letter country code (typically "SE")
- `parent_node`: Hierarchical parent in store structure
- `walls`: Object mapping wall IDs to IP addresses
- `skip_wdm`: Boolean flag to skip WDM configuration changes (keeps template unchanged)

### 4. Store IP Mapping (`store_ip_mapping.properties`)

**Purpose**: Simple mapping of store IDs to server IP addresses for web-UI configuration

**Format**:
```properties
# Store IP Mapping Properties File
# Format: StoreID:IPAddress
9999:192.168.26.213
1674:10.1.0.20
1655:192.168.55.100
```

**Usage**: 
- Loaded by generator to create web-ui-config.xml change elements
- Optional: if file missing, web-UI changes are skipped
- Generates: `<change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://IP:8080/app-wdm"/>`

---

## 🔧 Common Workflows

### Generate Configuration for All Stores (Separate Files)
```bash
python generate_store_config.py --all
```
**Output**: Individual XML files in `output/` directory (`store_9999_config.xml`, etc.)

### Generate Combined Configuration (All Stores in One File)
```bash
python generate_store_config.py --all --combined
```
**Output**: Single file `output/all_stores_config.xml` containing all stores

### Generate Configuration for Specific Store
```bash
python generate_store_config.py --store 1161
```
**Output**: Single file `output/store_1161_config.xml`

### Validate Generated Configuration
```bash
# Validate single file
python validate_config.py --file output/store_9999_config.xml

# Validate all files in directory
python validate_config.py --directory output

# Validate with summary only
python validate_config.py --directory output --summary
```

### Adding a New Store

1. **Edit** `store_wall_mapping.json`:
   ```json
   "1234": {
     "name": "New Store",
     "country": "SE",
     "parent_node": "ENTERPRISE.TENANT.SWEDEN",
     "walls": {
       "1": "10.12.34.101",
       "2": "10.12.34.102",
       "100": "10.12.34.200"
     }
   }
   ```

2. **Optionally edit** `store_ip_mapping.properties`:
   ```properties
   1234:10.12.34.50
   ```

3. **Generate configuration**:
   ```bash
   python generate_store_config.py --store 1234
   ```

4. **Validate**:
   ```bash
   python validate_config.py --file output/store_1234_config.xml
   ```

### Skipping WDM Configuration for a Store

For stores that should keep the template unchanged (no WDM or web-UI changes):
```json
"1681": {
  "name": "Lund",
  "country": "SE",
  "parent_node": "ENTERPRISE.TENANT.SWEDEN",
  "skip_wdm": true,
  "walls": {}
}
```

---

## 📐 Coding Patterns & Conventions

### XML Generation Pattern
1. Load base template from `template.xml`
2. Deep copy sections (systems, time-regimes, central-is)
3. Create nodes section with store-specific data
4. Inject wall changes into CSE-wdm node
5. Inject web-UI changes into CSE-wdm node
6. Format with proper indentation using `minidom`

### Generated XML Structure
```xml
<?xml version="1.0" encoding="UTF-8"?>
<structure>
    <systems>...</systems>
    <time-regimes>...</time-regimes>
    <central-is>...</central-is>
    <nodes>
        <node alias="GKR-Store" country="SE" name="Store Name" 
              parent-node-ident="ENTERPRISE.TENANT.SWEDEN" 
              rsid="9999" 
              unique-name="ENTERPRISE.TENANT.SWEDEN.STORE_NAME">
            <!-- Child nodes including CSE-wdm -->
            <node alias="CSE-wdm" country="SE" name="WDM" unique-name="9999.WDM">
                <change file="wall-config.xml" url="wall-config.walls.1.clientId" value="192.168.99.101"/>
                <change file="wall-config.xml" url="wall-config.walls.2.clientId" value="192.168.99.102"/>
                <change file="wall-config.xml" url="wall-config.walls.100.clientId" value="192.168.99.200"/>
                <change file="web-ui-config.xml" url="webUiConfig.system.serverAddress" value="http://192.168.26.213:8080/app-wdm"/>
            </node>
        </node>
    </nodes>
</structure>
```

### Wall Types & IDs
- **Wall 1**: Dispensing wall (mandatory)
- **Walls 2, 3**: Additional dispensing walls (optional)
- **Wall 100**: Disposal wall (optional)

### URL Patterns for Configuration Changes
- **Wall config**: `wall-config.walls.X.clientId` (where X is wall ID)
- **Web-UI config**: `webUiConfig.system.serverAddress`

### Swedish Character Normalization
The `normalize_identifier()` function converts Swedish characters for XML identifiers:
- Å/å → A/a
- Ä/ä → A/a
- Ö/ö → O/o
- É/é → E/e
- Ü/ü → U/u
- Spaces and special characters → underscore

Example: "Östra - 1161 Coop Krokek" → "OSTRA_1161_COOP_KROKEK"

### Error Handling
- JSON parsing errors: Exit with error message
- XML parsing errors: Exit with error message
- Invalid IP addresses: Validation error
- Missing mandatory walls: Validation error
- File I/O errors: Graceful error handling with informative messages

---

## 🧪 Testing & Validation

### Manual Testing Process
1. Generate configuration for all stores
2. Validate all generated files
3. Check output for errors/warnings
4. Verify mandatory walls present
5. Verify IP address uniqueness
6. Verify XML structure compliance

### Validation Output Examples
```
✓ Valid configuration
   🚨 Errors (0):
   ⚠️  Warnings (0):

📊 Validation Summary:
   ✅ Valid files: 8
   ❌ Invalid files: 0
   📁 Total files: 8
```

---

## 📝 Configuration Details

### Current Stores in System
Based on `store_wall_mapping.json`:
- **1161**: Östra - Coop Krokek (1 wall)
- **1038**: Östra - Coop Hammarby Sjöstad (2 walls: 1, 100)
- **1346**: Väst - Coop Mellerud (3 walls: 1, 2, 100)
- **1828**: Östra - Stora Coop Spånga (3 walls: 1, 2, 100)
- **1677**: Mitt - Coop Forum Marieberg (2 walls: 1, 100)
- **1681**: Lund (skip_wdm: true)
- **1664**: Bromma (skip_wdm: true)
- **1674**: Haggvik (skip_wdm: true)

### Required Systems in Template
- GKR-Store
- CSE-sdc-store_SE
- CSE-pos-server-STORE_SE
- GKR-mwb-store
- CSE-lps-store
- CSE-wdm

---

## 🚨 Important Notes for AI Agents

### When Generating New Stores
1. Always validate store ID is unique
2. Ensure mandatory wall 1 is present (unless skip_wdm is true)
3. Use valid IPv4 addresses
4. Avoid duplicate IP addresses across walls
5. Follow existing naming conventions
6. Run validation after generation

### When Modifying Scripts
1. Preserve XML structure and formatting
2. Maintain compatibility with existing store mappings
3. Keep validation rules consistent
4. Don't break command-line interface
5. Test with existing stores after changes

### When Debugging Issues
1. Check JSON syntax in mapping files
2. Verify IP address format (IPv4 only)
3. Ensure template.xml is valid
4. Check for duplicate store IDs
5. Validate mandatory walls are present
6. Review error messages from validator

### File Modification Guidelines
- **Do modify**: `store_wall_mapping.json`, `store_ip_mapping.properties` (adding new stores)
- **Rarely modify**: `generate_store_config.py`, `validate_config.py` (only for new features/fixes)
- **Don't modify**: `template.xml` (unless changing base structure), generated output files

---

## 📚 Related Documentation

- **README.md**: User-facing documentation with quick start guide
- **CLAUDE.md**: Legacy AI assistant guidance (less comprehensive)
- **store_configuration_automation_plan.md**: Detailed technical implementation plan
- **External Reference**: GKStoresConfig_Prod_001only_updated_capital_S.xml (previous customer example)

---

## 🎓 Learning Resources

### Understanding the Project
1. Read README.md for user perspective
2. Review store_configuration_automation_plan.md for technical details
3. Examine template.xml to understand base structure
4. Look at generated output files to see final result
5. Study store_wall_mapping.json for configuration patterns

### Key Concepts
- **Structure XML**: Import format for store manager application
- **Change Elements**: Specify configuration changes to apply
- **CSE-wdm Node**: Target node for wall configurations
- **Wall Types**: Different wall types (dispensing vs disposal)
- **XPath-style URLs**: Target specific configuration values

---

## 💡 Common Questions & Answers

**Q: Why are some stores marked with `skip_wdm: true`?**  
A: These stores don't require WDM (Wall Display Management) configuration changes. The template remains unchanged for these stores.

**Q: What's the difference between separate and combined output?**  
A: Separate creates individual XML files per store (`store_9999_config.xml`). Combined creates one file with all stores (`all_stores_config.xml`).

**Q: Why is only wall 1 mandatory now?**  
A: Requirements changed - only wall 1 (dispensing) is mandatory. Wall 100 (disposal) and walls 2, 3 are optional.

**Q: What happens if `store_ip_mapping.properties` is missing?**  
A: Generator will show a warning and skip web-ui-config changes. Wall configurations will still be generated.

**Q: Can store names contain Swedish characters?**  
A: Yes! Store names support Swedish characters (Å, Ä, Ö, etc.). The `normalize_identifier()` function converts them for XML identifiers.

**Q: How do I know if a configuration is valid?**  
A: Run the validator script. It checks XML structure, mandatory walls, IP addresses, and more.

**Q: What's the relationship to GKStores?**  
A: GKStores is a previous customer's configuration. This project uses similar patterns (change elements in nodes) but is simpler (no HybridInfoservers).

---

## 🔄 Version History & Evolution

**Current Version**: 1.0

**Key Milestones**:
- ✅ Initial implementation with 3 test stores
- ✅ Added combined output mode
- ✅ Added web-ui-config support
- ✅ Changed mandatory walls to only wall 1
- ✅ Added skip_wdm support for stores
- ✅ Swedish character normalization
- ✅ Comprehensive validation

**Future Enhancements** (potential):
- Interactive mode for adding stores
- GUI for configuration management
- Integration with store manager API
- Automated testing suite
- Support for additional wall types
- Batch update capabilities

---

## 📞 Integration Points

### Upstream Dependencies
- `store_wall_mapping.json`: Primary configuration source
- `store_ip_mapping.properties`: Web-UI server IPs
- `template.xml`: Base structure template

### Downstream Consumers
- Store manager application (imports generated XML)
- Manual review processes
- Configuration validation workflows

### External Systems
- None (standalone automation solution)

---

## 🎯 Success Indicators

When this project is working correctly:
- ✅ Generated configurations for all stores successfully
- ✅ Wall configuration changes properly added to CSE-wdm nodes
- ✅ Web-UI configuration changes added based on IP mapping
- ✅ Unique IP addresses assigned per wall per store
- ✅ Server IP addresses configured for web-ui-config
- ✅ Mandatory wall 1 included for all non-skipped stores
- ✅ Optional walls included where specified
- ✅ Proper XML structure and formatting
- ✅ Template-based approach ensures consistency
- ✅ Support for both separate and combined output formats
- ✅ Dual configuration system (wall + web-UI) working seamlessly
- ✅ All validations pass without errors

---

**Last Updated**: 2025-10-07  
**Project Status**: Production-ready  
**Python Version**: 3.x (modern features)  
**Primary Maintainer**: User mpenkava
