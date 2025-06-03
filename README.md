# Delivery Route Planner

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)

A sophisticated PyQt5-based desktop application for optimizing delivery routes in urban areas. This application combines advanced graph algorithms with an intuitive user interface to solve the Traveling Salesman Problem (TSP) for delivery route optimization.

## 🌟 Key Features

### Core Functionality
- **Interactive GUI** with embedded Folium map using modern dark tile themes
- **Dual Route Optimization** algorithms:
  - **Held-Karp** - Exact algorithm with optimal results (for ≤12 stops)
  - **Christofides** - 1.5-approximation algorithm for larger datasets
- **Algorithm Comparison** with performance metrics and visual route differences
- **Multithreaded Processing** for maintaining UI responsiveness during complex calculations

### User Experience
- **Comprehensive Onboarding** with welcome dialogs and step-by-step tutorials
- **Interactive Tutorials** featuring UI element highlighting and progress tracking
- **Tabbed Help System** with detailed documentation and algorithm explanations
- **Contextual Tooltips** for all UI elements to assist new users
- **Dark Theme** with consistent styling throughout the application

### Advanced Features
- **Offline Support** with automatic internet connectivity detection
- **Intelligent Caching System** for graphs and route data (1-week retention)
- **Dynamic Stop Management** supporting unlimited delivery locations
- **Real-time Map Updates** with numbered markers and route visualization
- **Flexible Configuration** via `config.py` with robust runtime fallbacks

## 🔧 Installation

### System Requirements
- Python 3.8 or higher
- PyQt5 with WebEngine support
- 4GB+ RAM recommended for large route calculations
- Internet connection (for initial map data)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/route-planner.git
   cd route-planner
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

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
```bash
python main.py
```

The application will automatically set up the virtual environment, install dependencies if needed, and launch the Route Planner interface.

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
├── run_route_planner.sh  # Environment setup and launcher script
├── settings.json         # Runtime settings (auto-generated)
├── route_planner.log     # Application logs
├── cache/                # Cached graph data for performance
└── __pycache__/          # Python bytecode cache
```

### Key Files Explained
- **main.py**: Launcher script that ensures proper environment activation
- **main_app.py**: Core application with UI, algorithms, and business logic
- **config.py**: Configuration settings for customizing application behavior
- **run_route_planner.sh**: Shell script for environment setup and application launch

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

## 🚀 Development Status

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

## 🔧 Troubleshooting

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
