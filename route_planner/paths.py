#!/usr/bin/env python3
"""
Path Utilities for Cross-Platform Compatibility
==============================================

This module provides path-related utility functions that ensure
cross-platform compatibility for the Route Planner application.
"""

import os
import sys
import platform
from pathlib import Path

def get_app_dir():
    """
    Get the application directory in a cross-platform compatible way.
    
    Returns:
        Path: The application directory
    """
    return Path(__file__).parent.absolute()

def get_home_dir():
    """
    Get the user's home directory in a cross-platform compatible way.
    
    Returns:
        Path: The user's home directory
    """
    return Path.home()

def get_config_dir():
    """
    Get the configuration directory in a cross-platform compatible way.
    
    Returns:
        Path: The configuration directory
    """
    # Check for WINDOWS_MOCK environment variable for testing
    if os.environ.get('WINDOWS_MOCK') == 'true':
        app_data = os.environ.get('APPDATA')
        if app_data:
            return Path(app_data) / "RoutePlanner"
    
    if platform.system() == "Windows":
        # Use AppData/Roaming on Windows
        app_data = os.environ.get('APPDATA')
        if app_data:
            return Path(app_data) / "RoutePlanner"
        else:
            return get_home_dir() / ".route_planner"
    elif platform.system() == "Darwin":  # macOS
        return get_home_dir() / "Library/Application Support/RoutePlanner"
    else:  # Linux and other Unix
        xdg_config = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config:
            return Path(xdg_config) / "route_planner"
        else:
            return get_home_dir() / ".config/route_planner"

def get_cache_dir():
    """
    Get the cache directory in a cross-platform compatible way.
    
    Returns:
        Path: The cache directory
    """
    app_dir = get_app_dir()
    cache_dir = app_dir / "cache"
    
    # Create cache directory if it doesn't exist
    if not cache_dir.exists():
        try:
            cache_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create cache directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            cache_dir = Path(tempfile.gettempdir()) / "route_planner_cache"
            cache_dir.mkdir(parents=True, exist_ok=True)
    
    return cache_dir

def get_data_dir():
    """
    Get the data directory in a cross-platform compatible way.
    
    Returns:
        Path: The data directory
    """
    app_dir = get_app_dir()
    data_dir = app_dir / "data"
    
    # Create data directory if it doesn't exist
    if not data_dir.exists():
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create data directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            data_dir = Path(tempfile.gettempdir()) / "route_planner_data"
            data_dir.mkdir(parents=True, exist_ok=True)
    
    return data_dir

def get_logs_dir():
    """
    Get the logs directory in a cross-platform compatible way.
    
    Returns:
        Path: The logs directory
    """
    app_dir = get_app_dir()
    logs_dir = app_dir / "logs"
    
    # Create logs directory if it doesn't exist
    if not logs_dir.exists():
        try:
            logs_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"Warning: Failed to create logs directory: {e}")
            # Fallback to a temporary directory
            import tempfile
            logs_dir = Path(tempfile.gettempdir()) / "route_planner_logs"
            logs_dir.mkdir(parents=True, exist_ok=True)
    
    return logs_dir

def get_platform_script(script_name):
    """
    Get the appropriate script name for the current platform.
    
    Args:
        script_name (str): Base name of the script
    
    Returns:
        Path: The platform-specific script path
    """
    app_dir = get_app_dir().parent  # Go up one level to project root
    
    if platform.system() == "Windows":
        # Check for .bat extension first, then .py
        if (app_dir / f"{script_name}.bat").exists():
            return app_dir / f"{script_name}.bat"
        else:
            return app_dir / f"{script_name}.py"
    else:
        # Check for .sh extension first, then .py
        if (app_dir / f"{script_name}.sh").exists():
            return app_dir / f"{script_name}.sh"
        else:
            return app_dir / f"{script_name}.py"

def make_executable(file_path):
    """
    Make a file executable (Unix only).
    
    Args:
        file_path (Path): Path to the file
    """
    if platform.system() != "Windows" and os.path.exists(file_path):
        current_mode = os.stat(file_path).st_mode
        executable_mode = current_mode | 0o111  # Add executable bit for user/group/others
        os.chmod(file_path, executable_mode)

def ensure_dir_exists(dir_path):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        dir_path (Path): Path to the directory
    
    Returns:
        bool: True if the directory exists or was created, False otherwise
    """
    try:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {dir_path}: {e}")
        return False

def get_venv_python():
    """
    Get the path to the Python executable in the virtual environment.
    
    Returns:
        Path: Path to the Python executable
    """
    app_dir = get_app_dir()
    venv_dir = app_dir / ".venv"
    
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "python.exe"
    else:
        return venv_dir / "bin" / "python"

def get_venv_pip():
    """
    Get the path to the pip executable in the virtual environment.
    
    Returns:
        Path: Path to the pip executable
    """
    app_dir = get_app_dir()
    venv_dir = app_dir / ".venv"
    
    if platform.system() == "Windows":
        return venv_dir / "Scripts" / "pip.exe"
    else:
        return venv_dir / "bin" / "pip"

def normalize_path(path_str):
    """
    Normalize a path string to a Path object, handling platform-specific separators.
    
    Args:
        path_str (str): Path string to normalize
    
    Returns:
        Path: Normalized path
    """
    # Convert to Path object which handles normalization
    return Path(path_str)

if __name__ == "__main__":
    # Print path information for debugging
    print(f"Application Directory: {get_app_dir()}")
    print(f"Home Directory: {get_home_dir()}")
    print(f"Config Directory: {get_config_dir()}")
    print(f"Cache Directory: {get_cache_dir()}")
    print(f"Data Directory: {get_data_dir()}")
    print(f"Logs Directory: {get_logs_dir()}")
    print(f"Platform: {platform.system()}")
    print(f"Python: {sys.executable}")
    if platform.system() == "Windows":
        print(f"Windows-specific script: {get_platform_script('run_route_planner')}")
    else:
        print(f"Unix-specific script: {get_platform_script('run_route_planner')}")
