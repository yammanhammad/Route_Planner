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

1. **Launch the Application**
   - Windows: Double-click `RoutePlanner.exe`
   - Linux: Run `route-planner` from terminal or application menu
   - macOS: Run `route-planner` from terminal

2. **Add Delivery Stops**
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
