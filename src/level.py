import pygame
import math
import os
from src.platform import Platform
from src.enemy import Enemy
from src.background import Background
from src.constants import *

class LevelExit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Create exit portal
        self.image = pygame.Surface((50, 80))
        self.image.fill(EXIT_COLOR)
        
        # Add some visual flair to the exit
        pygame.draw.ellipse(self.image, (255, 255, 255), (5, 5, 40, 70))
        pygame.draw.ellipse(self.image, EXIT_COLOR, (10, 10, 30, 60))
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Animation
        self.animation_timer = 0
    
    def update(self):
        # Simple pulsing animation
        self.animation_timer += 0.1
        pulse = abs(math.sin(self.animation_timer)) * 10
        
        # Adjust size slightly based on pulse
        self.image.fill(EXIT_COLOR)
        pygame.draw.ellipse(self.image, (255, 255, 255), (5, 5, 40, 70))
        pygame.draw.ellipse(self.image, EXIT_COLOR, (10 + pulse/4, 10 + pulse/4, 30 - pulse/2, 60 - pulse/2))

class Level:
    def __init__(self, level_data):
        self.name = level_data["name"]
        self.background_color = level_data["background_color"]
        self.player_start_pos = level_data["player_start"]
        
        # Create sprite groups
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # Create level exit
        self.exit = LevelExit(level_data["exit_pos"][0], level_data["exit_pos"][1])
        
        # Create background
        level_num = 1
        if "Level 2" in level_data["name"]:
            level_num = 2
        elif "Level 3" in level_data["name"]:
            level_num = 3
        self.background = Background(level_num)
        
        # Load level elements
        self.load_platforms(level_data["platforms"])
        self.load_enemies(level_data["enemies"])
    
    def load_platforms(self, platform_data):
        for p_data in platform_data:
            x, y, width, height = p_data
            platform = Platform(x, y, width, height)
            self.platforms.add(platform)
    
    def load_enemies(self, enemy_data):
        for e_data in enemy_data:
            x, y, patrol_distance, enemy_type = e_data
            enemy = Enemy(x, y, patrol_distance, enemy_type)
            self.enemies.add(enemy)
    
    def reset_player_position(self, player):
        player.rect.x = self.player_start_pos[0]
        player.rect.y = self.player_start_pos[1]
        player.velocity_x = 0
        player.velocity_y = 0
        player.set_invincible()  # Make player invincible when spawning
    
    
    def check_exit_collision(self, player):
        # Check if player has reached the exit
        return player.rect.colliderect(self.exit.rect)
    
    def check_enemy_collision(self, player):
        # Don't check collisions if player is invincible
        if player.invincible:
            return False
            
        # Check if player collides with any enemy
        for enemy in self.enemies:
            if player.rect.colliderect(enemy.rect):
                return True
            
            # Check for projectile collisions
            for projectile in enemy.projectiles:
                if player.rect.colliderect(projectile.rect):
                    projectile.kill()  # Remove the projectile
                    return True
        
        return False
    
    
    def update(self, player):
        # Update background
        self.background.update()
        
        # Update all platforms
        for platform in self.platforms:
            platform.update()
        
        # Update all enemies
        for enemy in self.enemies:
            enemy.update(self.platforms, player)
        
        # Update exit
        self.exit.update()
        
        # Get solid platforms for collision detection
        solid_platforms = [p for p in self.platforms if p.solid]
        
        # Update player with collisions
        player.update(solid_platforms)
    
    def draw(self, screen):
        # Draw background
        self.background.draw(screen)
        
        # Draw platforms
        self.platforms.draw(screen)
        
        # Draw exit
        screen.blit(self.exit.image, self.exit.rect)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
