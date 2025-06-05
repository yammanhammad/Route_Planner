#!/usr/bin/env python3
"""
Route Planner - Primary Entry Point
===================================

This is the main development and direct execution entry point.
Use this for:
- Development and testing
- Direct Python execution: python main.py
- IDE integration

For end-users, see the installation guide for easier methods.
"""
import sys
import subprocess
from pathlib import Path


def main():
    """Main entry point that delegates to the package entry point."""
    # Try to import and run the package directly
    try:
        from route_planner.core import main as app_main
        app_main()
    except ImportError:
        # Fallback: delegate to shell script for proper environment setup
        project_root = Path(__file__).parent.absolute()
        shell_script = project_root / ('run_route_planner.bat' if sys.platform == 'win32' else 'run_route_planner.sh')
        
        if not shell_script.exists():
            print(f"❌ {shell_script.name} not found")
            sys.exit(1)
        
        # Execute the shell script which handles environment activation
        try:
            # Pass any command line arguments to the shell script
            result = subprocess.run([str(shell_script)] + sys.argv[1:], 
                                   cwd=str(project_root))
            sys.exit(result.returncode)
        except KeyboardInterrupt:
            print("\n🛑 Application interrupted by user")
            sys.exit(0)
        except Exception as e:
            print(f"❌ Error running application: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
