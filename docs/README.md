# Route Planner Documentation

This directory contains comprehensive documentation for the Route Planner application.

## User Documentation

- [User Guide](#user-guide)
- [Windows Guide](WINDOWS_GUIDE.md) - Installation, troubleshooting, and compatibility for Windows users
- [Release Notes](RELEASE_NOTES.md) - Version history and feature updates
- [Contributing](CONTRIBUTING.md) - Guidelines for contributors

## Quick Links

- [Installation Guide](../README.md#-quick-start)
- [Development Guide](../DEVELOPMENT.md) - For developers and contributors

## User Guide

### Getting Started

### Getting Started

**Choose the installation method that works best for you:**

1. **🖥️ Pre-built Executables & Packages (Easiest - Recommended for Non-Technical Users)**
   
   **Windows:**
   - Download from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest)
   - Choose `RoutePlanner-Bundled.zip` (recommended) or `RoutePlanner-Setup.exe`
   - Extract/install and run `RoutePlanner.exe`
   
   **Linux/macOS:**
   - Download `route_planner-1.1.1-py3-none-any.whl` from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest)
   - Create a virtual environment (recommended):
     ```bash
     python3 -m venv route-planner-env
     source route-planner-env/bin/activate
     ```
   - Install: `pip install route_planner-1.1.1-py3-none-any.whl`
   - Run: `route-planner`
   
   *✨ All executables and packages are automatically built using GitHub Actions CI/CD - no compilation needed!*

2. **📦 Python Package (For Python Users)**
   ```bash
   pip install route-planner
   route-planner
   ```

3. **🔧 From Source (For Developers)**
   - See [Installation Guide](../README.md#-quick-start) for detailed instructions

2. **Launch the Application**
   - Windows: Double-click `RoutePlanner.exe`
   - Linux/macOS: Run `route-planner` from terminal or application menu

3. **Add Delivery Stops**
   - Click the "+ Stop" button
   - Enter address or coordinates
   - Repeat for all delivery locations

3. **Configure Route Settings**
   - Select algorithm (Auto, Held-Karp, or Christofides)
   - Set additional options like traffic conditions
   - Choose map style

4. **Calculate Route**
   - Click "Plan Route" button
   - Wait for algorithm to complete
   - Review the optimized route

5. **Use the Route**
   - Follow numbered stops in sequence
   - View turn-by-turn directions
   - Export route to GPS or PDF

### Interface Guide

- **Map Area**: Central display showing stops and route
- **Sidebar**: Controls for adding stops and settings
- **Bottom Panel**: Algorithm performance and statistics
- **Top Bar**: Quick actions and application controls

### Advanced Features

- **Offline Mode**: Use Route Planner without internet
- **Custom Algorithms**: Adjust optimization parameters
- **Data Import/Export**: CSV, JSON, and GPX support
- **Route Comparison**: Compare different algorithms

## Technical Documentation

For technical documentation, including architecture details, API references, and development guidelines, see [DEVELOPMENT.md](../DEVELOPMENT.md).
