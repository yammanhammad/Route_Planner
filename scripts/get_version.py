#!/usr/bin/env python3
"""
Utility script to get the current version from the package.
This ensures version consistency across all files and documentation.
"""

import sys
from pathlib import Path

def get_version():
    """Get the current version from route_planner/__init__.py"""
    # Add parent directory to path to import route_planner
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    sys.path.insert(0, str(project_dir))
    
    try:
        from route_planner import __version__
        return __version__
    except ImportError:
        # Fallback: read directly from file
        init_file = project_dir / "route_planner" / "__init__.py"
        if init_file.exists():
            import re
            with open(init_file, 'r', encoding='utf-8') as f:
                content = f.read()
            match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
            if match:
                return match.group(1)
    
    raise RuntimeError("Unable to determine version")

if __name__ == "__main__":
    print(get_version())
