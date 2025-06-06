#!/usr/bin/env python3
"""
Build AppImage Package for Route Planner
=======================================

This script creates an AppImage package for the Route Planner application.
AppImage provides a convenient way to distribute Linux applications that
can run on any distribution without installation.
"""

import os
import platform
import subprocess
import sys
import shutil
import tempfile
from pathlib import Path

def check_requirements():
    """Check if all requirements for building AppImage are met."""
    print("Checking AppImage build requirements...")
    
    # Check if we're on Linux
    if platform.system() != "Linux":
        print("❌ AppImage can only be built on Linux")
        return False
    
    # Check for required tools
    tools = ['wget', 'appimagetool']
    missing = []
    
    for tool in tools:
        try:
            subprocess.run(['which', tool], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("Please install the missing tools and try again.")
        print("For appimagetool, download from: https://github.com/AppImage/AppImageKit/releases")
        return False
    
    return True

def get_version():
    """Get the current version of Route Planner."""
    try:
        # Try importing from the route_planner package
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from route_planner import __version__
        return __version__
    except ImportError:
        try:
            # Try using version module
            from scripts.version import get_version
            return get_version()
        except ImportError:
            # Fallback to a default version
            print("⚠️ Could not determine version, using 1.0.0")
            return "1.0.0"

def build_appimage():
    """Build an AppImage package for Route Planner."""
    if not check_requirements():
        return 1
    
    print("Building AppImage package...")
    version = get_version()
    project_root = Path(__file__).parent.parent
    build_dir = project_root / "build" / "appimage"
    
    # Clean up previous build
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Create build directory structure
    app_dir = build_dir / "RoutePlanner.AppDir"
    app_dir.mkdir(parents=True)
    
    # Create application structure
    bin_dir = app_dir / "usr" / "bin"
    bin_dir.mkdir(parents=True)
    
    # Create desktop entry
    desktop_file = app_dir / "RoutePlanner.desktop"
    with open(desktop_file, "w") as f:
        f.write("""[Desktop Entry]
Name=Route Planner
Exec=route-planner
Icon=route-planner
Type=Application
Categories=Office;Utility;
Comment=Delivery Route Optimization Application
Terminal=false
""")
    
    # Create AppRun script
    app_run = app_dir / "AppRun"
    with open(app_run, "w") as f:
        f.write("""#!/bin/bash
SELF=$(readlink -f "$0")
HERE=${SELF%/*}
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3/site-packages:${PYTHONPATH}"
exec "${HERE}/usr/bin/route-planner" "$@"
""")
    os.chmod(app_run, 0o755)
    
    # Install the package into the AppDir
    print("Installing Route Planner package into AppDir...")
    subprocess.run([
        sys.executable, "-m", "pip", "install", 
        "--prefix", str(app_dir / "usr"),
        "--no-deps",
        project_root
    ], check=True)
    
    # Create a simple wrapper script
    wrapper_script = bin_dir / "route-planner"
    with open(wrapper_script, "w") as f:
        f.write(f"""#!/bin/bash
python3 -m route_planner.core "$@"
""")
    os.chmod(wrapper_script, 0o755)
    
    # Copy icon
    icon_path = project_root / "icon.png"
    if icon_path.exists():
        shutil.copy(icon_path, app_dir / "route-planner.png")
    else:
        print("⚠️ No icon found, using default")
        # Create a simple colored square as a placeholder icon
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (256, 256), color=(41, 128, 185))
            draw = ImageDraw.Draw(img)
            img.save(app_dir / "route-planner.png")
        except ImportError:
            print("⚠️ Pillow not available, skipping icon creation")
    
    # Generate AppImage
    print(f"Generating AppImage for Route Planner v{version}...")
    os.chdir(build_dir)
    subprocess.run([
        "appimagetool",
        "RoutePlanner.AppDir",
        f"RoutePlanner-{version}-x86_64.AppImage"
    ], check=True)
    
    # Output success message
    appimage_path = build_dir / f"RoutePlanner-{version}-x86_64.AppImage"
    if appimage_path.exists():
        print(f"✅ AppImage created successfully: {appimage_path}")
        print(f"   Size: {appimage_path.stat().st_size / 1024 / 1024:.1f} MB")
        return 0
    else:
        print("❌ AppImage creation failed")
        return 1

if __name__ == "__main__":
    sys.exit(build_appimage())
