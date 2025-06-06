from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Read version dynamically (same system as package)
def get_version():
    """Get version using the same dynamic system as the package."""
    import os
    import subprocess
    from pathlib import Path
    
    # Get current directory (setup.py location)
    current_dir = Path.cwd()
    
    # Try git tags first (single source of truth)
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            cwd=current_dir,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().lstrip('v')
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    
    # Try environment variable
    version = os.getenv('VERSION')
    if version:
        return version.lstrip('v')
    
    # Fallback version (must match package fallback)
    return "1.1.12"

setup(
    name="route-planner",
    version=get_version(),
    author="Route Planner Development Team",
    author_email="your.email@example.com",
    description="A PyQt5-based delivery route optimization application",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yammanhammad/Route_Planner",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "route-planner=route_planner.core:main",
        ],
    },
)
