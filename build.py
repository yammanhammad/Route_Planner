#!/usr/bin/env python3
"""
Route Planner Build Script
==========================

This script creates distributable packages for the Route Planner application.
It generates:
1. Source distribution (.tar.gz)
2. Wheel distribution (.whl)
3. Platform-specific archives (.zip for Windows, .tar.gz for Linux/macOS)
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path
import argparse
import datetime

def run_command(cmd, cwd=None):
    """Run a command and return its output."""
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            check=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(cmd)}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        sys.exit(1)

def main():
    """Main build function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Build Route Planner distribution packages')
    parser.add_argument('--version', default='1.0.0', help='Version number for the release')
    parser.add_argument('--clean', action='store_true', help='Clean build directories before building')
    parser.add_argument('--all', action='store_true', help='Build all package types')
    parser.add_argument('--sdist', action='store_true', help='Build source distribution')
    parser.add_argument('--wheel', action='store_true', help='Build wheel distribution')
    parser.add_argument('--archive', action='store_true', help='Build platform-specific archive')
    
    args = parser.parse_args()
    
    # If no specific package type is selected, build all
    if not (args.sdist or args.wheel or args.archive):
        args.all = True
    
    # If --all is specified, build all package types
    if args.all:
        args.sdist = args.wheel = args.archive = True
    
    # Get project directory
    project_dir = Path(__file__).parent.absolute()
    build_dir = project_dir / 'dist'
    
    # Create version with date for archive filename
    today = datetime.datetime.now().strftime('%Y%m%d')
    version_with_date = f"{args.version}-{today}"
    
    # Clean build directories if requested
    if args.clean:
        print("🧹 Cleaning build directories...")
        for dir_to_clean in ['build', 'dist', '*.egg-info']:
            for path in project_dir.glob(dir_to_clean):
                if path.is_dir():
                    shutil.rmtree(path)
                else:
                    path.unlink()
    
    # Create build directory if it doesn't exist
    build_dir.mkdir(exist_ok=True, parents=True)
    
    # Determine platform-specific info
    if platform.system() == 'Windows':
        platform_name = 'windows'
        archive_ext = 'zip'
        archive_cmd = ['powershell', 'Compress-Archive', '-Path']
    elif platform.system() == 'Darwin':
        platform_name = 'macos'
        archive_ext = 'tar.gz'
        archive_cmd = ['tar', 'czf']
    else:
        platform_name = 'linux'
        archive_ext = 'tar.gz'
        archive_cmd = ['tar', 'czf']
    
    # Build source distribution if requested
    if args.sdist:
        print("📦 Building source distribution...")
        run_command([sys.executable, 'setup.py', 'sdist'], cwd=project_dir)
        print("✅ Source distribution created")
    
    # Build wheel distribution if requested
    if args.wheel:
        print("🛞 Building wheel distribution...")
        run_command([sys.executable, 'setup.py', 'bdist_wheel'], cwd=project_dir)
        print("✅ Wheel distribution created")
    
    # Build platform-specific archive if requested
    if args.archive:
        print(f"📚 Building {platform_name} archive...")
        
        # Create a temporary directory for the archive contents
        archive_dir = project_dir / 'build' / f'route-planner-{version_with_date}'
        if archive_dir.exists():
            shutil.rmtree(archive_dir)
        archive_dir.mkdir(exist_ok=True, parents=True)
        
        # Files to include in the archive
        include_files = [
            'main.py', 'main_app.py', 'config.py', 'requirements.txt',
            'run_route_planner.sh', 'run_route_planner.bat', 'route_planner.py',
            'setup_env.py', 'install.py', 'README.md', 'LICENSE'
        ]
        
        # Directories to include
        include_dirs = ['route_planner']
        
        # Copy files to the archive directory
        for file in include_files:
            if (project_dir / file).exists():
                shutil.copy2(project_dir / file, archive_dir)
                # Make scripts executable in the archive
                if file.endswith('.py') or file.endswith('.sh') or file.endswith('.bat'):
                    os.chmod(archive_dir / file, 0o755)
        
        # Copy directories to the archive directory
        for dir_name in include_dirs:
            if (project_dir / dir_name).exists():
                shutil.copytree(
                    project_dir / dir_name, 
                    archive_dir / dir_name,
                    dirs_exist_ok=True
                )
        
        # Create empty directories that should be in the archive
        (archive_dir / 'cache').mkdir(exist_ok=True)
        
        # Create the archive
        archive_name = f"route-planner-{version_with_date}-{platform_name}.{archive_ext}"
        archive_path = build_dir / archive_name
        
        if platform.system() == 'Windows':
            # Windows uses PowerShell for creating zip archives
            run_command(
                archive_cmd + [
                    str(archive_dir) + '\\*', 
                    '-DestinationPath', 
                    str(archive_path)
                ]
            )
        else:
            # Linux/macOS use tar
            os.chdir(archive_dir.parent)
            run_command(
                archive_cmd + [
                    str(archive_path),
                    archive_dir.name
                ]
            )
        
        print(f"✅ {platform_name.capitalize()} archive created: {archive_name}")
    
    print("\n🎉 Build completed successfully!")
    print(f"📁 Distribution files are available in: {build_dir}")

if __name__ == "__main__":
    main()
