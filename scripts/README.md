# Scripts

This directory contains utility scripts for building, installing, and running the Route Planner application.

## Installation Scripts

- `install.py` - Cross-platform installation script
- `setup_env.py` - Environment setup utility
- `build.py` - Build script for creating distribution packages

## Platform-Specific Launchers

- `run_route_planner.sh` - Unix/Linux/macOS launcher script
- `run_route_planner.bat` - Windows batch launcher script

## Usage

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
