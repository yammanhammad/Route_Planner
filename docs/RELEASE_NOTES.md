# Release Notes

This document contains all release notes for Route Planner, with the most recent version at the top.

**🚀 Quick Installation:** Download the latest version from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest):
- **Windows**: Choose `RoutePlanner-Bundled.zip` for the easiest installation experience
- **Linux/macOS**: Choose `route_planner-1.1.1-py3-none-any.whl` for easy pip installation

*All Windows executables and cross-platform packages are automatically built and published using GitHub Actions.*

## Route Planner v1.1.1 (Latest)

**Release Date:** June 2025

### 🚀 Cross-Platform Package Release
- **Cross-Platform Packages Available**: Python wheel and source distributions now available for Linux/macOS
- **GitHub Actions Build**: All packages (Windows executables + cross-platform Python packages) automatically built via CI/CD
- **Easy Installation**: Non-technical users can now easily install on any platform using pre-built packages

### 📦 Installation Options
- **Windows**: Download executable packages (`RoutePlanner-Bundled.zip` or `RoutePlanner-Setup.exe`)
- **Linux/macOS**: Download Python wheel (`route_planner-1.1.1-py3-none-any.whl`) and install with pip
- **All Platforms**: Standard PyPI installation (`pip install route-planner`) also available

## Route Planner v1.1.0

**Release Date:** December 2024

### 🧹 Major Cleanup & Modernization
- **Removed Obsolete Scripts**: Cleaned up manual build scripts and unnecessary files
- **Streamlined Entry Points**: Single main.py entry point with refactored code structure
- **Updated Documentation**: Comprehensive update of all installation guides and documentation
- **Removed Legacy Directories**: Eliminated linux/ and tests/ directories
- **Version Consistency**: Updated all version references to v1.1.0

### 🚀 Installation Improvements
- **Cross-Platform Packages**: Now available for Linux/macOS via GitHub Actions builds
- **Simplified Instructions**: Installation guides now start with easiest methods for non-technical users
- **Better Organization**: Clear prioritization of pre-built packages → Python package → source installation
- **GitHub Actions Integration**: All Windows executables and cross-platform packages built automatically via CI/CD

### 🔧 Development Enhancements
- **Code Refactoring**: Moved route_planner/main.py to route_planner/core.py for better organization
- **Build Process**: Fixed YAML syntax in GitHub Actions workflow
- **Entry Point Consistency**: Updated all references to use new code structure

## Route Planner v1.0.3

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
- Windows: `run_route_planner.bat` or download executable from releases
- macOS/Linux: `./scripts/run_route_planner.sh` or use pip install

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
