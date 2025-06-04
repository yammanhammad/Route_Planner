# Release Notes

This document contains all release notes for Route Planner, with the most recent version at the top.

## Route Planner v1.0.3 (Latest)

**Release Date:** May 15, 2025

### What's New
- **Windows Compatibility Enhancement**: Fixed Visual C++ Redistributable dependency issues
- **Bundled Package**: Added option with automatic VCRedist installation
- **Installer Package**: Added professional Windows installer
- **Map Performance**: 35% faster rendering and reduced memory usage
- **Cache System**: Improved offline map caching with better compression
- **Dark Mode**: Enhanced UI contrast and accessibility

### Bug Fixes
- Fixed crash when loading certain complex routes
- Corrected distance calculation for multi-segment routes
- Resolved occasional freezing during algorithm execution
- Fixed memory leak in map tile rendering
- Addressed accessibility issues with screen readers

### Developer Notes
- Moved all Windows builds to GitHub Actions CI/CD
- Enhanced PyInstaller configuration for better dependency handling
- Added runtime hook for Visual C++ compatibility
- Updated documentation with installation guides

## Route Planner v1.0.2

**Release Date:** March 10, 2025

### What's New
- **Intelligent Algorithm Selection**: Automatically chooses between Held-Karp and Christofides
- **Interactive Tutorial**: Added step-by-step guidance for new users
- **Keyboard Shortcuts**: Added comprehensive keyboard navigation
- **Route Export**: Added GPX and CSV export options
- **Location Search**: Enhanced address search with autocomplete

### Bug Fixes
- Fixed memory leak in route rendering
- Corrected scaling issues on high-DPI displays
- Resolved compatibility issues with older Python versions
- Fixed internationalization issues with address formatting

### Developer Notes
- Added testing infrastructure
- Enhanced build scripts
- Updated requirements to support Python 3.11+

## Route Planner v1.0.1

**Release Date:** January 20, 2025

### What's New
- **Linux Support**: Added comprehensive Linux compatibility
- **Offline Mode**: Enhanced caching for offline operation
- **Performance Optimization**: 25% faster route calculation
- **Documentation**: Added comprehensive user guide

### Bug Fixes
- Fixed UI scaling on high-DPI displays
- Resolved startup crash on certain Linux distributions
- Corrected path issues in the file system handler

### Developer Notes
- Added Linux installation scripts
- Enhanced cross-platform path handling
- Updated documentation for contributors

## Route Planner v1.0.0 - Initial Release

**Release Date:** December 5, 2024

### Features
- Interactive GUI with embedded Folium map using dark tile themes
- Dual algorithm support: Held-Karp (optimal) and Christofides (approximation)
- Complete onboarding system with guided tutorials
- Offline operation with intelligent caching
- Cross-platform support for Windows, macOS, and Linux
- Comprehensive Windows compatibility with proper batch file handling and path management

### Installation Options

#### Option 1: Quick Start (Recommended)
Download the platform-specific archive for your operating system, extract it, and run:
- Windows: `install.py` or `run_route_planner.bat`
- macOS/Linux: `./install.py` or `./run_route_planner.sh`

#### Option 2: Python Package (All Platforms)
```bash
pip install route-planner
route-planner
```

### Known Issues
- Occasional delay when loading map tiles for the first time
- Minor UI scaling issues on very high-resolution displays
- Some path issues on Windows systems with non-ASCII usernames

---

See the [GitHub repository](https://github.com/yammanhammad/Route_Planner) for more details and the latest updates.
