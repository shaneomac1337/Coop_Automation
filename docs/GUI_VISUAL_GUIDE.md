# 🎨 GUI Visual Guide

## 🖥️ What You'll See

When you start the GUI, you'll see a clean interface divided into clear sections:

---

## 📸 Interface Layout

### 🏷️ **Top Section: Title**
```
🏪 Coop Store Configuration Generator
```
Large, friendly title at the top

---

### ⚙️ **Section 1: Configuration Files**
```
╔═══════════════════════════════════╗
║  Configuration Files              ║
║                                   ║
║  Store Mapping:                   ║
║  [store_wall_mapping.json]        ║
║                                   ║
║  Template File:                   ║
║  [template.xml]                   ║
║                                   ║
║  Output Directory:                ║
║  [output]                         ║
╚═══════════════════════════════════╝
```

**What it does:** Shows file paths  
**What to do:** Usually leave as-is (defaults work!)

---

### 🎯 **Section 2: Store Selection**
```
╔═══════════════════════════════════╗
║  Store Selection                  ║
║                                   ║
║  ⦿ Generate All Stores (Separate) ║
║  ○ Generate All Stores (Combined) ║
║  ○ Generate Single Store          ║
║                                   ║
║  Select Store:                    ║
║  [1038 - Östra - 1038 Coop Ham...▼]║
╚═══════════════════════════════════╝
```

**What it does:** Choose what to generate  
**What to do:** Click radio button, pick store if needed

---

### 🎬 **Section 3: Action Buttons**
```
┌──────────┐ ┌─────────┐ ┌──────────┐ ┌────┐
│🚀 Generate│ │✓Validate│ │📁 Open   │ │🔄  │
│   Config  │ │ Output  │ │  Folder  │ │    │
└──────────┘ └─────────┘ └──────────┘ └────┘
```

**What each does:**
- **🚀 Generate Configuration** - Creates XML files
- **✓ Validate Output** - Checks if files are correct
- **📁 Open Output Folder** - Opens file explorer
- **🔄 Reload Stores** - Refreshes store list

---

### 📝 **Section 4: Output Log**
```
╔═══════════════════════════════════╗
║  Output Log                       ║
║                                   ║
║  ✓ Loaded 8 stores from mapping   ║
║  🚀 Starting configuration...     ║
║  📦 Generating separate files...  ║
║     📄 output/store_1038_config.xml
║     📄 output/store_1161_config.xml
║  ✅ Generated 8 configuration files!
║                                   ║
║  [Clear Log]                      ║
╚═══════════════════════════════════╝
```

**What it does:** Shows what's happening  
**What to watch:** 
- ✓ = Success (green)
- ❌ = Error (red)
- ⚠️ = Warning (yellow)
- 🚀 = Starting
- 📦 = Processing
- ✅ = Complete

---

### 📊 **Section 5: Status Bar**
```
┌─────────────────────────────────────┐
│ Ready                               │
└─────────────────────────────────────┘
```

**What it shows:** Current operation status  
**Status examples:**
- "Ready" - Waiting for action
- "Generating..." - Creating files
- "Validating..." - Checking files
- "Generation completed successfully!" - Done!

---

## 🎮 Step-by-Step Visual Walkthrough

### 🎯 **Scenario 1: Generate All Stores**

**Step 1:** Select the radio button
```
⦿ Generate All Stores (Separate Files)  ← Click here
○ Generate All Stores (Combined File)
○ Generate Single Store
```

**Step 2:** Click the big button
```
┌──────────────────────┐
│  🚀 Generate         │  ← Click here
│     Configuration    │
└──────────────────────┘
```

**Step 3:** Watch the log fill up
```
✓ Loaded 8 stores from mapping
🚀 Starting configuration generation...
📦 Generating separate files for all stores...
   Adding store 1038...
   Adding store 1161...
   ...
✅ Generated 8 configuration files!
```

**Step 4:** See success message
```
┌────────────────────────────┐
│      ✅ Success            │
│                            │
│  Configuration generated   │
│  successfully!             │
│                            │
│         [ OK ]             │
└────────────────────────────┘
```

---

### 🎯 **Scenario 2: Generate Single Store**

**Step 1:** Select single store mode
```
○ Generate All Stores (Separate Files)
○ Generate All Stores (Combined File)
⦿ Generate Single Store                   ← Click here
```

**Step 2:** Pick a store from dropdown
```
Select Store:
┌─────────────────────────────────────┐
│ 1038 - Östra - 1038 Coop Hammarby...│ ← Click ▼
└─────────────────────────────────────┘
  1038 - Östra - 1038 Coop Hammarby...  ← Pick one
  1161 - Östra - 1161 Coop Krokek
  1346 - Väst - 1346 Coop Mellerud
  1828 - Östra - 1828 Stora Coop Spånga
  ...
```

**Step 3:** Generate
```
┌──────────────────────┐
│  🚀 Generate         │  ← Click
│     Configuration    │
└──────────────────────┘
```

**Step 4:** Watch log
```
✓ Loaded 8 stores from mapping
🚀 Starting configuration generation...
📦 Generating configuration for store 1038...
✅ Generated configuration file!
   📄 output/store_1038_config.xml
```

---

### 🎯 **Scenario 3: Validate Results**

**Step 1:** Click validate button
```
┌──────────┐ ┌─────────┐
│🚀Generate│ │✓Validate│  ← Click this one
└──────────┘ └─────────┘
```

**Step 2:** Watch validation
```
🔍 Starting validation...
Validating: output/store_1038_config.xml
   ✅ Valid configuration
Validating: output/store_1161_config.xml
   ✅ Valid configuration
...
📊 Validation Summary:
   ✅ Valid files: 8
   ❌ Invalid files: 0
   📁 Total files: 8
```

**Step 3:** See result
```
┌────────────────────────────┐
│      ✅ Success            │
│                            │
│  All configurations are    │
│  valid!                    │
│                            │
│         [ OK ]             │
└────────────────────────────┘
```

---

### 🎯 **Scenario 4: Open Output Folder**

**Step 1:** Click folder button
```
┌─────────┐ ┌──────────┐
│✓Validate│ │📁 Open   │  ← Click here
└─────────┘ │  Folder  │
            └──────────┘
```

**Step 2:** File explorer opens automatically!
```
📁 output/
   📄 store_1038_config.xml
   📄 store_1161_config.xml
   📄 store_1346_config.xml
   📄 store_1828_config.xml
   ...
```

---

## 🎨 Color Guide

The GUI uses visual cues to help you:

### ✅ Success Messages (Green)
- "✓ Loaded stores"
- "✅ Generated successfully"
- "Valid configuration"

### ❌ Error Messages (Red)
- "❌ Error: File not found"
- "Invalid IP address"
- "Missing mandatory wall"

### ⚠️ Warning Messages (Yellow)
- "⚠️ Warning: IP mapping file not found"
- "No XML files found"

### 📊 Info Messages (Blue)
- "🚀 Starting..."
- "📦 Generating..."
- "🔍 Validating..."

---

## 🎯 Button States

Buttons change to show what's happening:

### 🟢 Active State
```
┌──────────────────┐
│  🚀 Generate     │  ← Clickable
│     Configuration│
└──────────────────┘
```

### 🔴 Disabled State (During Operation)
```
┌──────────────────┐
│  🚀 Generate     │  ← Grayed out
│     Configuration│  (Please wait...)
└──────────────────┘
```

**Why?** Prevents clicking twice while processing!

---

## 💡 Visual Tips

### 🎯 Tip 1: Watch the Status Bar
```
Bottom of window:
┌─────────────────────────────────┐
│ Generating... ⏳                │  ← Changes during operations
└─────────────────────────────────┘
```

### 🎯 Tip 2: Scroll the Log
```
If log is full:
╔═══════════════════╗
║ Lots of text...   ║
║ More text...      ║
║ Even more...      ║  ← Scroll bar appears
║ ▲                 ║     automatically
║ █                 ║
║ ▼                 ║
╚═══════════════════╝
```

### 🎯 Tip 3: Resize Window
```
Grab any corner:
┌─────────────────┐
│  GUI Window     │
│                 │
│                 ╱  ← Drag to resize
└────────────────╱
```

### 🎯 Tip 4: Clear Log When Needed
```
Log getting cluttered?
┌────────────┐
│ Clear Log  │  ← Click to reset
└────────────┘
```

---

## 🎊 Success Indicators

### You'll Know It Worked When You See:

1. **✅ Popup Dialog**
```
┌────────────────────────────┐
│      ✅ Success            │
│                            │
│  Configuration generated   │
│  successfully!             │
│                            │
│         [ OK ]             │
└────────────────────────────┘
```

2. **✅ Green Checkmarks in Log**
```
✅ Generated 8 configuration files!
   📄 output/store_1038_config.xml
   📄 output/store_1161_config.xml
   ...
```

3. **✅ Valid in Status Bar**
```
┌─────────────────────────────────────┐
│ Generation completed successfully! ✅│
└─────────────────────────────────────┘
```

4. **✅ Files in Output Folder**
```
📁 output/
   📄 store_1038_config.xml  ← New files!
   📄 store_1161_config.xml  ← Just created!
```

---

## 🚨 Error Indicators

### You'll Know There's a Problem When You See:

1. **❌ Error Popup**
```
┌────────────────────────────┐
│      ❌ Error              │
│                            │
│  Configuration generation  │
│  failed:                   │
│  File not found            │
│                            │
│         [ OK ]             │
└────────────────────────────┘
```

2. **❌ Red X in Log**
```
❌ Error: File not found: template.xml
```

3. **❌ Error Status**
```
┌─────────────────────────────────┐
│ Generation failed ❌            │
└─────────────────────────────────┘
```

**What to do:** Read the error message and fix the issue!

---

## 🎓 Learning Path

### 👶 Beginner (First Time)
1. Just click "🚀 Generate Configuration" with defaults
2. Watch the log to see what happens
3. Click "📁 Open Output Folder" to see results

### 🎓 Intermediate (Getting Comfortable)
1. Try different generation modes
2. Use validation after generation
3. Pick specific stores from dropdown

### 🚀 Advanced (Power User)
1. Generate combined files
2. Understand log messages
3. Fix validation errors
4. Customize configuration paths

---

## 🎯 Quick Reference Card

```
╔══════════════════════════════════════════════════╗
║  🏪 COOP STORE CONFIG GENERATOR - QUICK GUIDE    ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  START:                                          ║
║  • Double-click: start_gui.bat                   ║
║  • Or run: python gui.py                         ║
║                                                  ║
║  GENERATE ALL:                                   ║
║  1. Select: ⦿ Generate All Stores (Separate)    ║
║  2. Click: 🚀 Generate Configuration            ║
║  3. Wait for: ✅ Success message                ║
║                                                  ║
║  GENERATE ONE:                                   ║
║  1. Select: ⦿ Generate Single Store             ║
║  2. Pick store from dropdown                     ║
║  3. Click: 🚀 Generate Configuration            ║
║                                                  ║
║  VALIDATE:                                       ║
║  • Click: ✓ Validate Output                     ║
║  • Check log for results                         ║
║                                                  ║
║  VIEW FILES:                                     ║
║  • Click: 📁 Open Output Folder                 ║
║                                                  ║
║  SYMBOLS:                                        ║
║  ✓ = Success  |  ❌ = Error  |  ⚠️ = Warning    ║
║  🚀 = Starting  |  📦 = Processing  |  ✅ = Done ║
║                                                  ║
╚══════════════════════════════════════════════════╝
```

---

**Remember:** The GUI is designed to be simple and safe. You can't break anything by clicking buttons. Just watch the log and follow the messages! 🎉

---

**Visual Guide Version:** 1.0  
**Last Updated:** November 6, 2025  
**Made with:** ❤️ and lots of emojis
