# Default configuration for Delivery Route Planner
# Modify values as needed for your local environment

# Main configuration
HQ_COORD = (24.848000, 67.032000)  # Headquarters coordinates (change to your location)
MIN_STOP_DISTANCE = 0.003  # Minimum distance between stops (~330m)
MAX_STOPS_EXACT_ALGORITHM = 12  # Maximum stops for exact algorithm
DEFAULT_STOPS = 5  # Default number of stops

# Map configuration
MAP_ZOOM = 14  # Initial zoom level for maps
MAP_TILES = "cartodb dark_matter"  # Map tile style (alternatives: "openstreetmap", "cartodbpositron")
BUFFER_SIZE = 0.003  # Approximately 330 meters buffer for graph extraction
JITTER_BASE = 0.00008  # Base jitter size for node disambiguation (~9m per step)
POINT_JITTER = 0.00005  # Jitter amount for marker placement (~5.5m)

# UI configuration
PANEL_WIDTH = 400  # Width of the control panel in pixels
SPINBOX_HEIGHT = 30  # Height of number spinboxes

# Cache configuration
CACHE_TIMEOUT = 60 * 60 * 24 * 7  # 1 week in seconds

# Logging configuration
LOG_LEVEL = "INFO"  # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
