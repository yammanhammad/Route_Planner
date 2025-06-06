"""
Route Planner Pack    except (subprocess.CalledProcessError, FileNotFoundError, ImportError):
        # Fallback for environments without git or in packaged distributions
        return "1.1.15"
=====================

A PyQt5-based delivery route optimization application with interactive map visualization 
and comprehensive offline support.
"""

def _get_version():
    """Get version from git tags (single source of truth) or fallback."""
    try:
        import subprocess
        from pathlib import Path
        project_root = Path(__file__).parent.parent
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            cwd=project_root,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().lstrip('v')
    except (subprocess.CalledProcessError, FileNotFoundError, ImportError):
        # Fallback for environments without git or in packaged distributions
        return "1.1.13"

__version__ = _get_version()
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
