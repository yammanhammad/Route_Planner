#!/usr/bin/env python3
"""
Route Planner Console Interface

A fallback console interface for Route Planner when GUI dependencies are not available.
"""

import sys
import os
import logging

def console_main():
    """Main console interface for Route Planner."""
    print("=" * 60)
    print("Route Planner - Console Mode")
    print("=" * 60)
    print()
    
    print("This is a fallback console interface for Route Planner.")
    print("The full GUI version requires PyQt5 and other dependencies.")
    print()
    
    print("To use the full version, please install the required dependencies:")
    print("  pip install -r requirements.txt")
    print()
    
    print("For help and documentation, visit:")
    print("  https://github.com/innoxent/Route_Planner")
    print()
    
    # Try to show some basic information
    try:
        # Get the project directory
        project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Check if config exists
        config_path = os.path.join(project_dir, 'config.py')
        if os.path.exists(config_path):
            print("✅ Configuration file found")
        else:
            print("❌ Configuration file not found")
            
        # Check if requirements file exists
        req_path = os.path.join(project_dir, 'requirements.txt')
        if os.path.exists(req_path):
            print("✅ Requirements file found")
            try:
                with open(req_path, 'r') as f:
                    requirements = f.read().strip().split('\n')
                print(f"   Dependencies needed: {len([r for r in requirements if r.strip() and not r.startswith('#')])}")
            except Exception:
                pass
        else:
            print("❌ Requirements file not found")
            
    except Exception as e:
        print(f"Error checking project status: {e}")
    
    print()
    print("=" * 60)
    return 0

if __name__ == '__main__':
    sys.exit(console_main())
