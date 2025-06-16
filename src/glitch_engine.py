import pygame
import random
import time
from src.constants import *

class GlitchEngine:
    def __init__(self, game):
        self.game = game
        self.active_glitches = []
        self.glitch_timer = 0
        self.glitch_interval = GLITCH_INTERVAL
        self.glitch_duration = GLITCH_DURATION
        self.last_glitch_time = time.time()
        self.notification_text = ""
        self.notification_time = 0
        
        # Available glitch effects
        self.glitch_effects = [
            self.reversed_gravity,
            self.flickering_sprites,
            self.input_lag,
            self.color_distortion,
            self.screen_shake,
            self.platform_disappear,
            self.speed_change,
            self.pixelation
        ]
        
        # Glitch state variables
        self.original_gravity = GRAVITY
        self.input_buffer = []
        self.input_lag_frames = 0
        self.flicker_state = True
        self.flicker_timer = 0
        self.color_shift = (0, 0, 0)
        self.shake_amount = 0
        self.screen_offset = (0, 0)
        self.rotation_angle = 0
        self.pixel_size = 1
        self.speed_multiplier = 1.0
        self.disappearing_platforms = []
        
        # Surface for post-processing effects
        self.screen_surface = None
    
    def update(self):
        current_time = time.time()
        
        # Check if it's time for a new glitch
        if current_time - self.last_glitch_time > self.glitch_interval:
            self.trigger_random_glitch()
            self.last_glitch_time = current_time
            
            # Play glitch sound if available
            if hasattr(self.game, 'sound_manager'):
                self.game.sound_manager.play_sound('glitch')
        
        # Update active glitches
        for glitch in self.active_glitches[:]:
            if current_time - glitch['start_time'] > self.glitch_duration:
                self.end_glitch(glitch)
                self.active_glitches.remove(glitch)
            else:
                # Update glitch effects
                if glitch['effect'].__name__ == 'flickering_sprites':
                    self.update_flickering()
                elif glitch['effect'].__name__ == 'screen_shake':
                    self.update_screen_shake()
                elif glitch['effect'].__name__ == 'platform_disappear':
                    self.update_disappearing_platforms()
    
    def trigger_random_glitch(self):
        # Choose a random glitch effect
        effect = random.choice(self.glitch_effects)
        
        # Start the glitch
        glitch = {
            'effect': effect,
            'start_time': time.time()
        }
        
        # Apply the glitch effect
        effect(True)
        
        # Add to active glitches
        self.active_glitches.append(glitch)
        
        # Set notification
        self.notification_text = f"GLITCH: {effect.__name__.replace('_', ' ').upper()}"
        self.notification_time = time.time()
    
    def end_glitch(self, glitch):
        # Revert the glitch effect
        glitch['effect'](False)
    
    def reversed_gravity(self, activate):
        if activate:
            # Reverse gravity
            self.game.player.velocity_y = -self.game.player.velocity_y  # Immediate direction change
            self.game.player.gravity = -self.original_gravity
            # Set a ceiling boundary for reversed gravity
            self.game.player.ceiling_enabled = True
        else:
            # Restore normal gravity
            self.game.player.velocity_y = -self.game.player.velocity_y  # Immediate direction change
            self.game.player.gravity = self.original_gravity
            self.game.player.ceiling_enabled = False
    
    def flickering_sprites(self, activate):
        if activate:
            self.flicker_timer = 0
            self.flicker_state = True
        else:
            # Ensure sprites are visible when effect ends
            self.flicker_state = True
    
    def update_flickering(self):
        # Update flicker state every few frames
        self.flicker_timer += 1
        if self.flicker_timer >= 5:  # Adjust for flicker speed
            self.flicker_state = not self.flicker_state
            self.flicker_timer = 0
    
    def input_lag(self, activate):
        if activate:
            # Set random input lag between 5-15 frames
            self.input_lag_frames = random.randint(5, 15)
            self.input_buffer = []
        else:
            # Clear input lag
            self.input_lag_frames = 0
            self.input_buffer = []
    
    def process_input(self, event):
        # If input lag is active, buffer the input
        if self.input_lag_frames > 0:
            self.input_buffer.append((pygame.time.get_ticks(), event))
            return None
        return event
    
    def get_lagged_input(self):
        current_time = pygame.time.get_ticks()
        result = []
        
        # Process buffered inputs that have waited long enough
        for timestamp, event in self.input_buffer[:]:
            if current_time - timestamp >= self.input_lag_frames * (1000 / FPS):
                result.append(event)
                self.input_buffer.remove((timestamp, event))
        
        return result
    
    def color_distortion(self, activate):
        if activate:
            # Random color shift
            self.color_shift = (
                random.randint(-100, 100),
                random.randint(-100, 100),
                random.randint(-100, 100)
            )
        else:
            # Reset color
            self.color_shift = (0, 0, 0)
    
    def screen_shake(self, activate):
        if activate:
            self.shake_amount = random.randint(5, 15)
        else:
            self.shake_amount = 0
            self.screen_offset = (0, 0)
    
    def update_screen_shake(self):
        if self.shake_amount > 0:
            self.screen_offset = (
                random.randint(-self.shake_amount, self.shake_amount),
                random.randint(-self.shake_amount, self.shake_amount)
            )
    
    def pixelation(self, activate):
        if activate:
            self.pixel_size = random.choice([2, 3, 4, 6, 8])
        else:
            self.pixel_size = 1
    
    def speed_change(self, activate):
        if activate:
            # Random speed multiplier between 0.5 and 2.0
            self.speed_multiplier = random.uniform(0.5, 2.0)
            self.game.player.speed = PLAYER_SPEED * self.speed_multiplier
        else:
            # Reset speed
            self.game.player.speed = PLAYER_SPEED
            self.speed_multiplier = 1.0
    
    def platform_disappear(self, activate):
        if activate:
            # Select random platforms to disappear
            if hasattr(self.game, 'current_level'):
                all_platforms = list(self.game.current_level.platforms.sprites())
                # Don't make the ground platform disappear
                potential_platforms = [p for p in all_platforms if p.rect.y < SCREEN_HEIGHT - 100]
                
                if potential_platforms:
                    # Choose 1-3 platforms to disappear
                    num_to_disappear = min(len(potential_platforms), random.randint(1, 3))
                    self.disappearing_platforms = random.sample(potential_platforms, num_to_disappear)
                    
                    # Set initial alpha
                    for platform in self.disappearing_platforms:
                        platform.original_image = platform.image.copy()
                        platform.alpha = 255
                        platform.disappearing = True
        else:
            # Restore all platforms
            for platform in self.disappearing_platforms:
                if hasattr(platform, 'original_image'):
                    platform.image = platform.original_image
                    platform.disappearing = False
                    platform.solid = True
                    platform.alpha = 255
            self.disappearing_platforms = []
    
    def update_disappearing_platforms(self):
        # Gradually make platforms transparent
        for platform in self.disappearing_platforms:
            if hasattr(platform, 'disappearing') and platform.disappearing:
                platform.alpha = max(0, platform.alpha - 5)
                
                # Create a transparent version of the original image
                platform.image = platform.original_image.copy()
                platform.image.set_alpha(platform.alpha)
                
                # When fully transparent, disable collisions
                if platform.alpha <= 0:
                    platform.solid = False
                else:
                    platform.solid = True
    
    def apply_screen_effects(self, screen):
        # Create a copy of the screen if needed
        if self.screen_surface is None or self.screen_surface.get_size() != screen.get_size():
            self.screen_surface = pygame.Surface(screen.get_size())
        
        # Copy the current screen
        self.screen_surface.blit(screen, (0, 0))
        
        # Apply color distortion
        if self.color_shift != (0, 0, 0):
            # Simple color shift by drawing a semi-transparent overlay
            overlay = pygame.Surface(screen.get_size())
            r = max(0, min(255, 128 + self.color_shift[0]))
            g = max(0, min(255, 128 + self.color_shift[1]))
            b = max(0, min(255, 128 + self.color_shift[2]))
            overlay.fill((r, g, b))
            overlay.set_alpha(50)  # Semi-transparent
            screen.blit(overlay, (0, 0))
        
        # Apply screen shake
        if self.shake_amount > 0:
            temp_surface = pygame.Surface(screen.get_size())
            temp_surface.fill((0, 0, 0))  # Fill with black
            temp_surface.blit(self.screen_surface, self.screen_offset)
            screen.blit(temp_surface, (0, 0))
        
        # Apply pixelation
        if self.pixel_size > 1:
            width, height = screen.get_size()
            
            # Scale down
            small_surface = pygame.transform.scale(
                screen, 
                (width // self.pixel_size, height // self.pixel_size)
            )
            
            # Scale back up (pixelated)
            pixelated = pygame.transform.scale(
                small_surface,
                (width, height)
            )
            
            # Replace screen content
            screen.blit(pixelated, (0, 0))
        
        # Draw glitch notification
        current_time = time.time()
        if current_time - self.notification_time < GLITCH_NOTIFICATION_TIME and self.notification_text:
            font = pygame.font.SysFont(None, 48)
            text_surface = font.render(self.notification_text, True, GLITCH_COLOR)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(text_surface, text_rect)
        
        return screen
