#!/usr/bin/env python3
"""
Route Planner Launcher
======================

This script detects the operating system and launches the appropriate script.
"""

import os
import platform
import subprocess
import sys
from pathlib import Path

def main():
    """Main entry point that delegates to platform-specific scripts."""
    project_root = Path(__file__).parent.absolute()
    
    # Determine which script to run based on platform
    if platform.system() == "Windows":
        script_path = project_root / 'run_route_planner.bat'
    else:  # Linux, MacOS, etc.
        script_path = project_root / 'run_route_planner.sh'
    
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
