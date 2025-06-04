#!/bin/bash
# Quick installation test script
# This simulates the installation process without requiring sudo

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Test installation in a temporary directory
TEST_DIR="/tmp/route-planner-test-$$"
echo "Testing Route Planner installation process..."
echo "Test directory: $TEST_DIR"

# Create test installation directory
mkdir -p "$TEST_DIR"

# Copy application files (excluding git, cache, and pycache)
print_status "Copying application files..."
rsync -av --exclude='.git' --exclude='__pycache__' --exclude='cache' --exclude='*.pyc' . "$TEST_DIR/"

# Create virtual environment
print_status "Creating Python virtual environment..."
python3 -m venv "$TEST_DIR/venv"

# Install dependencies
print_status "Installing Python dependencies..."
cd "$TEST_DIR"
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Test icon creation
print_status "Testing icon creation..."
if [ -f "linux/create_icon.py" ]; then
    if python3 -c "import PIL" 2>/dev/null; then
        python3 linux/create_icon.py
        if [ -d "linux/icons" ]; then
            print_success "Icon creation successful"
        else
            print_error "Icon creation failed - no icons directory"
        fi
    else
        print_error "PIL/Pillow not available"
        exit 1
    fi
else
    print_error "Icon creation script not found"
    exit 1
fi

# Test main application import
print_status "Testing main application import..."
if python3 -c "import sys; sys.path.insert(0, '.'); import main; print('✅ Main application imports successfully')"; then
    print_success "Application import test passed"
else
    print_error "Application import test failed"
    exit 1
fi

deactivate

print_success "All installation tests passed!"
print_status "Cleaning up test directory: $TEST_DIR"
rm -rf "$TEST_DIR"

echo "✅ Installation process verification complete!"
