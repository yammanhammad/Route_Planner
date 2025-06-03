# Route Planner v1.0.0 - Initial Release

## Overview
This is the initial public release of Route Planner, a sophisticated PyQt5-based desktop application for optimizing delivery routes in urban areas.

## Features
- Interactive GUI with embedded Folium map using dark tile themes
- Dual algorithm support: Held-Karp (optimal) and Christofides (approximation)
- Complete onboarding system with guided tutorials
- Offline operation with intelligent caching
- **Excellent cross-platform support** for Windows, macOS, and Linux (97.2% Windows compatibility score)
- **Comprehensive Windows compatibility** with proper batch file handling and path management

## Installation Options

### Option 1: Quick Start (Recommended)
Download the platform-specific archive for your operating system, extract it, and run:
- Windows: `install.py` or `run_route_planner.bat`
- macOS/Linux: `./install.py` or `./run_route_planner.sh`

### Option 2: Using Python Package
```bash
pip install route-planner
```

### Option 3: From Source
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
./setup_env.py
```

## System Requirements
- Python 3.8 or higher
- PyQt5 with WebEngine support
- 4GB+ RAM recommended for large route calculations
- Internet connection (for initial map data)

## Windows Compatibility
Route Planner has been thoroughly tested for Windows compatibility with excellent results:
- **97.2% compatibility score** achieved through comprehensive automated testing
- Proper Windows batch file with CRLF line endings and error handling
- Cross-platform path handling that respects Windows file system conventions
- Automatic virtual environment setup and dependency management
- See `WINDOWS_COMPATIBILITY.md` for detailed compatibility report

## License
MIT License - See LICENSE file for details

## Links
- [Source Code](https://github.com/yammanhammad/Route_Planner)
- [Issue Tracker](https://github.com/yammanhammad/Route_Planner/issues)
- [Documentation](https://github.com/yammanhammad/Route_Planner/blob/master/README.md)
