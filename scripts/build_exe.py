#!/usr/bin/env python3
"""
Build Script for Creating Standalone Executable

This script uses PyInstaller to create a standalone .exe file
that includes all dependencies and can run without Python installed.

Usage:
    python build_exe.py
"""

import subprocess
import sys
from pathlib import Path
import shutil


def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("❌ PyInstaller is not installed")
        print("\nTo install PyInstaller, run:")
        print("   pip install pyinstaller")
        return False


def clean_build_folders():
    """Clean up previous build artifacts."""
    folders_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']
    
    print("\n🧹 Cleaning previous build artifacts...")
    
    for folder in folders_to_clean:
        if Path(folder).exists():
            shutil.rmtree(folder)
            print(f"   Removed: {folder}/")
    
    for pattern in files_to_clean:
        for file in Path('.').glob(pattern):
            file.unlink()
            print(f"   Removed: {file}")


def build_executable():
    """Build the standalone executable using PyInstaller."""
    print("\n🚀 Building standalone executable...")
    print("   This may take a few minutes...\n")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single .exe file
        '--windowed',                   # No console window (GUI only)
        '--name=CoopStoreConfig',       # Name of the executable
        '--icon=NONE',                  # No icon (can add later)
        '--add-data=config;config',     # Include entire config folder
        '--hidden-import=pandas',       # Ensure pandas is included
        '--hidden-import=openpyxl',     # Ensure openpyxl is included
        'src/gui.py'                    # Main script
    ]
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ Build successful!")
        print("\n📦 Executable created:")
        print(f"   Location: dist/CoopStoreConfig.exe")
        print(f"   Size: ~{get_file_size('dist/CoopStoreConfig.exe')}")
        return True
    else:
        print("\n❌ Build failed!")
        print("\nError output:")
        print(result.stderr)
        return False


def get_file_size(filepath):
    """Get file size in MB."""
    try:
        size_bytes = Path(filepath).stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f} MB"
    except:
        return "Unknown"


def create_distribution_package():
    """Create a distribution package with the executable and required files."""
    print("\n📦 Creating distribution package...")
    
    dist_folder = Path('dist/CoopStoreConfig')
    dist_folder.mkdir(exist_ok=True)
    
    # Copy executable
    exe_source = Path('dist/CoopStoreConfig.exe')
    if exe_source.exists():
        shutil.copy2(exe_source, dist_folder / 'CoopStoreConfig.exe')
        print("   ✓ Copied executable")
    
    # Copy required files
    files_to_copy = [
        'README.md',
        'docs/GUI_QUICKSTART.md'
    ]
    
    for file in files_to_copy:
        source = Path('..') / file if not Path(file).exists() else Path(file)
        if source.exists():
            shutil.copy2(source, dist_folder / Path(file).name)
            print(f"   ✓ Copied {Path(file).name}")
    
    # Copy config folder
    config_source = Path('../config')
    config_dest = dist_folder / 'config'
    if config_source.exists():
        shutil.copytree(config_source, config_dest, dirs_exist_ok=True)
        print(f"   ✓ Copied config/ folder")
    
    # Create output folder
    (dist_folder / 'output').mkdir(exist_ok=True)
    print("   ✓ Created output folder")
    
    # Create README for distribution
    create_dist_readme(dist_folder)
    
    print(f"\n✅ Distribution package ready!")
    print(f"   Location: {dist_folder}")
    print(f"\n📋 Package contents:")
    print(f"   - CoopStoreConfig.exe (standalone executable)")
    print(f"   - Configuration files (JSON, XML, properties)")
    print(f"   - Documentation (README, Quick Start)")
    print(f"   - output/ (for generated files)")


def create_dist_readme(dist_folder):
    """Create a README for the distribution package."""
    readme_content = """# Coop Store Configuration Generator

## Quick Start

1. **Double-click** `CoopStoreConfig.exe` to launch the application
2. **Select** your generation mode
3. **Click** "Generate Configuration" button
4. **Done!** Find your files in the `output/` folder

## No Installation Required

This is a standalone application - no Python or dependencies needed!

## Features

- Generate store configurations
- Validate generated files
- Convert Excel to JSON
- Open output folder directly

## Documentation

See `GUI_QUICKSTART.md` for detailed instructions.

## Configuration Files

- `store_wall_mapping.json` - Store and wall IP mappings
- `template.xml` - Base structure template
- `store_ip_mapping.properties` - Server IP mappings
- `service_cards_mapping.json` - Service card mappings

## Need Help?

Check the documentation files or contact support.

---

**Version:** 1.0  
**Built:** November 6, 2025
"""
    
    with open(dist_folder / 'README.txt', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    print("   ✓ Created distribution README")


def main():
    """Main build process."""
    print("=" * 60)
    print("  Coop Store Configuration Generator")
    print("  Executable Build Script")
    print("=" * 60)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("\n⚠️  Please install PyInstaller first:")
        print("   pip install pyinstaller")
        sys.exit(1)
    
    # Clean previous builds
    clean_build_folders()
    
    # Build executable
    if not build_executable():
        print("\n❌ Build process failed!")
        sys.exit(1)
    
    # Create distribution package
    create_distribution_package()
    
    print("\n" + "=" * 60)
    print("  Build Complete! 🎉")
    print("=" * 60)
    print("\n📦 Your executable is ready to use!")
    print("\n🚀 To test it:")
    print("   1. Navigate to: dist/CoopStoreConfig/")
    print("   2. Double-click: CoopStoreConfig.exe")
    print("\n📤 To distribute:")
    print("   1. Zip the entire 'dist/CoopStoreConfig/' folder")
    print("   2. Send to users")
    print("   3. Users just unzip and run the .exe!")
    print("\n✅ No Python installation required on target machines!")


if __name__ == "__main__":
    main()
