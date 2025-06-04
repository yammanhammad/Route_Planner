# 🚚 Route Planner - Delivery Route Optimization

![Version](https://img.shields.io/badge/ve## ⚙️ System Requirements

### 💻 Windows Users (Executable)
- Windows 7 or newer
- 4GB RAM recommended
- 200MB disk space
- Internet connection (for initial map data)

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

---0.2-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Windows Compatibility](https://img.shields.io/badge/Windows%20Compatibility-✅%20Ready-brightgreen.svg)

A sophisticated desktop application for optimizing delivery routes using advanced algorithms. Perfect for delivery drivers, sales teams, logistics coordinators, and anyone who needs to visit multiple locations efficiently.

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

## 🚀 Quick Start

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

### 🛠️ Option 3: Development Setup

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

## � Quick Start

### Option 1: Using Installation Script (Recommended)

```bash
# Clone the repository
git clone https://github.com/yammanhammad/Route_Planner.git
cd Route_Planner

# Run the installation script
python scripts/install.py
```

### Option 2: Using Platform Launchers

```bash
# On Windows
scripts\run_route_planner.bat

# On macOS/Linux
./scripts/run_route_planner.sh
```

### Option 3: Direct Python Execution

```bash
# Set up environment
python scripts/setup_env.py

# Run the application
python main.py
```

```bash
# For Windows (Run as Administrator)
python install.py --global

# For macOS/Linux
sudo ./install.py --global
```

### Option 2: Virtual Environment Setup

If you prefer to run the application from a virtual environment:

```bash
# For Windows
python setup_env.py

# For macOS/Linux
./setup_env.py
```

This will create a virtual environment, install dependencies, and provide instructions for running the application.

### Option 3: Manual Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/route-planner.git
   cd route-planner
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   # For Windows
   python -m venv .venv
   .venv\Scripts\activate

   # For macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### System Requirements
- Python 3.8 or higher
- PyQt5 with WebEngine support
- 4GB+ RAM recommended for large route calculations
- Internet connection (for initial map data)

### Dependencies
- **PyQt5** (≥5.15) - GUI framework and web engine
- **PyQtWebEngine** (≥5.15) - Web rendering for maps
- **NetworkX** (≥3.2) - Graph algorithms and data structures
- **Folium** (≥0.16) - Interactive map visualization
- **OSMnx** (≥2.0.0) - OpenStreetMap network analysis
- **Shapely** - Geometric operations and spatial analysis
- **scikit-learn** (≥1.3) - KD-Tree for spatial operations

## 📋 Usage

### Running the Application

After installation, you can run the application in several ways:

1. **Using the desktop shortcut** (if created during installation)

2. **Using the command line:**
   ```bash
   route-planner
   ```

3. **Running the script directly:**
   ```bash
   # For Windows
   python route_planner.py

   # For macOS/Linux
   ./route_planner.py
   ```

### First-Time Usage
1. The welcome dialog introduces key features of the application
2. Follow the interactive tutorial for a guided walkthrough
3. Add delivery stops using the "+ Stop" button
4. Select an algorithm (Auto, Held-Karp, or Christofides)
5. Click "Plan Route" to calculate the optimal delivery sequence

### Configuration
Modify `config.py` to customize various aspects of the application:

```python
# Example configuration options
HQ_COORD = (24.848000, 67.032000)  # Headquarters coordinates
MAP_ZOOM = 14                      # Initial map zoom level
MAP_TILES = "cartodb dark_matter"  # Map tile style
MAX_STOPS_EXACT_ALGORITHM = 12     # Maximum stops for exact algorithm
```

Key configuration categories:
- **Geographic settings**: HQ coordinates, distance parameters, map zoom levels
- **Algorithm parameters**: Maximum stops for exact algorithms, buffer sizes
- **UI settings**: Panel dimensions, component sizes, styling parameters
- **Performance settings**: Cache timeouts, logging levels, optimization thresholds

## 🏗️ Architecture

### Main Components
- **PlannerUI** - Main application window with integrated controls and map display
- **Worker** - Background thread handling computational tasks with progress reporting
- **WelcomeDialog** - First-time user onboarding experience
- **TutorialManager** - Interactive tutorial system with 10 guided steps
- **HelpDialog** - Comprehensive help and documentation with tabbed interface

### Algorithmic Implementation
1. **Held-Karp Algorithm**
   - Dynamic programming approach for exact TSP solution
   - Time complexity: O(2^n * n^2)
   - Guarantees optimal solution but becomes slow for >12 stops

2. **Christofides Algorithm**
   - Approximation algorithm with 1.5x optimality guarantee
   - Time complexity: O(n^3)
   - Fast execution with near-optimal results for larger datasets

### Key Technical Features
- **Smart Node Disambiguation** - Automatic jittering prevents overlapping delivery points
- **Dual Algorithm Selection** - Auto-selection based on problem size and complexity
- **Intelligent Caching** - File-based caching with SHA1 keys for fast retrieval
- **Offline Functionality** - Local map tiles and cached graph data for no-internet operation
- **Comprehensive Logging** - Detailed performance metrics and error tracking

## 📁 File Structure
```
├── main.py               # Application launcher script
├── main_app.py           # Core application code (UI, algorithms, logic)
├── config.py             # Configuration constants
├── requirements.txt      # Python dependencies
├── run_route_planner.sh  # Linux/macOS launcher script
├── run_route_planner.bat # Windows launcher script
├── route_planner.py      # Cross-platform launcher
├── setup_env.py          # Virtual environment setup script
├── install.py            # Installation script
├── LICENSE               # MIT License file
├── settings.json         # Runtime settings (auto-generated)
├── route_planner.log     # Application logs
├── cache/                # Cached graph data for performance
└── route_planner/        # Package directory
```

### Key Files Explained
- **main.py**: Launcher script that ensures proper environment activation
- **main_app.py**: Core application with UI, algorithms, and business logic
- **config.py**: Configuration settings for customizing application behavior
- **run_route_planner.sh/bat**: Platform-specific launcher scripts
- **route_planner.py**: Cross-platform launcher that selects the appropriate script

## 🧠 Algorithms

### Held-Karp Algorithm
- **Implementation**: Dynamic programming approach for the TSP
- **Complexity**: O(2^n * n^2) time, O(n * 2^n) space
- **Optimality**: Guarantees the optimal solution
- **Constraints**: Practical for problems with ≤12 delivery stops
- **Use Case**: When finding the mathematically optimal route is critical

### Christofides Algorithm
- **Implementation**: Minimum spanning tree with minimum-weight matching
- **Complexity**: O(n^3) time
- **Optimality**: Guarantees routes at most 1.5x longer than optimal
- **Advantages**: Much faster for large problems, polynomial time complexity
- **Use Case**: When handling many stops (>12) and near-optimal is acceptable

## 📈 Performance Considerations

### Computational Performance
- The application automatically selects the appropriate algorithm based on problem size
- For ≤12 stops, Held-Karp provides optimal solutions in reasonable time
- For >12 stops, Christofides algorithm scales much better while maintaining good route quality
- Multithreaded processing keeps the UI responsive during calculations

### Memory Management
- Efficient graph representation using NetworkX
- Smart caching of road networks to minimize memory usage
- Automatic cleanup of temporary resources

### Caching System
- File-based caching of expensive computations (graph data, distance matrices)
- SHA1 hash keys based on query parameters for fast retrieval
- 1-week retention policy with automatic cleanup
- Cache hit rates displayed in debug logs

## � Project Structure

```
Route_Planner/
├── route_planner/          # Main application package
│   ├── __init__.py         # Package initialization
│   ├── main.py            # Application entry point
│   ├── app.py             # Main application logic
│   ├── paths.py           # Cross-platform path utilities
│   ├── algorithms/        # Route optimization algorithms
│   └── ui/               # User interface components
├── scripts/              # Installation and build scripts
│   ├── install.py        # Cross-platform installer
│   ├── build.py          # Distribution builder
│   ├── setup_env.py      # Environment setup
│   ├── run_route_planner.sh   # Unix launcher
│   └── run_route_planner.bat  # Windows launcher
├── docs/                 # Documentation
│   ├── RELEASE_NOTES.md  # Version history
│   ├── WINDOWS_COMPATIBILITY.md  # Windows support info
│   ├── CONTRIBUTING.md   # Contribution guidelines
│   └── README.md         # Documentation index
├── tests/                # Test suite
│   └── README.md         # Testing guidelines
├── main.py              # Application entry point
├── main_app.py          # Main application file
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── setup.py            # Package setup
├── MANIFEST.in         # Package manifest
├── CHANGELOG.md        # Version changelog
├── README.md           # This file
└── LICENSE             # MIT license
```

## �🚀 Development Status

### Completed Features ✅
- Full route optimization with dual TSP algorithms
- Complete onboarding and interactive tutorial system
- Dark theme implementation with comprehensive styling
- Offline functionality with intelligent caching
- Interactive map with dynamic marker management
- Multithreaded processing for responsive UI
- Configuration management and error handling
- Help system with tabbed documentation

### Technical Implementation
- **Algorithm Performance**: Held-Karp for optimal results (≤12 stops), Christofides for scalability
- **UI Responsiveness**: QThread-based background processing prevents UI freezing
- **Offline Capability**: Local caching with 1-week retention for graphs and route data
- **Memory Management**: Efficient cleanup and context managers for resource handling

## � Cross-Platform Support

### Windows
- Fully compatible with Windows 10/11
- Desktop shortcut creation during installation
- Batch script launcher for easy execution

### macOS
- Compatible with macOS 10.15+ (Catalina and newer)
- Support for Apple Silicon via Rosetta 2
- Command file launcher for desktop execution

### Linux
- Compatible with major distributions (Ubuntu, Fedora, Debian, etc.)
- Desktop entry creation for integration with application menus
- Shell script launcher with proper environment activation

## �🔧 Troubleshooting

### Common Issues
- **Map not displaying**: Check internet connection or verify cached map data
- **Slow route calculation**: For many stops, try using the Christofides algorithm
- **Application crashes**: Check system resources and review log file

### Log Files
The application maintains detailed logs at `route_planner.log` with information about:
- Performance metrics for route calculations
- Graph retrieval and processing times
- Algorithm execution details
- Error conditions and exception details

## 📜 License
MIT License

## 👥 Support
- Interactive tutorials available in-app (Help → Tutorial)
- Comprehensive help system with algorithm explanations
- Tooltip assistance for all UI elements
- Log file analysis for performance troubleshooting

---
© 2025 Route Planner Development Team
