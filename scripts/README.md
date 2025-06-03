# Scripts

This directory contains utility scripts for building, installing, and running the Route Planner application.

## Windows Executable Builder 🖱️

**For creating user-friendly Windows distributions:**

- `build_windows_dist.py` - Complete Windows distribution builder
- `build_exe.py` - Simple executable builder
- `build_for_windows.bat` - Automated Windows build script
- `installer.nsi` - NSIS installer script

### Building Windows Executable
```bash
# Complete automated build
python scripts/build_windows_dist.py

# Simple executable only
python scripts/build_exe.py

# Windows batch (double-click to run)
scripts\build_for_windows.bat
```

**Output**: Creates `dist_windows/` with:
- `RoutePlanner.exe` - Standalone executable 
- `RoutePlanner-Portable.zip` - Complete portable package
- Ready for distribution to Windows users!

## Installation Scripts

- `install.py` - Cross-platform installation script
- `setup_env.py` - Environment setup utility
- `build.py` - Build script for creating distribution packages

## Platform-Specific Launchers

- `run_route_planner.sh` - Unix/Linux/macOS launcher script
- `run_route_planner.bat` - Windows batch launcher script

## Usage

### Windows User-Friendly Distribution
```bash
# Build everything for Windows users
python scripts/build_windows_dist.py

# Share the resulting RoutePlanner-Portable.zip
# Users just extract and double-click RoutePlanner.exe!
```

### Quick Installation
```bash
python scripts/install.py
```

### Environment Setup
```bash
python scripts/setup_env.py
```

### Building Distribution
```bash
python scripts/build.py
```

### Running the Application
```bash
# On Unix/Linux/macOS
./scripts/run_route_planner.sh

# On Windows
scripts\run_route_planner.bat
```

## Windows Build Details

The Windows executable builder creates a completely standalone application:

**Benefits for Windows Users:**
- ✅ No Python installation required
- ✅ Double-click to run
- ✅ Professional Windows integration
- ✅ Portable - runs from any location
- ✅ Error handling with friendly messages

**Technical Details:**
- Uses PyInstaller for executable creation
- Embeds all dependencies (~50-80 MB final size)
- Includes application icon and version info
- Ready for code signing and distribution

For detailed instructions, see: `../docs/WINDOWS_BUILD_GUIDE.md`
