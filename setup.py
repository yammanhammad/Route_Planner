from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

# Read version from package
def get_version():
    """Get version from route_planner/__init__.py"""
    import re
    with open("route_planner/__init__.py", "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
    if match:
        return match.group(1)
    raise RuntimeError("Unable to find version string")

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
