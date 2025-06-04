#!/bin/bash
# Route Planner User Installation Script (No Root Required)
# =========================================================
# This script installs Route Planner to the user's home directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
APP_NAME="Route Planner"
INSTALL_DIR="$HOME/.local/share/route-planner"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor"

# Function to print colored output
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Check requirements
check_requirements() {
    print_status "Checking requirements..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required. Install with: sudo apt install python3 python3-pip python3-venv"
        exit 1
    fi
    
    if ! command -v pip3 &> /dev/null; then
        print_error "pip3 is required. Install with: sudo apt install python3-pip"
        exit 1
    fi
    
    print_success "Requirements satisfied"
}

# Install application
install_app() {
    print_status "Installing Route Planner to $INSTALL_DIR..."
    
    # Create directories
    mkdir -p "$INSTALL_DIR" "$BIN_DIR" "$DESKTOP_DIR" "$ICON_DIR"
    
    # Copy files (excluding git, cache, and pycache)
    rsync -av --exclude='.git' --exclude='__pycache__' --exclude='cache' --exclude='*.pyc' . "$INSTALL_DIR/"
    
    # Create virtual environment
    print_status "Setting up Python environment..."
    python3 -m venv "$INSTALL_DIR/venv"
    source "$INSTALL_DIR/venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$INSTALL_DIR/requirements.txt"
    deactivate
    
    print_success "Application installed"
}

# Create launcher
create_launcher() {
    print_status "Creating launcher..."
    
    cat > "$BIN_DIR/route-planner" << EOF
#!/bin/bash
cd "$INSTALL_DIR"
source "$INSTALL_DIR/venv/bin/activate"
python3 main.py "\$@"
EOF
    
    chmod +x "$BIN_DIR/route-planner"
    
    # Add to PATH if not already there
    if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
        echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
        print_status "Added $BIN_DIR to PATH in .bashrc"
    fi
    
    print_success "Launcher created"
}

# Create desktop integration
create_desktop_integration() {
    print_status "Creating desktop integration..."
    
    # Create icon
    cd "$INSTALL_DIR"
    if [ -f "linux/create_icon.py" ]; then
        source venv/bin/activate
        python3 linux/create_icon.py
        deactivate
        
        # Install icons
        if [ -d "linux/icons" ]; then
            cp -r linux/icons/hicolor/* "$ICON_DIR/"
        fi
    fi
    
    # Create desktop entry
    cat > "$DESKTOP_DIR/route-planner.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Route Planner
GenericName=Delivery Route Optimizer
Comment=Optimize delivery routes using advanced algorithms
Exec=$BIN_DIR/route-planner
Icon=route-planner
Terminal=false
Categories=Office;Utility;Geography;
Keywords=route;delivery;optimization;map;navigation;
StartupNotify=true
StartupWMClass=Route Planner
EOF
    
    chmod +x "$DESKTOP_DIR/route-planner.desktop"
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR"
    fi
    
    print_success "Desktop integration created"
}

# Create uninstaller
create_uninstaller() {
    cat > "$BIN_DIR/uninstall-route-planner" << EOF
#!/bin/bash
echo "Removing Route Planner..."
rm -rf "$INSTALL_DIR"
rm -f "$BIN_DIR/route-planner"
rm -f "$DESKTOP_DIR/route-planner.desktop"
find "$ICON_DIR" -name "route-planner.*" -delete 2>/dev/null || true
rm -f "$BIN_DIR/uninstall-route-planner"
echo "✅ Route Planner removed successfully"
EOF
    
    chmod +x "$BIN_DIR/uninstall-route-planner"
    print_success "Uninstaller created"
}

# Main installation
main() {
    echo "=============================================="
    echo "    Route Planner User Installation"
    echo "=============================================="
    echo
    
    check_requirements
    install_app
    create_launcher
    create_desktop_integration
    create_uninstaller
    
    echo
    echo "=============================================="
    print_success "Installation completed!"
    echo "=============================================="
    echo
    echo "📱 The app will appear in your Applications menu"
    echo "💻 Run from terminal: route-planner"
    echo "🗑️  Uninstall with: uninstall-route-planner"
    echo
    print_status "Note: You may need to log out and back in for the app to appear in the menu"
    echo
}

# Run installation
main "$@"
