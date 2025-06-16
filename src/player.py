import pygame
import os
import time
from src.constants import *
from src.sprite_loader import SpriteLoader

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        # Animation frames
        self.sprites = {
            'idle_right': [],
            'idle_left': [],
            'run_right': [],
            'run_left': [],
            'jump_right': [],
            'jump_left': [],
            'fall_right': [],
            'fall_left': [],
            'wall_slide_right': [],
            'wall_slide_left': []
        }
        
        # Load sprites using the sprite loader
        self.sprites = SpriteLoader.load_player_sprites()
        
        # Animation state
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.current_state = 'idle_right'
        self.image = self.sprites[self.current_state][0]
        self.rect = self.image.get_rect()
        
        # Set initial position
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 100
        
        # Movement variables
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        
        # Advanced movement mechanics
        self.jump_count = 0
        self.max_jumps = 2  # Double jump
        self.jump_held = False
        self.jump_time = 0
        self.max_jump_time = 15  # Frames for variable jump height
        self.wall_sliding = False
        
        # Invincibility
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 2  # 2 seconds of invincibility when spawning
        self.wall_slide_speed = 1
        self.wall_jump_power = 10
        
        # Physics properties (can be modified by glitches)
        self.gravity = GRAVITY
        self.ceiling_enabled = False  # For reversed gravity
        self.speed = PLAYER_SPEED
        self.jump_power = JUMP_POWER
        
        # Sound effects
        self.load_sounds()
    
    def load_sounds(self):
        # Initialize sound effects
        self.jump_sound = None
        self.land_sound = None
        self.wall_slide_sound = None
        self.double_jump_sound = None
        
        # Try to load sounds if they exist
        try:
            pygame.mixer.init()
            
            # Import resource_path function
            try:
                # First try to import from the module
                from resource_path import resource_path
            except ImportError:
                # Define it locally if import fails
                def resource_path(relative_path):
                    try:
                        base_path = sys._MEIPASS
                    except Exception:
                        base_path = os.path.abspath(".")
                    return os.path.join(base_path, relative_path)
            
            # Try multiple possible paths for the jump sound
            possible_paths = [
                resource_path(os.path.join('assets', 'sounds', 'jump-audio.mp3')),
                resource_path(os.path.join('assets', 'sounds', 'jump-audio.wav')),
                resource_path(os.path.join('assets', 'sounds', 'jump.mp3')),
                resource_path(os.path.join('assets', 'sounds', 'jump.wav')),
                os.path.join('assets', 'sounds', 'jump-audio.mp3'),
                os.path.join('assets', 'sounds', 'jump-audio.wav')
            ]
            
            # Try each path until we find a valid sound file
            for path in possible_paths:
                try:
                    if os.path.exists(path):
                        self.jump_sound = pygame.mixer.Sound(path)
                        self.double_jump_sound = self.jump_sound  # Use same sound for double jump
                        print(f"Successfully loaded jump sound from: {path}")
                        break
                except Exception as e:
                    print(f"Failed to load sound from {path}: {e}")
            
            if self.jump_sound is None:
                print("Could not find any jump sound files")
                
        except Exception as e:
            print(f"Sound files could not be loaded: {e}. Continuing without sound.")
    
    def handle_event(self, event):
        # Handle key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.velocity_x = -self.speed
                self.facing_right = False
            if event.key == pygame.K_RIGHT:
                self.velocity_x = self.speed
                self.facing_right = True
            if event.key == pygame.K_SPACE:
                self.handle_jump_press()
        
        # Handle key release events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and self.velocity_x < 0:
                self.velocity_x = 0
            if event.key == pygame.K_RIGHT and self.velocity_x > 0:
                self.velocity_x = 0
            if event.key == pygame.K_SPACE:
                self.jump_held = False
    
    def handle_input(self):
        """Handle continuous keyboard input"""
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.velocity_x = -self.speed
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.velocity_x = self.speed
            self.facing_right = True
        else:
            self.velocity_x = 0
            
        # Variable jump height when holding jump button
        if keys[pygame.K_SPACE] and self.jump_held and self.jump_time < self.max_jump_time and self.velocity_y < 0:
            self.velocity_y -= 0.5  # Continue pushing up while jump is held
            self.jump_time += 1
    
    def handle_jump_press(self):
        # First jump when on ground
        if self.on_ground:
            self.jump()
            self.jump_held = True
            self.jump_time = 0
            self.jump_count = 1
            if self.jump_sound:
                self.jump_sound.play()
        # Wall jump
        elif self.wall_sliding:
            self.wall_jump()
            self.jump_held = True
            self.jump_time = 0
            if self.jump_sound:
                self.jump_sound.play()
        # Double jump in air
        elif self.jump_count < self.max_jumps:
            self.jump()
            self.jump_held = True
            self.jump_time = 0
            self.jump_count += 1
            if self.double_jump_sound:
                self.double_jump_sound.play()
    
    def jump(self):
        self.velocity_y = -self.jump_power
        self.on_ground = False
        self.wall_sliding = False
    
    def wall_jump(self):
        # Jump away from wall
        if self.facing_right:
            self.velocity_x = -self.wall_jump_power
            self.velocity_y = -self.jump_power
        else:
            self.velocity_x = self.wall_jump_power
            self.velocity_y = -self.jump_power
        
        self.wall_sliding = False
        self.on_ground = False
    
    def apply_gravity(self):
        if not self.on_ground:
            if self.wall_sliding:
                self.velocity_y += self.gravity * 0.5  # Reduced gravity when wall sliding
                if self.velocity_y > self.wall_slide_speed:
                    self.velocity_y = self.wall_slide_speed
            else:
                self.velocity_y += self.gravity
                # Terminal velocity
                if self.velocity_y > MAX_FALL_SPEED:
                    self.velocity_y = MAX_FALL_SPEED
    
    def check_wall_slide(self, platforms):
        # Check if player is touching a wall and not on ground
        if not self.on_ground and self.velocity_y > 0:
            # Create a rect slightly wider than the player to detect walls
            wall_check_rect = self.rect.inflate(4, 0)
            
            for platform in platforms:
                # Check left side
                if self.velocity_x < 0 and wall_check_rect.left <= platform.rect.right and wall_check_rect.right > platform.rect.right:
                    if wall_check_rect.bottom > platform.rect.top and wall_check_rect.top < platform.rect.bottom:
                        self.wall_sliding = True
                        self.facing_right = True  # Facing away from wall
                        if self.wall_slide_sound and not pygame.mixer.get_busy():
                            self.wall_slide_sound.play()
                        return
                
                # Check right side
                if self.velocity_x > 0 and wall_check_rect.right >= platform.rect.left and wall_check_rect.left < platform.rect.left:
                    if wall_check_rect.bottom > platform.rect.top and wall_check_rect.top < platform.rect.bottom:
                        self.wall_sliding = True
                        self.facing_right = False  # Facing away from wall
                        if self.wall_slide_sound and not pygame.mixer.get_busy():
                            self.wall_slide_sound.play()
                        return
            
            # If we get here, not touching any walls
            self.wall_sliding = False
    
    def update_animation(self):
        # Determine animation state based on movement
        if self.on_ground:
            if self.velocity_x == 0:
                state = 'idle_right' if self.facing_right else 'idle_left'
            else:
                state = 'run_right' if self.facing_right else 'run_left'
        else:
            if self.wall_sliding:
                state = 'wall_slide_right' if self.facing_right else 'wall_slide_left'
            elif self.velocity_y < 0:
                state = 'jump_right' if self.facing_right else 'jump_left'
            else:
                state = 'fall_right' if self.facing_right else 'fall_left'
        
        # Update animation state
        if state != self.current_state:
            self.current_state = state
            self.current_sprite = 0
        
        # Advance animation frame
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.sprites[self.current_state]):
            self.current_sprite = 0
        
        # Update image
        self.image = self.sprites[self.current_state][int(self.current_sprite)]
    
    def check_collisions(self, platforms):
        # Check for platform collisions
        was_on_ground = self.on_ground
        self.on_ground = False
        
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Landing on top of a platform
                if self.velocity_y > 0 and self.rect.bottom - self.velocity_y <= platform.rect.top + 10:
                    self.rect.bottom = platform.rect.top
                    self.velocity_y = 0
                    self.on_ground = True
                    self.jump_count = 0  # Reset jump count when landing
                    
                    # Play landing sound if we just landed
                    if not was_on_ground and self.land_sound:
                        self.land_sound.play()
                
                # Hitting a platform from below
                elif self.velocity_y < 0 and self.rect.top - self.velocity_y >= platform.rect.bottom - 10:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0
                
                # Side collision
                elif self.velocity_x > 0 and self.rect.right - self.velocity_x <= platform.rect.left + 10:
                    self.rect.right = platform.rect.left
                    self.velocity_x = 0
                elif self.velocity_x < 0 and self.rect.left - self.velocity_x >= platform.rect.right - 10:
                    self.rect.left = platform.rect.right
                    self.velocity_x = 0
    
    def update(self, platforms=None):
        # Handle continuous input
        self.handle_input()
        
        # Update invincibility timer
        if self.invincible:
            current_time = time.time()
            if current_time - self.invincible_timer > self.invincible_duration:
                self.invincible = False
        
        # Apply gravity
        self.apply_gravity()
        
        # Check for wall sliding
        if platforms:
            self.check_wall_slide(platforms)
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check collisions with platforms
        if platforms:
            self.check_collisions(platforms)
        
        # Keep player on screen (temporary boundary check)
        if self.rect.left < 0:
            self.rect.left = 0
            # Enable wall sliding on screen edges
            if self.velocity_y > 0 and not self.on_ground:
                self.wall_sliding = True
                self.facing_right = True
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            # Enable wall sliding on screen edges
            if self.velocity_y > 0 and not self.on_ground:
                self.wall_sliding = True
                self.facing_right = False
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
            self.jump_count = 0
        # Add ceiling check for reversed gravity
        if self.ceiling_enabled and self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
        
        # Update animation
        self.update_animation()
    
    def set_invincible(self):
        self.invincible = True
        self.invincible_timer = time.time()
    
    def draw(self, screen):
        # If invincible, make the player flash
        if self.invincible and int(time.time() * 10) % 2 == 0:
            # Create a white flash effect
            flash_image = self.image.copy()
            flash_image.fill((255, 255, 255, 128), None, pygame.BLEND_RGBA_MULT)
            screen.blit(flash_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        # Debug visualization
        if DEBUG_MODE:
            # Draw bounding box
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 1)
            
            # Draw state text
            font = pygame.font.SysFont(None, 24)
            state_text = font.render(f"State: {self.current_state}", True, (255, 255, 255))
            jumps_text = font.render(f"Jumps: {self.jump_count}/{self.max_jumps}", True, (255, 255, 255))
            ground_text = font.render(f"On Ground: {self.on_ground}", True, (255, 255, 255))
            wall_text = font.render(f"Wall Slide: {self.wall_sliding}", True, (255, 255, 255))
            
            screen.blit(state_text, (self.rect.x, self.rect.y - 60))
            screen.blit(jumps_text, (self.rect.x, self.rect.y - 40))
            screen.blit(ground_text, (self.rect.x, self.rect.y - 20))
            screen.blit(wall_text, (self.rect.x, self.rect.y - 80))
