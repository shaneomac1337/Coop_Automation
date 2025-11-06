# Configuration Files

This folder contains all configuration, mapping, and template files used by the Store Configuration Generator.

## 📁 Folder Structure

```
config/
├── templates/       # XML template files
├── mappings/        # Store and service mappings
└── examples/        # Example configuration files
```

## 📄 File Descriptions

### Templates (`templates/`)

- **`template.xml`** - Main store configuration template
  - Base XML structure for store configurations
  - Contains placeholders that get populated with store-specific data

- **`web-ui-config.xml`** - Web UI configuration template
  - Configuration for web interface settings

- **`wall-config.xml`** - Wall display configuration template
  - Template for wall display settings

### Mappings (`mappings/`)

- **`store_wall_mapping.json`** - Store to wall mapping
  - Maps store numbers to wall configurations
  - Defines which walls are active for each store
  - Contains store-specific settings

- **`service_cards_mapping.json`** - Service cards configuration
  - Maps service card IDs to display configurations
  - Contains service card names and settings
  - Generated from Excel files using the converter tool

- **`store_ip_mapping.properties`** - Store IP addresses
  - Maps store numbers to IP addresses
  - Used for network configuration in web-ui-config

### Examples (`examples/`)

- **`GKStoresConfig_Prod_001only_updated_capital_S.xml`** - Production example
  - Real-world example of a generated configuration
  - Reference for understanding output format

## 🔧 Usage

### In Command Line

```bash
# Use default files (recommended)
python src/generate_store_config.py --all

# Use custom files
python src/generate_store_config.py --all \
    --mapping config/mappings/store_wall_mapping.json \
    --template config/templates/template.xml \
    --ip-mapping config/mappings/store_ip_mapping.properties \
    --service-cards config/mappings/service_cards_mapping.json
```

### In GUI

The GUI automatically uses files from `config/` folders. File paths are pre-configured:
- Store Mapping: `config/mappings/store_wall_mapping.json`
- Template: `config/templates/template.xml`
- IP Mapping: `config/mappings/store_ip_mapping.properties`
- Service Cards: `config/mappings/service_cards_mapping.json`

## 📝 File Formats

### store_wall_mapping.json

```json
{
  "1234": {
    "storeNumber": "1234",
    "storeName": "Example Store",
    "wallChanges": [
      {
        "action": "add",
        "wall": {
          "id": "Wall_1",
          "name": "Main Display",
          "ipAddress": "192.168.1.10"
        }
      }
    ]
  }
}
```

### service_cards_mapping.json

```json
{
  "CARD001": {
    "id": "CARD001",
    "name": "Service Card 1",
    "enabled": true,
    "settings": { }
  }
}
```

### store_ip_mapping.properties

```properties
1234=192.168.1.100
5678=192.168.2.100
```

## ⚠️ Important Notes

1. **Backup Before Editing**: Always backup configuration files before making changes
2. **JSON Validation**: Ensure JSON files are valid (use a JSON validator)
3. **IP Addresses**: Use valid IP address formats in properties files
4. **Store Numbers**: Store numbers must match across all mapping files
5. **Character Encoding**: Files must be UTF-8 encoded

## 🔄 Updating Configuration

### Adding a New Store

1. Add entry to `store_wall_mapping.json`
2. Add IP address to `store_ip_mapping.properties`
3. Add any service cards to `service_cards_mapping.json`
4. Generate configuration using the tool

### Modifying Templates

1. Edit the appropriate template XML file
2. Ensure XML is valid (use XML validator)
3. Test with a single store before batch generation

### Converting Excel to JSON

Use the GUI or command line converter:

```bash
python src/convert_service_cards_to_json.py input.xlsx output.json
```

Or use the GUI's "Service Cards Conversion" section.

## 🛡️ Version Control

- ✅ **DO commit**: Template files, mapping files
- ❌ **DON'T commit**: Sensitive production data, temporary files
- 📝 **Consider**: Using `.example` files for sensitive configurations

## 📚 Related Documentation

- See `../docs/README.md` for project overview
- See `../docs/GUI_QUICKSTART.md` for GUI usage
- See `../docs/SERVICE_CARDS_IMPLEMENTATION.md` for service cards details
