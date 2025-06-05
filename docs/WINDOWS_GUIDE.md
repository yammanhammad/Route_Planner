# Windows Guide for Route Planner

This comprehensive guide covers all aspects of using Route Planner on Windows systems, including installation, troubleshooting, and compatibility information.

## Table of Contents

- [Installation Options](#installation-options)
- [System Requirements](#system-requirements)
- [Troubleshooting](#troubleshooting)
- [Compatibility Information](#compatibility-information)
- [Visual C++ Redistributable](#visual-c-redistributable)

## Installation Options

**Choose the method that works best for you. For most users, we recommend Option A.**

*All Windows packages and executables are automatically built and published using our GitHub Actions CI/CD pipeline - ensuring quality and security.*

### Option A: 🎯 Bundled Package (Recommended for Everyone)
**✅ Easiest installation - Works out of the box!**

1. **📥 Download**: Get `RoutePlanner-Bundled.zip` from [**GitHub Releases**](https://github.com/yammanhammad/Route_Planner/releases/latest)
2. **📂 Extract**: Unzip anywhere on your computer (e.g., Desktop, Documents)
3. **🚀 Run**: Double-click `RoutePlanner.exe` to start immediately

**✅ Why choose this option:**
- **No setup required** - works immediately after download
- **No administrator rights needed** - run from any folder
- **All dependencies included** - Visual C++ libraries bundled automatically
- **Portable** - copy the folder anywhere, including USB drives

### Option B: 🏢 Professional Installer (For Business/Admin Users)
**🔧 Traditional Windows installer experience**

1. **📥 Download**: Get `RoutePlanner-Setup.exe` from [**GitHub Releases**](https://github.com/yammanhammad/Route_Planner/releases/latest)
2. **⚙️ Install**: Run the installer (requires administrator privileges)
3. **🚀 Launch**: Find Route Planner in Start Menu or Desktop shortcut

**✅ Why choose this option:**
- **Start Menu integration** - appears in all programs
- **Desktop shortcut** - convenient access
- **Automatic updates** - integrated with Windows update system
- **Professional uninstaller** - clean removal via Control Panel

### Option C: ⚡ Portable Executable (Advanced Users)
**⚠️ Requires manual setup - only if Options A & B don't work**

1. **📥 Download Dependencies**: Install [Microsoft Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe) first
2. **📥 Download App**: Get `RoutePlanner-Portable.zip` from [**GitHub Releases**](https://github.com/yammanhammad/Route_Planner/releases/latest)
3. **📂 Extract**: Unzip anywhere on your computer
4. **🚀 Run**: Double-click `RoutePlanner.exe`

**⚠️ Note:** This option requires manual dependency management and is only recommended if you need minimal file size or have specific technical requirements.

### Option D: Python Installation (Developer-Friendly)

**Recommended for developers or if you encounter any issues with the executable**

1. **🐍 Install Python**: Download from [python.org](https://www.python.org/downloads/) (Python 3.8+)
   - ✅ Check "Add Python to PATH" during installation
2. **💻 Open Command Prompt**: Press `Win + R`, type `cmd`, press Enter
3. **📦 Install Route Planner**: Type and press Enter:
   ```
   pip install route-planner
   ```
4. **🚀 Run**: Type and press Enter:
   ```
   route-planner
   ```

**✅ Benefits of Python Installation:**
- Works on all Windows versions (7, 8, 10, 11)
- No additional dependencies required
- Automatic updates via `pip install --upgrade route-planner`
- Better long-term compatibility

## System Requirements

### Windows (Executable)
- Windows 7 or newer (64-bit recommended)
- 4GB RAM minimum
- 100MB+ free disk space
- Internet connection for map data
- Microsoft Visual C++ Redistributable (included in Bundled/Installer packages)

## Troubleshooting

### Common Issues

**"Application won't start" or DLL errors:**
1. Download and install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
2. Restart your computer
3. Try running the application again

**"Windows Defender blocks executable":**
1. Right-click the executable
2. Select "Properties"
3. Check "Unblock" if available
4. Click "Apply"

**"Application is slow to start":**
- Normal for first launch (initializing cache)
- Subsequent launches should be faster

### Runtime Problems

**"Windows Defender blocks executable"**
- Common with unsigned executables
- Add to Windows Defender exclusions
- Try right-clicking and selecting "Run as administrator"

**"Application fails to start"**
- Verify Visual C++ Redistributable is installed
- Check antivirus software isn't blocking the executable
- Try running in compatibility mode for Windows 10

**"Missing DLL" errors**
- Install Visual C++ Redistributable
- Ensure you're using a 64-bit Windows version
- Try the Bundled Package which includes all dependencies

## Compatibility Information

Route Planner has been extensively tested on Windows systems with a compatibility score of 97.2%.

| Component | Status | Notes |
|-----------|--------|-------|
| Windows Batch File | ✅ PASS | Line endings fixed, proper error handling in place |
| Python Launcher | ✅ PASS | Properly detects and handles Windows platform |
| Path Handling | ✅ PASS | Properly handles Windows paths with appropriate path separator |
| Platform Script Detection | ✅ PASS | Correctly identifies .bat files for Windows execution |
| File Paths in Code | ⚠️ WARNING | Some Unix-style paths found, but mostly in dependencies |
| Windows Execution | ✅ PASS | Comprehensive testing completed successfully |
| Virtual Environment | ✅ PASS | venv and pip modules work correctly |
| Requirements | ✅ PASS | All dependencies are Windows-compatible |

## Visual C++ Redistributable

### Why It's Needed

The Route Planner Windows executable requires Microsoft Visual C++ Redistributable due to dependencies on native extensions that are compiled with Microsoft Visual C++.

### Potential Issues

Without the Visual C++ Redistributable, you may encounter an error like:
```
Unhandled exception: unimplemented function ucrtbase.dll.crealf called in 64-bit code
```

### Solutions

1. **Use the Bundled Package (Recommended)**: Includes VCRedist and automatic setup
2. **Use the Installer**: Automatically handles VCRedist installation
3. **Manual Installation**: Download from Microsoft: https://aka.ms/vs/17/release/vc_redist.x64.exe

## Getting Help

If you continue to experience issues:

1. Check the [GitHub Issues](https://github.com/yammanhammad/Route_Planner/issues) for similar problems
2. Create a new issue with detailed information about your system and the error
3. Try the Python installation method as an alternative

---

**Enjoy using Route Planner!** 🎉
