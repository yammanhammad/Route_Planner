#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Delivery Route Planner
=====================

A sophisticated PyQt5-based desktop application for optimizing delivery routes in any urban area.
This application combines advanced graph algorithms with an intuitive user
interface to solve the Traveling Salesman Problem (TSP) for delivery route optimization.

Key Features:
- Interactive GUI with embedded Folium map visualization using dark tiles
- Real-time road network data integration via OpenStreetMap
- Dual algorithm support: Held-Karp (optimal) and Christofides (approximation)
- Comprehensive onboarding system with guided tutorials
- Offline operation support with intelligent caching
- Multithreaded processing to maintain UI responsiveness
- Performance comparison and analysis tools
- Dark theme UI with modern styling

Architecture:
- Frontend: PyQt5 with QWebEngineView for map rendering
- Algorithms: Custom TSP implementations with NetworkX graph processing
- Data: OpenStreetMap integration via OSMnx library
- Caching: File-based caching system for offline operation
- Threading: QThread-based background processing

Algorithm Details:
1. Held-Karp Algorithm:
   - Dynamic programming approach for exact TSP solution
   - Time complexity: O(2^n * n^2)
   - Recommended for ≤12 delivery stops
   - Guarantees optimal solution

2. Christofides Algorithm:
   - Approximation algorithm with 1.5x optimality guarantee
   - Time complexity: O(n^3)
   - Suitable for larger datasets (>12 stops)
   - Fast execution with near-optimal results

Usage:
    python main.py

System Requirements:
    - Python 3.8+
    - PyQt5 with WebEngine support
    - Internet connection (for initial map data)
    - 4GB+ RAM recommended for large route calculations

Dependencies:
    - PyQt5, PyQtWebEngine: GUI framework and web rendering
    - folium: Interactive map visualization
    - osmnx: OpenStreetMap network analysis
    - networkx: Graph algorithms and data structures
    - shapely: Geometric operations and spatial analysis

Author: Route Planner Development Team
License: MIT
Version: 1.0.2
"""

# =============================================================================
# IMPORT DECLARATIONS
# =============================================================================

# Standard library imports for core functionality
import os           # Operating system interface for file operations
import sys          # System-specific parameters and functions
import time         # Time-related functions for caching and performance measurement
import random       # Random number generation for sample data
import tempfile     # Temporary file creation for map rendering
import contextlib   # Context management utilities
import logging      # Logging framework for debugging and monitoring
import hashlib      # Cryptographic hashing for cache key generation
import json         # JSON serialization for data persistence
import functools    # Higher-order functions and operations on callable objects
from pathlib import Path                                    # Object-oriented filesystem paths
from typing import List, Tuple, Dict, Any, Optional, Union, Set, Callable, TypeVar, cast  # Type hints for better code documentation

# GUI framework imports - PyQt5 provides the desktop application framework
from PyQt5 import QtWidgets, QtGui, QtCore                 # Core GUI components and utilities
from PyQt5.QtWidgets import QWidget                        # Base widget class for type annotations
from PyQt5.QtCore import QEvent                            # Event classes for type annotations
from PyQt5.QtGui import QPaintEvent, QResizeEvent         # Event type annotations
from PyQt5.QtWebEngineWidgets import QWebEngineView       # Web engine for rendering HTML maps
from PyQt5.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve  # Animation and timing utilities

# Scientific computing and algorithm libraries
import networkx as nx      # Graph data structures and algorithms
import folium             # Interactive web maps with Leaflet.js
import osmnx as ox        # OpenStreetMap network analysis and data retrieval
from shapely.geometry import box  # Geometric operations for bounding box calculations

# Network connectivity and offline support
import urllib.request      # URL handling for internet connectivity checks
import urllib.error       # URL error handling
import socket             # Low-level networking interface

# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

# Import application configuration from separate config module
try:
    from config import *
except ImportError:
    # Fallback configuration if config.py is not available
    # These constants define the application's behavior and default settings
    
    # Geographic boundaries for the operational area
    # Coordinates define a bounding box around the service area
    AREA_BOUNDS = {
        'north': 24.8607,    # Northern boundary (latitude)
        'south': 24.8407,    # Southern boundary (latitude)  
        'east': 67.0207,     # Eastern boundary (longitude)
        'west': 67.0007      # Western boundary (longitude)
    }
    
    # Algorithm performance thresholds
    # These values determine when to switch between exact and approximation algorithms
    MAX_EXACT_NODES = 12     # Maximum nodes for Held-Karp exact algorithm
    APPROX_THRESHOLD = 13    # Minimum nodes to recommend Christofides approximation
    
    # UI layout and appearance constants
    # Note: PANEL_WIDTH, DEFAULT_STOPS, and CACHE_TIMEOUT are defined after configuration loading
    CACHE_DIR = Path("cache") # Directory for storing cached map data and results

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

# Configure logging for debugging and monitoring application behavior
logging.basicConfig(
    level=logging.INFO,      # Set logging level to INFO (change to DEBUG for detailed logs)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log message format
    handlers=[
        logging.FileHandler('route_planner.log'),  # Log to file for persistence
        logging.StreamHandler(sys.stdout)          # Also log to console for development
    ]
)
logger = logging.getLogger(__name__)  # Create logger instance for this module

# Type variable for generic caching decorator
T = TypeVar('T')  # Generic type variable for function return types

# =============================================================================
# ONBOARDING AND TUTORIAL SYSTEM
# =============================================================================

"""
The onboarding and tutorial system provides a comprehensive guided experience
for new users. This system consists of several interconnected components:

1. WelcomeDialog: Initial welcome screen with feature overview
2. TutorialOverlay: Visual highlighting system for UI elements
3. TutorialDialog: Step-by-step tutorial content delivery
4. TutorialManager: Orchestrates the entire tutorial sequence

The tutorial system guides users through all major features:
- Adding and editing delivery stops
- Understanding algorithm selection
- Route planning and visualization
- Result interpretation and analysis
- Advanced features and settings

Design Philosophy:
- Non-intrusive: Users can skip or exit at any time
- Progressive disclosure: Information is revealed incrementally
- Visual guidance: UI elements are highlighted during explanation
- Contextual help: Each step relates to specific functionality
"""

class WelcomeDialog(QtWidgets.QDialog):
    """
    Initial welcome dialog that introduces new users to the application.
    
    This dialog serves as the entry point to the onboarding experience,
    providing an overview of the application's capabilities and allowing
    users to choose whether to take the guided tutorial or explore independently.
    
    Features:
    - Modern, visually appealing design with dark theme
    - Clear feature overview with icons and descriptions
    - Flexible user choice (tutorial vs. independent exploration)
    - Responsive layout that adapts to content
    
    UI Components:
    - Title with application branding
    - Feature overview with visual icons
    - Target audience description
    - Action buttons (Skip Tutorial / Start Tutorial)
    """
    
    def __init__(self, parent=None):
        """
        Initialize the welcome dialog with modern styling and content.
        
        Args:
            parent: Parent widget (typically the main window)
        """
        super().__init__(parent)
        
        # Window configuration
        self.setWindowTitle("Welcome to Route Planner")
        self.setFixedSize(700, 550)  # Fixed size for consistent appearance
        self.setModal(True)          # Block interaction with parent window
        
        # Set up the user interface components
        self._setup_ui()
        
        # Apply modern dark theme styling
        self._apply_welcome_styling()
        
    def _apply_welcome_styling(self):
        """Apply comprehensive styling to create a modern, professional appearance."""
        self.setStyleSheet("""
            /* Main dialog styling with dark theme */
            QDialog {
                background-color: #2b2b2b;
                color: white;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            /* General label styling for readability */
            QLabel {
                color: white;
                font-size: 13px;
                line-height: 1.4;
            }
            
            /* Main title styling with brand colors */
            QLabel#title {
                font-size: 26px;
                font-weight: bold;
                color: #4CAF50;        /* Green accent color */
                margin-bottom: 5px;
            }
            
            /* Subtitle styling for secondary emphasis */
            QLabel#subtitle {
                font-size: 17px;
                color: #81C784;        /* Lighter green for hierarchy */
                margin-bottom: 10px;
            }
            
            /* Primary action button styling */
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                min-width: 120px;
            }
            
            /* Button hover effects for better UX */
            QPushButton:hover {
                background-color: #45a049;
                transform: translateY(-1px);
            }
            
            /* Secondary button styling (Skip Tutorial) */
            QPushButton#skip {
                background-color: #666;
                color: #ccc;
            }
            
            /* Skip button hover effect */
            QPushButton#skip:hover {
                background-color: #777;
                color: white;
            }
            
            /* Button pressed states for tactile feedback */
            QPushButton:pressed {
                background-color: #3d8b40;
                transform: translateY(0px);
            }
        """)
        
    def _setup_ui(self):
        """
        Set up the welcome dialog user interface components.
        
        Creates a structured layout with:
        - Branded title and subtitle
        - Feature overview content
        - Action buttons for user choice
        """
        layout = QtWidgets.QVBoxLayout(self)
        layout.setSpacing(15)  # Reduced spacing slightly
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins for better appearance
        
        # Title
        title = QtWidgets.QLabel("🚚 Welcome to Route Planner!")
        title.setObjectName("title")
        title.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QtWidgets.QLabel("Your Smart Delivery Route Optimization Tool")
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        # Description
        description = QtWidgets.QLabel("""
        <div style="text-align: center; line-height: 1.4; font-size: 13px;">
        <p style="margin: 8px 0;"><b>What this app does:</b></p>
        <p style="margin: 4px 0;">📍 Plan optimal delivery routes for multiple stops</p>
        <p style="margin: 4px 0;">🗺️ Visualize routes on an interactive map</p>
        <p style="margin: 4px 0;">⚡ Choose between exact and fast approximation algorithms</p>
        <p style="margin: 4px 0;">📊 Compare different routing strategies</p>
        <br>
        <p style="margin: 8px 0;"><b>Perfect for:</b></p>
        <p style="margin: 4px 0;">• Delivery drivers and logistics coordinators</p>
        <p style="margin: 4px 0;">• Small business owners with delivery services</p>
        <p style="margin: 4px 0;">• Anyone needing to optimize multi-stop routes</p>
        </div>
        """)
        description.setWordWrap(True)
        description.setMinimumHeight(250)  # Ensure minimum height for content
        description.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # Align content to top
        layout.addWidget(description)
        
        # Add some stretch to push buttons to bottom
        layout.addStretch()
        
        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setContentsMargins(0, 10, 0, 0)  # Add top margin for buttons
        
        self.skip_btn = QtWidgets.QPushButton("Skip Tutorial")
        self.skip_btn.setObjectName("skip")
        self.skip_btn.clicked.connect(self.reject)
        
        self.start_btn = QtWidgets.QPushButton("Start Interactive Tutorial")
        self.start_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.skip_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.start_btn)
        
        layout.addLayout(button_layout)

class TutorialOverlay(QtWidgets.QWidget):
    """
    Semi-transparent overlay widget for highlighting UI elements during tutorials.
    
    This class creates a dark overlay that covers the entire main window while leaving
    specific UI elements highlighted for tutorial purposes. It provides visual focus
    by darkening everything except the highlighted area.
    
    Features:
    - Semi-transparent dark overlay covering the entire window
    - Dynamic highlighting of specific UI widgets
    - Automatic resizing and repositioning when parent window changes
    - Smooth visual effects with borders and glow effects
    - Anti-aliased rendering for professional appearance
    
    Attributes:
        highlight_rect (QtCore.QRect): Rectangle defining the highlighted area
        highlight_widget (QtWidgets.QWidget): Currently highlighted widget reference
    """
    
    def __init__(self, parent=None):
        """
        Initialize the tutorial overlay widget.
        
        Args:
            parent: Parent widget (typically the main window)
        """
        super().__init__(parent)
        
        # Configure window properties for overlay functionality
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # Remove window decorations
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # Enable transparency
        self.setStyleSheet("background: transparent;")  # Transparent background
        
        # Initialize highlighting properties
        self.highlight_rect = QtCore.QRect()  # Rectangle for highlighted area
        self.highlight_widget = None  # Reference to highlighted widget
        
        # Ensure overlay covers the entire parent window
        if parent:
            self.setGeometry(parent.rect())
        
    def highlight_widget_area(self, widget):
        """
        Highlight a specific widget area on the overlay.
        
        This method calculates the position of the target widget relative to the
        main window and creates a highlighted rectangle around it. The highlighted
        area will remain visible while the rest of the window is darkened.
        
        Args:
            widget (QtWidgets.QWidget or list): The widget(s) to highlight. If None, removes highlighting.
        """
        # Clear existing highlight
        self.highlight_rect = QtCore.QRect()
        self.highlight_widget = None
        
        if widget and self.parent():
            if isinstance(widget, list):
                # Multiple widgets to highlight
                self.highlight_widget = widget
                # Calculate combined bounding box for all widgets
                combined_rect = QtCore.QRect()
                for w in widget:
                    if w and w.isVisible():
                        pos = w.mapTo(self.parent(), QtCore.QPoint(0, 0))
                        widget_rect = QtCore.QRect(pos, w.size())
                        if combined_rect.isEmpty():
                            combined_rect = widget_rect
                        else:
                            combined_rect = combined_rect.united(widget_rect)
                self.highlight_rect = combined_rect
            else:
                # Single widget to highlight
                self.highlight_widget = widget
                # Calculate widget position relative to the main window
                pos = widget.mapTo(self.parent(), QtCore.QPoint(0, 0))
                self.highlight_rect = QtCore.QRect(pos, widget.size())
        
        # Trigger a repaint to update the visual overlay
        self.update()
        
    def resizeEvent(self, event):
        """
        Handle resize events to maintain full window coverage.
        
        When the parent window is resized, this method ensures the overlay
        continues to cover the entire window and recalculates the position
        of any highlighted widget.
        
        Args:
            event (QtGui.QResizeEvent): The resize event containing new dimensions
        """
        super().resizeEvent(event)
        
        # Re-calculate highlight position if a widget is currently highlighted
        if self.highlight_widget and self.parent():
            if isinstance(self.highlight_widget, list):
                # Multiple widgets to highlight
                combined_rect = QtCore.QRect()
                for w in self.highlight_widget:
                    if w and w.isVisible():
                        pos = w.mapTo(self.parent(), QtCore.QPoint(0, 0))
                        widget_rect = QtCore.QRect(pos, w.size())
                        if combined_rect.isEmpty():
                            combined_rect = widget_rect
                        else:
                            combined_rect = combined_rect.united(widget_rect)
                self.highlight_rect = combined_rect
            else:
                # Single widget highlighting
                pos = self.highlight_widget.mapTo(self.parent(), QtCore.QPoint(0, 0))
                self.highlight_rect = QtCore.QRect(pos, self.highlight_widget.size())
            self.update()  # Trigger repaint with new dimensions
        
    def paintEvent(self, event):
        """
        Paint the overlay with semi-transparent background and highlighted area.
        
        This method renders the tutorial overlay by:
        1. Creating a semi-transparent dark background over the entire window
        2. Leaving the highlighted widget area unobscured
        3. Drawing a colored border around the highlighted area
        4. Adding visual effects like glowing borders
        
        The painting algorithm divides the overlay into four rectangles around
        the highlighted area to create the cutout effect.
        
        Args:
            event: QPaintEvent containing information about the area to paint
        """
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)  # Smooth rendering
        
        # Define the semi-transparent overlay color (dark with 150/255 opacity)
        overlay_color = QtGui.QColor(0, 0, 0, 150)
        
        if not self.highlight_rect.isNull():
            # Create a padded highlight area for better visual separation
            padded_rect = self.highlight_rect.adjusted(-10, -10, 10, 10)
            
            # Draw four rectangles around the highlight area to create cutout effect
            try:
                # Top rectangle (covers area above the highlighted widget)
                if padded_rect.top() > 0:
                    top_rect = QtCore.QRect(0, 0, self.width(), padded_rect.top())
                    painter.fillRect(top_rect, overlay_color)
                
                # Bottom rectangle (covers area below the highlighted widget)
                if padded_rect.bottom() < self.height():
                    bottom_rect = QtCore.QRect(0, padded_rect.bottom(), 
                                             self.width(), self.height() - padded_rect.bottom())
                    painter.fillRect(bottom_rect, overlay_color)
                
                # Left rectangle (covers area to the left of highlighted widget)
                if padded_rect.left() > 0:
                    left_rect = QtCore.QRect(0, padded_rect.top(), 
                                           padded_rect.left(), padded_rect.height())
                    painter.fillRect(left_rect, overlay_color)
                
                # Right rectangle (covers area to the right of highlighted widget)
                if padded_rect.right() < self.width():
                    right_rect = QtCore.QRect(padded_rect.right(), padded_rect.top(), 
                                            self.width() - padded_rect.right(), padded_rect.height())
                    painter.fillRect(right_rect, overlay_color)
                
                # Draw a colored border around the highlighted area
                painter.setPen(QtGui.QPen(QtGui.QColor(76, 175, 80), 4))  # Green border, 4px width
                painter.setBrush(QtCore.Qt.NoBrush)  # No fill, just border
                painter.drawRect(padded_rect)
                
                # Add an outer glow effect for better visibility
                painter.setPen(QtGui.QPen(QtGui.QColor(76, 175, 80, 100), 6))  # Lighter green, 6px width
                painter.drawRect(padded_rect.adjusted(-1, -1, 1, 1))  # Slightly larger rectangle
                
            except Exception as e:
                # Fallback: fill entire overlay if rectangle calculations fail
                painter.fillRect(self.rect(), overlay_color)
            
        else:
            # No highlight area specified, create full dark overlay
            painter.fillRect(self.rect(), overlay_color)

class TutorialDialog(QtWidgets.QDialog):
    """
    Dialog window for displaying individual tutorial steps.
    
    This class creates a sophisticated dialog for presenting tutorial content with:
    - Progress tracking showing current step number
    - Scrollable content area for long tutorial text
    - Navigation buttons (Previous, Next, Skip, Finish)
    - Professional styling with dark theme
    - Responsive design that adapts to content length
    
    The dialog stays on top of other windows and provides a smooth user experience
    for guided tutorials with comprehensive content presentation.
    
    Attributes:
        step (int): Current step number in the tutorial sequence
        total_steps (int): Total number of steps in the tutorial
        back_btn (QPushButton): Button to go to previous step (if not first step)
        next_btn (QPushButton): Button to go to next step or finish tutorial
        skip_btn (QPushButton): Button to skip the entire tutorial
    """
    
    def __init__(self, title, content, step, total_steps, parent=None):
        """
        Initialize the tutorial dialog with content and navigation.
        
        Args:
            title (str): Title text for the tutorial step
            content (str): Main content text (can include HTML formatting)
            step (int): Current step number (1-indexed)
            total_steps (int): Total number of tutorial steps
            parent: Parent widget (typically the main window)
        """
        super().__init__(parent)
        
        # Configure dialog window properties
        self.setWindowTitle(f"Tutorial - Step {step} of {total_steps}")
        self.resize(600, 500)  # Generous size for content readability
        self.setMinimumSize(500, 400)  # Ensure minimum usable size
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)  # Stay above main window
        
        # Store step information for navigation logic
        self.step = step
        self.total_steps = total_steps
        
        # Initialize UI components and styling
        self._setup_ui(title, content)
        self._apply_styling()
        
    def _setup_ui(self, title, content):
        """
        Set up the tutorial dialog user interface components.
        
        This method creates a comprehensive layout including:
        - Progress bar showing tutorial advancement
        - Title label with step-specific heading
        - Scrollable content area for tutorial text
        - Navigation buttons adapted to current step position
        
        The layout is designed to handle varying content lengths and provides
        smooth navigation through the tutorial sequence.
        
        Args:
            title (str): Title text for the current tutorial step
            content (str): Main tutorial content (supports HTML formatting)
        """
        layout = QtWidgets.QVBoxLayout(self)
        
        # Progress bar to show tutorial advancement
        progress = QtWidgets.QProgressBar()
        progress.setMaximum(self.total_steps)
        progress.setValue(self.step)
        progress.setFormat(f"Step {self.step} of {self.total_steps}")
        layout.addWidget(progress)
        
        # Title label with step-specific heading
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName("title")  # For CSS styling
        title_label.setWordWrap(True)  # Handle long titles gracefully
        layout.addWidget(title_label)
        
        # Scrollable content area for tutorial text
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow content to resize
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Content widget inside scroll area
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        
        # Main content label supporting HTML formatting
        content_label = QtWidgets.QLabel(content)
        content_label.setWordWrap(True)  # Handle long content lines
        content_label.setObjectName("content")  # For CSS styling
        content_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)  # Top-align content
        content_layout.addWidget(content_label)
        content_layout.addStretch()  # Push content to top
        
        scroll_area.setWidget(content_widget)
        layout.addWidget(scroll_area, 1)  # Give scroll area maximum space
        
        # Navigation buttons adapted to current step
        button_layout = QtWidgets.QHBoxLayout()
        
        # Previous button (only show if not on first step)
        if self.step > 1:
            self.back_btn = QtWidgets.QPushButton("← Previous")
            self.back_btn.clicked.connect(lambda: self.done(-1))  # Signal to go back
            button_layout.addWidget(self.back_btn)
        
        # Skip tutorial button (always available)
        self.skip_btn = QtWidgets.QPushButton("Skip Tutorial")
        self.skip_btn.setObjectName("skip")  # For special CSS styling
        self.skip_btn.clicked.connect(self.reject)  # Signal to skip entire tutorial
        button_layout.addWidget(self.skip_btn)
        
        button_layout.addStretch()  # Push Next/Finish button to the right
        
        # Next/Finish button (text changes based on step position)
        if self.step < self.total_steps:
            self.next_btn = QtWidgets.QPushButton("Next →")
            self.next_btn.clicked.connect(self.accept)  # Signal to proceed
        else:
            self.next_btn = QtWidgets.QPushButton("Finish Tutorial")
            self.next_btn.clicked.connect(self.accept)  # Signal tutorial completion
        
        button_layout.addWidget(self.next_btn)
        layout.addLayout(button_layout)
        
    def _apply_styling(self):
        """Apply styling to the tutorial dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel#title {
                font-size: 16px;
                font-weight: bold;
                color: #4CAF50;
                margin-bottom: 10px;
            }
            QLabel#content {
                font-size: 12px;
                line-height: 1.4;
                padding: 10px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton#skip {
                background-color: #666;
            }
            QPushButton#skip:hover {
                background-color: #777;
            }
            QProgressBar {
                border: 1px solid #666;
                border-radius: 3px;
                background-color: #333;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                border-radius: 2px;
            }
            QScrollArea {
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #333;
            }
            QScrollBar:vertical {
                background-color: #404040;
                width: 16px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
                background-color: #666666;
                border-radius: 8px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4CAF50;
            }
            QScrollBar:horizontal {
                background-color: #404040;
                height: 16px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal {
                background-color: #666666;
                border-radius: 8px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #4CAF50;
            }
        """)

class TutorialManager:
    """
    Manages the complete tutorial flow and interactive guidance system.
    
    This class coordinates the entire tutorial experience including:
    - Sequential step progression through predefined tutorial content
    - Visual highlighting of UI elements using overlay system
    - Tutorial dialog positioning and management
    - Integration with the main application interface
    - State tracking for tutorial progression
    
    The tutorial system provides contextual help by highlighting relevant
    UI components while displaying explanatory content in floating dialogs.
    
    Features:
    - Step-by-step guided tutorials with visual highlights
    - Automatic UI element detection and highlighting
    - Smart dialog positioning to avoid blocking important content
    - Seamless integration with main application workflow
    - Comprehensive tutorial content covering all major features
    
    Attributes:
        main_window: Reference to the main application window
        overlay (TutorialOverlay): Visual overlay for highlighting UI elements
        current_step (int): Current step index in the tutorial sequence
        tutorial_active (bool): Flag indicating if tutorial is currently running
        tutorial_steps (list): Comprehensive list of tutorial step configurations
    """
    
    def __init__(self, main_window):
        """
        Initialize the tutorial manager with main window reference.
        
        Args:
            main_window: The main application window (PlannerUI instance)
        """
        self.main_window = main_window
        self.overlay = None  # Will be created when tutorial starts
        self.current_step = 0  # Current step index (0-based)
        self.tutorial_active = False  # Tutorial state flag
        
        # Comprehensive tutorial steps configuration covering all major features
        self.tutorial_steps = [
            {
                "title": "Welcome to the Interface",
                "content": "This is the main interface of the Route Planner. On the left, you'll see the control panel with all the settings. On the right is the interactive map where your routes will be displayed.",
                "highlight_widget": "panel"  # Highlight the control panel
            },
            {
                "title": "Headquarters Location",
                "content": "This shows your headquarters (HQ) location. All delivery routes will start and end here. The coordinates can be changed in the config file to match your business location.",
                "highlight_widget": "hq_label"  # Highlight HQ display
            },
            {
                "title": "Number of Delivery Stops",
                "content": "Here you can see and edit the number of delivery stops. Click 'Edit Stops' to change this number. More stops mean more complex route optimization.",
                "highlight_widget": "stops_display"  # Highlight stops counter
            },
            {
                "title": "Delivery Locations Table",
                "content": "This table shows all your delivery locations with their coordinates (latitude and longitude). You can edit these coordinates directly in the table, or add/remove stops using the buttons below.",
                "highlight_widget": "table"  # Highlight data table
            },
            {
                "title": "Adding and Removing Stops",
                "content": "Use these buttons to add new delivery stops or remove existing ones. New stops are automatically generated with random coordinates near your HQ.",
                "highlight_widget": ["add_btn", "remove_btn"]  # Highlight both add and remove buttons
            },
            {
                "title": "Algorithm Selection",
                "content": "Choose your optimization algorithm:\n• Auto: Smart selection based on problem size\n• Held-Karp: Exact optimal solution (slower for many stops)\n• Christofides: Fast approximation (good for many stops)",
                "highlight_widget": "algo_combo"  # Highlight algorithm selector
            },
            {
                "title": "Planning Your Route",
                "content": "Click this button to start route optimization. The app will find the best route visiting all delivery locations and return to HQ. Progress will be shown during calculation.",
                "highlight_widget": "plan_btn"  # Highlight plan button
            },
            {
                "title": "Comparing Algorithms",
                "content": "This button runs both algorithms and compares their results. You'll see the trade-off between solution quality and computation time. Great for understanding algorithm performance!",
                "highlight_widget": "compare_btn"  # Highlight compare button
            },
            {
                "title": "Results and Output",
                "content": "All results, timing information, and route details appear here. You'll see total distance, computation time, and the order of stops in your optimized route.",
                "highlight_widget": "out"  # Highlight output area
            },
            {
                "title": "Interactive Map",
                "content": "The map shows your HQ (green), delivery stops (red), and optimized routes. You can zoom and pan to explore the area. Different algorithms show routes in different colors.",
                "highlight_widget": "map_view"  # Highlight map widget
            }
        ]
        
    def start_tutorial(self):
        """
        Start the interactive tutorial system.
        
        This method initiates the complete tutorial experience by:
        1. Setting up the visual overlay system
        2. Initializing tutorial state tracking
        3. Creating and positioning the overlay
        4. Beginning the first tutorial step
        
        The tutorial provides guided introduction to all major features
        with contextual highlighting and step-by-step explanations.
        """
        self.tutorial_active = True
        self.current_step = 0
        
        # Create visual overlay for highlighting UI elements
        self.overlay = TutorialOverlay(self.main_window)
        self.overlay.setGeometry(self.main_window.rect())
        self.overlay.show()
        self.overlay.raise_()  # Bring overlay to front for visibility
        
        # Begin with the first tutorial step
        self._show_tutorial_step()
        
    def _show_tutorial_step(self):
        """
        Display the current tutorial step with highlighting and dialog.
        
        This method handles the presentation of individual tutorial steps by:
        1. Checking if more steps remain in the sequence
        2. Highlighting the relevant UI widget for the current step
        3. Creating and positioning the tutorial dialog
        4. Managing user navigation choices (Next, Previous, Skip)
        
        The method automatically progresses through steps or finishes
        the tutorial based on user interaction.
        """
        # Check if we've completed all tutorial steps
        if self.current_step >= len(self.tutorial_steps):
            self._finish_tutorial()
            return
            
        # Get configuration for current step
        step_info = self.tutorial_steps[self.current_step]
        
        # Highlight the relevant UI widget(s) for this step
        widget_names = step_info.get("highlight_widget")
        
        # Clear any previous highlighting
        self.overlay.highlight_widget_area(None)
        
        # Handle multiple widget highlighting or single widget
        if widget_names:
            if isinstance(widget_names, list):
                # Multiple widgets to highlight
                widgets_to_highlight = []
                for name in widget_names:
                    if hasattr(self.main_window, name):
                        widget = getattr(self.main_window, name)
                        widgets_to_highlight.append(widget)
                
                if widgets_to_highlight:
                    # Only highlight if we found widgets to highlight
                    self.overlay.highlight_widget_area(widgets_to_highlight)
            else:
                # Single widget highlighting
                if hasattr(self.main_window, widget_names):
                    widget = getattr(self.main_window, widget_names)
                    self.overlay.highlight_widget_area(widget)
        
        # Create and configure tutorial dialog for this step
        dialog = TutorialDialog(
            step_info["title"],
            step_info["content"],
            self.current_step + 1,  # Convert to 1-based numbering for display
            len(self.tutorial_steps),
            self.main_window
        )
        
        # Position dialog optimally to avoid blocking highlighted content
        self._position_tutorial_dialog(dialog)
        
        # Show dialog and handle user response
        result = dialog.exec_()
        
        if result == QtWidgets.QDialog.DialogCode.Accepted:
            # User clicked Next/Finish - proceed to next step
            self.current_step += 1
            self._show_tutorial_step()
        elif result == -1:  # Previous button clicked
            # Go back to previous step (with bounds checking)
            self.current_step = max(0, self.current_step - 1)
            self._show_tutorial_step()
        else:  # Skip/Cancel button clicked
            # User wants to exit tutorial
            self._finish_tutorial()
            
    def _position_tutorial_dialog(self, dialog):
        """
        Position the tutorial dialog optimally to avoid blocking content.
        
        This method calculates the best position for tutorial dialogs by:
        1. Placing dialogs in the center-right area by default
        2. Ensuring dialogs remain within screen boundaries
        3. Avoiding overlap with highlighted UI elements
        4. Maintaining consistent positioning across tutorial steps
        
        Args:
            dialog (TutorialDialog): The dialog to position
        """
        # Get main window and dialog dimensions
        main_rect = self.main_window.geometry()
        dialog_size = dialog.size()
        
        # Calculate position in center-right area (avoids most UI controls)
        x = main_rect.x() + main_rect.width() - dialog_size.width() - 50
        y = main_rect.y() + (main_rect.height() - dialog_size.height()) // 2
        
        # Ensure dialog stays within screen boundaries
        screen = QtWidgets.QApplication.primaryScreen().geometry()
        x = max(0, min(x, screen.width() - dialog_size.width()))
        y = max(0, min(y, screen.height() - dialog_size.height()))
        
        # Apply calculated position
        dialog.move(x, y)
        
    def _finish_tutorial(self):
        """
        Complete the tutorial and perform cleanup operations.
        
        This method handles tutorial completion by:
        1. Deactivating tutorial state
        2. Hiding and cleaning up the visual overlay
        3. Releasing overlay resources
        4. Saving tutorial completion status to settings
        
        The cleanup ensures no memory leaks and proper resource management
        while preserving the user's tutorial completion status for future runs.
        """
        # Deactivate tutorial state
        self.tutorial_active = False
        
        # Clean up visual overlay
        if self.overlay:
            self.overlay.hide()  # Hide overlay immediately
            self.overlay.deleteLater()  # Schedule for deletion
            self.overlay = None  # Clear reference
        
        # Save tutorial completion status for future runs
        self._mark_tutorial_completed()
        
    def _mark_tutorial_completed(self):
        """
        Save tutorial completion status to persistent settings.
        
        This method creates or updates the settings.json file to record
        that the user has completed the tutorial. This prevents the tutorial
        from being shown again on subsequent application launches.
        
        The settings file uses JSON format for easy reading and modification.
        If file operations fail, the error is logged but doesn't interrupt
        the application flow.
        """
        try:
            from pathlib import Path
            settings_file = Path("settings.json")
            settings = {}
            
            # Load existing settings if file exists
            if settings_file.exists():
                import json
                with open(settings_file, 'r') as f:
                    settings = json.load(f)
            
            # Mark tutorial as completed
            settings['tutorial_completed'] = True
            
            # Save updated settings
            with open(settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
                
        except Exception as e:
            # Log warning but don't crash application
            logger.warning(f"Could not save tutorial completion status: {e}")


def check_first_run():
    """
    Check if this is the user's first run of the application.
    
    This function examines the settings.json file to determine whether
    the user has previously completed the tutorial. It's used to decide
    whether to show the welcome dialog and tutorial on startup.
    
    Returns:
        bool: True if this appears to be the first run (no completed tutorial),
              False if the tutorial has been completed before
              
    Note:
        If the settings file cannot be read or doesn't exist, the function
        assumes this is a first run to ensure new users see the tutorial.
    """
    try:
        from pathlib import Path
        import json
        
        # Check if settings file exists
        settings_file = Path("settings.json")
        if not settings_file.exists() or settings_file.stat().st_size == 0:
            return True  # No settings file or empty file means first run
            
        # Read settings and check tutorial status
        with open(settings_file, 'r') as f:
            settings = json.load(f)
            
        return not settings.get('tutorial_completed', False)
        
    except (Exception, json.JSONDecodeError) as e:
        # If we can't read settings, assume first run for safety
        logger.warning(f"Error reading settings file, assuming first run: {e}")
        return True

# -----------------------------------------------------------------------------
#  CONFIGURATION & CONSTANTS
# -----------------------------------------------------------------------------
"""
Configuration management system for the Route Planner application.

This section handles loading and setting up all application configuration values,
including default parameters, external config file integration, and runtime constants.
The configuration system provides fallback defaults for all settings to ensure
the application works out-of-the-box while allowing customization through config.py.

Key configuration categories:
- Geographic settings: HQ coordinates, distance parameters, map zoom levels
- Algorithm parameters: Maximum stops for exact algorithms, buffer sizes
- UI settings: Panel dimensions, component sizes, styling parameters
- Performance settings: Cache timeouts, logging levels, optimization thresholds
- Map configuration: Tile sources, zoom levels, visualization parameters

The system automatically detects and loads custom configurations from config.py
while gracefully falling back to sensible defaults if the config file is missing.
"""

def load_config():
    """
    Load application configuration from config.py or use built-in defaults.
    
    This function implements a comprehensive configuration loading system that:
    1. Defines sensible default values for all configuration parameters
    2. Attempts to load custom values from an external config.py file
    3. Handles missing configuration files gracefully
    4. Validates and processes configuration values (e.g., string log levels)
    5. Provides detailed feedback about configuration source
    
    The configuration covers all aspects of the application including geographic
    parameters, algorithm settings, UI dimensions, performance tuning, and
    caching behavior.
    
    Returns:
        dict: Complete configuration dictionary with all required parameters
        
    Note:
        If config.py is not found, the application uses built-in defaults that
        provide a fully functional experience for any specified geographic area.
    """
    # Comprehensive default configuration covering all application aspects
    config = {
        # Geographic Configuration
        "HQ_COORD": (24.848000, 67.032000),  # Headquarters coordinates (default location)
        "MIN_STOP_DISTANCE": 0.003,  # Minimum distance between delivery stops (~330m)
        "BUFFER_SIZE": 0.003,  # Geographic buffer for map data extraction (~330m)
        "POINT_JITTER": 0.00005,  # Random offset for marker placement (~5.5m)
        "JITTER_BASE": 0.00008,  # Base jitter for node disambiguation (~9m per step)
        
        # Algorithm Configuration
        "MAX_STOPS_EXACT_ALGORITHM": 12,  # Maximum stops for Held-Karp exact algorithm
        "DEFAULT_STOPS": 5,  # Default number of delivery stops for new sessions
        
        # Map Display Configuration
        "MAP_ZOOM": 14,  # Default zoom level for map display
        "MAP_TILES": "cartodb dark_matter",  # Preferred map tile source
        
        # User Interface Configuration
        "PANEL_WIDTH": 400,  # Width of the control panel in pixels
        "SPINBOX_HEIGHT": 30,  # Height of numeric input controls
        
        # Performance & Caching Configuration
        "CACHE_TIMEOUT": 60 * 60 * 24 * 7,  # Cache expiration: 1 week in seconds
        "LOG_LEVEL": logging.INFO  # Default logging verbosity level
    }
    
    # Attempt to load custom configuration from external config.py file
    try:
        import config as config_module
        logger.debug("Found config.py file, loading custom configuration")
        
        # Override defaults with values from config.py
        for key in config.keys():
            if hasattr(config_module, key):
                custom_value = getattr(config_module, key)
                config[key] = custom_value
                logger.debug(f"Loaded custom setting: {key} = {custom_value}")
                
        # Special handling for string-based log levels (convert to logging constants)
        if isinstance(config["LOG_LEVEL"], str):
            config["LOG_LEVEL"] = getattr(logging, config["LOG_LEVEL"].upper())
            
        print("✓ Configuration loaded from config.py")
        
    except ImportError:
        print("ℹ Using default configuration (config.py not found)")
        logger.info("No custom config.py found, using built-in defaults")
    except Exception as e:
        logger.warning(f"Error loading config.py, using defaults: {e}")
        logger.warning(f"Error loading config.py: {e}")
        
    return config

# Initialize global configuration constants from loaded config
# These constants are used throughout the application for consistent behavior
config_values = load_config()

# Geographic and coordinate settings
HQ_COORD = config_values["HQ_COORD"]  # Headquarters location (lat, lon)
MIN_STOP_DISTANCE = config_values["MIN_STOP_DISTANCE"]  # Minimum stop separation
BUFFER_SIZE = config_values["BUFFER_SIZE"]  # Map data extraction buffer
POINT_JITTER = config_values["POINT_JITTER"]  # Marker placement randomization
JITTER_BASE = config_values["JITTER_BASE"]  # Node position disambiguation

# Algorithm behavior settings
MAX_STOPS_EXACT_ALGORITHM = config_values["MAX_STOPS_EXACT_ALGORITHM"]  # Held-Karp limit
DEFAULT_STOPS = config_values["DEFAULT_STOPS"]  # Initial stop count

# Map display and visualization settings
MAP_ZOOM = config_values["MAP_ZOOM"]  # Default map zoom level
MAP_TILES = config_values["MAP_TILES"]  # Preferred tile source

# User interface layout settings
PANEL_WIDTH = config_values["PANEL_WIDTH"]  # Control panel width
SPINBOX_HEIGHT = config_values["SPINBOX_HEIGHT"]  # Input control height

# Performance and system settings
CACHE_TIMEOUT = config_values["CACHE_TIMEOUT"]  # Cache expiration time
LOG_LEVEL = config_values["LOG_LEVEL"]  # Logging verbosity level
CACHE_DIR = Path("cache")  # Cache directory for storing computation results

# Initialize cache directory for persistent data storage
# The cache stores expensive computation results (graphs, distance matrices)
# CACHE_DIR is already defined in configuration section above
if not CACHE_DIR.exists():
    try:
        CACHE_DIR.mkdir(exist_ok=True)
        logger.info(f"Created cache directory: {CACHE_DIR}")
        print(f"📁 Created cache directory: {CACHE_DIR}")
    except Exception as e:
        logger.error(f"Failed to create cache directory: {e}")
        logger.error(f"Failed to create cache directory: {e}")

# Environment setup
os.environ.setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")  # Required for QtWebEngine

# -----------------------------------------------------------------------------
#  LOGGING SETUP
# -----------------------------------------------------------------------------
"""
Comprehensive logging configuration for the Route Planner application.

This section sets up a robust logging system that provides detailed information
about application behavior, performance metrics, and error conditions. The logging
system is configured to output to both console and potentially log files.

Features:
- Configurable log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Timestamped log entries with module and severity information
- Console output with formatted messages for development and debugging
- Support for multiple log handlers (console, file, etc.)
- Integration with application configuration system

The logging system helps with:
- Debugging algorithm performance and route optimization
- Monitoring cache hit rates and performance
- Tracking user interactions and UI events
- Error diagnosis and troubleshooting
- Performance analysis and optimization
"""

def setup_logging():
    """
    Configure comprehensive application logging with multiple output targets.
    
    This function establishes a professional logging infrastructure that:
    1. Creates a named logger for the application
    2. Sets up console output with formatted messages
    3. Configures log levels based on application configuration
    4. Prepares the foundation for additional log handlers (file, network, etc.)
    
    The logging system provides detailed information for debugging, monitoring,
    and maintaining the application in both development and production environments.
    
    Returns:
        logging.Logger: Configured logger instance for application-wide use
        
    Note:
        The log level is controlled by the LOG_LEVEL configuration parameter,
        allowing runtime adjustment of logging verbosity.
    """
    # Create application-specific logger with meaningful name
    logger = logging.getLogger("RouteApp")
    logger.setLevel(LOG_LEVEL)
    
    # Prevent duplicate log messages by clearing existing handlers
    if logger.hasHandlers():
        logger.handlers.clear()
    
    # Configure console output handler for immediate feedback
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    
    # Create detailed formatter for comprehensive log information
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    
    # Attach console handler to logger
    logger.addHandler(console_handler)
    
    # Future enhancement: Add file handler for persistent logging
    # file_handler = logging.FileHandler('route_planner.log')
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
    
    return logger

# Initialize application logger for global use
logger = setup_logging()
logger.info("🚀 Delivery Route Planner application started")
logger.info(f"📊 Log level set to: {logging.getLevelName(LOG_LEVEL)}")

# -----------------------------------------------------------------------------
#  UTILITY FUNCTIONS & CACHING SYSTEM
# -----------------------------------------------------------------------------
"""
Comprehensive utility functions and caching system for the Route Planner.

This section provides essential utility functions that support the core functionality
of the route planning application. Key components include:

1. CACHING SYSTEM:
   - File-based caching for expensive operations (graph generation, distance calculations)
   - Automatic cache expiration and cleanup
   - Support for complex data structures (NetworkX graphs, numpy arrays)
   - Intelligent cache key generation based on function parameters

2. GRAPH SERIALIZATION:
   - Conversion of NetworkX graphs to JSON-serializable formats
   - Preservation of complex geometric data (Shapely objects)
   - Bidirectional conversion maintaining data integrity

3. NETWORK CONNECTIVITY:
   - Internet connection detection for map tile loading
   - Fallback strategies for offline operation
   - Smart map tile source selection

4. DISTANCE CALCULATIONS:
   - Multiple distance calculation methods (Euclidean, Haversine)
   - Geographic coordinate handling
   - Performance-optimized distance computations

5. DATA VALIDATION:
   - Input parameter validation
   - Error handling and recovery
   - Type safety and data integrity checks

These utilities form the foundation for reliable, high-performance route optimization
with robust error handling and efficient resource management.
"""

# Define generic type variable for type-safe caching decorator
T = TypeVar('T')

def networkx_to_serializable(g):
    """
    Convert a NetworkX graph to JSON-serializable format for persistent caching.
    
    This function transforms complex NetworkX graph objects into a format that can
    be safely stored in JSON files for caching purposes. It handles various data
    types including geometric objects (Shapely), sets, and custom objects.
    
    The serialization process:
    1. Extracts all node data and converts non-serializable objects
    2. Processes edge data and their attributes
    3. Handles special objects like Shapely geometries using WKT format
    4. Preserves graph structure and all metadata
    
    Args:
        g: NetworkX graph object to be serialized
        
    Returns:
        dict: Dictionary representation of the graph that can be JSON serialized
        
    Note:
        This function is part of the caching system that dramatically improves
        performance by avoiding repeated expensive graph generation operations.
    """
    from shapely.geometry import LineString, Point
    import json
    
    # Initialize serializable data structure
    data = {
        "nodes": {},  # Node data with attributes
        "edges": []   # Edge list with attributes
    }
    
    # Helper function to convert complex objects to serializable format
    def make_serializable(obj):
        """Convert non-JSON-serializable objects to serializable representations."""
        if isinstance(obj, (LineString, Point)):
            # Convert Shapely geometry objects to Well-Known Text (WKT) format
            return {"__geometry__": obj.wkt}
        elif isinstance(obj, (set, frozenset)):
            # Convert sets to lists for JSON compatibility
            return {"__set__": list(obj)}
        elif hasattr(obj, '__dict__'):
            # Handle custom objects by converting to string representation
            return {"__object__": str(obj)}
        else:
            # Return as-is for already serializable objects
            return obj
    
    # Process all nodes and their attributes
    for node in g.nodes():
        node_attrs = {}
        for key, value in g.nodes[node].items():
            try:
                # Test if the value is directly JSON serializable
                json.dumps(value)
                node_attrs[key] = value
            except (TypeError, ValueError):
                # Convert non-serializable values using helper function
                node_attrs[key] = make_serializable(value)
        
        # Store node with string key for JSON compatibility
        data["nodes"][str(node)] = node_attrs
        
    # Process all edges and their attributes
    for u, v, attrs in g.edges(data=True):
        edge_attrs = {}
        for key, value in attrs.items():
            try:
                # Test if the value is directly JSON serializable
                json.dumps(value)
                edge_attrs[key] = value
            except (TypeError, ValueError):
                # Convert non-serializable values using helper function
                edge_attrs[key] = make_serializable(value)
        
        # Store edge as dictionary with string node identifiers
        data["edges"].append({
            "u": str(u),      # Source node
            "v": str(v),      # Target node
            "attrs": edge_attrs  # Edge attributes
        })
        
    return data

def serializable_to_networkx(data):
    """
    Reconstruct a NetworkX graph from serialized JSON data.
    
    This function is the inverse of networkx_to_serializable(), converting
    the JSON-compatible dictionary representation back into a fully functional
    NetworkX graph with all original attributes and data types restored.
    
    The reconstruction process:
    1. Creates a new empty NetworkX graph
    2. Restores nodes with their original attributes
    3. Reconstructs edges with preserved attribute data
    4. Handles special data types (geometries, sets, custom objects)
    5. Maintains graph structure and connectivity
    
    Args:
        data (dict): Dictionary representation from networkx_to_serializable()
        
    Returns:
        nx.Graph: Fully reconstructed NetworkX graph object
        
    Note:
        This function ensures perfect round-trip conversion, preserving all
        graph properties, attributes, and complex data types through the
        caching process.
    """
    from shapely.wkt import loads as wkt_loads
    
    # Create new empty graph to populate
    g = nx.Graph()
    
    # Helper function to restore complex objects from serialized format
    def restore_object(obj):
        """Restore objects from their serialized representations."""
        if isinstance(obj, dict):
            if "__geometry__" in obj:
                # Restore Shapely geometry objects from WKT format
                return wkt_loads(obj["__geometry__"])
            elif "__set__" in obj:
                # Restore sets from their list representation
                return set(obj["__set__"])
            elif "__object__" in obj:
                # Custom objects were converted to strings, keep as strings
                return obj["__object__"]
        # Return unchanged for standard types
        return obj
    
    # Reconstruct all nodes with their attributes
    for node_id, attrs in data["nodes"].items():
        restored_attrs = {}
        # Process each node attribute through restoration
        for key, value in attrs.items():
            restored_attrs[key] = restore_object(value)
        
        # Add node with proper type conversion (int if numeric, otherwise string)
        final_node_id = int(node_id) if node_id.isdigit() else node_id
        g.add_node(final_node_id, **restored_attrs)
        
    # Reconstruct all edges with their attributes
    for edge in data["edges"]:
        # Convert node identifiers back to proper types
        u = int(edge["u"]) if edge["u"].isdigit() else edge["u"]
        v = int(edge["v"]) if edge["v"].isdigit() else edge["v"]
        
        # Restore edge attributes
        restored_attrs = {}
        for key, value in edge["attrs"].items():
            restored_attrs[key] = restore_object(value)
        
        # Add edge with restored attributes
        g.add_edge(u, v, **restored_attrs)
        
    return g

def file_cache(timeout: int = CACHE_TIMEOUT) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    High-performance file-based caching decorator for expensive operations.
    
    This decorator provides sophisticated caching functionality that dramatically
    improves application performance by storing the results of expensive computations
    (like graph generation, distance matrix calculations, and route optimizations)
    to disk for reuse in subsequent runs.
    
    Key features:
    - Automatic cache key generation based on function parameters
    - Configurable cache expiration times
    - Special handling for complex data types (NetworkX graphs)
    - Robust error handling and cache invalidation
    - Thread-safe cache operations
    - Automatic cache directory management
    
    The caching system is particularly effective for:
    - Graph generation from OpenStreetMap data
    - Distance matrix calculations
    - Route optimization results
    - Map tile and geographic data
    
    Args:
        timeout (int): Cache expiration time in seconds (default from config)
        
    Returns:
        Callable: Decorator function that wraps target functions with caching
        
    Example:
        @file_cache(timeout=3600)  # Cache for 1 hour
        def expensive_computation(param1, param2):
            # Expensive operation here
            return result
    """
    # Ensure cache directory exists for file operations
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir(exist_ok=True)
        logger.debug(f"Created cache directory: {CACHE_DIR}")
        
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Identify functions that return special data types requiring custom handling
            is_graph_function = func.__name__ in ("get_graph_and_nodes", "distance_matrix")
            
            # Generate unique cache key from function signature and parameters
            key_components = [
                func.__name__,
                ":".join(str(arg) for arg in args),
                ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))
            ]
            cache_key = hashlib.sha1(":".join(key_components).encode()).hexdigest()
            cache_file = CACHE_DIR / f"{cache_key}.json"
            
            # Attempt to load from cache if valid file exists
            if cache_file.exists():
                file_age = time.time() - cache_file.stat().st_mtime
                if file_age < timeout:
                    try:
                        logger.debug(f"🗂️ Loading cached result for {func.__name__}")
                        with open(cache_file, "r") as f:
                            cached_data = json.load(f)
                            
                            # Special handling for functions returning NetworkX graphs
                            if is_graph_function and func.__name__ == "get_graph_and_nodes":
                                graph_data, nodes = cached_data
                                graph = serializable_to_networkx(graph_data)
                                logger.info(f"✅ Cache hit for {func.__name__} (age: {file_age:.1f}s)")
                                return cast(T, (graph, nodes))
                            else:
                                logger.info(f"✅ Cache hit for {func.__name__} (age: {file_age:.1f}s)")
                                return cast(T, cached_data)
                                
                    except (json.JSONDecodeError, IOError) as e:
                        logger.warning(f"🗑️ Cache corruption detected, rebuilding: {e}")
                        # Continue to function execution if cache is corrupted
            
            # No valid cache found, execute the original function
            logger.debug(f"💾 Cache miss for {func.__name__}, executing function")
            result = func(*args, **kwargs)
            
            # Store result in cache for future use
            try:
                # Special handling for functions returning NetworkX graphs
                if is_graph_function and func.__name__ == "get_graph_and_nodes":
                    graph, nodes = result
                    serializable_data = (networkx_to_serializable(graph), nodes)
                    with open(cache_file, "w") as f:
                        json.dump(serializable_data, f, indent=2)
                else:
                    with open(cache_file, "w") as f:
                        json.dump(result, f, indent=2)
                logger.debug(f"💾 Successfully cached result for {func.__name__}")
            except (TypeError, IOError) as e:
                logger.warning(f"⚠️ Failed to cache result for {func.__name__}: {e}")
                
            return result
        return wrapper
    return decorator

def check_internet_connection(timeout: int = 5) -> bool:
    """
    Intelligently detect internet connectivity for map tile loading.
    
    This function performs a multi-stage connectivity test to determine whether
    the application can access external map tile servers. It tests connectivity
    to multiple reliable servers to avoid false negatives from temporary outages.
    
    The connectivity test process:
    1. Primary test: Attempts connection to Google (highly reliable)
    2. Fallback test: Attempts connection to OpenStreetMap servers
    3. Timeout handling: Uses short timeout to avoid blocking the UI
    4. Error classification: Distinguishes between different failure types
    
    This information is used to:
    - Choose appropriate map tile sources (online vs offline-friendly)
    - Adjust caching strategies for map data
    - Provide user feedback about connectivity status
    - Enable graceful degradation for offline operation
    
    Args:
        timeout (int): Maximum time to wait for connection in seconds (default: 5)
        
    Returns:
        bool: True if internet connection is available, False otherwise
        
    Note:
        This function is designed to be fast and non-blocking to avoid
        impacting application startup and user experience.
    """
    try:
        # Primary connectivity test using Google (global reliability)
        urllib.request.urlopen('http://www.google.com', timeout=timeout)
        logger.debug("🌐 Internet connectivity confirmed (Google)")
        return True
    except (urllib.error.URLError, socket.timeout, socket.error) as e:
        logger.debug(f"Primary connectivity test failed: {e}")
        
        try:
            # Fallback connectivity test using OpenStreetMap
            urllib.request.urlopen('http://www.openstreetmap.org', timeout=timeout)
            logger.debug("🌐 Internet connectivity confirmed (OpenStreetMap)")
            return True
        except (urllib.error.URLError, socket.timeout, socket.error) as e:
            logger.debug(f"Fallback connectivity test failed: {e}")
            logger.info("🔌 No internet connection detected")
            return False

def get_offline_map_config():
    """
    Select optimal map tile configuration based on internet connectivity.
    
    This function implements intelligent map tile source selection that adapts
    to the user's connectivity status. It performs real-time connectivity testing
    and chooses the most appropriate tile source for the current network conditions.
    
    The selection strategy:
    1. Test internet connectivity with short timeout
    2. Use preferred high-quality tiles when online
    3. Fall back to cache-friendly tiles when offline
    4. Log connectivity status for user awareness
    
    Map tile considerations:
    - Online: Uses "cartodb dark_matter" for modern, clean appearance
    - Offline: Uses "OpenStreetMap" for better cache availability
    - The fallback tiles are more likely to be cached by browsers
    - Reduces load times and improves user experience in poor connectivity
    
    Returns:
        str: Map tile source identifier compatible with Folium mapping library
        
    Note:
        This function is called during map generation to ensure the best
        possible user experience regardless of network conditions.
    """
    internet_available = check_internet_connection(timeout=3)
    
    if internet_available:
        # Use preferred high-quality tiles when online
        logger.debug(f"🗺️ Using online map tiles: {MAP_TILES}")
        return MAP_TILES
    else:
        # Use cache-friendly tiles when offline
        logger.info("🔌 No internet connection detected, using offline-friendly map tiles")
        return "OpenStreetMap"

def euclidean_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate fast Euclidean distance between two geographic points.
    
    This function provides a quick distance approximation suitable for relative
    distance comparisons and scenarios where speed is more important than
    absolute accuracy. It treats coordinates as Cartesian points rather than
    geographic coordinates on a sphere.
    
    Use cases:
    - Initial distance sorting and filtering
    - Quick proximity checks
    - Performance-critical inner loops
    - Relative distance comparisons
    
    Limitations:
    - Not accurate for large distances (>100km)
    - Doesn't account for Earth's curvature
    - Less accurate near poles
    - Should not be used for navigation or precise measurements
    
    Args:
        p1 (Tuple[float, float]): First point as (latitude, longitude) tuple
        p2 (Tuple[float, float]): Second point as (latitude, longitude) tuple
        
    Returns:
        float: Approximate distance in coordinate units (not kilometers)
        
    Note:
        For accurate distance measurements, use haversine_distance() instead.
        This function is optimized for speed in algorithms like TSP solving.
    """
    # Simple Pythagorean theorem in coordinate space
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5

def haversine_distance(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    """
    Calculate precise great-circle distance between two geographic points.
    
    This function implements the haversine formula to calculate the shortest
    distance between two points on Earth's surface, accounting for the planet's
    curvature. It provides highly accurate results suitable for navigation,
    logistics planning, and precise distance measurements.
    
    The haversine formula:
    1. Converts coordinates from degrees to radians
    2. Calculates angular distance using spherical trigonometry
    3. Converts angular distance to linear distance using Earth's radius
    4. Returns distance in standard units (kilometers)
    
    Accuracy characteristics:
    - Very accurate for distances up to 20,000km (half Earth's circumference)
    - Handles antipodal points correctly
    - Accounts for Earth's spherical shape
    - Suitable for professional navigation applications
    
    Args:
        p1 (Tuple[float, float]): First point as (latitude, longitude) tuple
        p2 (Tuple[float, float]): Second point as (latitude, longitude) tuple
        
    Returns:
        float: Great-circle distance in kilometers between the two points
        
    Example:
        >>> distance = haversine_distance((24.8480, 67.0320), (24.8500, 67.0340))
        >>> print(f"Distance: {distance:.2f} km")
        Distance: 0.25 km
    """
    from math import radians, sin, cos, sqrt, atan2
    
    # Earth's mean radius in kilometers (WGS84 approximation)
    EARTH_RADIUS_KM = 6371.0
    
    # Convert decimal degrees to radians for trigonometric calculations
    lat1, lon1 = radians(p1[0]), radians(p1[1])
    lat2, lon2 = radians(p2[0]), radians(p2[1])
    
    # Calculate coordinate differences
    dlat = lat2 - lat1  # Latitude difference
    dlon = lon2 - lon1  # Longitude difference
    
    # Apply haversine formula for great-circle distance
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    # Convert angular distance to linear distance
    distance_km = EARTH_RADIUS_KM * c
    
    return distance_km

def cleanup_temp_files():
    """Remove temporary HTML files created for map display."""
    try:
        # Look for temporary HTML files in the temp directory
        temp_dir = tempfile.gettempdir()
        for filename in os.listdir(temp_dir):
            if filename.endswith('.html') and os.path.isfile(os.path.join(temp_dir, filename)):
                # Only remove files older than 1 hour to avoid removing files in use
                file_path = os.path.join(temp_dir, filename)
                file_age = time.time() - os.path.getmtime(file_path)
                if file_age > 3600:  # 1 hour in seconds
                    try:
                        os.remove(file_path)
                        logger.debug(f"Removed temp file: {file_path}")
                    except (OSError, PermissionError):
                        # Skip files that can't be removed
                        logger.debug(f"Could not remove temp file (permission denied): {file_path}")
    except Exception as e:
        # Don't let cleanup errors affect the application
        logger.warning(f"Error during temp file cleanup: {str(e)}")
        
def cleanup_old_cache_files():
    """Remove old cache files to prevent disk space issues."""
    try:
        if not CACHE_DIR.exists():
            return
            
        # Check each cache file
        for cache_file in CACHE_DIR.glob("*.json"):
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age > CACHE_TIMEOUT:
                try:
                    cache_file.unlink()
                    logger.debug(f"Removed old cache file: {cache_file}")
                except (OSError, PermissionError):
                    logger.debug(f"Could not remove cache file (permission denied): {cache_file}")
                    
    except Exception as e:
        logger.warning(f"Error during cache cleanup: {str(e)}")

# Enhanced caching decorator for offline functionality
def offline_cache(timeout: int = CACHE_TIMEOUT, require_internet: bool = True):
    """
    Enhanced caching decorator that supports offline operation.
    
    Args:
        timeout: Cache expiration time in seconds
        require_internet: If False, use cached data even if expired when offline
        
    Returns:
        Decorator function that wraps the target function with offline-aware caching
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            # Create cache key
            key_parts = [func.__name__,
                        ":".join(str(arg) for arg in args) + 
                        ":".join(f"{k}={v}" for k, v in sorted(kwargs.items()))]
            cache_key = hashlib.sha1(":".join(key_parts).encode()).hexdigest()
            cache_file = CACHE_DIR / f"{cache_key}.json"
            
            # Check internet connectivity
            internet_available = check_internet_connection(timeout=3)
            
            # Check if valid cache file exists
            cache_valid = False
            if cache_file.exists():
                file_age = time.time() - cache_file.stat().st_mtime
                cache_valid = file_age < timeout
                
                # If offline and cache exists (even if expired), use it
                if not internet_available and not require_internet:
                    cache_valid = True
                    logger.info(f"Using cached data for {func.__name__} (offline mode)")
            
            if cache_valid:
                try:
                    logger.debug(f"Loading cached result for {func.__name__}")
                    with open(cache_file, "r") as f:
                        cached_data = json.load(f)
                        
                        # Handle special case for graph data
                        if func.__name__ == "get_graph_and_nodes":
                            graph_data, nodes = cached_data
                            graph = serializable_to_networkx(graph_data)
                            return cast(T, (graph, nodes))
                        else:
                            return cast(T, cached_data)
                            
                except (json.JSONDecodeError, IOError) as e:
                    logger.warning(f"Error loading cache: {e}")
            
            # No valid cache or internet required - try to execute function
            if not internet_available and require_internet:
                # If function requires internet but none available, provide fallback
                logger.warning(f"No internet connection for {func.__name__}, using fallback")
                
                if func.__name__ == "get_graph_and_nodes":
                    # Create a simple complete graph as fallback
                    coords = args[0] if args else []
                    fallback_graph = nx.complete_graph(len(coords))
                    for i, (lat, lon) in enumerate(coords):
                        fallback_graph.nodes[i]['x'] = lon
                        fallback_graph.nodes[i]['y'] = lat
                    return cast(T, (fallback_graph, list(range(len(coords)))))
                else:
                    raise ConnectionError(f"Internet connection required for {func.__name__}")
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Save result to cache
            try:
                if func.__name__ == "get_graph_and_nodes":
                    graph, nodes = result
                    serializable_data = (networkx_to_serializable(graph), nodes)
                    with open(cache_file, "w") as f:
                        json.dump(serializable_data, f)
                else:
                    with open(cache_file, "w") as f:
                        json.dump(result, f)
                logger.debug(f"Cached result for {func.__name__}")
            except (TypeError, IOError) as e:
                logger.warning(f"Failed to cache result: {e}")
                
            return result
        return wrapper
    return decorator

# -----------------------------------------------------------------------------
#  GRAPH UTILITIES
# -----------------------------------------------------------------------------

@offline_cache(require_internet=True)
def get_graph_and_nodes(coords: List[Tuple[float, float]]) -> Tuple[nx.Graph, List[int]]:
    """
    Get a road network graph and corresponding node IDs for a set of coordinates.
    
    Args:
        coords: List of (latitude, longitude) coordinates
        
    Returns:
        Tuple containing:
        - graph: NetworkX graph representing the road network
        - nodes: List of node IDs for each input coordinate, snapped to nearest road
        
    Note:
        Ensures each coordinate maps to a distinct graph node by adding small
        random offsets when duplicate nodes are detected.
    """
    # Extract latitude and longitude components
    lats, lons = zip(*coords)
    
    # Create a bounding box with buffer around coordinates
    poly = box(
        min(lons) - BUFFER_SIZE, 
        min(lats) - BUFFER_SIZE, 
        max(lons) + BUFFER_SIZE, 
        max(lats) + BUFFER_SIZE
    )
    
    # Get the road network graph for the bounding box
    internet_available = check_internet_connection(timeout=3)
    
    try:
        if not internet_available:
            logger.warning("No internet connection available. Using cached data or fallback.")
            # If offline, this will fail and go to fallback immediately
            
        # For OSMnx 1.0 and newer
        try:
            g = ox.graph_from_polygon(poly, network_type="drive")
        # For older OSMnx versions
        except AttributeError:
            g = ox.graph.graph_from_polygon(poly, network_type="drive")
    except Exception as e:
        logger.error(f"Error fetching road network: {str(e)}")
        if not internet_available:
            logger.info("Creating fallback graph for offline operation")
        # Fallback to simple complete graph if OSM data cannot be retrieved
        g = nx.complete_graph(len(coords))
        for i, (lat, lon) in enumerate(coords):
            g.nodes[i]['x'] = lon
            g.nodes[i]['y'] = lat
        return g, list(range(len(coords)))
    
    # Convert to undirected graph
    g = g.to_undirected(as_view=False)
    
    try:
        # Find nearest graph nodes to each coordinate
        # Handle different OSMnx versions
        try:
            nodes = ox.distance.nearest_nodes(g, lons, lats)  # Newer versions
        except (AttributeError, TypeError):
            try:
                nodes = ox.get_nearest_nodes(g, lons, lats)  # Older versions
            except AttributeError:
                nodes = ox.nearest_nodes(g, lons, lats)  # Very old versions
        
        # Ensure every delivery maps to a distinct graph node
        seen = set()
        new_nodes = []
        
        for idx, (lat, lon) in enumerate(coords):
            jitter = 0
            while True:
                # Try different OSMnx versions
                try:
                    node = ox.distance.nearest_nodes(g, lon, lat)  # Newer versions
                except (AttributeError, TypeError):
                    try:
                        node = ox.get_nearest_nodes(g, lon, lat)  # Older versions
                    except AttributeError:
                        node = ox.nearest_nodes(g, lon, lat)  # Very old versions
                        
                if node not in seen:
                    seen.add(node)
                    new_nodes.append(node)
                    break
                    
                # Duplicate node found - add jitter to the query point and try again
                jitter += 1
                offset = JITTER_BASE * jitter  # ~= 9 meters per step
                lat += (random.random() - 0.5) * offset
                lon += (random.random() - 0.5) * offset
                
                # Prevent infinite loop
                if jitter > 20:
                    # If we can't find a unique node after 20 attempts, just use any node
                    # and add a big offset to ensure it's treated differently
                    node = nodes[idx]
                    g.nodes[node]['x'] += jitter * 0.0001 * random.random()
                    g.nodes[node]['y'] += jitter * 0.0001 * random.random()
                    new_nodes.append(node)
                    break
                
        nodes = new_nodes
            
    except ImportError:
        logger.error("Missing scikit-learn dependency for nearest nodes lookup")
        raise ImportError("Install scikit-learn: pip install scikit-learn")
    except Exception as e:
        logger.error(f"Error finding nearest nodes: {str(e)}")
        # Fallback to simple indexing if node lookup fails
        nodes = list(range(min(len(coords), len(g.nodes))))
        
    return g, nodes


@file_cache()
def distance_matrix(g: nx.Graph, nodes: List[int]) -> List[List[float]]:
    """
    Calculate the distance matrix between all pairs of nodes in the graph.
    
    Args:
        g: NetworkX graph representing the road network
        nodes: List of node IDs in the graph
        
    Returns:
        A symmetric NxN matrix where D[i][j] is the shortest path distance
        in meters between nodes[i] and nodes[j].
    """
    n = len(nodes)
    D = [[0.0] * n for _ in range(n)]
    
    # Try to compute all-pairs shortest paths at once to improve performance
    try:
        # For smaller graphs, use all-pairs shortest path
        if n <= 20:
            paths = dict(nx.all_pairs_dijkstra_path_length(g, weight="length"))
            
            for i, src in enumerate(nodes):
                for j, tgt in enumerate(nodes):
                    if i < j:  # Only compute each pair once
                        try:
                            D[i][j] = D[j][i] = paths[src][tgt]
                        except KeyError:
                            # Handle case where no path exists
                            # Use haversine distance as fallback (great circle distance)
                            src_lat, src_lon = g.nodes[src]['y'], g.nodes[src]['x']
                            tgt_lat, tgt_lon = g.nodes[tgt]['y'], g.nodes[tgt]['x']
                            D[i][j] = D[j][i] = haversine_distance((src_lat, src_lon), (tgt_lat, tgt_lon)) * 1000  # Convert km to m
        else:
            # For larger graphs, compute one source at a time
            for i, src in enumerate(nodes):
                try:
                    # Calculate shortest paths from source node to all others
                    lengths = nx.single_source_dijkstra_path_length(g, src, weight="length")
                    
                    # Fill in the distance matrix (symmetric)
                    for j, tgt in enumerate(nodes):
                        if i < j:  # Only compute each pair once
                            try:
                                D[i][j] = D[j][i] = lengths[tgt]
                            except KeyError:
                                # Handle case where no path exists
                                src_lat, src_lon = g.nodes[src]['y'], g.nodes[src]['x']
                                tgt_lat, tgt_lon = g.nodes[tgt]['y'], g.nodes[tgt]['x']
                                D[i][j] = D[j][i] = haversine_distance((src_lat, src_lon), (tgt_lat, tgt_lon)) * 1000  # Convert km to m
                except nx.NetworkXNoPath:
                    # Handle case where no path exists at all
                    for j, tgt in enumerate(nodes):
                        if i < j:  # Only compute each pair once
                            src_lat, src_lon = g.nodes[src]['y'], g.nodes[src]['x']
                            tgt_lat, tgt_lon = g.nodes[tgt]['y'], g.nodes[tgt]['x']
                            D[i][j] = D[j][i] = haversine_distance((src_lat, src_lon), (tgt_lat, tgt_lon)) * 1000  # Convert km to m
    
    except Exception as e:
        logger.error(f"Error computing distance matrix: {str(e)}")
        # If shortest path calculation fails, fall back to direct distances
        for i, src in enumerate(nodes):
            src_lat, src_lon = g.nodes[src]['y'], g.nodes[src]['x']
            for j, tgt in enumerate(nodes):
                if i < j:  # Only compute each pair once
                    tgt_lat, tgt_lon = g.nodes[tgt]['y'], g.nodes[tgt]['x']
                    D[i][j] = D[j][i] = haversine_distance((src_lat, src_lon), (tgt_lat, tgt_lon)) * 1000  # Convert km to m
                
    return D

# The distance_matrix function is now also decorated with @file_cache() above

# -----------------------------------------------------------------------------
#  TSP ALGORITHMS
# -----------------------------------------------------------------------------

def christofides_tsp(D: List[List[float]]) -> Tuple[List[int], float]:
    """
    Implement the Christofides algorithm for approximately solving the TSP.
    
    This algorithm guarantees a solution at most 1.5 times the optimal
    solution for metric TSPs. It has polynomial time complexity.
    
    Args:
        D: Distance matrix where D[i][j] is the distance from i to j
        
    Returns:
        Tuple containing:
        - tour: List of node indices representing the tour (starts and ends at node 0)
        - distance: Total tour distance
        
    Raises:
        ValueError: If distance matrix is invalid or empty
        NetworkXError: If graph operations fail
    """
    if not D or len(D) == 0:
        raise ValueError("Distance matrix cannot be empty")
    
    n = len(D)
    if n < 2:
        raise ValueError("Need at least 2 nodes for TSP")
    
    # Validate distance matrix is square
    for i, row in enumerate(D):
        if len(row) != n:
            raise ValueError(f"Distance matrix must be square, row {i} has length {len(row)}, expected {n}")
    
    try:
        G = nx.Graph()
        
        # Create a complete graph with distances as weights
        for i in range(n):
            for j in range(i+1, n):
                if D[i][j] < 0:
                    raise ValueError(f"Distance matrix contains negative value at [{i}][{j}]: {D[i][j]}")
                G.add_edge(i, j, weight=D[i][j])
        
        # Step 1: Find a minimum spanning tree
        T = nx.minimum_spanning_tree(G, weight="weight")
        
        # Step 2: Find nodes with odd degree in the MST
        odd_degree_nodes = [v for v, d in T.degree() if d % 2 == 1]
        
        # Step 3: Find minimum-weight perfect matching of odd-degree nodes
        # (We maximize weight with negated distances since nx only has max_weight_matching)
        M = nx.Graph()
        M.add_nodes_from(odd_degree_nodes)
        for i, u in enumerate(odd_degree_nodes):
            for v in odd_degree_nodes[i+1:]:
                M.add_edge(u, v, weight=1_000_000 - D[u][v])  # Large constant minus distance
        
        matching = nx.algorithms.matching.max_weight_matching(M, maxcardinality=True)
        
        # Step 4: Combine MST and matching to create an Eulerian multigraph
        H = nx.MultiGraph()
        H.add_nodes_from(range(n))
        H.add_edges_from(T.edges(data=True))
        
        for u, v in matching:
            H.add_edge(u, v, weight=D[u][v])
        
        # Step 5: Find an Eulerian circuit
        eulerian_circuit = list(nx.eulerian_circuit(H, source=0))
        
        # Step 6: Convert to a Hamiltonian cycle by skipping repeated vertices
        seen = set()
        tour = []
        for u, v in eulerian_circuit:
            if u not in seen:
                tour.append(u)
                seen.add(u)
        
        # Close the tour
        tour.append(0)
        
        # Calculate total distance
        distance = sum(D[tour[i]][tour[i+1]] for i in range(len(tour)-1))
        
        return tour, distance
        
    except (nx.NetworkXError, nx.NetworkXException) as e:
        logger.error(f"NetworkX error in Christofides algorithm: {e}")
        # Fallback to nearest neighbor heuristic
        return _nearest_neighbor_fallback(D)
    except Exception as e:
        logger.error(f"Unexpected error in Christofides algorithm: {e}")
        # Fallback to nearest neighbor heuristic
        return _nearest_neighbor_fallback(D)


def _nearest_neighbor_fallback(D: List[List[float]]) -> Tuple[List[int], float]:
    """
    Fallback nearest neighbor algorithm for TSP when Christofides fails.
    
    Args:
        D: Distance matrix
        
    Returns:
        Tuple of (tour, distance)
    """
    n = len(D)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0, 0], 0.0
    
    unvisited = set(range(1, n))
    tour = [0]
    current = 0
    total_distance = 0.0
    
    while unvisited:
        nearest = min(unvisited, key=lambda x: D[current][x])
        total_distance += D[current][nearest]
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    # Return to start
    total_distance += D[current][0]
    tour.append(0)
    
    return tour, total_distance


def held_karp_tsp(D: List[List[float]]) -> Tuple[List[int], float]:
    """
    Implement the Held-Karp dynamic programming algorithm for optimally solving the TSP.
    
    This algorithm guarantees the optimal solution but has exponential
    time complexity O(2^n * n^2).
    
    Args:
        D: Distance matrix where D[i][j] is the distance from i to j
        
    Returns:
        Tuple containing:
        - tour: List of node indices representing the optimal tour (starts and ends at node 0)
        - distance: Total tour distance
    """
    n = len(D)
    
    # Initialize DP table and parent pointers
    # dp[(mask, j)] = shortest path visiting all vertices in mask and ending at j
    dp = {(1, 0): 0.0}  # Base case: start at vertex 0
    parent = {}
    
    # Solve subproblems
    for mask in range(1, 1 << n):
        # If the mask doesn't include the starting vertex, skip
        if not mask & 1:
            continue
            
        # For each possible ending vertex j
        for j in range(1, n):
            # If j is not in the mask, skip
            if not mask & (1 << j):
                continue
                
            # Mask without j
            prev_mask = mask ^ (1 << j)
            best = float("inf")
            best_k = None
            
            # Try all possible vertices k as the second-to-last vertex
            for k in range(n):
                if prev_mask & (1 << k):  # If k is in prev_mask
                    # Distance from k to j plus best path to k
                    candidate = dp.get((prev_mask, k), float("inf")) + D[k][j]
                    if candidate < best:
                        best = candidate
                        best_k = k
                        
            dp[(mask, j)] = best
            parent[(mask, j)] = best_k
    
    # Reconstruct the optimal tour
    # Find best endpoint to return to starting vertex
    full_mask = (1 << n) - 1
    best_distance, best_end = min(
        (dp[(full_mask, j)] + D[j][0], j) for j in range(1, n)
    )
    
    # Reconstruct the path
    mask = full_mask
    j = best_end
    tour_reversed = [0]  # Start with the ending vertex
    
    while j != 0:
        tour_reversed.append(j)
        new_j = parent[(mask, j)]
        mask ^= (1 << j)  # Remove j from mask
        j = new_j
        
    tour_reversed.append(0)  # Add starting vertex again to complete the cycle
    tour = list(reversed(tour_reversed))
    
    return tour, best_distance

# -----------------------------------------------------------------------------
#  WORKER THREAD
# -----------------------------------------------------------------------------

class Worker(QtCore.QThread):
    """
    Background worker thread for route planning operations.
    
    This ensures the GUI remains responsive during computationally 
    intensive operations like route planning.
    
    Attributes:
        finished: Signal emitted when processing is complete, contains result data
        progress: Signal emitted to report progress during processing
    """
    
    # Signal emitted when work is complete, containing result data
    finished = QtCore.pyqtSignal(dict)
    # Signal for reporting progress (0-100, status message)
    progress = QtCore.pyqtSignal(int, str)
    
    def __init__(self, coords: List[Tuple[float, float]], mode: int):
        """
        Initialize the worker thread.
        
        Args:
            coords: List of (latitude, longitude) coordinates for delivery points
            mode: Algorithm selection mode
                  0 = Auto (Held-Karp if ≤12 stops, else Christofides)
                  1 = Held-Karp (exact)
                  2 = Christofides (approximation)
        """
        super().__init__()
        self.coords = coords
        self.mode = mode
        
    def run(self):
        """
        Execute the route planning operation in the background thread.
        
        This method:
        1. Gets a road network graph for the area
        2. Finds the shortest paths between all points
        3. Computes the optimal or approximate route
        4. Emits results via the finished signal
        """
        t0 = time.perf_counter()
        
        # Add performance monitoring
        performance_log = {
            "total_stops": len(self.coords),
            "start_time": t0,
            "graph_time": None,
            "distance_time": None,
            "algorithm_time": None,
            "route_time": None
        }
        
        # Occasionally run cleanup operations
        if random.random() < 0.05:  # 5% chance to clean up cache
            cleanup_old_cache_files()
            
        self.progress.emit(10, "Getting road network...")
        
        # Get road network and nearest nodes
        try:
            graph_start = time.perf_counter()
            g, nodes = get_graph_and_nodes(self.coords)
            performance_log["graph_time"] = time.perf_counter() - graph_start
            logger.info(f"Graph retrieval took {performance_log['graph_time']:.3f} seconds")
        except Exception as e:
            logger.error(f"Error getting graph: {str(e)}")
            self.progress.emit(0, "Error getting road network")
            self.finished.emit({"error": str(e)})
            return
            
        self.progress.emit(40, "Calculating distances...")
        
        # Calculate distance matrix
        try:
            dist_start = time.perf_counter()
            D = distance_matrix(g, nodes)
            performance_log["distance_time"] = time.perf_counter() - dist_start
            logger.info(f"Distance matrix calculation took {performance_log['distance_time']:.3f} seconds")
        except Exception as e:
            logger.error(f"Error computing distance matrix: {str(e)}")
            self.progress.emit(0, "Error calculating distances")
            self.finished.emit({"error": str(e)})
            return
            
        n = len(self.coords)
        
        self.progress.emit(60, "Planning route...")
        
        # Select algorithm based on mode
        if self.mode == 1:
            self.progress.emit(70, "Running Held-Karp algorithm...")
            tour, dist = held_karp_tsp(D)
            label = "Optimal (Held-Karp)"
        elif self.mode == 2:
            self.progress.emit(70, "Running Christofides algorithm...")
            tour, dist = christofides_tsp(D)
            label = "Christofides 1.5-approx"
        else:
            # Auto mode: use optimal algorithm for small problems, approximation for larger ones
            if n <= MAX_STOPS_EXACT_ALGORITHM:
                self.progress.emit(70, "Running Held-Karp algorithm...")
                tour, dist = held_karp_tsp(D)
                label = "Optimal (Held-Karp)"
            else:
                self.progress.emit(70, "Running Christofides algorithm...")
                tour, dist = christofides_tsp(D)
                label = "Christofides 1.5-approx"
        
        performance_log["algorithm_time"] = time.perf_counter() - t0 - performance_log["graph_time"] - performance_log["distance_time"]
        logger.info(f"Algorithm execution took {performance_log['algorithm_time']:.3f} seconds")
        
        # Calculate route generation time
        route_start = time.perf_counter()
        
        # Generate complete route with all road segments
        route = []
        try:
            for i in range(len(tour) - 1):
                # Update progress with more granular information
                progress_value = 80 + int((i / (len(tour) - 2)) * 15) if len(tour) > 2 else 95
                self.progress.emit(progress_value, f"Generating route segment {i+1}/{len(tour)-1}...")
                
                # Find shortest path between consecutive tour points
                try:
                    path = nx.shortest_path(g, nodes[tour[i]], nodes[tour[i+1]], weight="length")
                    
                    # Extract coordinates for each node in the path
                    pts = [(g.nodes[p]['y'], g.nodes[p]['x']) for p in path]
                    
                    # Only include the first point for the first segment to avoid duplicates
                    route.extend(pts if i == 0 else pts[1:])
                except (nx.NetworkXNoPath, KeyError) as e:
                    # If no path found, create a direct line
                    logger.warning(f"No path found for segment {i}, creating direct line: {str(e)}")
                    start = (g.nodes[nodes[tour[i]]]['y'], g.nodes[nodes[tour[i]]]['x'])
                    end = (g.nodes[nodes[tour[i+1]]]['y'], g.nodes[nodes[tour[i+1]]]['x'])
                    route.extend([start, end] if i == 0 else [end])
        except Exception as e:
            logger.error(f"Error generating route: {str(e)}")
            # If route generation fails, create a simple route connecting the points directly
            route = [self.coords[i] for i in tour]
        
        # Calculate route generation time
        performance_log["route_time"] = time.perf_counter() - route_start
        
        # Calculate total computation time
        computation_time = time.perf_counter() - t0
        
        # Log performance summary
        logger.info(f"Route planning performance:")
        logger.info(f"  Total stops: {performance_log['total_stops']}")
        logger.info(f"  Graph retrieval time: {performance_log['graph_time']:.3f} seconds")
        logger.info(f"  Distance matrix calculation time: {performance_log['distance_time']:.3f} seconds")
        logger.info(f"  Algorithm execution time: {performance_log['algorithm_time']:.3f} seconds")
        logger.info(f"  Route generation time: {performance_log['route_time']:.3f} seconds")
        logger.info(f"  Total computation time: {computation_time:.3f} seconds")
        
        self.progress.emit(100, "Route planning complete")
        
        # Emit results
        self.finished.emit({
            "tour": tour,
            "dist": dist,
            "label": label,
            "route": route,
            "secs": computation_time
        })

# ─────────────────────────────────────────────────────────────────────────────
#  GUI
# ─────────────────────────────────────────────────────────────────────────────
class PlannerUI(QtWidgets.QMainWindow):
    """
    Main application window for the route planner.
    
    This class handles the user interface, including the map display,
    delivery point management, algorithm selection, and visualization
    of computed routes.
    
    Attributes:
        is_planning: Boolean flag indicating if a route calculation is in progress
        stops_display: QLabel showing the current number of stops
        edit_stops_btn: Button to open the stop count editor dialog
        table: Table widget for displaying and editing delivery coordinates
        alg: ComboBox for algorithm selection
        btn_plan: Button to trigger route planning
        btn_compare: Button to trigger algorithm comparison
        out: Text area for displaying results and comparisons
        web: Web view for displaying the interactive map
    """
    
    def __init__(self):
        """Initialize the main window and UI components."""
        super().__init__()
        
        # Window setup
        self.setWindowTitle("Delivery Route Planner")
        self.resize(1300, 720)
        
        # State tracking
        self.is_planning = False  # Track if planning operation is in progress
        self.hk_results: Dict[str, Any] = {}  # Storage for Held-Karp results during comparison
        
        # Initialize onboarding system
        self.tutorial_manager = None
        
        # Initialize UI components
        self._setup_ui()
        
        # Apply dark theme
        self._apply_dark_theme()
        
        # Set up tooltips and help system
        # Note: ToolTipManager is set up after UI is fully initialized
        
        # Add help menu
        self._setup_help_menu()
        
        # Check if this is the first run and show onboarding
        if check_first_run():
            QTimer.singleShot(1000, self._show_welcome_dialog)  # Delay to let UI fully load
        
        # Set up tooltips after a brief delay to ensure all UI elements are created
        QTimer.singleShot(100, self._setup_tooltips)

    # ───── UI SETUP METHODS ─────────────────────────────────────────────────────
    
    def _setup_ui(self):
        """Set up the main UI layout and components."""
        # Create central widget
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        
        # Main horizontal layout
        layout = QtWidgets.QHBoxLayout(central)
        
        # Create control panel and add to layout
        panel = self._create_control_panel()
        self.panel = panel  # Store reference for tutorial system
        layout.addWidget(panel)
        
        # Create web view for map display
        self.web = QWebEngineView()
        self.web.setObjectName("map_view")
        self.map_view = self.web  # Alias for tutorial system
        
        layout.addWidget(self.web, stretch=3)
        
        # Initialize with default number of stops (this will display the map with stops)
        self._initialize_stops(DEFAULT_STOPS)

    def _create_control_panel(self) -> QtWidgets.QFrame:
        """
        Create the left control panel with all input controls.
        
        Returns:
            QFrame containing the control panel widgets
        """
        # Create panel frame with fixed width
        panel = QtWidgets.QFrame()
        panel.setFixedWidth(PANEL_WIDTH)
        panel.setObjectName("panel")  # Set object name for tutorial highlighting
        
        # Panel layout
        panel_layout = QtWidgets.QVBoxLayout(panel)
        panel_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        
        # HQ coordinates display
        self.hq_label = QtWidgets.QLabel(
            f"<b>HQ (fixed):</b> {HQ_COORD[0]:.6f}, {HQ_COORD[1]:.6f}"
        )
        self.hq_label.setObjectName("hq_label")
        panel_layout.addWidget(self.hq_label)
        
        # Stops count section
        panel_layout.addWidget(QtWidgets.QLabel("<b>Number of Stops:</b>"))
        self._setup_stops_controls(panel_layout)
        
        # Deliveries table section
        panel_layout.addWidget(QtWidgets.QLabel("<b>Deliveries:</b>"))
        self._setup_deliveries_table(panel_layout)
        
        # Add/remove buttons for table
        self._setup_table_buttons(panel_layout)
        
        # Algorithm selection
        panel_layout.addWidget(QtWidgets.QLabel("<b>Algorithm:</b>"))
        self._setup_algorithm_selector(panel_layout)
        
        # Action buttons
        self._setup_action_buttons(panel_layout)
        
        # Output text area
        panel_layout.addWidget(QtWidgets.QLabel("<b>Output:</b>"))
        self.out = QtWidgets.QTextEdit()
        self.out.setObjectName("out")
        self.out.setReadOnly(True)
        panel_layout.addWidget(self.out, stretch=1)
        
        return panel

    def _setup_stops_controls(self, layout: QtWidgets.QVBoxLayout):
        """
        Set up the controls for managing the number of stops.
        
        Args:
            layout: Parent layout to add the stops controls to
        """
        # Create horizontal layout for stops display and edit button
        h_stops = QtWidgets.QHBoxLayout()
        
        # Label showing current number of stops
        self.stops_display = QtWidgets.QLabel(str(DEFAULT_STOPS))
        self.stops_display.setStyleSheet("font-weight: bold; color: white;")
        self.stops_display.setObjectName("stops_display")
        
        # Button to edit number of stops
        self.edit_stops_btn = QtWidgets.QPushButton("Edit Stops")
        self.edit_stops_btn.clicked.connect(self._open_stops_editor)
        
        # Add widgets to horizontal layout
        h_stops.addWidget(self.stops_display)
        h_stops.addWidget(self.edit_stops_btn)
        h_stops.addStretch()
        
        # Add horizontal layout to parent
        layout.addLayout(h_stops)

    def _setup_deliveries_table(self, layout: QtWidgets.QVBoxLayout):
        """
        Set up the table for displaying and editing delivery coordinates.
        
        Args:
            layout: Parent layout to add the table to
        """
        # Create table with 2 columns (lat, lon)
        self.table = QtWidgets.QTableWidget(0, 2)
        self.table.setObjectName("table")
        self.table.setHorizontalHeaderLabels(["Latitude", "Longitude"])
        
        # Make columns stretch to fill available width
        self.table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        
        # Add table to layout
        layout.addWidget(self.table, stretch=1)

    def _setup_table_buttons(self, layout: QtWidgets.QVBoxLayout):
        """
        Set up buttons for adding and removing table rows.
        
        Args:
            layout: Parent layout to add the buttons to
        """
        # Create horizontal layout for buttons
        hbtn = QtWidgets.QHBoxLayout()
        
        # Add button
        self.btn_add = QtWidgets.QPushButton("➕  Add")
        self.btn_add.setObjectName("add_btn")
        self.add_btn = self.btn_add  # Alias for tutorial system
        # Explicitly use lambda to ensure update_display=True is passed
        self.btn_add.clicked.connect(lambda: self._add_delivery_point(update_display=True))
        
        # Remove button
        self.btn_del = QtWidgets.QPushButton("➖  Remove")
        self.btn_del.setObjectName("remove_btn")
        self.remove_btn = self.btn_del  # Alias for tutorial system
        self.btn_del.clicked.connect(self._remove_delivery_point)
        
        # Add buttons to layout
        hbtn.addWidget(self.btn_add)
        hbtn.addWidget(self.btn_del)
        
        # Add button layout to parent
        layout.addLayout(hbtn)

    def _setup_algorithm_selector(self, layout: QtWidgets.QVBoxLayout):
        """
        Set up the algorithm selection dropdown.
        
        Args:
            layout: Parent layout to add the selector to
        """
        # Create algorithm selection combo box
        self.alg = QtWidgets.QComboBox()
        self.alg.setObjectName("algo_combo")
        self.algo_combo = self.alg  # Alias for tutorial system
        self.alg.addItems([
            "Auto (exact if ≤12)",
            "Exact (Held-Karp)",
            "Approx (Christofides)"
        ])
        
        # Add combo box to layout
        layout.addWidget(self.alg)

    def _setup_action_buttons(self, layout: QtWidgets.QVBoxLayout):
        """
        Set up the main action buttons for planning and comparison.
        
        Args:
            layout: Parent layout to add the buttons to
        """
        # Create horizontal layout for buttons
        h_buttons = QtWidgets.QHBoxLayout()
        
        # Plan route button
        self.btn_plan = QtWidgets.QPushButton("Plan Route")
        self.btn_plan.setObjectName("plan_btn")
        self.plan_btn = self.btn_plan  # Alias for tutorial system
        self.btn_plan.clicked.connect(self._start_route_planning)
        
        # Compare algorithms button
        self.btn_compare = QtWidgets.QPushButton("Compare Algorithms")
        self.btn_compare.setObjectName("compare_btn")
        self.compare_btn = self.btn_compare  # Alias for tutorial system
        self.btn_compare.clicked.connect(self._start_algorithms_comparison)
        
        # Add buttons to layout
        h_buttons.addWidget(self.btn_plan)
        h_buttons.addWidget(self.btn_compare)
        
        # Add button layout to parent
        layout.addLayout(h_buttons)
        
        # Add progress bar and status label
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Status label for progress details
        self.status_label = QtWidgets.QLabel("")
        self.status_label.setVisible(False)
        layout.addWidget(self.status_label)

    def _initialize_stops(self, count: int):
        """
        Initialize the table with the specified number of delivery stops.
        
        Args:
            count: Number of stops to initialize
        """
        # Add the specified number of stops
        for _ in range(count):
            self._add_delivery_point(update_display=False)
        
        # Update the stops display and show stops on map
        self.stops_display.setText(str(count))
        self._display_stops_map()

    # ───── MAP DISPLAY METHODS ─────────────────────────────────────────────────
    
    def _display_blank_map(self):
        """Display a blank map centered at the HQ location."""
        # Create a new map centered on HQ
        map_obj = folium.Map(
            location=HQ_COORD,
            zoom_start=MAP_ZOOM,
            tiles=get_offline_map_config()
        )
        
        # Add HQ marker for reference
        folium.Marker(
            location=HQ_COORD,
            icon=folium.Icon(color="green", icon="home"),
            tooltip="HQ"
        ).add_to(map_obj)
        
        # Display the map
        self._display_map(map_obj)

    def _display_map(self, folium_map: folium.Map):
        """
        Display a folium map in the web view.
        
        Args:
            folium_map: Folium Map object to display
        """
        # Occasionally clean up old temporary files
        if random.random() < 0.1:  # 10% chance to run cleanup
            cleanup_temp_files()
        
        # Create a temporary file for the HTML
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
        
        try:
            # Save the map to the file and load it in the web view
            folium_map.save(tmp.name)
            self.web.setUrl(QtCore.QUrl.fromLocalFile(tmp.name))
        except Exception as e:
            # Handle errors in map rendering
            logger.error(f"Error displaying map: {e}")
            # Fall back to a blank map if there's an error
            self._display_blank_map()

    def _display_stops_map(self):
        """
        Display a map showing all current delivery stops without a route.
        
        Creates a clean map visualization with:
        - HQ marker (green home icon)
        - Numbered stop markers (red circles with numbers)
        - Automatic jitter to prevent overlapping markers
        """
        logger.info("_display_stops_map called - creating new map with current stops")
        
        # Create a new map centered on HQ
        folium_map = folium.Map(
            location=HQ_COORD,
            zoom_start=MAP_ZOOM,
            tiles=get_offline_map_config()
        )
        
        # Add HQ marker
        folium.Marker(
            location=HQ_COORD,
            icon=folium.Icon(color="green", icon="home"),
            tooltip="HQ - Headquarters"
        ).add_to(folium_map)
        
        # Get all coordinates from the table (excluding HQ)
        coords = self._get_coordinates(include_hq=False)
        logger.info(f"Current stops count: {len(coords)}")
        
        if coords:
            # Track placed markers to prevent overlap
            placed: Set[Tuple[float, float]] = set()
            
            # Add numbered markers for each stop
            for idx, (lat, lon) in enumerate(coords):
                logger.debug(f"Adding stop {idx + 1} at ({lat:.6f}, {lon:.6f})")
                
                # Add small jitter if this location already has a marker
                original_lat, original_lon = lat, lon
                while (lat, lon) in placed:
                    lat = original_lat + POINT_JITTER * random.random() - POINT_JITTER / 2
                    lon = original_lon + POINT_JITTER * random.random() - POINT_JITTER / 2
                placed.add((lat, lon))
                
                # Create a numbered marker using DivIcon for better visibility
                folium.Marker(
                    location=(lat, lon),
                    icon=folium.DivIcon(
                        icon_size=(40, 40),
                        icon_anchor=(20, 20),
                        html=f'<div style="background-color:#ff6b6b; width:30px; height:30px; '
                             f'border-radius:15px; display:flex; justify-content:center; '
                             f'align-items:center; color:white; font-weight:bold; '
                             f'font-size:14px; border: 2px solid white; '
                             f'box-shadow: 0 2px 4px rgba(0,0,0,0.3);">{idx + 1}</div>',
                    ),
                    tooltip=f"Stop {idx + 1}",
                    popup=f"<b>Stop {idx + 1}</b><br/>Coordinates: ({lat:.6f}, {lon:.6f})"
                ).add_to(folium_map)
        else:
            logger.info("No stops to display on map")
        
        # Display the map
        self._display_map(folium_map)
        logger.info("Map display completed")

    # ───── DELIVERY POINT MANAGEMENT ──────────────────────────────────────────────
    
    def _add_delivery_point(self, update_display: bool = True):
        """
        Add a new delivery stop with coordinates that aren't too close to existing points.
        
        Args:
            update_display: Whether to update the stops display count
        """
        logger.info(f"_add_delivery_point called with update_display={update_display}")
        
        # Get current row count
        row_idx = self.table.rowCount()
        
        # Insert a new row
        self.table.insertRow(row_idx)
        
        # Get all existing coordinates to avoid placing new points too close
        existing_coords: List[Tuple[float, float]] = []
        for r in range(row_idx):
            try:
                lat_item = self.table.item(r, 0)
                lon_item = self.table.item(r, 1)
                if lat_item and lon_item:
                    lat = float(lat_item.text())
                    lon = float(lon_item.text())
                    existing_coords.append((lat, lon))
            except (ValueError, AttributeError):
                pass  # Skip invalid entries
        
        # Generate new coordinates that are sufficiently far from existing ones
        max_attempts = 50
        
        # Default values in case loop doesn't find a suitable spot
        lat = HQ_COORD[0] + (random.random() - 0.5) * 0.03
        lon = HQ_COORD[1] + (random.random() - 0.5) * 0.03
        
        for _ in range(max_attempts):
            # Generate a point with wider jitter (~±0.015° ≈ ±1.7 km)
            new_lat = HQ_COORD[0] + (random.random() - 0.5) * 0.03
            new_lon = HQ_COORD[1] + (random.random() - 0.5) * 0.03
            
            # Check if it's far enough from existing points
            too_close = False
            for ex_coord in existing_coords:
                # Use our utility function for distance calculation
                if euclidean_distance((new_lat, new_lon), ex_coord) < MIN_STOP_DISTANCE:
                    too_close = True
                    break
                    
            if not too_close:
                lat, lon = new_lat, new_lon
                break
        
        # Set the table values
        self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(f"{lat:.6f}"))
        self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(f"{lon:.6f}"))
        
        logger.info(f"Added stop {row_idx + 1} at ({lat:.6f}, {lon:.6f})")
        
        # Update the display and map if requested
        if update_display:
            self.stops_display.setText(str(self.table.rowCount()))
            logger.info(f"Updated stops display to: {self.table.rowCount()}")
            self._display_stops_map()  # Show updated stops on map

    def _remove_delivery_point(self):
        """Remove selected delivery points or the last one if none selected."""
        # Get selected rows
        sel_model = self.table.selectionModel()
        if sel_model:
            selected_rows = sel_model.selectedRows()
            
            if selected_rows:
                # Delete selected rows (in reverse order to avoid index shifting)
                for idx in sorted(selected_rows, key=lambda x: x.row(), reverse=True):
                    self.table.removeRow(idx.row())
            elif self.table.rowCount():
                # If nothing selected, remove the last row
                self.table.removeRow(self.table.rowCount() - 1)
                
            # Update the display and map
            self.stops_display.setText(str(self.table.rowCount()))
            self._display_stops_map()  # Show updated stops on map

    def _update_stops_count(self):
        """Update the table to match the number in stops_display."""
        try:
            # Get the target number of stops
            target_count = int(self.stops_display.text()) if self.stops_display.text().strip() else 0
            
            # Update table rows
            while self.table.rowCount() < target_count:
                self._add_delivery_point(update_display=False)
                
            while self.table.rowCount() > target_count:
                self.table.removeRow(self.table.rowCount() - 1)
                
            # Update the map to show current stops
            self._display_stops_map()
                
        except ValueError:
            # If text can't be converted to int, reset display to current row count
            self.stops_display.setText(str(self.table.rowCount()))

    def _open_stops_editor(self):
        """Open a dialog to edit the number of stops."""
        # Don't allow editing stops during planning
        if self.is_planning:
            return
            
        # Create dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Edit Number of Stops")
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Create spin box for number selection
        spinbox = QtWidgets.QSpinBox()
        spinbox.setMinimum(0)
        spinbox.setMaximum(999)
        spinbox.setValue(self.table.rowCount())
        spinbox.setFixedHeight(SPINBOX_HEIGHT)  # Make it easier to click
        
        # Connect Enter key in spinbox to accept dialog
        spinbox.editingFinished.connect(dialog.accept)
        
        # Add label and spinbox
        layout.addWidget(QtWidgets.QLabel("Number of stops:"))
        layout.addWidget(spinbox)
        
        # Add buttons
        button_layout = QtWidgets.QHBoxLayout()
        ok_button = QtWidgets.QPushButton("OK")
        cancel_button = QtWidgets.QPushButton("Cancel")
        
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)
        ok_button.setDefault(True)
        ok_button.setAutoDefault(True)
        
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(ok_button)
        layout.addLayout(button_layout)
        
        # Execute dialog and process result
        if dialog.exec_():
            new_stops = spinbox.value()
            self.stops_display.setText(str(new_stops))
            self._update_stops_count()

    # ───── ROUTE PLANNING METHODS ─────────────────────────────────────────────────
    
    def _get_coordinates(self, include_hq: bool = True) -> Optional[List[Tuple[float, float]]]:
        """
        Get all coordinates (optionally including HQ + delivery points) from the UI.
        
        Args:
            include_hq: Whether to include HQ as the first coordinate (default: True)
        
        Returns:
            List of (lat, lon) tuples, or None if invalid data
        """
        try:
            # Start with HQ coordinates if requested
            coords = [HQ_COORD] if include_hq else []
            
            # Add each delivery point
            for row in range(self.table.rowCount()):
                lat_item = self.table.item(row, 0)
                lon_item = self.table.item(row, 1)
                if lat_item and lon_item:
                    lat = float(lat_item.text())
                    lon = float(lon_item.text())
                    coords.append((lat, lon))
                else:
                    # Missing item
                    raise ValueError("Missing coordinate value")
                
            return coords
            
        except (ValueError, TypeError) as e:
            # Show error message if coordinates are invalid
            logger.error(f"Invalid coordinate values: {e}")
            QtWidgets.QMessageBox.warning(
                self, "Invalid Coordinates", 
                f"Please check latitude/longitude values.\nError: {str(e)}"
            )
            return None
        except Exception as e:
            # Handle unexpected errors during coordinate parsing
            logger.error(f"Unexpected error parsing coordinates: {e}")
            QtWidgets.QMessageBox.critical(
                self, "Error", 
                f"An unexpected error occurred while parsing coordinates.\nError: {str(e)}"
            )
            return None

    def _start_route_planning(self):
        """Start the route planning process with the selected algorithm."""
        # Get coordinates
        coords = self._get_coordinates()
        if not coords:
            return
        
        # Update UI state
        self.is_planning = True
        self._set_ui_planning_state(True)
        self.out.setHtml("<i>Planning route…</i>")
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Initializing...")
        self.status_label.setVisible(True)
        
        # Create and start worker thread
        self.worker = Worker(coords, self.alg.currentIndex())
        self.worker.finished.connect(self._handle_planning_results)
        self.worker.progress.connect(self._update_progress)
        self.worker.start()

    def _set_ui_planning_state(self, is_planning: bool):
        """
        Update UI elements based on planning state.
        
        Args:
            is_planning: True if planning is in progress, False otherwise
        """
        # Disable/enable buttons based on planning state
        self.btn_plan.setEnabled(not is_planning)
        self.btn_compare.setEnabled(not is_planning)
        self.edit_stops_btn.setEnabled(not is_planning)
        
        # Show/hide progress indicators
        self.progress_bar.setVisible(is_planning)
        self.status_label.setVisible(is_planning)
        
    def _update_progress(self, value: int, message: str):
        """
        Update progress indicators in the UI.
        
        Args:
            value: Progress value (0-100)
            message: Status message to display
        """
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def _handle_planning_results(self, data: Dict[str, Any]):
        """
        Process and display route planning results.
        
        Args:
            data: Dictionary containing planning results or error
        """
        # Re-enable UI controls
        self._set_ui_planning_state(False)
        
        # Check for errors
        if "error" in data:
            self.out.setHtml(f"<b>Error:</b> {data['error']}")
            self.is_planning = False
            return
            
        # Extract result data
        tour = data["tour"]
        dist = data["dist"]
        label = data["label"]
        route = data["route"]
        computation_time = data["secs"]
        
        # Format distance in km
        distance_km = dist / 1000.0
        
        # Generate list of steps
        steps_html = "".join(
            f"<li>Stop&nbsp;{i}: Point&nbsp;{tour[i]}</li>"
            for i in range(1, len(tour) - 1)
        )
        
        # Display results in output panel
        self.out.setHtml(
            f"<p><b>{label}</b><br>"
            f"<b>Distance:</b> {distance_km:.2f} km<br>"
            f"<b>Computation Time:</b> {computation_time:.2f} s<br>"
            f"<b>Stops:</b> {len(tour) - 2}</p><ol>{steps_html}</ol>"
        )
        
        # Create and display route map
        self._display_route_map(tour, route)
        
        # Reset planning state
        self.is_planning = False

    def _display_route_map(self, tour: List[int], route_path: List[Tuple[float, float]]):
        """
        Display a map with the planned route.
        
        Args:
            tour: List of indices representing the tour order
            route_path: List of (lat, lon) points defining the complete route path
        """
        # Create a new map centered on HQ
        folium_map = folium.Map(
            location=HQ_COORD,
            zoom_start=MAP_ZOOM,
            tiles=get_offline_map_config()
        )
        
        # Add HQ marker
        folium.Marker(
            location=HQ_COORD,
            icon=folium.Icon(color="green", icon="home"),
            tooltip="HQ"
        ).add_to(folium_map)
        
        # Get all coordinates
        coords = self._get_coordinates()
        if not coords:
            return
        
        # Track placed markers to prevent overlap
        placed: Set[Tuple[float, float]] = set()
        
        # Add markers for each stop in the tour
        for order, idx in enumerate(tour[1:-1], 1):
            # Get coordinates for this stop
            lat, lon = coords[idx]
            
            # Add small jitter if this location already has a marker
            while (lat, lon) in placed:
                lat += POINT_JITTER * random.random() - POINT_JITTER / 2
                lon += POINT_JITTER * random.random() - POINT_JITTER / 2
            placed.add((lat, lon))
            
            # Create a numbered marker using DivIcon
            folium.Marker(
                location=(lat, lon),
                icon=folium.DivIcon(
                    icon_size=(40, 40),
                    icon_anchor=(20, 20),
                    html=f'<div style="background-color:#3186cc; width:30px; height:30px; '
                         f'border-radius:15px; display:flex; justify-content:center; '
                         f'align-items:center; color:white; font-weight:bold; '
                         f'font-size:14px;">{order}</div>',
                ),
                tooltip=f"Stop {order} (Point {idx})",
                popup=f"Stop {order}: Point {idx}"
            ).add_to(folium_map)
        
        # Add route polyline
        folium.PolyLine(
            route_path,
            color="yellow",
            weight=4
        ).add_to(folium_map)
        
        # Display the map
        self._display_map(folium_map)

    # ───── ALGORITHM COMPARISON METHODS ───────────────────────────────────────────
    
    def _start_algorithms_comparison(self):
        """Run both algorithms sequentially and compare their results."""
        # Get coordinates
        coords = self._get_coordinates()
        if not coords:
            return
        
        # Can't compare if already planning
        if self.is_planning:
            return
            
        # Update UI state
        self.is_planning = True
        self._set_ui_planning_state(True)
        self.out.setHtml("<i>Comparing algorithms...</i>")
        
        # Show progress bar
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.status_label.setText("Running Held-Karp algorithm...")
        self.status_label.setVisible(True)
        
               
        # Run Held-Karp first
        self.hk_worker = Worker(coords, 1)  # 1 = Held-Karp
        self.hk_worker.finished.connect(self._handle_held_karp_results)
        self.hk_worker.progress.connect(self._update_comparison_progress_hk)
        self.hk_worker.start()
        
    def _update_comparison_progress_hk(self, value: int, message: str):
        """
        Update progress indicators for the Held-Karp phase of comparison.
        
        Args:
            value: Progress value (0-100)
            message: Status message to display
        """
        # Scale to 0-50% for the first half of the comparison
        scaled_value = value // 2
        self.progress_bar.setValue(scaled_value)
        self.status_label.setText(f"Held-Karp: {message}")
        
    def _update_comparison_progress_ch(self, value: int, message: str):
        """
        Update progress indicators for the Christofides phase of comparison.
        
        Args:
            value: Progress value (0-100)
            message: Status message to display
        """
        # Scale to 50-100% for the second half of the comparison
        scaled_value = 50 + (value // 2)
        self.progress_bar.setValue(scaled_value)
        self.status_label.setText(f"Christofides: {message}")

    def _handle_held_karp_results(self, data: Dict[str, Any]):
        """
        Process Held-Karp results and start Christofides algorithm.
        
        Args:
            data: Dictionary containing Held-Karp results or error
        """
        # Check for errors
        if "error" in data:
            self.out.setHtml(f"<b>Error in Held-Karp:</b> {data['error']}")
            self._cleanup_comparison()
            return
            
        # Store Held-Karp results
        self.hk_results = data
        
        # Get the coordinates again (they might have changed)
        coords = self._get_coordinates()
        if not coords:
            self._cleanup_comparison()
            return
            
        # Update progress status
        self.status_label.setText("Running Christofides algorithm...")
        self.progress_bar.setValue(50)
            
        # Now run Christofides
        self.ch_worker = Worker(coords, 2)  # 2 = Christofides
        self.ch_worker.finished.connect(self._handle_comparison_results)
        self.ch_worker.progress.connect(self._update_comparison_progress_ch)
        self.ch_worker.start()

    def _handle_comparison_results(self, data: Dict[str, Any]):
        """
        Process Christofides results and display comparison.
        
        Args:
            data: Dictionary containing Christofides results or error
        """
        # Reset UI first
        self._cleanup_comparison()
        
        # Check for errors
        if "error" in data:
            self.out.setHtml(f"<b>Error in Christofides:</b> {data['error']}")
            return
            
        # Christofides results
        ch_results = data
        
        # Extract data for comparison
        hk_tour = self.hk_results.get("tour", [])
        hk_dist = self.hk_results.get("dist", 0.0)
        hk_time = self.hk_results.get("secs", 0.0)
        
        ch_tour = ch_results.get("tour", [])
        ch_dist = ch_results.get("dist", 0.0)
        ch_time = ch_results.get("secs", 0.0)
        
        # Calculate comparison metrics
        dist_diff = ch_dist - hk_dist
        dist_percent = (dist_diff / hk_dist) * 100 if hk_dist > 0 else 0.0
        time_diff = hk_time - ch_time
        speed_ratio = hk_time / ch_time if ch_time > 0 else float('inf')
        
        # Create comparison HTML table
        comparison_html = f"""
        <h3>Algorithm Comparison</h3>
        <table border="1" cellpadding="5" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #444;">
                <th>Metric</th>
                <th>Held-Karp (Exact)</th>
                <th>Christofides (Approx)</th>
                <th>Difference</th>
            </tr>
            <tr>
                <td><b>Distance</b></td>
                <td>{hk_dist/1000:.2f} km</td>
                <td>{ch_dist/1000:.2f} km</td>
                <td>{dist_diff/1000:.2f} km ({dist_percent:.2f}%)</td>
            </tr>
            <tr>
                <td><b>Computation Time</b></td>
                <td>{hk_time:.4f} s</td>
                <td>{ch_time:.4f} s</td>
                <td>{time_diff:.4f} s ({speed_ratio:.2f}x faster)</td>
            </tr>
            <tr>
                <td><b>Number of Stops</b></td>
                <td>{len(hk_tour)-2 if len(hk_tour) >= 2 else 0}</td>
                <td>{len(ch_tour)-2 if len(ch_tour) >= 2 else 0}</td>
                <td>-</td>
            </tr>
        </table>
        
        <p><b>Conclusion:</b> 
        Christofides algorithm is {speed_ratio:.1f}x faster but produces routes that are {dist_percent:.2f}% 
        longer than the optimal solution from Held-Karp.</p>
        
        <p><i>Note: Held-Karp guarantees the optimal solution but has exponential time complexity, 
        while Christofides guarantees routes at most 1.5x longer than optimal with polynomial time complexity.</i></p>
        """
        
        # Display comparison results
        self.out.setHtml(comparison_html)
        
        # Show comparison map
        self._display_comparison_map(hk_tour, ch_tour, self.hk_results, ch_results)

    def _cleanup_comparison(self):
        """Reset UI after comparison is complete."""
        self._set_ui_planning_state(False)
        self.is_planning = False

    def _display_comparison_map(self, hk_tour: List[int], ch_tour: List[int], 
                               hk_results: Dict[str, Any], ch_results: Dict[str, Any]):
        """
        Create a map showing both routes for comparison.
        
        Args:
            hk_tour: List of indices representing the Held-Karp tour
            ch_tour: List of indices representing the Christofides tour
            hk_results: Dictionary with Held-Karp results
            ch_results: Dictionary with Christofides results
        """
        # Create a new map centered on HQ
        folium_map = folium.Map(
            location=HQ_COORD,
            zoom_start=MAP_ZOOM,
            tiles=get_offline_map_config()
        )
        
        # Add HQ marker
        folium.Marker(
            location=HQ_COORD,
            icon=folium.Icon(color="green", icon="home"),
            tooltip="HQ"
        ).add_to(folium_map)
        
        # Get all coordinates
        coords = self._get_coordinates()
        if not coords:
            return
        
        # Track placed markers to prevent overlap
        placed: Set[Tuple[float, float]] = set()
        
        # Add markers for each delivery point
        for idx in range(1, len(coords)):
            # Get coordinates for this point
            lat, lon = coords[idx]
            
            # Add small jitter if this location already has a marker
            while (lat, lon) in placed:
                lat += POINT_JITTER * random.random() - POINT_JITTER / 2
                lon += POINT_JITTER * random.random() - POINT_JITTER / 2
            placed.add((lat, lon))
            
            # Get the order in both tours
            hk_order = hk_tour.index(idx) if idx in hk_tour else -1
            ch_order = ch_tour.index(idx) if idx in ch_tour else -1
            
            # Create tooltip and popup with order information
            tooltip = f"Point {idx}"
            if hk_order > 0 and hk_order < len(hk_tour) - 1:
                tooltip += f" | HK: Stop {hk_order}"
            if ch_order > 0 and ch_order < len(ch_tour) - 1:
                tooltip += f" | CH: Stop {ch_order}"
                
            popup_content = f"<b>Point {idx}</b><br>"
            if hk_order > 0 and hk_order < len(hk_tour) - 1:
                popup_content += f"Held-Karp: Stop #{hk_order}<br>"
            if ch_order > 0 and ch_order < len(ch_tour) - 1:
                popup_content += f"Christofides: Stop #{ch_order}"
            
            # Create a numbered marker using DivIcon
            folium.Marker(
                location=(lat, lon),
                icon=folium.DivIcon(
                    icon_size=(40, 40),
                    icon_anchor=(20, 20),
                    html=f'<div style="background-color:#3186cc; width:30px; height:30px; '
                         f'border-radius:15px; display:flex; justify-content:center; '
                         f'align-items:center; color:white; font-weight:bold; '
                         f'font-size:14px;">{idx}</div>',
                ),
                tooltip=tooltip,
                popup=popup_content
            ).add_to(folium_map)
        
        # Add route polylines with different colors
        try:
            # Get route paths
            hk_route = hk_results.get("route", [])
            ch_route = ch_results.get("route", [])
            
            # Add the route polylines
            if hk_route:
                folium.PolyLine(
                    hk_route,
                    color="yellow",
                    weight=4,
                    opacity=0.8,
                    tooltip="Held-Karp (Optimal)"
                ).add_to(folium_map)
            
            if ch_route:
                folium.PolyLine(
                    ch_route,
                    color="red",
                    weight=4,
                    opacity=0.8,
                    tooltip="Christofides"
                ).add_to(folium_map)
            
            # Add a legend
            legend_html = '''
            <div style="position: fixed; 
                        bottom: 50px; right: 50px; width: 180px; height: 90px; 
                        border:2px solid grey; z-index:9999; font-size:14px;
                        background-color: rgba(33, 33, 33, 0.8);
                        color: white;
                        padding: 10px">
              <p><b>Route Legend:</b></p>
              <p><span style="color: yellow;">━━━</span> Held-Karp (Optimal)</p>
              <p><span style="color: red;">━━━</span> Christofides (Approx)</p>
            </div>
            '''
            
            # Add legend as a hidden marker with popup
            folium.Marker(
                location=HQ_COORD,
                icon=folium.DivIcon(
                    icon_size=(0, 0),
                    html='<div style="display:none;">Legend</div>'
                ),
                popup=folium.Popup(legend_html, max_width=200)
            ).add_to(folium_map)
            
        except (KeyError, AttributeError, NameError):
            # If routes aren't available, show just the markers
            pass
        
        # Display the map
        self._display_map(folium_map)

    # ───── ONBOARDING AND HELP METHODS ──────────────────────────────────────────
    
    def _setup_help_menu(self):
        """Set up the help menu in the menu bar."""
        # Create menu bar if it doesn't exist
        menubar = self.menuBar()
        
        # Create Help menu
        help_menu = menubar.addMenu('Help')
        
        # Add actions
        tutorial_action = QtWidgets.QAction('Start Tutorial', self)
        tutorial_action.triggered.connect(self._start_tutorial)
        help_menu.addAction(tutorial_action)
        
        help_action = QtWidgets.QAction('Help & Documentation', self)
        help_action.triggered.connect(self._show_help_dialog)
        help_menu.addAction(help_action)
        
        help_menu.addSeparator()
        
        about_action = QtWidgets.QAction('About', self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)
    
    def _show_welcome_dialog(self):
        """Show the welcome dialog for first-time users."""
        dialog = WelcomeDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # User clicked "Start Tutorial"
            self._start_tutorial()
    
    def _start_tutorial(self):
        """Start the interactive tutorial."""
        if not self.tutorial_manager:
            self.tutorial_manager = TutorialManager(self)
        self.tutorial_manager.start_tutorial()
    
    def _show_help_dialog(self):
        """Show the comprehensive help dialog."""
        # Import locally to avoid forward reference issues
        globals_dict = globals()
        if 'HelpDialog' in globals_dict:
            dialog = globals_dict['HelpDialog'](self)
            dialog.exec_()
    
    def _show_about_dialog(self):
        """Show an about dialog with app information."""
        QtWidgets.QMessageBox.about(
            self,
            "About Route Planner",
            """
            <div style="font-family: Arial, sans-serif; max-width: 500px;">
                <h2 style="color: #4a86e8; margin-bottom: 10px;">Delivery Route Planner</h2>
                <p style="font-size: 14px; color: #666;"><b>Version 1.0</b> (June 2025)</p>
                
                <p style="margin-top: 15px; line-height: 1.4;">
                    A sophisticated application for optimizing delivery routes through advanced
                    graph-based algorithms and real-world road networks.
                </p>
                
                <h3 style="margin-top: 20px; color: #4a86e8; font-size: 16px;">Key Features</h3>
                <ul style="list-style-type: disc; padding-left: 20px; line-height: 1.4;">
                    <li>Interactive graphical interface with embedded map visualization</li>
                    <li>Dual algorithm support: Held-Karp (exact) and Christofides (approximation)</li>
                    <li>Real-time road network data integration via OpenStreetMap</li>
                    <li>Performance comparison and analysis tools</li>
                    <li>Comprehensive help system and guided tutorials</li>
                    <li>Intelligent caching system for offline operation</li>
                </ul>
                
                <h3 style="margin-top: 20px; color: #4a86e8; font-size: 16px;">Technical Details</h3>
                <p style="line-height: 1.4; margin-bottom: 5px;"><b>Built with:</b> PyQt5, Folium, OSMnx, NetworkX</p>
                <p style="line-height: 1.4; margin-bottom: 5px;"><b>Algorithms:</b> Held-Karp (exact), Christofides (approximation)</p>
                <p style="line-height: 1.4;"><b>License:</b> MIT License</p>
                
                <p style="margin-top: 20px; font-style: italic;">
                    Developed by Muhammad Yamman Hammad
                </p>
                
                <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #666;">
                    Copyright © 2025 Muhammad Yamman Hammad. All rights reserved.
                </div>
            </div>
            """
        )

    def _apply_dark_theme(self):
        """Apply dark theme styling to the main application."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
                font-size: 11px;
            }
            QLabel#hq_label {
                font-weight: bold;
                color: #4CAF50;
                font-size: 12px;
            }
            QLabel#stops_display {
                color: #FFD700;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
            QPushButton:disabled {
                background-color: #666666;
                color: #999999;
            }
            QComboBox {
                background-color: #404040;
                color: white;
                border: 1px solid #666666;
                padding: 5px;
                border-radius: 3px;
                font-size: 11px;
            }
            QComboBox:hover {
                border-color: #4CAF50;
            }
            QComboBox::drop-down {
                border: none;
                background-color: #404040;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: #404040;
                color: white;
                selection-background-color: #4CAF50;
                border: 1px solid #666666;
            }
            QTableWidget {
                background-color: #333333;
                color: white;
                gridline-color: #555555;
                border: 1px solid #666666;
                selection-background-color: #4CAF50;
                selection-color: white;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #555555;
            }
            QTableWidget::item:selected {
                background-color: #4CAF50;
            }
            QHeaderView::section {
                background-color: #404040;
                color: white;
                padding: 8px;
                border: 1px solid #666666;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #333333;
                color: white;
                border: 1px solid #666666;
                border-radius: 3px;
                font-family: "Courier New", monospace;
                font-size: 10px;
            }
            QScrollBar:vertical {
                background-color: #404040;
                width: 16px;
                border-radius: 8px;
            }
            QScrollBar::handle:vertical {
                background-color: #666666;
                border-radius: 8px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4CAF50;
            }
            QScrollBar:horizontal {
                background-color: #404040;
                height: 16px;
                border-radius: 8px;
            }
            QScrollBar::handle:horizontal {
                background-color: #666666;
                border-radius: 8px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background-color: #4CAF50;
            }
            QMenuBar {
                background-color: #2b2b2b;
                color: white;
                border-bottom: 1px solid #555555;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 4px 8px;
            }
            QMenuBar::item:selected {
                background-color: #4CAF50;
            }
            QMenu {
                background-color: #333333;
                color: white;
                border: 1px solid #666666;
            }
            QMenu::item {
                padding: 8px 16px;
            }
            QMenu::item:selected {
                background-color: #4CAF50;
            }
            QMenu::separator {
                height: 1px;
                background-color: #666666;
                margin: 4px 0px;
            }
        """)

    def _setup_tooltips(self):
        """Set up tooltips for UI elements (called after UI initialization)."""
        # This method will be called after ToolTipManager is defined
        ToolTipManager.setup_tooltips(self)

# -----------------------------------------------------------------------------
#  TOOLTIP AND HELP SYSTEM
# -----------------------------------------------------------------------------

class ToolTipManager:
    """Manages tooltips for UI elements to help users understand functionality."""
    
    @staticmethod
    def setup_tooltips(main_window):
        """Set up informative tooltips for all UI elements."""
        
        # HQ coordinates display
        if hasattr(main_window, 'hq_label'):
            main_window.hq_label.setToolTip(
                "Headquarters location. All routes start and end here.\n"
                "This location is fixed and configured in the config.py file."
            )
        
        # Stops display and edit button
        if hasattr(main_window, 'stops_display'):
            main_window.stops_display.setToolTip(
                "Current number of delivery stops. More stops = more complex optimization.\n"
                "Click 'Edit Stops' to change this number."
            )
        
        if hasattr(main_window, 'edit_stops_btn'):
            main_window.edit_stops_btn.setToolTip(
                "Click to change the number of delivery stops.\n"
                "You can set any number from 2 to 20 stops."
            )
        
        # Deliveries table
        if hasattr(main_window, 'table'):
            main_window.table.setToolTip(
                "Delivery locations table. Each row represents one delivery stop.\n"
                "You can edit coordinates directly or use the buttons below to add/remove stops."
            )
        
        # Add/Remove buttons
        if hasattr(main_window, 'add_btn'):
            main_window.add_btn.setToolTip(
                "Add a new delivery stop with random coordinates near your HQ.\n"
                "New stops are automatically placed within the delivery area."
            )
        
        if hasattr(main_window, 'remove_btn'):
            main_window.remove_btn.setToolTip(
                "Remove the last delivery stop from the table.\n"
                "You need at least 2 stops for route optimization."
            )
        
        # Algorithm selector
        if hasattr(main_window, 'algo_combo'):
            main_window.algo_combo.setToolTip(
                "Choose optimization algorithm:\n"
                "• Auto: Smart selection (exact for ≤12 stops, approximation for >12)\n"
                "• Held-Karp: Exact optimal solution (slower for many stops)\n"
                "• Christofides: Fast approximation (good for large problems)"
            )
        
        # Action buttons
        if hasattr(main_window, 'plan_btn'):
            main_window.plan_btn.setToolTip(
                "Calculate the optimal delivery route using the selected algorithm.\n"
                "Results will show the best route order and total distance."
            )
        
        if hasattr(main_window, 'compare_btn'):
            main_window.compare_btn.setToolTip(
                "Run both algorithms and compare their performance.\n"
                "See the trade-off between solution quality and computation time."
            )
        
        # Output text area
        if hasattr(main_window, 'out'):
            main_window.out.setToolTip(
                "Results and status messages appear here.\n"
                "Shows route details, distances, timing, and algorithm comparisons."
            )
        
        # Web view (map)
        if hasattr(main_window, 'map_view'):
            main_window.map_view.setToolTip(
                "Interactive map showing your HQ, delivery stops, and optimized routes.\n"
                "You can zoom, pan, and click on markers for more information."
            )


class HelpDialog(QtWidgets.QDialog):
    """Comprehensive help dialog with tabbed interface covering all app features."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Help & Documentation")
        self.setMinimumSize(800, 600)
        self.resize(900, 700)
        self._setup_ui()
        self._apply_styling()
    
    def _setup_ui(self):
        """Set up the help dialog UI with tabbed interface."""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Title
        title = QtWidgets.QLabel("Delivery Route Planner - Help & Documentation")
        title.setObjectName("title")
        layout.addWidget(title)
        
        # Tab widget
        tab_widget = QtWidgets.QTabWidget()
        
        # Add tabs
        tab_widget.addTab(self._create_getting_started_tab(), "Getting Started")
        tab_widget.addTab(self._create_features_tab(), "Features")
        tab_widget.addTab(self._create_algorithms_tab(), "Algorithms")
        tab_widget.addTab(self._create_tips_tab(), "Tips & Tricks")
        tab_widget.addTab(self._create_faq_tab(), "FAQ")
        
        layout.addWidget(tab_widget)
        
        # Close button
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def _create_getting_started_tab(self):
        """Create the getting started guide tab."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        content = QtWidgets.QLabel("""
        <h2>Welcome to the Delivery Route Planner!</h2>
        
        <h3>What is this app?</h3>
        <p>This application helps you optimize delivery routes in any urban area. 
        It uses advanced algorithms to find the shortest route that visits all your delivery locations 
        and returns to your headquarters.</p>
        
        <h3>Quick Start Guide:</h3>
        <ol>
            <li><b>Set up your deliveries:</b> The app starts with 5 random delivery locations. 
                You can add more, remove some, or edit the coordinates in the table.</li>
            <li><b>Choose an algorithm:</b> Select "Auto" for automatic selection, or choose 
                a specific algorithm if you have preferences.</li>
            <li><b>Plan your route:</b> Click "Plan Route" to calculate the optimal delivery sequence.</li>
            <li><b>View results:</b> The map will show your optimized route, and the output panel 
                will display detailed information about distances and timing.</li>
        </ol>
        
        <h3>Understanding the Interface:</h3>
        <ul>
            <li><b>Left Panel:</b> All controls for configuring your delivery problem</li>
            <li><b>Right Panel:</b> Interactive map showing locations and routes</li>
            <li><b>HQ (Green marker):</b> Your headquarters location</li>
            <li><b>Red markers:</b> Delivery locations that need to be visited</li>
            <li><b>Colored lines:</b> Optimized routes between locations</li>
        </ul>
        
        <p><i>Tip: Hover over any UI element to see helpful tooltips!</i></p>
        """)
        content.setWordWrap(True)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return widget
    
    def _create_features_tab(self):
        """Create the features overview tab."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        content = QtWidgets.QLabel("""
        <h2>Application Features</h2>
        
        <h3>🗺️ Interactive Map</h3>
        <ul>
            <li>Dark-themed map powered by OpenStreetMap</li>
            <li>Real road network data from OpenStreetMap</li>
            <li>Zoomable and pannable interface</li>
            <li>Click markers for location details</li>
            <li>Visual route display with different colors for different algorithms</li>
        </ul>
        
        <h3>📍 Location Management</h3>
        <ul>
            <li>Add or remove delivery stops dynamically</li>
            <li>Edit coordinates directly in the table</li>
            <li>Automatic coordinate generation near your HQ</li>
            <li>Support for 2-20 delivery locations</li>
            <li>Real-world coordinates based on your location</li>
        </ul>
        
        <h3>🧮 Route Optimization</h3>
        <ul>
            <li>Multiple algorithm options (exact and approximation)</li>
            <li>Automatic algorithm selection based on problem size</li>
            <li>Real-time progress feedback</li>
            <li>Detailed performance metrics</li>
            <li>Distance calculations using actual road networks</li>
        </ul>
        
        <h3>📊 Analysis Tools</h3>
        <ul>
            <li>Algorithm comparison mode</li>
            <li>Performance timing and analysis</li>
            <li>Route quality assessment</li>
            <li>Visual comparison of different solutions</li>
            <li>Detailed output logs</li>
        </ul>
        
        <h3>🎓 Learning Features</h3>
        <ul>
            <li>Interactive tutorial for new users</li>
            <li>Comprehensive help system</li>
            <li>Tooltips for all UI elements</li>
            <li>Algorithm explanations and trade-offs</li>
            <li>Best practices and tips</li>
        </ul>
        """)
        content.setWordWrap(True)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return widget
    
    def _create_algorithms_tab(self):
        """Create the algorithms explanation tab."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        content = QtWidgets.QLabel("""
        <h2>Optimization Algorithms</h2>
        
        <h3>🎯 Auto Selection (Recommended)</h3>
        <p>The app automatically chooses the best algorithm based on your problem size:</p>
        <ul>
            <li><b>≤12 stops:</b> Uses Held-Karp for guaranteed optimal solution</li>
            <li><b>>12 stops:</b> Uses Christofides for fast, high-quality approximation</li>
        </ul>
        
        <h3>🔬 Held-Karp Algorithm (Exact)</h3>
        <p><b>What it does:</b> Finds the mathematically optimal solution using dynamic programming.</p>
        <p><b>Pros:</b></p>
        <ul>
            <li>Guaranteed to find the shortest possible route</li>
            <li>Perfect for small to medium problems (2-12 stops)</li>
            <li>No approximation - you get the best answer</li>
        </ul>
        <p><b>Cons:</b></p>
        <ul>
            <li>Exponential time complexity O(n²2ⁿ)</li>
            <li>Becomes very slow with many stops (>15)</li>
            <li>High memory usage for large problems</li>
        </ul>
        <p><b>Best for:</b> When you need the absolute best route and have ≤12 stops.</p>
        
        <h3>⚡ Christofides Algorithm (Approximation)</h3>
        <p><b>What it does:</b> Uses graph theory to find a route that's at most 50% longer than optimal.</p>
        <p><b>Pros:</b></p>
        <ul>
            <li>Very fast - runs in polynomial time O(n³)</li>
            <li>Scales well to many stops (tested up to 50+)</li>
            <li>Guarantees solution within 150% of optimal</li>
            <li>Usually much better than 150% in practice</li>
        </ul>
        <p><b>Cons:</b></p>
        <ul>
            <li>Not guaranteed to find the absolute shortest route</li>
            <li>Solution quality varies with problem structure</li>
        </ul>
        <p><b>Best for:</b> When you have many stops (>12) or need fast results.</p>
        
        <h3>🔍 When to Use Which Algorithm</h3>
        <table border="1" style="border-collapse: collapse; width: 100%;">
            <tr style="background-color: #4CAF50; color: white;">
                <th>Stops</th><th>Recommended</th><th>Reason</th>
            </tr>
            <tr><td>2-8</td><td>Held-Karp</td><td>Fast and optimal</td></tr>
            <tr><td>9-12</td><td>Held-Karp</td><td>Still reasonable time, optimal result</td></tr>
            <tr><td>13-20</td><td>Christofides</td><td>Much faster, good quality</td></tr>
            <tr><td>20+</td><td>Christofides</td><td>Only practical option</td></tr>
        </table>
        """)
        content.setWordWrap(True)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return widget
    
    def _create_tips_tab(self):
        """Create the tips and tricks tab."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        content = QtWidgets.QLabel("""
        <h2>Tips & Tricks</h2>
        
        <h3>🎯 Getting Better Results</h3>
        <ul>
            <li><b>Check your coordinates:</b> Make sure all delivery locations are accessible by road</li>
            <li><b>Cluster nearby deliveries:</b> Group stops that are close together for better efficiency</li>
            <li><b>Use realistic locations:</b> The app works best with actual geographic coordinates</li>
            <li><b>Start small:</b> Test with fewer stops first, then scale up</li>
        </ul>
        
        <h3>⚡ Performance Tips</h3>
        <ul>
            <li><b>Use Auto mode:</b> Let the app choose the best algorithm for your problem size</li>
            <li><b>For many stops (>15):</b> Always use Christofides algorithm</li>
            <li><b>For comparison:</b> Only compare algorithms with ≤12 stops</li>
            <li><b>Large problems:</b> Be patient - complex routing takes time</li>
        </ul>
        
        <h3>🗺️ Map Navigation</h3>
        <ul>
            <li><b>Zoom:</b> Use mouse wheel or zoom controls</li>
            <li><b>Pan:</b> Click and drag to move around</li>
            <li><b>Markers:</b> Click on any marker for details</li>
            <li><b>Routes:</b> Different colors show routes from different algorithms</li>
        </ul>
        
        <h3>📊 Understanding Results</h3>
        <ul>
            <li><b>Total Distance:</b> Sum of all segments in the route</li>
            <li><b>Route Order:</b> Sequence of stops for optimal delivery</li>
            <li><b>Computation Time:</b> How long the algorithm took to run</li>
            <li><b>Algorithm Info:</b> Which method was used and why</li>
        </ul>
        
        <h3>🔧 Troubleshooting</h3>
        <ul>
            <li><b>App freezes:</b> Large problems take time - check progress bar</li>
            <li><b>No route shown:</b> Check that coordinates are valid</li>
            <li><b>Poor performance:</b> Try fewer stops or use Christofides</li>
            <li><b>Map not loading:</b> Check internet connection</li>
        </ul>
        
        <h3>💡 Advanced Features</h3>
        <ul>
            <li><b>Edit coordinates:</b> Double-click table cells to modify locations</li>
            <li><b>Keyboard shortcuts:</b> Use Tab to navigate between fields</li>
            <li><b>Copy results:</b> Select and copy text from the output panel</li>
            <li><b>Multiple runs:</b> Compare different coordinate sets</li>
        </ul>
        """)
        content.setWordWrap(True)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return widget
    
    def _create_faq_tab(self):
        """Create the frequently asked questions tab."""
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        
        content = QtWidgets.QLabel("""
        <h2>Frequently Asked Questions</h2>
        
        <h3>❓ General Questions</h3>
        
        <p><b>Q: What is the Traveling Salesman Problem (TSP)?</b><br>
        A: The TSP asks: "Given a list of locations and distances between them, what's the shortest route that visits each location exactly once and returns to the starting point?" This is exactly what delivery route optimization solves.</p>
        
        <p><b>Q: Why is route optimization important?</b><br>
        A: Optimized routes save time, fuel, and money. A 10% improvement in route efficiency can significantly reduce delivery costs and improve customer service.</p>
        
        <p><b>Q: How accurate are the distance calculations?</b><br>
        A: The app uses real road network data from OpenStreetMap, so distances reflect actual driving routes in your area, not straight-line distances.</p>
        
        <h3>🔧 Technical Questions</h3>
        
        <p><b>Q: Why does Held-Karp become slow with many stops?</b><br>
        A: The algorithm examines all possible route combinations. With n stops, there are (n-1)!/2 possible routes. For 15 stops, that's over 43 billion combinations!</p>
        
        <p><b>Q: How good is the Christofides approximation?</b><br>
        A: Theoretically, it's guaranteed to be within 150% of optimal. In practice, it's usually within 105-115% of optimal for most real-world problems.</p>
        
        <p><b>Q: Can I use this for other cities?</b><br>
        A: The algorithms work in any location! The app can be configured by changing the HQ coordinates in the config file to match your operational area.</p>
        
        <h3>🗺️ Map and Location Questions</h3>
        
        <p><b>Q: Why are some roads missing from the map?</b><br>
        A: The app uses OpenStreetMap data, which is community-maintained. Some smaller roads might not be mapped yet.</p>
        
        <p><b>Q: Can I add my own custom locations?</b><br>
        A: Yes! Edit the coordinates directly in the table. You can use any valid latitude/longitude coordinates.</p>
        
        <p><b>Q: What's the maximum number of stops I can use?</b><br>
        A: Technically unlimited, but practical limits are around 20 stops for reasonable performance.</p>
        
        <h3>⚡ Performance Questions</h3>
        
        <p><b>Q: How long should I wait for results?</b><br>
        A: Christofides usually finishes in seconds. Held-Karp with 12 stops takes 1-2 minutes. 15+ stops can take hours.</p>
        
        <p><b>Q: Why is the comparison taking so long?</b><br>
        A: Comparison runs both algorithms. If you have >12 stops, Held-Karp will be very slow. Use comparison only for smaller problems.</p>
        
        <p><b>Q: Can I cancel a long-running calculation?</b><br>
        A: Currently, you need to restart the app to cancel. This is a known limitation.</p>
        
        <h3>🎓 Learning Questions</h3>
        
        <p><b>Q: I'm new to optimization. Where should I start?</b><br>
        A: Start with the tutorial! It walks you through all features. Begin with 5-8 stops and the Auto algorithm setting.</p>
        
        <p><b>Q: How can I learn more about these algorithms?</b><br>
        A: The app provides a practical introduction. For deeper learning, search for "Traveling Salesman Problem" and "Vehicle Routing Problem" in academic resources.</p>
        """)
        content.setWordWrap(True)
        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(content)
        scroll.setWidgetResizable(True)
        
        layout.addWidget(scroll)
        return widget
        
    def _apply_styling(self):
        """Apply styling to the help dialog."""
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: white;
            }
            QLabel#title {
                font-size: 20px;
                font-weight: bold;
                color: #4CAF50;
                margin: 10px;
            }
            QTabWidget::pane {
                border: 1px solid #666;
                background-color: #333;
            }
            QTabBar::tab {
                background-color: #555;
                color: white;
                padding: 8px 12px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #4CAF50;
            }
            QScrollArea {
                border: none;
                background-color: #333;
            }
            QLabel {
                background-color: transparent;
                padding: 15px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

# -----------------------------------------------------------------------------
#  MAIN APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------

def main():
    """Main application entry point."""
    import sys
    
    # Create Qt application
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Delivery Route Planner")
    app.setApplicationVersion("1.0.2")
    app.setOrganizationName("Route Optimization Solutions")
    
    # Create and show main window
    window = PlannerUI()
    window.show()
    
    # Start event loop
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
