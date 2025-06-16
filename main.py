#!/usr/bin/env python3
"""
Glitch Runner - A 2D platformer game
Version 2.0 - June 16, 2025
"""
import pygame
import sys
import os

# Try to import the resource_path function
try:
    from resource_path import resource_path
except ImportError:
    # If not available, define it here
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

# Add the current directory to the path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.game import Game

def main():
    # Initialize pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Run the game
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
