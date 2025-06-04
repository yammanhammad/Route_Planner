#!/bin/bash
# Route Planner Linux Installation Script
# ======================================
# This script provides a simple one-command installation for Linux users

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="Route Planner"
EXECUTABLE_NAME="route-planner"
INSTALL_DIR="/opt/route-planner"
BIN_LINK="/usr/local/bin/route-planner"
DESKTOP_FILE="/usr/share/applications/route-planner.desktop"
ICON_DIR="/usr/share/icons/hicolor"

# Function to print colored output
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

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        print_error "This script must be run as root (use sudo)"
        print_status "Usage: sudo ./install-linux.sh"
        exit 1
    fi
}

# Check system requirements
check_requirements() {
    print_status "Checking system requirements..."
    
    # Check Python 3
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is required but not installed"
        print_status "Install with: sudo apt install python3 python3-pip python3-venv"
        exit 1
    fi
    
    # Check pip
    if ! command -v pip3 &> /dev/null; then
        print_warning "pip3 not found, installing..."
        apt update && apt install -y python3-pip
    fi
    
    # Check required system packages
    local packages=("python3-dev" "python3-venv" "python3-tk" "libqt5-dev")
    local missing_packages=()
    
    for package in "${packages[@]}"; do
        if ! dpkg -l | grep -q "^ii.*$package "; then
            missing_packages+=("$package")
        fi
    done
    
    if [ ${#missing_packages[@]} -ne 0 ]; then
        print_status "Installing required system packages: ${missing_packages[*]}"
        apt update
        apt install -y "${missing_packages[@]}"
    fi
    
    print_success "System requirements satisfied"
}

# Install the application
install_application() {
    print_status "Installing Route Planner..."
    
    # Create installation directory
    mkdir -p "$INSTALL_DIR"
    
    # Copy application files
    # Copy files (excluding git, cache, and pycache)
    rsync -av --exclude='.git' --exclude='__pycache__' --exclude='cache' --exclude='*.pyc' . "$INSTALL_DIR/"
    
    # Create virtual environment
    print_status "Creating Python virtual environment..."
    python3 -m venv "$INSTALL_DIR/venv"
    
    # Activate virtual environment and install dependencies
    print_status "Installing Python dependencies..."
    source "$INSTALL_DIR/venv/bin/activate"
    pip install --upgrade pip
    pip install -r "$INSTALL_DIR/requirements.txt"
    deactivate
    
    print_success "Application installed to $INSTALL_DIR"
}

# Create executable launcher
create_launcher() {
    print_status "Creating system launcher..."
    
    cat > "$BIN_LINK" << EOF
#!/bin/bash
# Route Planner Launcher
cd "$INSTALL_DIR"
source "$INSTALL_DIR/venv/bin/activate"
python3 main_app.py "\$@"
deactivate
EOF
    
    chmod +x "$BIN_LINK"
    print_success "Launcher created at $BIN_LINK"
}

# Install desktop integration
install_desktop_integration() {
    print_status "Installing desktop integration..."
    
    # Create application icon
    if [ -f "linux/create_icon.py" ]; then
        cd "$INSTALL_DIR"
        source venv/bin/activate
        
        # Check if PIL/Pillow is available
        if python3 -c "import PIL" 2>/dev/null; then
            print_status "Creating application icons..."
            python3 linux/create_icon.py
            
            # Install icons if created successfully
            if [ -d "linux/icons" ]; then
                cp -r linux/icons/hicolor/* "$ICON_DIR/"
                print_success "Application icons installed"
            else
                print_warning "Icon creation succeeded but icons directory not found"
            fi
        else
            print_warning "PIL/Pillow not available, skipping icon creation"
            # Create a simple text-based fallback icon or skip
        fi
        
        deactivate
    else
        print_warning "Icon creation script not found, skipping custom icons"
    fi
    
    # Install desktop entry
    cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Route Planner
GenericName=Delivery Route Optimizer
Comment=Optimize delivery routes using advanced algorithms and TSP solutions
Exec=$BIN_LINK
Icon=route-planner
Terminal=false
Categories=Office;Utility;Geography;Education;
Keywords=route;delivery;optimization;map;navigation;TSP;algorithm;
StartupNotify=true
StartupWMClass=Route Planner
EOF
    
    chmod 644 "$DESKTOP_FILE"
    
    # Update desktop database
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database /usr/share/applications
    fi
    
    # Update icon cache
    if command -v gtk-update-icon-cache &> /dev/null; then
        gtk-update-icon-cache -f -t "$ICON_DIR"
    fi
    
    print_success "Desktop integration installed"
}

# Create uninstaller
create_uninstaller() {
    cat > "/usr/local/bin/uninstall-route-planner" << 'EOF'
#!/bin/bash
# Route Planner Uninstaller

echo "Removing Route Planner..."

# Remove installation directory
sudo rm -rf /opt/route-planner

# Remove launcher
sudo rm -f /usr/local/bin/route-planner

# Remove desktop entry
sudo rm -f /usr/share/applications/route-planner.desktop

# Remove icons
sudo find /usr/share/icons -name "route-planner.*" -delete 2>/dev/null || true

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    sudo update-desktop-database /usr/share/applications
fi

# Update icon cache
if command -v gtk-update-icon-cache &> /dev/null; then
    sudo gtk-update-icon-cache -f -t /usr/share/icons/hicolor
fi

# Remove uninstaller itself
sudo rm -f /usr/local/bin/uninstall-route-planner

echo "✅ Route Planner has been completely removed from your system"
EOF
    
    chmod +x "/usr/local/bin/uninstall-route-planner"
    print_success "Uninstaller created at /usr/local/bin/uninstall-route-planner"
}

# Main installation process
main() {
    echo "=================================================="
    echo "         Route Planner Linux Installer"
    echo "=================================================="
    echo
    
    check_root
    check_requirements
    install_application
    create_launcher
    install_desktop_integration
    create_uninstaller
    
    echo
    echo "=================================================="
    print_success "Installation completed successfully!"
    echo "=================================================="
    echo
    echo "You can now:"
    echo "  • Launch from Applications menu: '$APP_NAME'"
    echo "  • Run from terminal: '$EXECUTABLE_NAME'"
    echo "  • Create desktop shortcut from Apps menu"
    echo
    echo "To uninstall: run 'sudo uninstall-route-planner'"
    echo
    print_status "Starting Route Planner..."
    
    print_status "Verifying installation..."
    
    # Test Python environment and basic imports
    cd "$INSTALL_DIR"
    source venv/bin/activate
    
    # Test if virtual environment is working
    if python3 -c "import sys; print('Python executable:', sys.executable)" 2>/dev/null; then
        print_success "Virtual environment is working"
    else
        print_warning "Virtual environment test failed"
    fi
    
    # Test if required packages are installed
    if python3 -c "import PyQt5, networkx, folium, osmnx; print('✅ Core dependencies available')" 2>/dev/null; then
        print_success "Core dependencies verified"
    else
        print_warning "Some dependencies may be missing"
    fi
    
    deactivate
    
    print_success "Installation verification completed!"
}

# Handle interruption
trap 'print_error "Installation interrupted"; exit 1' INT TERM

# Run main installation
main "$@"
