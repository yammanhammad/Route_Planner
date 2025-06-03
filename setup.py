from setuptools import setup, find_packages
import os

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the requirements from requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="route-planner",
    version="1.0.0",
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
            "route-planner=route_planner.main:main",
        ],
    },
)
