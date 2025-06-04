#!/usr/bin/env python3
"""
Route Planner Main Entry Point
==============================

This is the main entry point for the Route Planner application.
It imports and runs the main UI application.
"""

def main():
    """Main entry point for the Route Planner application."""
    from route_planner.app import main as app_main
    app_main()


if __name__ == "__main__":
    main()
