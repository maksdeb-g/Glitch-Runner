import pygame
import math
import os
import random
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
        
        # Determine level number
        level_num = 1
        if "Level 2" in level_data["name"]:
            level_num = 2
        elif "Level 3" in level_data["name"]:
            level_num = 3
        elif "Level 4" in level_data["name"]:
            level_num = 4
        elif "Level 5" in level_data["name"]:
            level_num = 5
            
        # Create background
        self.background = Background(level_num)
        
        # Screen shake settings
        self.shake_enabled = level_data.get("shake_enabled", False)
        self.shake_offset_x = 0
        self.shake_offset_y = 0
        self.shake_intensity = SHAKE_INTENSITY_LEVEL4 if level_num == 4 else SHAKE_INTENSITY_LEVEL5
        
        # Advanced glitches (for level 5)
        self.advanced_glitches = level_data.get("advanced_glitches", False)
        self.glitch_timer = 0
        self.glitch_effect = None
        self.glitch_duration = 0
        
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
    
    def update_screen_shake(self):
        """Update screen shake effect"""
        if self.shake_enabled:
            # Constant screen shake for levels 4-5
            self.shake_offset_x = random.randint(-self.shake_intensity, self.shake_intensity)
            self.shake_offset_y = random.randint(-self.shake_intensity, self.shake_intensity)
    
    def update_advanced_glitches(self):
        """Update advanced glitch effects for level 5"""
        if not self.advanced_glitches:
            return
            
        self.glitch_timer += 1
        
        # Check if we need to start a new glitch effect
        if self.glitch_effect is None and self.glitch_timer >= 180:  # Every 3 seconds
            if random.random() < 0.3:  # 30% chance
                self.start_glitch_effect()
                self.glitch_timer = 0
        
        # Update current glitch effect
        if self.glitch_effect:
            self.glitch_duration -= 1
            if self.glitch_duration <= 0:
                self.glitch_effect = None
    
    def start_glitch_effect(self):
        """Start a random advanced glitch effect"""
        # Removed "invert" since it requires numpy/surfarray
        effect_type = random.choice(["color_shift", "static"])
        self.glitch_effect = effect_type
        self.glitch_duration = random.randint(15, 45)  # 0.25 to 0.75 seconds
    
    def apply_glitch_effect(self, screen):
        """Apply the current glitch effect to the screen"""
        if not self.glitch_effect:
            return
            
        # Create a copy of the screen
        screen_copy = screen.copy()
        
        if self.glitch_effect == "color_shift":
            # Simple color shift without using surfarray
            shift_amount = random.randint(3, 8)
            screen.blit(screen_copy, (shift_amount, 0))
            
        elif self.glitch_effect == "static":
            # Add static noise to a portion of the screen
            height = random.randint(5, 20)
            y_pos = random.randint(0, SCREEN_HEIGHT - height)
            
            # Create static noise
            static = pygame.Surface((SCREEN_WIDTH, height))
            for x in range(0, SCREEN_WIDTH, 2):
                for y in range(0, height, 2):
                    if random.random() < 0.5:
                        color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
                        static.set_at((x, y), color)
            
            # Apply static with transparency
            static.set_alpha(100)
            screen.blit(static, (0, y_pos))
    
    def update(self, player):
        # Update background
        self.background.update()
        
        # Update screen shake
        self.update_screen_shake()
        
        # Update advanced glitches
        self.update_advanced_glitches()
        
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
        
        # Calculate shake offset
        offset_x = self.shake_offset_x
        offset_y = self.shake_offset_y
        
        # Draw platforms with shake offset
        for platform in self.platforms:
            screen.blit(platform.image, (platform.rect.x + offset_x, platform.rect.y + offset_y))
        
        # Draw exit with shake offset
        screen.blit(self.exit.image, (self.exit.rect.x + offset_x, self.exit.rect.y + offset_y))
        
        # Draw enemies with shake offset
        for enemy in self.enemies:
            enemy.draw(screen, offset_x, offset_y)
        
        # Apply advanced glitch effects (level 5)
        if self.advanced_glitches:
            self.apply_glitch_effect(screen)
