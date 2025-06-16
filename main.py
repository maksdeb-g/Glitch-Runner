#!/usr/bin/env python3
"""
Glitch Runner - A 2D platformer game
"""
import pygame
import sys
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
