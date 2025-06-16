import pygame
from src.constants import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        
        # Create a rectangle for the platform
        self.image = pygame.Surface((width, height))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        
        # Set position
        self.rect.x = x
        self.rect.y = y
        
        # For glitch effects
        self.original_image = self.image.copy()
        self.alpha = 255
        self.disappearing = False
        self.solid = True  # For collision detection
        
    def update(self):
        # For animation or other updates
        pass
