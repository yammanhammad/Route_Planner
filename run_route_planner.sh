#!/bin/bash
# Route Planner - Root Launcher Script
# This script delegates to the actual launcher in the scripts directory

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Execute the main launcher script
exec "$SCRIPT_DIR/scripts/run_route_planner.sh" "$@"
