# Scripts Directory

This directory contains essential utility scripts for building, installing, and running the Route Planner application.

## Overview

These scripts serve three main functions:
- Development environment setup and installation
- Application launching across platforms
- Windows build and packaging configuration

## Key Scripts

### Environment and Installation

- `setup_env.py` - Sets up development environment with dependencies
- `install.py` - Cross-platform installation script

### Application Launchers

- `run_route_planner.sh` - Unix/Linux/macOS launcher script
- `run_route_planner.bat` - Windows batch launcher script

### Windows Build Configuration

- `windows_build.spec` - PyInstaller spec file for Windows builds
- `runtime_hook_vcruntime.py` - Runtime hook for Visual C++ compatibility
- `installer.nsi` - NSIS installer script for Windows installer creation

## Usage Examples

### Development Environment Setup
```bash
python scripts/setup_env.py
```

### Application Installation
```bash
python scripts/install.py
```

### Running the Application
```bash
# On Unix/Linux/macOS
./scripts/run_route_planner.sh

# On Windows
scripts\run_route_planner.bat
```

## Windows Build Process

Windows executables are automatically built by the GitHub Actions CI/CD pipeline. The workflow:

1. Uses `windows_build.spec` as the PyInstaller configuration
2. Applies `runtime_hook_vcruntime.py` for VC++ compatibility
3. Builds standalone executable and installer using `installer.nsi`
4. Uploads assets to GitHub Releases

For detailed information on the Windows build process, see [../DEVELOPMENT.md](../DEVELOPMENT.md#building-and-packaging).

## Notes for Contributors

When modifying scripts:
- Maintain cross-platform compatibility
- Test on Windows, macOS, and Linux when possible
- Follow the project's code style guidelines
- Update documentation comments
- Add appropriate error handling

For comprehensive development information, see [../DEVELOPMENT.md](../DEVELOPMENT.md).
