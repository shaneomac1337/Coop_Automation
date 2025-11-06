# GUI Screenshot

The GUI application provides a clean, modern interface for generating store configurations.

## Main Window

```
╔═══════════════════════════════════════════════════════════════════════╗
║  🏪 Coop Store Configuration Generator                                ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────── Configuration Files ─────────────────────┐ ║
║  │                                                                   │ ║
║  │  Store Mapping:    [store_wall_mapping.json              ]       │ ║
║  │                                                                   │ ║
║  │  Template File:    [template.xml                         ]       │ ║
║  │                                                                   │ ║
║  │  Output Directory: [output                               ]       │ ║
║  │                                                                   │ ║
║  └───────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌───────────────────────── Store Selection ───────────────────────┐ ║
║  │                                                                   │ ║
║  │  ⦿ Generate All Stores (Separate Files)                          │ ║
║  │  ○ Generate All Stores (Combined File)                           │ ║
║  │  ○ Generate Single Store                                         │ ║
║  │                                                                   │ ║
║  │  Select Store:  [1038 - Östra - 1038 Coop Hammarby Sjöstad   ▼] │ ║
║  │                                                                   │ ║
║  └───────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║        ┌────────────────┐  ┌──────────────┐  ┌──────────────┐       ║
║        │ 🚀 Generate    │  │ ✓ Validate   │  │ 📁 Open      │  🔄   ║
║        │  Configuration │  │   Output     │  │  Output Folder│       ║
║        └────────────────┘  └──────────────┘  └──────────────┘       ║
║                                                                       ║
║  ┌────────────────────────── Output Log ────────────────────────────┐║
║  │                                                                   │║
║  │  ✓ Loaded 8 stores from store_wall_mapping.json                  │║
║  │  🚀 Starting configuration generation...                          │║
║  │  📦 Generating separate files for all stores...                   │║
║  │     Adding store 1038 to combined configuration...                │║
║  │     Adding store 1161 to combined configuration...                │║
║  │     Adding store 1346 to combined configuration...                │║
║  │     Adding store 1828 to combined configuration...                │║
║  │     Adding store 1677 to combined configuration...                │║
║  │                                                                   │║
║  │  ✅ Generated 8 configuration files!                              │║
║  │     📄 output/store_1038_config.xml                               │║
║  │     📄 output/store_1161_config.xml                               │║
║  │     📄 output/store_1346_config.xml                               │║
║  │     📄 output/store_1828_config.xml                               │║
║  │     📄 output/store_1677_config.xml                               │║
║  │     📄 output/store_1681_config.xml                               │║
║  │     📄 output/store_1664_config.xml                               │║
║  │     📄 output/store_4280_config.xml                               │║
║  │                                                                   ▲║
║  │                                                                   █║
║  │                                                                   ▼║
║  │                           [Clear Log]                             │║
║  └───────────────────────────────────────────────────────────────────┘║
║                                                                       ║
║  Generation completed successfully!                                   ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Key Features Visible

1. **Clean Layout** - Everything organized in clear sections
2. **Visual Feedback** - Emojis and symbols for quick recognition
3. **Store Dropdown** - Easy store selection with full names
4. **Radio Buttons** - Clear choice between generation modes
5. **Large Buttons** - Easy to click, clearly labeled
6. **Scrollable Log** - See detailed progress and results
7. **Status Bar** - Current operation status at bottom

## Color Scheme

The actual GUI uses:
- Standard system colors for native look
- Clear text on light background
- Highlighted buttons for actions
- Scrollable areas with visible scrollbars

## Window Size

- **Default**: 800 x 700 pixels
- **Resizable**: Can be made larger or smaller
- **Centered**: Opens in center of screen

## Font

- **Main Interface**: System default font
- **Log Output**: Monospace font (Consolas/Courier)
- **Title**: Larger, bold font

## To See the Real GUI

Simply run:
```bash
python gui.py
```

Or double-click:
```
start_gui.bat
```

The actual GUI will look better than ASCII art! 😊
