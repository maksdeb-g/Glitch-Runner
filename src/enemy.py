import pygame
import random
from src.constants import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance=100, enemy_type="basic"):
        super().__init__()
        
        self.enemy_type = enemy_type
        
        # Create enemy sprite
        self.image = pygame.Surface((ENEMY_WIDTH, ENEMY_HEIGHT))
        
        # Different colors/shapes for different enemy types
        if enemy_type == "basic":
            self.image.fill(ENEMY_COLOR)
        elif enemy_type == "jumper":
            self.image.fill((255, 100, 0))  # Orange
            # Add a triangle on top to indicate jumper
            pygame.draw.polygon(self.image, (255, 200, 0), [(0, 0), (ENEMY_WIDTH, 0), (ENEMY_WIDTH//2, -10)])
        elif enemy_type == "shooter":
            self.image.fill((150, 0, 0))  # Dark red
            # Add a circle to indicate shooter
            pygame.draw.circle(self.image, (255, 255, 0), (ENEMY_WIDTH//2, ENEMY_HEIGHT//2), 10)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement variables
        self.velocity_x = ENEMY_SPEED
        self.velocity_y = 0
        self.direction = 1  # 1 for right, -1 for left
        self.on_ground = False
        
        # Patrol behavior
        self.start_x = x
        self.patrol_distance = patrol_distance
        
        # Enemy-specific behavior
        self.jump_timer = 0
        self.shoot_timer = 0
        self.projectiles = pygame.sprite.Group()
        
        # Animation
        self.animation_frame = 0
        self.animation_speed = 0.1
    
    def update(self, platforms, player=None):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY
            if self.velocity_y > MAX_FALL_SPEED:
                self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check for collisions with platforms
        self.on_ground = False
        for platform in platforms:
            if platform.solid and self.rect.colliderect(platform.rect):
                # Landing on top of a platform
                if self.velocity_y > 0 and self.rect.bottom - self.velocity_y <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                # Hitting a platform from below
                elif self.velocity_y < 0 and self.rect.top - self.velocity_y >= platform.rect.bottom - 10:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                # Side collision - reverse direction
                elif self.velocity_x > 0:
                    self.rect.right = platform.rect.left
                    self.direction *= -1
                    self.velocity_x = ENEMY_SPEED * self.direction
                elif self.velocity_x < 0:
                    self.rect.left = platform.rect.right
                    self.direction *= -1
                    self.velocity_x = ENEMY_SPEED * self.direction
        
        # Patrol behavior - reverse direction at patrol limits
        if self.rect.x > self.start_x + self.patrol_distance:
            self.direction = -1
            self.velocity_x = ENEMY_SPEED * self.direction
        elif self.rect.x < self.start_x - self.patrol_distance:
            self.direction = 1
            self.velocity_x = ENEMY_SPEED * self.direction
        
        # Enemy-specific behavior
        if self.enemy_type == "jumper" and self.on_ground:
            self.jump_timer += 1
            if self.jump_timer >= 120:  # Jump every 2 seconds
                self.velocity_y = -JUMP_POWER * 0.7  # Jump not as high as player
                self.jump_timer = 0
        
        elif self.enemy_type == "shooter" and player:
            self.shoot_timer += 1
            if self.shoot_timer >= 180:  # Shoot every 3 seconds
                # Only shoot if player is in line of sight
                if abs(player.rect.y - self.rect.y) < 100:  # Within vertical range
                    # Determine direction to shoot
                    direction = 1 if player.rect.x > self.rect.x else -1
                    self.shoot(direction)
                    self.shoot_timer = 0
        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update()
            # Remove projectiles that go off screen
            if (projectile.rect.right < 0 or 
                projectile.rect.left > SCREEN_WIDTH or
                projectile.rect.bottom < 0 or
                projectile.rect.top > SCREEN_HEIGHT):
                projectile.kill()
        
        # Update animation
        self.animation_frame += self.animation_speed
        if self.animation_frame >= 4:  # Assuming 4 frames of animation
            self.animation_frame = 0
    
    def shoot(self, direction):
        projectile = Projectile(
            self.rect.centerx, 
            self.rect.centery, 
            direction
        )
        self.projectiles.add(projectile)
    
    def draw(self, screen, offset_x=0, offset_y=0):
        # Draw the enemy with screen shake offset
        screen.blit(self.image, (self.rect.x + offset_x, self.rect.y + offset_y))
        
        # Draw projectiles with screen shake offset
        for projectile in self.projectiles:
            screen.blit(projectile.image, (projectile.rect.x + offset_x, projectile.rect.y + offset_y))
        
        # Debug visualization
        if DEBUG_MODE:
            # Draw patrol range
            pygame.draw.line(
                screen, 
                (255, 0, 0), 
                (self.start_x - self.patrol_distance + offset_x, self.rect.bottom + 5 + offset_y),
                (self.start_x + self.patrol_distance + offset_x, self.rect.bottom + 5 + offset_y),
                1
            )
            
            # Draw enemy type
            font = pygame.font.SysFont(None, 20)
            type_text = font.render(self.enemy_type, True, (255, 255, 255))
            screen.blit(type_text, (self.rect.x + offset_x, self.rect.y - 20 + offset_y))


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        
        # Create projectile sprite
        self.image = pygame.Surface((10, 6))
        self.image.fill((255, 255, 0))  # Yellow projectile
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Movement
        self.speed = 7
        self.direction = direction
    
    def update(self):
        # Move the projectile
        self.rect.x += self.speed * self.direction
