# GUI Quick Start Guide

## 🚀 Getting Started in 3 Easy Steps

### Step 1: Launch the Application

**Option A - Windows Users:**
- Double-click `start_gui.bat`

**Option B - All Users:**
- Open terminal in project folder
- Run: `python gui.py`

### Step 2: Generate Configuration

1. **Choose Generation Mode:**
   - ☑️ Generate All Stores (Separate Files) - Creates one XML per store
   - ☐ Generate All Stores (Combined File) - Creates single XML with all stores
   - ☐ Generate Single Store - Pick one store from dropdown

2. **Click "🚀 Generate Configuration" Button**

3. **Watch the Output Log** - See real-time progress

### Step 3: Validate & Access Files

1. **Click "✓ Validate Output" Button** - Checks all generated files

2. **Click "📁 Open Output Folder" Button** - Opens the output directory

Done! Your configuration files are ready to use.

---

## 📋 GUI Interface Guide

### Main Window Sections

```
┌─────────────────────────────────────────────┐
│  🏪 Coop Store Configuration Generator      │
├─────────────────────────────────────────────┤
│                                             │
│  ╔═══════ Configuration Files ═════════╗   │
│  ║ Store Mapping: [store_wall_mapping.json]│
│  ║ Template File: [template.xml]       ║   │
│  ║ Output Directory: [output]          ║   │
│  ╚═════════════════════════════════════╝   │
│                                             │
│  ╔═══ Service Cards Conversion ════════╗   │
│  ║ Excel File: [service-cards.xlsx]    ║   │
│  ║ JSON Output: [service_cards_mapping.json]│
│  ║ [Browse...]                         ║   │
│  ║    [📊 Convert Excel to JSON]       ║   │
│  ╚═════════════════════════════════════╝   │
│                                             │
│  ╔═══════ Store Selection ═════════════╗   │
│  ║ ○ Generate All Stores (Separate Files)  │
│  ║ ○ Generate All Stores (Combined File)   │
│  ║ ○ Generate Single Store              ║   │
│  ║ Select Store: [1038 - Östra - 1038...▼] │
│  ╚═════════════════════════════════════╝   │
│                                             │
│  [🚀 Generate] [✓ Validate] [📁 Open] [🔄] │
│                                             │
│  ╔═══════ Output Log ════════════════╗     │
│  ║ ✓ Loaded 8 stores from mapping    ║     │
│  ║ 🚀 Starting configuration...       ║     │
│  ║ ✓ Generated configuration...       ║     │
│  ║                                    ║     │
│  ╚════════════════════════════════════╝     │
│                                             │
│  Status: Ready                              │
└─────────────────────────────────────────────┘
```

---

## 🎯 Common Tasks

### Task 1: Generate All Store Configs
1. Select "Generate All Stores (Separate Files)"
2. Click "Generate Configuration"
3. Wait for completion message
4. Files appear in `output/` folder

### Task 2: Generate Single Store Config
1. Select "Generate Single Store"
2. Choose store from dropdown (e.g., "1038 - Östra - 1038 Coop Hammarby Sjöstad")
3. Click "Generate Configuration"
4. Check output log for file location

### Task 3: Generate Combined Config
1. Select "Generate All Stores (Combined File)"
2. Click "Generate Configuration"
3. Find `all_stores_config.xml` in output folder

### Task 4: Validate Configurations
1. Generate configurations first
2. Click "Validate Output"
3. Check log for validation results
4. All valid ✅ or see errors ❌

### Task 5: View Generated Files
1. Click "Open Output Folder"
2. File explorer opens automatically
3. Browse XML configuration files

### Task 6: Convert Excel to JSON (Service Cards)
1. Make sure you have pandas installed: `pip install pandas openpyxl`
2. Click "Browse..." button in Service Cards Conversion section
3. Select your `service-cards.xlsx` file
4. Click "📊 Convert Excel to JSON"
5. Watch log for conversion progress
6. Check output for `service_cards_mapping.json`

---

## 💡 Tips & Tricks

### 🎯 Tip 1: Real-Time Feedback
- Watch the Output Log for detailed progress
- Green checkmarks ✓ mean success
- Red X marks ❌ indicate errors

### 🎯 Tip 2: Store Selection
- Type to search in the dropdown
- Store ID and name both appear
- Reload button refreshes the list

### 🎯 Tip 3: Error Handling
- GUI runs tasks in background threads
- Application stays responsive during generation
- Errors appear in popup dialogs AND log

### 🎯 Tip 4: Clear Log
- Use "Clear Log" button to reset output
- Helps when running multiple operations

### 🎯 Tip 5: Validation First
- Always validate after generation
- Catches configuration errors early
- Shows detailed error messages

---

## ⚙️ Configuration Files

### Default Settings (No Changes Needed)
```
Store Mapping:    store_wall_mapping.json
Template File:    template.xml
Output Directory: output
```

### To Customize:
1. Edit text fields in "Configuration Files" section
2. Click "Reload Stores" if mapping file changed
3. Generate configurations with new settings

---

## 🔧 Troubleshooting

### Problem: "No stores found"
**Solution:** 
- Check `store_wall_mapping.json` exists
- Click "🔄 Reload Stores" button
- Verify JSON file is valid

### Problem: "Template file not found"
**Solution:**
- Verify `template.xml` exists in project folder
- Check "Template File" path in GUI
- Use default path: `template.xml`

### Problem: "Generation failed"
**Solution:**
- Read error message in Output Log
- Check file permissions for output folder
- Ensure mapping files have correct format

### Problem: "Validation shows errors"
**Solution:**
- Check Output Log for specific errors
- Common issues: Invalid IPs, missing walls
- Fix data in `store_wall_mapping.json`
- Regenerate configurations

### Problem: GUI window too small
**Solution:**
- Drag window corners to resize
- Output log section expands automatically
- Default size: 800x700 pixels

---

## 🎓 Advanced Features

### Background Processing
- Generation runs in separate thread
- GUI remains responsive
- Can view log during generation

### Cross-Platform
- Works on Windows, macOS, Linux
- "Open Folder" adapts to OS
- Consistent interface everywhere

### No Installation
- Uses Python's built-in tkinter
- No extra packages needed
- Just Python 3.6+

---

## 📞 Need Help?

### Check These First:
1. ✅ Output Log - Shows detailed messages
2. ✅ README.md - Full documentation
3. ✅ Validation output - Specific errors

### Common Questions:

**Q: Can I use CLI instead of GUI?**
A: Yes! All CLI commands still work. GUI is optional.

**Q: Where are generated files saved?**
A: In the `output/` folder by default. Click "Open Folder" to see them.

**Q: Can I generate multiple times?**
A: Yes! Files are overwritten. Validation shows if successful.

**Q: What if I close GUI during generation?**
A: Generation continues in background. Check output folder for files.

---

## ✅ Success Checklist

- [x] GUI launches without errors
- [x] Store list loads (8+ stores)
- [x] Generate button creates files
- [x] Validation passes for all files
- [x] Output folder opens correctly
- [x] Log shows clear messages

**Ready to generate configurations!** 🎉

---

**Version:** 1.0  
**Last Updated:** November 6, 2025  
**Compatible With:** Python 3.6+
