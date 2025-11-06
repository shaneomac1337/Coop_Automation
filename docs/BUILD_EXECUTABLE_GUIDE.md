# Building Standalone Executable Guide

## 🎯 Goal

Create a standalone `.exe` file that runs without Python installed!

---

## 📋 Prerequisites

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2 (Optional): Install pandas for Excel conversion

```bash
pip install pandas openpyxl
```

**Note:** If you don't need Excel conversion, you can skip this.

---

## 🚀 Quick Build

### Method 1: Use the Build Script (Recommended)

```bash
python build_exe.py
```

**That's it!** The script will:
- ✅ Check dependencies
- ✅ Clean previous builds
- ✅ Build the executable
- ✅ Create distribution package
- ✅ Copy all required files

**Output:** `dist/CoopStoreConfig/` folder ready to distribute!

### Method 2: Manual PyInstaller Command

```bash
pyinstaller --onefile --windowed --name=CoopStoreConfig ^
    --add-data="store_wall_mapping.json;." ^
    --add-data="template.xml;." ^
    --add-data="store_ip_mapping.properties;." ^
    --add-data="service_cards_mapping.json;." ^
    --hidden-import=pandas ^
    --hidden-import=openpyxl ^
    gui.py
```

**Output:** `dist/CoopStoreConfig.exe`

---

## 📦 What You Get

### After Running `build_exe.py`:

```
dist/
└── CoopStoreConfig/
    ├── CoopStoreConfig.exe          ← The standalone executable!
    ├── store_wall_mapping.json      ← Configuration files
    ├── template.xml
    ├── store_ip_mapping.properties
    ├── service_cards_mapping.json
    ├── README.txt                    ← Simple instructions
    ├── GUI_QUICKSTART.md             ← Detailed guide
    └── output/                       ← Empty folder for results
```

### File Size

- **Executable:** ~50-80 MB (includes Python + all dependencies)
- **Total package:** ~55-85 MB

**Why so large?** It includes:
- Python interpreter
- tkinter GUI framework
- pandas library (if included)
- openpyxl library (if included)
- All your code

---

## 🎁 Distribution

### Option 1: Zip the Folder

```powershell
# PowerShell
Compress-Archive -Path "dist\CoopStoreConfig" -DestinationPath "CoopStoreConfig_v1.0.zip"
```

```bash
# Or manually
Right-click "dist/CoopStoreConfig" → Send to → Compressed (zipped) folder
```

### Option 2: Create Installer (Advanced)

Use tools like:
- **Inno Setup** (free) - Create professional installer
- **NSIS** (free) - Nullsoft installer
- **Advanced Installer** (paid) - Feature-rich

---

## 📤 Sharing with Users

### What to Send

**Send the entire `CoopStoreConfig` folder (or zip file)**

### User Instructions

1. **Extract** the zip file (if zipped)
2. **Double-click** `CoopStoreConfig.exe`
3. **Use the GUI** - No installation needed!

### Requirements for Users

✅ **Windows 10/11** (any version)  
✅ **No Python required**  
✅ **No dependencies required**  
✅ **No admin rights required** (usually)

---

## 🔧 Customization

### Change Executable Name

Edit `build_exe.py`:
```python
'--name=YourAppName',  # Change this line
```

### Add Application Icon

1. Create or find an `.ico` file (e.g., `icon.ico`)
2. Edit `build_exe.py`:
```python
'--icon=icon.ico',  # Change from '--icon=NONE'
```

### Include Additional Files

Edit `build_exe.py`:
```python
files_to_copy = [
    'store_wall_mapping.json',
    'template.xml',
    # Add more files here
    'your_file.txt',
]
```

---

## 🐛 Troubleshooting

### Problem: "PyInstaller not found"

**Solution:**
```bash
pip install pyinstaller
```

### Problem: "Module not found" error when running .exe

**Solution:** Add hidden imports in `build_exe.py`:
```python
'--hidden-import=module_name',
```

### Problem: Antivirus blocks the .exe

**Solution:**
- This is normal for PyInstaller executables
- Add exception in antivirus software
- Or use code signing certificate (for professional distribution)

### Problem: .exe is too large

**Solutions:**
1. **Exclude pandas** if not needed:
   ```python
   # Remove these lines from build_exe.py:
   '--hidden-import=pandas',
   '--hidden-import=openpyxl',
   ```
   Size reduction: ~30-40 MB

2. **Use UPX compression:**
   ```bash
   # Install UPX first: https://upx.github.io/
   pyinstaller --onefile --upx-dir=C:\path\to\upx ...
   ```

### Problem: Slow startup

**Normal behavior:**
- First run: 5-10 seconds (extracting)
- Subsequent runs: 2-5 seconds

**Faster alternative:** Use `--onedir` instead of `--onefile`
```python
'--onedir',  # Creates folder with DLLs (faster startup)
```

---

## 🎨 Build Options Explained

### `--onefile`
- Creates single `.exe` file
- Easier to distribute
- Slower startup (extracts to temp folder)

### `--windowed`
- No console window
- Pure GUI application
- Use `--console` to see debug output during development

### `--name=CoopStoreConfig`
- Sets executable name
- Default would be `gui.exe`

### `--add-data`
- Bundles data files into executable
- Format: `source;destination` (Windows)
- Format: `source:destination` (Linux/Mac)

### `--hidden-import`
- Forces inclusion of modules
- Needed when PyInstaller can't detect imports
- Required for pandas, openpyxl, etc.

---

## 📊 Build Process Timeline

1. **Install PyInstaller** - 1 minute
2. **Run build script** - 2-5 minutes
3. **Test executable** - 1 minute
4. **Create distribution** - Done automatically!

**Total:** ~5-10 minutes

---

## ✅ Verification Checklist

After building, verify:

- [ ] `CoopStoreConfig.exe` exists in `dist/CoopStoreConfig/`
- [ ] Double-clicking `.exe` launches GUI
- [ ] All configuration files are present
- [ ] Store list loads correctly
- [ ] Generation works
- [ ] Validation works
- [ ] Excel conversion works (if pandas included)
- [ ] Output folder opens correctly

---

## 🎯 Best Practices

### For Development
```bash
# Keep console window for debugging
pyinstaller --onefile --console --name=CoopStoreConfig gui.py
```

### For Production
```bash
# Use the build script
python build_exe.py
```

### For Testing
1. Test on clean Windows machine
2. No Python installed
3. Fresh user account
4. Different Windows versions

---

## 📚 Advanced Topics

### Multi-Platform Builds

**Windows executable** (.exe):
- Build on Windows machine

**macOS application** (.app):
- Build on macOS machine
- Use same PyInstaller commands

**Linux binary**:
- Build on Linux machine
- Use same PyInstaller commands

**Note:** Must build on target platform!

### Code Signing

For professional distribution:
1. Get code signing certificate
2. Sign the executable:
   ```bash
   signtool sign /f certificate.pfx /p password CoopStoreConfig.exe
   ```

### Automated Builds

Use GitHub Actions or similar:
```yaml
# .github/workflows/build.yml
- name: Build executable
  run: python build_exe.py
```

---

## 🎁 Distribution Checklist

Ready to distribute? Check:

- [ ] Tested on clean machine
- [ ] All features work
- [ ] Documentation included
- [ ] Version number set
- [ ] Release notes written
- [ ] Antivirus scan completed
- [ ] File size acceptable
- [ ] Startup time acceptable

---

## 💡 Tips & Tricks

### Tip 1: Faster Rebuilds

During development:
```bash
# Don't clean build folder
pyinstaller gui.spec  # Reuses previous build
```

### Tip 2: Debug Mode

If exe doesn't work:
```bash
# Build with console window
pyinstaller --console gui.py
# See error messages in console
```

### Tip 3: Reduce Size

Exclude test files:
```python
'--exclude-module=pytest',
'--exclude-module=unittest',
```

### Tip 4: Faster Startup

Use `--onedir` mode:
- Folder with multiple files
- Much faster startup
- Slightly harder to distribute

---

## 🔗 Resources

### PyInstaller Documentation
https://pyinstaller.org/en/stable/

### Common Issues
https://github.com/pyinstaller/pyinstaller/wiki/If-Things-Go-Wrong

### UPX Compression
https://upx.github.io/

---

## 🎉 Success!

Once built, you have:
- ✅ Standalone executable
- ✅ No Python required
- ✅ Easy distribution
- ✅ Professional appearance
- ✅ Works on any Windows machine

**Just zip and share!** 📦

---

## 📞 Need Help?

### Build Issues
- Check PyInstaller version: `pyinstaller --version`
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Check dependencies: `pip list`

### Runtime Issues
- Test with console mode first
- Check Windows Event Viewer for errors
- Run from command prompt to see errors

---

**Last Updated:** November 6, 2025  
**PyInstaller Version:** 6.x+  
**Tested On:** Windows 10/11

**Happy Building!** 🚀
