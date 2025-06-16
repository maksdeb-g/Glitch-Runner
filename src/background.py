import pygame
import os
import random
import math
from src.constants import *

class Background:
    """Class to handle the game background with glitch effects"""
    
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
        
        # Get background color from level data
        if level_num == 1:
            self.bg_color = (20, 20, 35)  # Darker blue/purple for better contrast
        elif level_num == 2:
            self.bg_color = (25, 10, 40)  # Darker purple for better contrast
        else:
            self.bg_color = (40, 5, 20)  # Darker red for better contrast
        
        # Create procedural background elements
        self.grid_size = 40  # Larger grid for less visual noise
        self.grid_color = (255, 255, 255, 5)  # Very transparent white
        
        # Glitch effect variables
        self.glitch_lines = []
        self.glitch_blocks = []
        self.glitch_timer = 0
        self.generate_glitch_elements()
    
    def generate_glitch_elements(self):
        """Generate random glitch elements based on level"""
        # Clear existing elements
        self.glitch_lines = []
        self.glitch_blocks = []
        
        # Generate horizontal glitch lines
        num_lines = self.level_num * 2
        for _ in range(num_lines):
            y = random.randint(0, SCREEN_HEIGHT)
            width = random.randint(50, 200)
            x = random.randint(0, SCREEN_WIDTH - width)
            opacity = random.randint(20, 60)  # Lower opacity for better visibility
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), opacity)
            self.glitch_lines.append({
                'x': x,
                'y': y,
                'width': width,
                'height': random.randint(1, 3),
                'color': color,
                'lifetime': random.randint(30, 120),
                'age': 0
            })
        
        # Generate glitch blocks
        num_blocks = self.level_num
        for _ in range(num_blocks):
            x = random.randint(0, SCREEN_WIDTH - 50)
            y = random.randint(0, SCREEN_HEIGHT - 50)
            width = random.randint(10, 50)
            height = random.randint(10, 50)
            opacity = random.randint(20, 60)  # Lower opacity for better visibility
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255), opacity)
            self.glitch_blocks.append({
                'x': x,
                'y': y,
                'width': width,
                'height': height,
                'color': color,
                'lifetime': random.randint(30, 120),
                'age': 0
            })
    
    def update(self):
        """Update background elements"""
        self.glitch_timer += 1
        
        # Regenerate glitch elements periodically
        if self.glitch_timer >= 60:  # Every second (assuming 60 FPS)
            self.glitch_timer = 0
            if random.random() < 0.2:  # 20% chance each second (reduced from 30%)
                self.generate_glitch_elements()
        
        # Update glitch lines
        for line in self.glitch_lines[:]:
            line['age'] += 1
            if line['age'] >= line['lifetime']:
                self.glitch_lines.remove(line)
        
        # Update glitch blocks
        for block in self.glitch_blocks[:]:
            block['age'] += 1
            if block['age'] >= block['lifetime']:
                self.glitch_blocks.remove(block)
    
    def draw_procedural_background(self, surface):
        """Draw a procedurally generated background"""
        # Fill with base color
        surface.fill(self.bg_color)
        
        # Draw grid (level 1) - simplified for better visibility
        if self.level_num == 1:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 3), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, 3), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Draw distorted grid (level 2) - simplified for better visibility
        elif self.level_num == 2:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                points = [(x, 0)]
                for y in range(self.grid_size, SCREEN_HEIGHT, self.grid_size):
                    offset = math.sin(y / 30 + self.glitch_timer / 10) * 5
                    points.append((x + offset, y))
                pygame.draw.lines(surface, (255, 255, 255, 5), False, points, 1)
            
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                points = [(0, y)]
                for x in range(self.grid_size, SCREEN_WIDTH, self.grid_size):
                    offset = math.sin(x / 30 + self.glitch_timer / 10) * 5
                    points.append((x, y + offset))
                pygame.draw.lines(surface, (255, 255, 255, 5), False, points, 1)
        
        # Draw corrupted grid (level 3) - simplified for better visibility
        elif self.level_num == 3:
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                for y in range(0, SCREEN_HEIGHT, self.grid_size):
                    if random.random() < 0.6:  # 60% chance to draw each cell (reduced from 80%)
                        cell_color = (
                            min(255, self.bg_color[0] + random.randint(0, 30)),
                            min(255, self.bg_color[1] + random.randint(0, 30)),
                            min(255, self.bg_color[2] + random.randint(0, 30))
                        )
                        pygame.draw.rect(surface, cell_color, 
                                        (x, y, self.grid_size, self.grid_size), 1)
        
        # Draw glitch lines
        for line in self.glitch_lines:
            # Calculate opacity based on lifetime
            alpha = 255 * (1 - line['age'] / line['lifetime'])
            color = line['color'][:3] + (int(alpha),)
            
            # Create a surface for the line with alpha
            line_surface = pygame.Surface((line['width'], line['height']), pygame.SRCALPHA)
            line_surface.fill(color)
            surface.blit(line_surface, (line['x'], line['y']))
        
        # Draw glitch blocks
        for block in self.glitch_blocks:
            # Calculate opacity based on lifetime
            alpha = 255 * (1 - block['age'] / block['lifetime'])
            color = block['color'][:3] + (int(alpha),)
            
            # Create a surface for the block with alpha
            block_surface = pygame.Surface((block['width'], block['height']), pygame.SRCALPHA)
            block_surface.fill(color)
            surface.blit(block_surface, (block['x'], block['y']))
    
    def draw(self, surface):
        """Draw the background"""
        if self.use_image:
            # Use the loaded image
            surface.blit(self.background, (0, 0))
        else:
            # Use procedurally generated background
            self.draw_procedural_background(surface)
