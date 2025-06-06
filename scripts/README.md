# Scripts Directory

Development, build, and deployment utilities for Route Planner.

## Overview

This directory contains automation scripts that handle version management, environment setup, building packages for different platforms, and deployment tasks. All scripts are designed to be platform-aware and can typically be run from any directory within the project.

## Quick Reference

```bash
# Version Management
python scripts/version.py                    # Show current version
python scripts/version.py --update X.Y.Z    # Update package version to X.Y.Z (e.g., 1.2.3)

# Environment & Development
python scripts/setup_env.py                  # Setup development environment
python scripts/install.py                    # Install package locally

# Package Building (Linux)
python scripts/build_flatpak.py              # Build Flatpak package
python scripts/build_appimage.py             # Build AppImage package

# Cross-platform Deployment
python scripts/universal_installer.py        # Universal installer script
python scripts/prepare_release.py            # Prepare release artifacts

# Application Launchers
./scripts/run_route_planner.sh               # Launch on Unix/Linux/macOS
scripts\run_route_planner.bat                # Launch on Windows
```

## Script Reference

### 🔧 Version Management
- **`version.py`** - Core version management utility (get/update version across all package files)
- **`version_info.py`** - Generates Windows-specific version metadata for PyInstaller builds
- **`prepare_release.py`** - Automates release preparation (changelog, tagging, artifact preparation)

### 📦 Package Building & Distribution
- **`build_flatpak.py`** - Creates Linux Flatpak packages with automatic dependency resolution
- **`build_appimage.py`** - Builds portable AppImage packages for Linux distributions
- **`universal_installer.py`** - Cross-platform installer with automatic platform detection
- **`install.py`** - Local package installation with dependency management

### 🚀 Development & Environment
- **`setup_env.py`** - Automated development environment setup (virtual environment, dependencies)
- **`run_route_planner.sh`** - Unix/Linux/macOS application launcher with environment detection
- **`run_route_planner.bat`** - Windows batch launcher script

### 🏗️ Build Configuration
- **`windows_build.spec`** - PyInstaller specification for Windows executable builds
- **`installer.nsi`** - NSIS script for Windows installer creation
- **`runtime_hook_vcruntime.py`** - PyInstaller runtime hook for Visual C++ redistributable compatibility

## Prerequisites

Before using these scripts, ensure you have:

- **Python 3.8+** with pip
- **Git** (for version management)
- **Platform-specific tools** (when building packages):
  - Linux: `flatpak-builder`, `appimagetool`
  - Windows: PyInstaller, NSIS (for builds)
- **Virtual environment** (recommended): Created automatically by `setup_env.py`

## Usage Examples

### 🛠️ Development Workflow

**1. Initial Setup (First Time)**
```bash
# Setup development environment (creates venv, installs dependencies)
python scripts/setup_env.py

# Install package in development mode
python scripts/install.py --dev
```

**2. Running the Application**
```bash
# Method 1: Direct execution (development)
python main.py

# Method 2: Using platform launchers
./scripts/run_route_planner.sh     # Unix/Linux/macOS
scripts\run_route_planner.bat      # Windows

# Method 3: After installation
route-planner                      # If installed globally
```

### 📋 Version Management

```bash
# Check current version
python scripts/version.py

# Update version for release
python scripts/version.py --update X.Y.Z

# Prepare release (updates changelog, creates tag)
python scripts/prepare_release.py --version X.Y.Z
```

### 📦 Building Packages

**Linux Packages:**
```bash
# Build Flatpak (requires flatpak-builder)
python scripts/build_flatpak.py

# Build AppImage (requires appimagetool)
python scripts/build_appimage.py
```

**Cross-Platform Installer:**
```bash
# Creates installer for current platform
python scripts/universal_installer.py

# With custom options
python scripts/universal_installer.py --target-dir ./dist --include-deps
```

### 🚀 Production Deployment

Most production builds are handled automatically by the GitHub Actions CI/CD pipeline, which:

1. **Automatically triggers** on tags and releases
2. **Builds for all platforms**: Windows executables, Linux packages, Python wheels
3. **Uploads to GitHub Releases** with automatic asset management
4. **Uses the scripts in this directory** for consistent builds across all platforms

For manual production builds, see [../DEVELOPMENT.md](../DEVELOPMENT.md#building-and-packaging).

## Script Behavior & Features

### 🎯 Smart Detection
- **Auto-detect project structure** and adapt paths accordingly
- **Platform-aware execution** with appropriate fallbacks
- **Virtual environment detection** and activation when needed
- **Dependency resolution** with automatic installation where appropriate

### 🛡️ Error Handling
- **Comprehensive validation** before executing build operations
- **Clear error messages** with actionable solutions
- **Graceful failure handling** with cleanup on interruption
- **Logging support** for debugging and monitoring

### ⚡ Performance
- **Caching mechanisms** for faster repeated builds
- **Parallel processing** where supported (build operations)
- **Incremental builds** that skip unnecessary steps
- **Resource cleanup** to prevent disk space issues

### 🔧 Customization
Most scripts accept command-line arguments for customization:

```bash
# Examples of common options
python scripts/build_flatpak.py --clean --verbose
python scripts/setup_env.py --python-version 3.11
python scripts/universal_installer.py --no-deps --target ./custom-dist
```

Use `--help` with any script to see available options.

## Windows-Specific Notes

Windows builds are automated through the GitHub Actions pipeline using:

- **`windows_build.spec`**: PyInstaller configuration with optimized settings
- **`runtime_hook_vcruntime.py`**: Ensures Visual C++ runtime compatibility
- **`installer.nsi`**: Creates professional Windows installer packages

For local Windows development, ensure you have:
- Python 3.8+ (from python.org, not Microsoft Store)
- Visual Studio Build Tools or Visual Studio Community
- Git for Windows with bash support

## Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Ensure you're in a properly configured environment
python scripts/setup_env.py
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

**Build failures:**
```bash
# Clean build cache and retry
rm -rf build/ dist/ *.egg-info/
python scripts/build_flatpak.py --clean
```

**Version inconsistencies:**
```bash
# Reset version across all files
python scripts/version.py --update $(python scripts/version.py)
```

### Getting Help

1. **Check script help**: Most scripts support `--help` or `-h`
2. **Review logs**: Build scripts create detailed logs in the project directory
3. **Development docs**: See [../DEVELOPMENT.md](../DEVELOPMENT.md) for comprehensive information
4. **GitHub Issues**: Report bugs or request features on the project repository

## Contributing to Scripts

When modifying or adding scripts:

### 📋 Guidelines
- **Follow Python conventions**: PEP 8, type hints, docstrings
- **Maintain cross-platform compatibility**: Test on Windows, macOS, and Linux
- **Add comprehensive error handling**: Clear messages and graceful failures
- **Include logging**: Use the project's logging configuration
- **Document thoroughly**: Update this README and add inline documentation

### 🧪 Testing
- **Test on multiple platforms** when possible
- **Verify edge cases**: Missing dependencies, permission issues, etc.
- **Check integration**: Ensure compatibility with CI/CD pipeline
- **Validate outputs**: Verify that generated packages/installers work correctly

### 📝 Documentation
- **Update this README** when adding new scripts or changing functionality
- **Add docstrings and comments** explaining complex logic
- **Include usage examples** for new functionality
- **Cross-reference** with main development documentation

For detailed development information and advanced topics, see [../DEVELOPMENT.md](../DEVELOPMENT.md).
