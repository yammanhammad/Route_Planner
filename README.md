# Delivery Route Planner

A PyQt5-based delivery route optimization application with interactive map visualization and comprehensive offline support.

## Features

### Core Functionality
- **Interactive GUI** with embedded Folium map using dark tile themes
- **Route Optimization** using two algorithms:
  - Held-Karp (exact algorithm for ≤12 stops)
  - Christofides (1.5-approximation for larger sets)
- **Comparative Analysis** of algorithm performance and results
- **Multithreaded Processing** to maintain UI responsiveness

### User Experience
- **Complete Onboarding System** with welcome dialogs and step-by-step tutorials
- **Interactive Tutorials** with UI element highlighting and progress tracking
- **Comprehensive Help System** with tabbed documentation
- **Tooltip Manager** providing contextual help for all UI elements
- **Dark Theme** with consistent styling across all components

### Advanced Features
- **Offline Support** with automatic internet connectivity detection
- **Intelligent Caching** system for graphs and route data (1-week retention)
- **Dynamic Stop Management** with unlimited delivery locations
- **Real-time Map Updates** with numbered markers and route visualization
- **Configuration Management** via `config.py` with runtime fallbacks

## Installation

### Requirements
```bash
pip install -r requirements.txt
```

### Dependencies
- PyQt5 (≥5.15) - GUI framework and web engine
- NetworkX (≥3.2) - Graph algorithms and data structures
- Folium (≥0.16) - Interactive map visualization
- OSMnx (≥2.0.0) - OpenStreetMap road network data
- Shapely - Geometric operations
- scikit-learn (≥1.3) - KD-Tree for spatial operations

## Usage

### Basic Operation
```bash
python main.py
```

### Configuration
Modify `config.py` to customize:
- HQ coordinates and default settings
- Map appearance and zoom levels
- Cache timeout and UI dimensions
- Logging levels and buffer sizes

## Architecture

### Main Components
- **PlannerUI** - Main application window with integrated controls
- **Worker** - Background thread for heavy computational tasks
- **WelcomeDialog** - First-time user onboarding
- **TutorialManager** - Interactive tutorial system with 10 guided steps
- **HelpDialog** - Comprehensive help and documentation system

### Key Features
- **Smart Node Disambiguation** - Automatic jittering for overlapping delivery points
- **Dual Algorithm Support** - Automatic selection based on problem size
- **Cache Management** - File-based caching with SHA1 keys for fast retrieval
- **Offline Functionality** - Local map tiles and cached graph data
- **Error Handling** - Comprehensive logging and user-friendly error messages

## File Structure
```
├── main.py           # Main application (3308 lines)
├── config.py         # Configuration constants
├── requirements.txt  # Python dependencies
├── settings.json     # Runtime settings (auto-generated)
├── cache/           # Cached graph data for performance
└── __pycache__/     # Python bytecode cache
```

## Development Status

### Completed Features ✅
- Full route optimization with TSP algorithms
- Complete onboarding and tutorial system
- Dark theme implementation with comprehensive styling
- Offline functionality with caching system
- Interactive map with dynamic marker management
- Multithreaded processing for responsive UI
- Configuration management and error handling
- Help system with 5-tab documentation

### Technical Implementation
- **Algorithm Performance**: Held-Karp for optimal results (≤12 stops), Christofides for scalability
- **UI Responsiveness**: QThread-based background processing prevents UI freezing
- **Offline Capability**: Local caching with 1-week retention for graphs and route data
- **Memory Management**: Efficient cleanup and context managers for resource handling

## License
Open source delivery route optimization tool for educational and commercial use.

## Support
- Interactive tutorials available in-app (Help → Tutorial)
- Comprehensive help system with algorithm explanations
- Tooltip assistance for all UI elements
