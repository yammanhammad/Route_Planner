#!/bin/bash
"""
Route Planner Launcher Script
============================

This script provides a robust way to launch the Route Planner application
with proper environment setup and dependency checking.
"""

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}🚀 Starting Route Planner...${NC}"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}✅ Python $PYTHON_VERSION detected${NC}"

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo -e "${YELLOW}🔧 Activating virtual environment...${NC}"
    source .venv/bin/activate
else
    echo -e "${YELLOW}⚠️  No virtual environment found, using system Python${NC}"
fi

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo -e "${YELLOW}📦 Checking dependencies...${NC}"
    pip install -r requirements.txt --quiet
fi

# Launch the application
echo -e "${GREEN}🎯 Launching Route Planner application...${NC}"
python3 -m route_planner.core "$@"
