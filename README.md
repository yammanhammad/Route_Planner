# 🚚 Route Planner - Delivery Route OptimizFor detailed options and troubleshooting, see the [Windows Guide](docs/WINDOWS_GUIDE.md).

### Linux 🐧
```bash
# Clone and install manually
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
python scripts/install.py
```

Or use the cross-platform installer from scripts directory.Version](https://img.shields.io/badge/version-1.1.0-blue.svg)
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
- **🔧 Cross-Platform** - Windows, macOS, and Linux support

## 🚀 Quick Start

### Windows
1. **Download** `RoutePlanner-Bundled.zip` from [GitHub Releases](https://github.com/yammanhammad/Route_Planner/releases/latest)
2. **Extract** anywhere on your computer
3. **Run** `setup.bat` or `RoutePlanner.exe` directly

For detailed options and troubleshooting, see the [Windows Guide](docs/WINDOWS_GUIDE.md).

### Linux
```bash
curl -sSL https://raw.githubusercontent.com/yammanhammad/Route_Planner/master/linux/quick-install.sh | bash
```

For more Linux options, see the [Linux Installation Guide](linux/README.md).

### macOS
```bash
# Install Python 3.8+ if needed
brew install python3

# Install Route Planner
pip3 install route-planner

# Run the application
route-planner
```

### Python (All Platforms)
```bash
pip install route-planner
route-planner
```

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
- **Missing dependencies**: Run `python scripts/setup_env.py`
- **Environment issues**: Use `python scripts/install.py` for automated setup

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
