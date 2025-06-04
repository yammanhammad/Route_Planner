#!/bin/bash
# Route Planner - Environment Setup and Launcher
# This script ensures the virtual environment is properly activated before running the application

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"
REQUIREMENTS_FILE="$PROJECT_DIR/requirements.txt"
MAIN_APP="$PROJECT_DIR/main.py"

echo -e "${BLUE}🎯 Route Planner Environment Setup${NC}"

# Change to project directory
cd "$PROJECT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    echo -e "${YELLOW}🔧 Creating virtual environment...${NC}"
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}⚡ Activating virtual environment...${NC}"
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo -e "${YELLOW}📦 Upgrading pip...${NC}"
pip install --upgrade pip --quiet

# Install/update requirements
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo -e "${YELLOW}📦 Installing/updating dependencies...${NC}"
    pip install -r "$REQUIREMENTS_FILE" --quiet
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ requirements.txt not found${NC}"
    exit 1
fi

# Verify main application exists
if [ ! -f "$MAIN_APP" ]; then
    echo -e "${RED}❌ main.py not found${NC}"
    exit 1
fi

# Run the application
echo -e "${GREEN}🚀 Starting Route Planner...${NC}"
python "$MAIN_APP" "$@"
