# Building Windows Executable

This guide explains how to create a standalone Windows executable that users can double-click to run, without requiring Python installation.

## Quick Build (Automated)

### For Windows Users
Run the automated build script:
```batch
scripts\build_for_windows.bat
```

### For Cross-Platform Build
```bash
python scripts/build_windows_dist.py
```

## Manual Build Process

### Prerequisites
1. Python 3.8+ installed
2. All Route Planner dependencies installed
3. PyInstaller package

### Step 1: Install Build Dependencies
```bash
pip install pyinstaller pillow
```

### Step 2: Build Executable
```bash
python scripts/build_exe.py
```

### Step 3: Create Distribution Package
```bash
python scripts/build_windows_dist.py
```

## Output Files

After successful build, you'll find in `dist_windows/`:

- **`RoutePlanner.exe`** - Standalone executable (~50-80 MB)
- **`RoutePlanner-Portable.zip`** - Complete portable package
- **`RoutePlanner_Portable/`** - Extracted portable version with documentation

## Distribution Options

### Option 1: Portable ZIP (Recommended)
- Share `RoutePlanner-Portable.zip`
- Users extract and double-click `RoutePlanner.exe`
- No installation needed

### Option 2: Direct Executable  
- Share just `RoutePlanner.exe`
- Single file, ready to run
- Minimal distribution size

### Option 3: Windows Installer
1. Install NSIS (Nullsoft Scriptable Install System)
2. Compile `scripts/installer.nsi`
3. Creates professional Windows installer

## User Experience

**For End Users:**
1. Download the portable ZIP
2. Extract to any folder (Desktop, Documents, etc.)
3. Double-click `RoutePlanner.exe`
4. Application starts immediately - no setup required!

**Benefits:**
- No Python installation needed
- No command line usage
- Works on Windows 7, 8, 10, 11
- Professional look and feel
- Error handling with user-friendly messages

## Technical Details

### What's Included in the Executable
- Complete Python runtime
- All required packages (PyQt5, Folium, etc.)
- Application code and assets
- Optimized for size and startup speed

### System Requirements for Built Executable
- Windows 7 or later (64-bit recommended)
- 4GB RAM minimum
- 100MB+ free disk space
- Internet connection for map data

### Build Specifications
- PyInstaller with `--onefile` option
- Windows-optimized launcher with error handling
- Embedded icon and version information
- Code signing ready (add certificate for distribution)

## Troubleshooting Build Issues

### Common Problems

**1. "PyInstaller not found"**
```bash
pip install pyinstaller --upgrade
```

**2. "Missing module" errors**
Add to the build script:
```python
--hidden-import module_name
```

**3. Large executable size**
- Normal for first build (50-80 MB)
- Includes entire Python runtime
- Consider UPX compression for smaller size

**4. Antivirus false positives**
- Common with PyInstaller executables
- Submit to antivirus vendors for whitelisting
- Consider code signing certificate

### Testing the Executable
```bash
# Test on clean Windows VM
# Verify no Python installation needed
# Check startup time and functionality
```

## Distribution Best Practices

1. **Test thoroughly** on different Windows versions
2. **Include documentation** (README.txt, LICENSE)
3. **Use descriptive names** (`RoutePlanner-v1.0.0-Windows.zip`)
4. **Provide support** (GitHub issues, contact info)
5. **Consider code signing** for trusted distribution

## Advanced Options

### Code Signing
```bash
# Add to PyInstaller command:
--uac-admin  # Request admin privileges
--version-file version.txt  # Version information
```

### Custom Icon
```bash
# Already included in build script:
--icon icon.ico
```

### Optimization
```bash
# Additional PyInstaller options:
--optimize 2      # Python optimization
--strip          # Remove debug symbols
--upx-dir path   # UPX compression
```

## Release Workflow

1. **Build executable** with latest code
2. **Test on clean Windows system**
3. **Create portable package** with documentation
4. **Upload to GitHub Releases**
5. **Update README** with download links
6. **Announce release** to users

This approach makes Route Planner accessible to all Windows users, regardless of their technical background!
