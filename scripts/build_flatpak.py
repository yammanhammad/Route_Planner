#!/usr/bin/env python3
"""
Build Flatpak Package for Route Planner
=======================================

This script creates a Flatpak package for the Route Planner application.
Flatpak provides a sandboxed environment for Linux applications that
can run on any distribution with the Flatpak runtime installed.
"""

import os
import platform
import subprocess
import sys
import shutil
import json
import tempfile
from pathlib import Path

def check_requirements():
    """Check if all requirements for building Flatpak are met."""
    print("Checking Flatpak build requirements...")
    
    # Check if we're on Linux
    if platform.system() != "Linux":
        print("❌ Flatpak can only be built on Linux")
        return False
    
    # Check for required tools
    tools = ['flatpak-builder', 'flatpak']
    missing = []
    
    for tool in tools:
        try:
            subprocess.run(['which', tool], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            missing.append(tool)
    
    if missing:
        print(f"❌ Missing required tools: {', '.join(missing)}")
        print("Please install the missing tools and try again.")
        print("You can install Flatpak tools with your package manager:")
        print("  - For Ubuntu/Debian: sudo apt install flatpak flatpak-builder")
        print("  - For Fedora: sudo dnf install flatpak flatpak-builder")
        print("  - For Arch: sudo pacman -S flatpak flatpak-builder")
        return False
    
    # Check for Flatpak runtimes
    try:
        result = subprocess.run(['flatpak', 'list', '--runtime'], 
                               stdout=subprocess.PIPE, text=True, check=True)
        
        if 'org.freedesktop.Platform' not in result.stdout:
            print("⚠️ FreeDesktop Platform runtime not found")
            print("Running: flatpak install flathub org.freedesktop.Platform//23.08")
            subprocess.run(['flatpak', 'install', 'flathub', 'org.freedesktop.Platform//23.08', '-y'], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Could not check Flatpak runtimes")
        print("Please make sure you have the FreeDesktop Platform runtime installed:")
        print("flatpak install flathub org.freedesktop.Platform//23.08")
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

def create_flatpak_manifest():
    """Create a Flatpak manifest for Route Planner."""
    version = get_version()
    project_root = Path(__file__).parent.parent
    manifest_dir = project_root / "flatpak"
    manifest_dir.mkdir(parents=True, exist_ok=True)
    
    # Get dependencies from requirements.txt
    dependencies = []
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        with open(req_file, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Clean up version specifiers
                    pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                    dependencies.append(pkg)
    
    # Create manifest
    manifest = {
        "app-id": "org.routeplanner.RoutePlanner",
        "runtime": "org.freedesktop.Platform",
        "runtime-version": "23.08",
        "sdk": "org.freedesktop.Sdk",
        "command": "route-planner",
        "finish-args": [
            "--share=network",
            "--share=ipc",
            "--socket=x11",
            "--socket=wayland",
            "--filesystem=home",
            "--device=dri"
        ],
        "modules": [
            {
                "name": "route-planner",
                "buildsystem": "simple",
                "build-commands": [
                    "cp -r . /app/lib/route-planner/",
                    "mkdir -p /app/bin",
                    "echo '#!/bin/bash' > /app/bin/route-planner",
                    "echo 'cd /app/lib/route-planner' >> /app/bin/route-planner",
                    "echo 'export PYTHONPATH=/app/lib/route-planner:$PYTHONPATH' >> /app/bin/route-planner",
                    "echo 'python3 -c \"import sys; sys.path.insert(0, \\\"/app/lib/route-planner\\\"); from route_planner.core import main; main()\" \"$@\"' >> /app/bin/route-planner",
                    "chmod +x /app/bin/route-planner",
                    "install -Dm644 flatpak/org.routeplanner.RoutePlanner.desktop /app/share/applications/org.routeplanner.RoutePlanner.desktop",
                    "mkdir -p /app/share/icons/hicolor/256x256/apps"
                ],
                "sources": [
                    {
                        "type": "dir",
                        "path": ".."
                    }
                ]
            }
        ]
    }
    
    # Create desktop file
    desktop_file_dir = manifest_dir
    desktop_file_dir.mkdir(parents=True, exist_ok=True)
    
    with open(desktop_file_dir / "org.routeplanner.RoutePlanner.desktop", "w") as f:
        f.write("""[Desktop Entry]
Name=Route Planner
Exec=route-planner
Icon=org.routeplanner.RoutePlanner
Type=Application
Categories=Office;Utility;
Comment=Delivery Route Optimization Application
Terminal=false
""")
    
    # Create launcher script
    script_dir = project_root / "scripts"
    with open(script_dir / "flatpak-run.sh", "w") as f:
        f.write("""#!/bin/sh
exec python3 -m route_planner.core "$@"
""")
    os.chmod(script_dir / "flatpak-run.sh", 0o755)
    
    # Save manifest
    with open(manifest_dir / "org.routeplanner.RoutePlanner.yml", "w") as f:
        yaml_str = json.dumps(manifest, indent=2)
        # Convert to YAML-like format expected by flatpak-builder
        yaml_str = yaml_str.replace('"', '')
        yaml_str = yaml_str.replace(',', '')
        yaml_str = yaml_str.replace('{', '')
        yaml_str = yaml_str.replace('}', '')
        yaml_str = yaml_str.replace('[', '')
        yaml_str = yaml_str.replace(']', '')
        f.write(yaml_str)
    
    return manifest_dir / "org.routeplanner.RoutePlanner.yml"

def build_flatpak(dry_run=False):
    """Build a Flatpak package for Route Planner."""
    if not check_requirements() and not dry_run:
        return 1
    
    print("Building Flatpak package...")
    version = get_version()
    project_root = Path(__file__).parent.parent
    build_dir = project_root / "build" / "flatpak"
    
    # Clean up previous build if not dry run
    if build_dir.exists() and not dry_run:
        shutil.rmtree(build_dir)
    
    # Create build directory if not dry run
    if not dry_run:
        build_dir.mkdir(parents=True)
    
    # Create manifest if it doesn't exist
    manifest_file = project_root / "flatpak" / "org.routeplanner.RoutePlanner.yml"
    if not manifest_file.exists():
        print("Creating Flatpak manifest...")
        if not dry_run:
            manifest_file = create_flatpak_manifest()
        else:
            # For dry run, just show what would be created
            print(f"Would create manifest at: {project_root / 'flatpak' / 'org.routeplanner.RoutePlanner.yml'}")
            print("Would create desktop file and launcher script")
    else:
        print(f"Using existing Flatpak manifest: {manifest_file}")
    
    # Build Flatpak
    if not dry_run:
        print(f"Building Flatpak for Route Planner v{version}...")
        try:
            subprocess.run([
                "flatpak-builder",
                "--force-clean",
                "--repo=repo",
                build_dir,
                str(manifest_file)
            ], cwd=project_root, check=True)
            
            # Create Flatpak bundle
            bundle_path = project_root / f"RoutePlanner-{version}.flatpak"
            subprocess.run([
                "flatpak", "build-bundle",
                "repo",
                str(bundle_path),
                "org.routeplanner.RoutePlanner"
            ], cwd=project_root, check=True)
            
            if bundle_path.exists():
                print(f"✅ Flatpak bundle created successfully: {bundle_path}")
                print(f"   Size: {bundle_path.stat().st_size / 1024 / 1024:.1f} MB")
                return 0
            else:
                print("❌ Flatpak bundle creation failed")
                return 1
        except subprocess.CalledProcessError as e:
            print(f"❌ Flatpak build failed: {e}")
            return 1
    else:
        # For dry run, just show what would be done
        print(f"Would build Flatpak for Route Planner v{version}")
        print(f"Would create bundle: {project_root / f'RoutePlanner-{version}.flatpak'}")
        return 0

if __name__ == "__main__":
    # Check for dry run
    dry_run = "--dry-run" in sys.argv or "-n" in sys.argv
    if dry_run:
        print("🧪 Running in dry run mode - no files will be created")
    
    # Check for help
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Usage: python build_flatpak.py [options]")
        print("\nOptions:")
        print("  --dry-run, -n    Run without creating any files")
        print("  --help, -h       Show this help message")
        sys.exit(0)
        
    sys.exit(build_flatpak(dry_run=dry_run))
