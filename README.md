# 🚚 Route Planner - Delivery Route Optimization

![Version](https://img.shields.io/badge/version-1.0.3-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)
![Windows](https://img.shields.io/badge/Windows-0078D4?logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?logo=linux&logoColor=black)
![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=white)

A sophisticated desktop application for optimizing delivery routes using advanced algorithms. Perfect for delivery drivers, sales teams, logistics coordinators, and anyone who needs to visit multiple locations efficiently.

## 📋 Table of Contents

- [🌟 Key Features](#-key-features)
- [🚀 Installation Guide](#-installation-guide)
- [📱 How to Use](#-how-to-use)
- [🛠️ Troubleshooting & Support](#-troubleshooting--support)
- [⚙️ System Requirements](#-system-requirements)
- [🧠 Algorithms Explained](#-algorithms-explained)
- [🏗️ Architecture & Technical Details](#-architecture--technical-details)
- [📁 Project Structure](#-project-structure)
- [🆘 Support & Documentation](#-support--documentation)

## 🌟 Key Features

- **🖥️ One-Click Windows Installation** - No Python knowledge required
- **🗺️ Interactive Map Interface** with real-time route visualization
- **🧠 Smart Route Optimization** using dual algorithms:
  - **Held-Karp**: Optimal solutions for small routes (≤12 stops)
  - **Christofides**: Fast approximation for large routes (>12 stops)
- **📱 User-Friendly Interface** with guided tutorials and dark theme
- **💾 Offline Support** with intelligent caching system
- **⚡ Multithreaded Processing** keeps interface responsive
- **🔧 Cross-Platform** - Windows, macOS, and Linux support

---

## 🚀 Installation Guide

Choose the installation method that best fits your needs:

### 📦 Windows - One-Click Installation (Recommended)

**The easiest way for Windows users** - no Python installation required:

1. **📥 Download**: Get the latest `RoutePlanner-Windows-Portable.zip` from [**GitHub Releases**](https://github.com/yammanhammad/Route_Planner/releases/latest)
2. **📂 Extract**: Unzip anywhere on your computer
3. **🖱️ Run**: Double-click `RoutePlanner.exe` to start!

**✅ Benefits:**
- No Python installation needed
- No command line required  
- Works on any Windows 7+ system
- Portable - runs from any location
- Automatic updates available

📚 **Need help?** See [Windows Installation Guide](docs/WINDOWS_EXECUTABLE_GUIDE.md) for troubleshooting

### 🐧 Linux - Multiple Options Available

#### Option A: One-Line Installer (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/yammanhammad/Route_Planner/master/linux/quick-install.sh | bash
```

#### Option B: User-Level Installation (No root required)
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
./linux/install-user.sh
```

#### Option C: System-Wide Installation
```bash
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner
sudo ./linux/install-linux.sh
```

**✅ What you get:**
- App appears in Applications menu
- Desktop integration with proper icon
- Launch from terminal with `route-planner`
- Automatic Python environment setup
- Easy uninstallation

📚 **For detailed Linux instructions, troubleshooting, and package installation:** [Linux Installation Guide](linux/README.md)

### 🍎 macOS - Python Installation

For macOS users, use the Python package manager method:

```bash
# Install Python 3.8+ if not already installed
brew install python3

# Install Route Planner
pip3 install route-planner

# Run the application
route-planner
```

**Requirements:**
- macOS 10.14 (Mojave) or newer
- Python 3.8 or higher
- Homebrew (for dependency management)

**Note:** A native macOS app bundle (.dmg) is planned for future releases.

### 🐍 Cross-Platform Python Installation

For Python developers or users on any platform:

```bash
# Install via pip
pip install route-planner

# Run the application
route-planner
```

**Verification:** After installation, verify it works:
```bash
route-planner --version  # Should show version 1.0.3
```

### 🛠️ Development Setup

For developers who want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner

# Set up environment
python scripts/setup_env.py

# Run the application
python main.py
```

📚 **For contributors:** See [Contributing Guide](docs/CONTRIBUTING.md)

### 📦 Option 1: Windows Users - One-Click Installation (Recommended)

**The easiest way for Windows users** - no Python installation required:

1. **📥 Download**: Get the latest `RoutePlanner-Windows-Portable.zip` from [**GitHub Releases**](https://github.com/yammanhammad/Route_Planner/releases/latest)
2. **📂 Extract**: Unzip anywhere on your computer
3. **🖱️ Run**: Double-click `RoutePlanner.exe` to start!

**✅ Benefits:**
- No Python installation needed
- No command line required  
- Works on any Windows 7+ system
- Portable - runs from any location
- Automatic updates available

### 🐍 Option 2: Python Installation (All Platforms)

For Python developers or users who prefer traditional installation:

```bash
# Install via pip
pip install route-planner

# Run the application
route-planner
```

### � Option 3: Linux One-Click Installation

For Linux users who want the app to appear in their Applications menu:

```bash
# One-line installer (Ubuntu/Debian)
curl -sSL https://raw.githubusercontent.com/yammanhammad/Route_Planner/master/linux/quick-install.sh | bash
```

**✅ What you get:**
- App appears in Applications menu
- Desktop integration with proper icon
- Launch from terminal with `route-planner`
- Automatic Python environment setup
- Easy uninstallation

For more Linux installation options, see [`linux/README.md`](linux/README.md)

### �🛠️ Option 4: Development Setup

For developers who want to contribute or modify the code:

```bash
# Clone the repository
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner

# Set up environment
python scripts/setup_env.py

# Run the application
python main.py
```

---

## 📱 How to Use

### 🎯 Getting Started

1. **🎉 Welcome**: The app guides you through setup on first launch
2. **📍 Add Stops**: Click "+ Stop" to add delivery locations
3. **🔄 Choose Algorithm**: 
   - **Auto** (recommended) - Automatically selects best algorithm
   - **Held-Karp** - Perfect routes for ≤12 stops
   - **Christofides** - Fast routes for >12 stops
4. **🗺️ Plan Route**: Click "Plan Route" to calculate optimal path
5. **📋 Follow Route**: Use the numbered sequence for efficient delivery

### 💡 Pro Tips

- **🎓 Tutorial**: Use Help → Tutorial for interactive guidance
- **💾 Offline Mode**: Works without internet after initial setup
- **⚙️ Customize**: Modify `config.py` for your specific needs
- **📊 Compare**: Use algorithm comparison to see performance differences

---

## 🛠️ Troubleshooting & Support

### 🚨 Common Issues

**Installation Problems:**
- **Windows:** See [Windows Installation Guide](docs/WINDOWS_EXECUTABLE_GUIDE.md)
- **Linux:** See [Linux Installation Guide](linux/README.md) 
- **macOS:** Ensure Python 3.8+ and PyQt5 are properly installed

**Runtime Issues:**
- **Map not loading:** Check internet connection for initial setup
- **Application won't start:** Verify all dependencies are installed
- **Performance issues:** Ensure 4GB+ RAM available

### 📚 Documentation Links

- 📖 [Full Documentation](docs/README.md)
- 🐧 [Linux Installation Guide](linux/README.md)
- 🏗️ [Windows Build Guide](docs/WINDOWS_BUILD_GUIDE.md)
- 🤝 [Contributing Guidelines](docs/CONTRIBUTING.md)
- 📋 [Release Notes](docs/RELEASE_NOTES_v1.0.3.md)

### 💬 Getting Help

- 🐛 **Found a bug?** [Open an issue](https://github.com/yammanhammad/Route_Planner/issues/new)
- 💡 **Feature request?** [Start a discussion](https://github.com/yammanhammad/Route_Planner/discussions)
- ❓ **Need help?** Check [existing issues](https://github.com/yammanhammad/Route_Planner/issues) first

---

## ⚙️ System Requirements

### 💻 Windows (Executable)
- Windows 7 or newer
- 4GB RAM recommended
- 200MB disk space
- Internet connection (for initial map data)

### 🐧 Linux (All Distributions)
- Ubuntu 18.04+, Debian 10+, or equivalent
- Python 3.8 or higher
- 4GB+ RAM recommended
- Desktop environment (GNOME, KDE, XFCE, etc.)

### 🍎 macOS
- macOS 10.14 (Mojave) or newer
- Python 3.8 or higher
- 4GB+ RAM recommended
- Homebrew (recommended for dependency management)

### 🐍 Python Users (All Platforms)
- Python 3.8 or higher
- PyQt5 with WebEngine support
- 4GB+ RAM recommended
- Internet connection (for initial setup)

### 📦 Key Dependencies
- **PyQt5** (≥5.15) - GUI framework and web engine
- **NetworkX** (≥3.2) - Graph algorithms and data structures
- **Folium** (≥0.16) - Interactive map visualization
- **OSMnx** (≥2.0.0) - OpenStreetMap network analysis
- **Shapely** - Geometric operations and spatial analysis

---

## 🧠 Algorithms Explained

### 🎯 Held-Karp Algorithm
- **Best For**: Small routes (≤12 stops)
- **Guarantee**: Mathematically optimal solution
- **Speed**: Slower for large routes
- **Use When**: Perfect route is critical

### ⚡ Christofides Algorithm  
- **Best For**: Large routes (>12 stops)
- **Guarantee**: At most 1.5x longer than optimal
- **Speed**: Very fast, even for 50+ stops
- **Use When**: Speed matters, near-optimal is acceptable

### 🤖 Auto Selection
- Automatically chooses the best algorithm
- Uses Held-Karp for ≤12 stops
- Switches to Christofides for >12 stops
- **Recommended for most users**

---

## 🏗️ Architecture & Technical Details

### 🎛️ Main Components
- **PlannerUI**: Main application window with integrated controls and map display
- **Worker**: Background thread handling computational tasks with progress reporting
- **WelcomeDialog**: First-time user onboarding experience
- **TutorialManager**: Interactive tutorial system with guided steps
- **HelpDialog**: Comprehensive help and documentation with tabbed interface

### ⚡ Performance Features
- **Multithreaded Processing**: Keeps UI responsive during route calculations
- **Smart Caching**: File-based caching with 1-week retention for graphs and route data
- **Offline Support**: Local map tiles and cached graph data for no-internet operation
- **Memory Management**: Efficient cleanup and context managers for resource handling

### 🎨 User Experience
- **Dark Theme**: Modern interface with consistent styling throughout
- **Interactive Tutorials**: Step-by-step guidance with UI element highlighting
- **Contextual Tooltips**: Help for all UI elements to assist new users
- **Real-time Updates**: Dynamic map markers and route visualization

---

## 📁 Project Structure

```
Route_Planner/
├── 📱 main.py                    # Application launcher
├── 🖥️ main_app.py               # Core application with UI and algorithms
├── ⚙️ config.py                 # Configuration settings
├── 📋 requirements.txt          # Python dependencies
├── 🐧 route_planner.py          # Cross-platform launcher
├── � run_route_planner.sh      # Unix launcher (root)
├── 🏁 run_route_planner.bat     # Windows launcher (root)
├── �📄 README.md                 # This documentation
├── 📜 LICENSE                   # MIT License
├── 📊 settings.json             # Runtime settings (auto-generated)
├── 📝 route_planner.log         # Application logs
├── 💾 cache/                    # Cached graph data for performance
├── � linux/                    # Linux installation scripts and desktop integration
│   ├── install-linux.sh         # System-wide installer
│   ├── install-user.sh          # User-level installer
│   ├── quick-install.sh         # One-line installer
│   ├── create_icon.py           # Icon generator
│   └── route-planner.desktop    # Desktop entry
├── �📚 docs/                     # Documentation
│   ├── RELEASE_NOTES*.md        # Version history and release notes
│   ├── WINDOWS_BUILD_GUIDE.md   # Windows build instructions
│   └── CONTRIBUTING.md          # Contribution guidelines
├── 🔧 scripts/                  # Build and utility scripts
│   ├── install.py               # Cross-platform installer
│   ├── setup_env.py             # Environment setup
│   ├── build_windows_dist.py    # Windows executable builder
│   ├── run_route_planner.sh     # Unix launcher (detailed)
│   └── run_route_planner.bat    # Windows launcher (detailed)
└── 🧪 tests/                    # Test suite
```

---

## 🔧 Configuration

You can customize the application by modifying `config.py`:

```python
# Example configuration options
HQ_COORD = (24.848000, 67.032000)  # Your headquarters coordinates
MAP_ZOOM = 14                      # Initial map zoom level
MAP_TILES = "cartodb dark_matter"  # Map tile style
MAX_STOPS_EXACT_ALGORITHM = 12     # Maximum stops for exact algorithm
```

**Configuration Categories:**
- **📍 Geographic**: HQ coordinates, distance parameters, map zoom levels
- **🧠 Algorithm**: Maximum stops for exact algorithms, buffer sizes  
- **🎨 UI**: Panel dimensions, component sizes, styling parameters
- **⚡ Performance**: Cache timeouts, logging levels, optimization thresholds

---

## 🌍 Cross-Platform Support

### 🪟 Windows
- ✅ Fully compatible with Windows 10/11
- ✅ One-click executable installation
- ✅ Desktop shortcut creation
- ✅ No Python installation required

### 🍎 macOS  
- ✅ Compatible with macOS 10.15+ (Catalina and newer)
- ✅ Support for Apple Silicon via Rosetta 2
- ✅ Python installation required

### 🐧 Linux
- ✅ Compatible with major distributions (Ubuntu, Fedora, Debian, etc.)
- ✅ Desktop entry creation for application menus
- ✅ Python installation required

---

## 🔍 Troubleshooting

### ❓ Common Issues

**🗺️ Map not displaying**
- Check internet connection for initial map download
- Verify cached map data in `cache/` folder

**🐌 Slow route calculation**  
- For many stops (>12), ensure you're using Christofides algorithm
- Check available system memory (4GB+ recommended)

**💥 Application crashes**
- Check `route_planner.log` for error details
- Verify system meets minimum requirements
- Try running with administrator privileges (Windows)

### 📋 Log Files
The application maintains detailed logs at `route_planner.log` with:
- ⏱️ Performance metrics for route calculations
- 📊 Graph retrieval and processing times  
- 🧠 Algorithm execution details
- ❌ Error conditions and exception details

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](docs/CONTRIBUTING.md) for details.

### 🚀 Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Route_Planner.git
cd Route_Planner

# Set up development environment
python scripts/setup_env.py

# Run tests
python -m pytest tests/

# Run the application
python main.py
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support & Documentation

- **📖 Interactive Tutorial**: Available in-app (Help → Tutorial)
- **📚 Help System**: Comprehensive documentation with algorithm explanations
- **💡 Tooltips**: Contextual help for all UI elements
- **📋 Issues**: Report bugs or request features on [GitHub Issues](https://github.com/yammanhammad/Route_Planner/issues)
- **📊 Performance**: Log file analysis for troubleshooting

---

## 🏆 Why Choose Route Planner?

✨ **Easy to Use**: One-click installation for Windows, guided tutorials, intuitive interface  
🧠 **Smart Algorithms**: Automatically selects optimal algorithm based on problem size  
⚡ **Fast Performance**: Multithreaded processing, intelligent caching, offline support  
🌍 **Cross-Platform**: Works on Windows, macOS, and Linux  
🔧 **Customizable**: Extensive configuration options for your specific needs  
🆓 **Open Source**: MIT licensed, free to use and modify  

---

**© 2025 Route Planner Development Team**

---

## 🔗 Additional Resources

- 🌐 [GitHub Repository](https://github.com/yammanhammad/Route_Planner)
- 📦 [Latest Releases](https://github.com/yammanhammad/Route_Planner/releases)
- 📊 [Project Roadmap](https://github.com/yammanhammad/Route_Planner/projects)
- 💬 [Community Discussions](https://github.com/yammanhammad/Route_Planner/discussions)
- 🐛 [Report Issues](https://github.com/yammanhammad/Route_Planner/issues)

**⭐ If you find Route Planner useful, please consider giving it a star on GitHub!**

⭐ **Star this repository if it helps you optimize your routes!** ⭐
