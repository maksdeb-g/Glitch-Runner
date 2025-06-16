import pygame
import os
import random
import math
from src.constants import *

class Background:
    """Class to handle the game background with simple effects"""
    
    def __init__(self, level_num):
        self.level_num = level_num
        
        # Try to load background image
        self.use_image = False
        self.background = None
        bg_path = os.path.join('assets', 'images', 'backgrounds', f'level{level_num}_bg.png')
        
        if os.path.exists(bg_path):
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.use_image = True
            except pygame.error:
                print(f"Could not load background image: {bg_path}")
        
        # Get background color from level data - using more neutral colors
        if level_num == 1:
            self.bg_color = (30, 30, 40)  # Soft blue-gray
        elif level_num == 2:
            self.bg_color = (35, 25, 45)  # Soft purple-gray
        else:
            self.bg_color = (40, 25, 30)  # Soft red-gray
        
        # Create procedural background elements
        self.grid_size = 80  # Much larger grid for minimal visual noise
        self.grid_color = (255, 255, 255, 2)  # Extremely transparent white
        
        # Minimal visual elements
        self.glitch_lines = []
        self.glitch_timer = 0
        
        # Only generate visual elements for level 2 and 3
        if level_num > 1:
            self.generate_minimal_elements()
    
    def generate_minimal_elements(self):
        """Generate minimal visual elements based on level"""
        # Clear existing elements
        self.glitch_lines = []
        
        # Generate just a few horizontal lines
        num_lines = self.level_num  # 2 for level 2, 3 for level 3
        for _ in range(num_lines):
            y = random.randint(0, SCREEN_HEIGHT)
            width = random.randint(100, 300)
            x = random.randint(0, SCREEN_WIDTH - width)
            opacity = random.randint(10, 30)  # Very low opacity
            color = (200, 200, 200, opacity)  # Light gray, less distracting
            self.glitch_lines.append({
                'x': x,
                'y': y,
                'width': width,
                'height': 1,  # Just 1 pixel height
                'color': color,
                'lifetime': random.randint(60, 180),
                'age': 0
            })
    
    def update(self):
        """Update background elements"""
        self.glitch_timer += 1
        
        # Only update visual elements for level 2 and 3
        if self.level_num > 1:
            # Regenerate elements very infrequently
            if self.glitch_timer >= 180:  # Every 3 seconds (assuming 60 FPS)
                self.glitch_timer = 0
                if random.random() < 0.1:  # Only 10% chance
                    self.generate_minimal_elements()
            
            # Update glitch lines
            for line in self.glitch_lines[:]:
                line['age'] += 1
                if line['age'] >= line['lifetime']:
                    self.glitch_lines.remove(line)
    
    def draw_procedural_background(self, surface):
        """Draw a very simple procedurally generated background"""
        # Fill with base color
        surface.fill(self.bg_color)
        
        # Level 1: Just a simple grid with large spacing
        if self.level_num == 1:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 2), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 2), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Level 2: Very subtle grid
        elif self.level_num == 2:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 3), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 3), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Level 3: Slightly more visible grid
        elif self.level_num == 3:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 4), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 4), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw minimal glitch lines (only for level 2 and 3)
        if self.level_num > 1:
            for line in self.glitch_lines:
                # Calculate opacity based on lifetime
                alpha = 255 * (1 - line['age'] / line['lifetime'])
                color = line['color'][:3] + (int(alpha),)
                
                # Create a surface for the line with alpha
                line_surface = pygame.Surface((line['width'], line['height']), pygame.SRCALPHA)
                line_surface.fill(color)
                surface.blit(line_surface, (line['x'], line['y']))
    
    def draw(self, surface):
        """Draw the background"""
        if self.use_image:
            # Use the loaded image
            surface.blit(self.background, (0, 0))
        else:
            # Use procedurally generated background
            self.draw_procedural_background(surface)
