#!/usr/bin/env python3
"""
Version management for Route Planner.
Follows global best practices: simple, single-purpose, minimal.
"""

import os
import re
import subprocess
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
INIT_FILE = PROJECT_ROOT / "route_planner" / "__init__.py"

def get_version_from_git():
    """Get version from git tags."""
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().lstrip('v')
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None

def get_version_from_package():
    """Get version from route_planner/__init__.py."""
    if not INIT_FILE.exists():
        return None
    
    try:
        with open(INIT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
        return match.group(1) if match else None
    except (IOError, OSError):
        return None

def get_version():
    """Get current version. Priority: git -> package -> env -> default."""
    # Try git first (for releases)
    version = get_version_from_git()
    if version:
        return version
    
    # Try package version
    version = get_version_from_package()
    if version:
        return version
    
    # Try environment (for CI)
    version = os.getenv('VERSION')
    if version:
        return version.lstrip('v')
    
    # Default fallback
    return "0.0.0"

def update_package_version(new_version):
    """Update version in __init__.py."""
    if not INIT_FILE.exists():
        print(f"Error: {INIT_FILE} not found")
        return False
    
    try:
        with open(INIT_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = re.sub(
            r'__version__ = [\'"][^\'"]*[\'"]',
            f'__version__ = "{new_version}"',
            content
        )
        
        if content != updated:
            with open(INIT_FILE, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"Updated version to {new_version}")
            return True
        else:
            print(f"Version already {new_version}")
            return True
            
    except Exception as e:
        print(f"Error updating version: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == '--update' and len(sys.argv) > 2:
            # Update package version
            success = update_package_version(sys.argv[2])
            sys.exit(0 if success else 1)
        elif sys.argv[1] == '--help':
            print("Usage:")
            print("  python version.py              # Show current version")
            print("  python version.py --update VER # Update package version")
            sys.exit(0)
    
    # Default: show current version
    print(get_version())
