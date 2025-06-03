#!/usr/bin/env python3
"""
Route Planner Launcher
======================

This script detects the operating system and launches the appropriate script.
It uses the paths module for cross-platform compatibility.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

# Add the current directory to sys.path if needed
current_dir = Path(__file__).parent.absolute()
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

try:
    # Try to import from the package
    from route_planner.paths import get_app_dir, get_platform_script
except ImportError:
    # If that fails, try to import directly
    sys.path.insert(0, str(current_dir / 'route_planner'))
    try:
        from paths import get_app_dir, get_platform_script
    except ImportError:
        # If all else fails, define the functions directly
        def get_app_dir():
            return Path(__file__).parent.absolute()
        
        def get_platform_script(script_name):
            app_dir = get_app_dir()
            if platform.system() == "Windows":
                return app_dir / f"{script_name}.bat"
            else:
                return app_dir / f"{script_name}.sh"

def main():
    """Main entry point that delegates to platform-specific scripts."""
    project_root = get_app_dir()
    
    # Determine which script to run based on platform
    script_path = get_platform_script('run_route_planner')
    
    if not script_path.exists():
        print(f"❌ {script_path.name} not found")
        sys.exit(1)
    
    # Execute the appropriate script
    try:
        # Pass any command line arguments to the script
        if platform.system() == "Windows":
            process = subprocess.Popen([str(script_path)] + sys.argv[1:], 
                                    cwd=str(project_root), shell=True)
        else:
            process = subprocess.Popen([str(script_path)] + sys.argv[1:], 
                                    cwd=str(project_root))
        process.wait()
        sys.exit(process.returncode)
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error running application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
