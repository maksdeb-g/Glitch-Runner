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
        elif level_num == 3:
            self.bg_color = (40, 25, 30)  # Soft red-gray
        elif level_num == 4:
            self.bg_color = (45, 15, 45)  # Purple-red mix
        else:  # Level 5
            self.bg_color = (50, 10, 20)  # Darker red
        
        # Create procedural background elements
        self.grid_size = 80  # Much larger grid for minimal visual noise
        self.grid_color = (255, 255, 255, 2)  # Extremely transparent white
        
        # Visual elements
        self.glitch_lines = []
        self.glitch_blocks = []
        self.glitch_timer = 0
        
        # Generate visual elements based on level
        if level_num > 1:
            self.generate_elements()
    
    def generate_elements(self):
        """Generate visual elements based on level"""
        # Clear existing elements
        self.glitch_lines = []
        self.glitch_blocks = []
        
        # Generate horizontal lines
        num_lines = self.level_num  # More lines for higher levels
        for _ in range(num_lines):
            y = random.randint(0, SCREEN_HEIGHT)
            width = random.randint(100, 300)
            x = random.randint(0, SCREEN_WIDTH - width)
            
            # Higher opacity for higher levels
            opacity = random.randint(10, 20) if self.level_num < 4 else random.randint(20, 40)
            
            # More varied colors for levels 4-5
            if self.level_num >= 4:
                color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255), opacity)
            else:
                color = (200, 200, 200, opacity)  # Light gray for lower levels
                
            self.glitch_lines.append({
                'x': x,
                'y': y,
                'width': width,
                'height': 1 if self.level_num < 4 else random.randint(1, 3),
                'color': color,
                'lifetime': random.randint(60, 180),
                'age': 0
            })
        
        # Generate glitch blocks only for levels 4-5
        if self.level_num >= 4:
            num_blocks = self.level_num - 2  # 2 for level 4, 3 for level 5
            for _ in range(num_blocks):
                x = random.randint(0, SCREEN_WIDTH - 50)
                y = random.randint(0, SCREEN_HEIGHT - 50)
                width = random.randint(10, 30)
                height = random.randint(10, 30)
                opacity = random.randint(15, 35)
                color = (random.randint(150, 255), random.randint(150, 255), random.randint(150, 255), opacity)
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
        
        # Only update visual elements for level 2+
        if self.level_num > 1:
            # Regenerate elements based on level
            if self.level_num < 4:
                # Levels 2-3: infrequent updates
                if self.glitch_timer >= 180:  # Every 3 seconds
                    self.glitch_timer = 0
                    if random.random() < 0.1:  # 10% chance
                        self.generate_elements()
            else:
                # Levels 4-5: more frequent updates
                if self.glitch_timer >= 90:  # Every 1.5 seconds
                    self.glitch_timer = 0
                    if random.random() < 0.3:  # 30% chance
                        self.generate_elements()
            
            # Update glitch lines
            for line in self.glitch_lines[:]:
                line['age'] += 1
                if line['age'] >= line['lifetime']:
                    self.glitch_lines.remove(line)
            
            # Update glitch blocks (only for levels 4-5)
            for block in self.glitch_blocks[:]:
                block['age'] += 1
                if block['age'] >= block['lifetime']:
                    self.glitch_blocks.remove(block)
    
    def draw_procedural_background(self, surface):
        """Draw a procedurally generated background"""
        # Fill with base color
        surface.fill(self.bg_color)
        
        # Draw grid based on level
        if self.level_num <= 3:
            # Levels 1-3: Simple grid with increasing opacity
            opacity = self.level_num + 1  # 2 for level 1, 3 for level 2, 4 for level 3
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, opacity), (x, 0), (x, SCREEN_HEIGHT), 1)
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                pygame.draw.line(surface, (255, 255, 255, opacity), (0, y), (SCREEN_WIDTH, y), 1)
        
        elif self.level_num == 4:
            # Level 4: Slightly distorted grid
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                points = [(x, 0)]
                for y in range(self.grid_size, SCREEN_HEIGHT, self.grid_size):
                    offset = math.sin(y / 50 + self.glitch_timer / 15) * 3
                    points.append((x + offset, y))
                pygame.draw.lines(surface, (255, 255, 255, 5), False, points, 1)
            
            for y in range(0, SCREEN_HEIGHT, self.grid_size):
                points = [(0, y)]
                for x in range(self.grid_size, SCREEN_WIDTH, self.grid_size):
                    offset = math.sin(x / 50 + self.glitch_timer / 15) * 3
                    points.append((x, y + offset))
                pygame.draw.lines(surface, (255, 255, 255, 5), False, points, 1)
        
        else:  # Level 5
            # Level 5: More corrupted grid
            for x in range(0, SCREEN_WIDTH, self.grid_size):
                for y in range(0, SCREEN_HEIGHT, self.grid_size):
                    if random.random() < 0.7:  # 70% chance to draw each cell
                        cell_color = (
                            min(255, self.bg_color[0] + random.randint(0, 20)),
                            min(255, self.bg_color[1] + random.randint(0, 20)),
                            min(255, self.bg_color[2] + random.randint(0, 20))
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
        
        # Draw glitch blocks (only for levels 4-5)
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
