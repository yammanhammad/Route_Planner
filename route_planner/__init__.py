"""
Route Planner Package
=====================

A PyQt5-based delivery route optimization application with interactive map visualization 
and comprehensive offline support.
"""

__version__ = "1.1.3"
__author__ = "Route Planner Development Team"

# Ensure config is available at package level
try:
    import sys
    from pathlib import Path
    
    # Add project root to path for config import
    project_root = Path(__file__).parent.parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Import config so it's available to all modules
    from config import *
except ImportError:
    # Fallback configuration
    pass

# Import core functionality
from route_planner.core import main
