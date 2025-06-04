#!/usr/bin/env python3
"""
PyInstaller spec file for Windows build with Visual C++ Runtime bundling
This file ensures the Windows executable includes all necessary runtime components
"""

import sys
import os
from pathlib import Path

# Project paths
project_root = Path(SPECPATH).parent
route_planner_dir = project_root / "route_planner"

# Data files to include
added_files = [
    (str(project_root / "main.py"), "."),
    (str(project_root / "config.py"), "."),
    (str(route_planner_dir), "route_planner"),
]

# Hidden imports - all modules that PyInstaller might miss
hiddenimports = [
    'PyQt5.QtCore',
    'PyQt5.QtWidgets', 
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtGui',
    'PyQt5.QtWebEngine',
    'folium',
    'folium.plugins',
    'branca',
    'branca.colormap',
    'branca.element',
    'requests',
    'geopy',
    'geopy.geocoders',
    'networkx',
    'networkx.algorithms',
    'numpy',
    'numpy.core',
    'matplotlib',
    'matplotlib.pyplot',
    'urllib3',
    'certifi',
    'osmnx',
    'shapely',
    'shapely.geometry',
    'json',
    'hashlib',
    'tempfile',
    'logging',
    'functools',
    'contextlib',
    'route_planner.app',
    'route_planner.core',
    'route_planner.paths',
]

# Runtime hooks to ensure proper loading
runtime_hooks = [str(Path(SPECPATH) / "runtime_hook_vcruntime.py")]

# Analysis phase
a = Analysis(
    [str(project_root / "main.py")],
    pathex=[str(project_root)],
    binaries=[],
    datas=added_files,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=[
        'tkinter',
        'test',
        'unittest',
        'pdb',
        'doctest',
        'difflib',
    ],
    win_no_prefer_redirects=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary binaries to reduce size
binaries_to_exclude = [
    'api-ms-win-core-path-l1-1-0.dll',
    'api-ms-win-core-string-l1-1-0.dll',
    'api-ms-win-core-errorhandling-l1-1-0.dll',
]

a.binaries = [x for x in a.binaries if not any(exc in x[0] for exc in binaries_to_exclude)]

# Bundle everything
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the executable with runtime bundling
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='RoutePlanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,  # Disable UPX to avoid runtime issues
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Hide console window
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "icon.ico") if (project_root / "icon.ico").exists() else None,
    version_file=None,
    # Key settings for fixing ucrtbase.dll.crealf issue
    exclude_binaries=False,
    manifest=None,  # Let PyInstaller handle manifest automatically
)
