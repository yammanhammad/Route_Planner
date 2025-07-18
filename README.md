# 🚚 Route Planner - Delivery Route Optimizer

![Version](https://img.shields.io/github/v/release/yammanhammad/Route_Planner?style=flat&logo=github)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Windows](https://img.shields.io/badge/Windows-0078D4?logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)

A sophisticated desktop application for optimizing delivery routes using advanced algorithms. Perfect for delivery drivers, sales teams, logistics coordinators, and anyone who needs to visit multiple locations efficiently.

## 📋 Table of Contents

- [🌟 Key Features](#-key-features)
- [🚀 Quick Start](#-quick-start)
- [📱 How to Use](#-how-to-use)
- [⚙️ System Requirements](#-system-requirements)
- [🛠️ Troubleshooting](#-troubleshooting)
- [📚 Documentation](#-documentation)
- [🧑‍💻 Development](#-development)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

## 🌟 Key Features

- **🖥️ One-Click Installation** - No Python knowledge required
- **🗺️ Interactive Map Interface** with real-time route visualization
- **🧠 Smart Route Optimization** using dual algorithms:
  - **Held-Karp**: Optimal solutions for small routes (≤12 stops)
  - **Christofides**: Fast approximation for large routes (>12 stops)
- **📱 User-Friendly Interface** with guided tutorials and dark theme
- **💾 Offline Support** with intelligent caching system
- **⚡ Multithreaded Processing** keeps interface responsive
- **�️ Cross-Platform Support**:
  - **Windows**: Native executable with auto-update
  - **Linux**: AppImage and Flatpak formats for all distributions
  - **macOS**: Universal installer with desktop integration

Choose the installation method that works best for you. **For non-technical users, we recommend starting with Option 1.**

### Option 1: 🖥️ Pre-built Executables & Packages (Easiest - No Technical Knowledge Required)

**Windows:**
1. **Download** the latest release from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest)
   - `RoutePlanner-Bundled.zip` (Recommended - includes all dependencies)
   - `RoutePlanner-Setup.exe` (Traditional installer)
2. **Extract** (for zip) or **install** (for exe) 
3. **Run** `RoutePlanner.exe`

💡 *Our universal installer automatically creates desktop shortcuts and application menu entries!*

✨ *All executables and packages (Windows .exe, Linux AppImage/Flatpak, Python wheels) are automatically built and published by our GitHub Actions CI/CD pipeline - no manual compilation needed!*

**Linux:**
1. **Choose your preferred format:**
   - `RoutePlanner-AppImage.AppImage` - Portable, runs anywhere (recommended)
   - `RoutePlanner-Flatpak.flatpak` - Sandboxed, better system integration
   - `route_planner-[VERSION]-py3-none-any.whl` - Python package
2. **AppImage** (easiest):
   ```bash
   # Download from GitHub Releases
   chmod +x RoutePlanner-AppImage.AppImage
   ./RoutePlanner-AppImage.AppImage
   ```
3. **Flatpak**:
   ```bash
   # Install from file
   flatpak install RoutePlanner-Flatpak.flatpak
   # Run
   flatpak run org.routeplanner.RoutePlanner
   ```
4. **Universal Installer** (automatic setup):
   ```bash
   python3 install.py
   ```
   This detects your Linux environment and installs appropriately.

5. **Run**: 
   - Find "Route Planner" in your application menu
   - Or run: `route-planner` from terminal

**macOS:**
1. **Download** from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest):
   - `route_planner-[VERSION]-py3-none-any.whl` (Python package)
   - `install.py` (Automatic installer script)
2. **Universal Installer** (Recommended):
   ```bash
   python3 install.py
   ```
   This automatically sets up everything including desktop integration!

3. **Manual Installation** (Advanced users):
   ```bash
   python3 -m venv route-planner-env
   source route-planner-env/bin/activate
   pip install route_planner-[VERSION]-py3-none-any.whl
   ```
4. **Run**: 
   - Find "Route Planner" in your Applications folder
   - Or run: `route-planner` from terminal

### Option 2: 📦 Python Package (For Python Users)

**All Platforms:**
```bash
pip install route-planner
route-planner
```

### Option 3: 🔧 From Source (For Developers)

**Linux/macOS:**
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
pip install -r requirements.txt
python main.py
```

**Windows:**
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
pip install -r requirements.txt
python main.py
```

### Option 4: 🚀 Quick Launcher Scripts

**Linux/macOS:**
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
chmod +x scripts/run_route_planner.sh
./scripts/run_route_planner.sh
```

**Windows:**
```cmd
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
scripts\run_route_planner.bat
```

---
**📖 Need Help?** See our detailed [Windows Guide](docs/WINDOWS_GUIDE.md) for troubleshooting and advanced options.

## 📱 How to Use

1. **Start the application** using your preferred installation method
2. **Add stops** by clicking "+ Stop" and entering addresses
3. **Choose algorithm** or use "Auto" for automatic selection
4. **Click "Plan Route"** to calculate the optimal path
5. **Follow the route** displayed on the map in numbered sequence

For a comprehensive guide with screenshots, see the [User Guide](docs/README.md).

## ⚙️ System Requirements

### Windows
- Windows 7 or newer (64-bit recommended)
- 4GB RAM minimum
- 100MB+ free disk space
- Internet connection for map data
- Microsoft Visual C++ Redistributable (included in Bundled package)

### Linux
- Ubuntu 18.04+, Debian 10+, or equivalent
- Desktop environment (GNOME, KDE, XFCE, etc.)
- 4GB+ RAM recommended

### macOS
- macOS 10.14 (Mojave) or newer
- Python 3.8 or higher
- 4GB+ RAM recommended

### All Platforms (Python Installation)
- Python 3.8 or higher
- PyQt5 with WebEngine support
- 4GB+ RAM recommended

## 🛠️ Troubleshooting

### Common Issues

**Windows**
- **"Application won't start"**: Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- **Windows Defender warning**: Right-click the exe → "Run as administrator"

**Linux**
- **Missing dependencies**: Use AppImage (no dependencies required) or `pip install -r requirements.txt`
- **Permission denied**: Run `chmod +x RoutePlanner-AppImage.AppImage` for AppImages
- **Environment issues**: Use the universal installer `python3 install.py` for automated setup
- **Sandboxing issues**: If using Flatpak, add permissions: `flatpak override org.routeplanner.RoutePlanner --filesystem=home`

**All Platforms**
- **Map not loading**: Check internet connection for initial setup
- **Performance issues**: Ensure 4GB+ RAM available

For more detailed troubleshooting, check:
- [Windows Guide](docs/WINDOWS_GUIDE.md)
- [GitHub Issues](https://github.com/yammanhammad/Route_Planner/issues)

## 📚 Documentation

- [Full Documentation](docs/README.md)
- [Windows Guide](docs/WINDOWS_GUIDE.md)
- [Release Notes](docs/RELEASE_NOTES.md)
- [Contributing Guidelines](docs/CONTRIBUTING.md)

## 🧑‍💻 Development

For developers interested in contributing or customizing Route Planner:

```bash
# Clone the repository
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner

# Set up development environment
python scripts/setup_env.py

# Run the application
python main.py
```

See [DEVELOPMENT.md](DEVELOPMENT.md) for comprehensive development information.

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

⭐ **Star this repository if it helps you optimize your routes!** ⭐
