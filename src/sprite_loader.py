import pygame
import os
from src.constants import *

class SpriteLoader:
    """Helper class to load and process sprite sheets"""
    
    @staticmethod
    def load_spritesheet(filename, frame_width, frame_height, num_frames):
        """Load a spritesheet and split it into individual frames"""
        try:
            # Try to load the spritesheet
            spritesheet = pygame.image.load(filename).convert_alpha()
            
            # Create a list to store individual frames
            frames = []
            
            # Extract each frame from the spritesheet
            for i in range(num_frames):
                # Calculate the position of the frame in the spritesheet
                x = i * frame_width
                y = 0
                
                # Create a new surface for the frame
                frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                
                # Copy the frame from the spritesheet
                frame.blit(spritesheet, (0, 0), (x, y, frame_width, frame_height))
                
                # Add the frame to the list
                frames.append(frame)
            
            return frames
        except pygame.error as e:
            print(f"Error loading spritesheet {filename}: {e}")
            return None
    
    @staticmethod
    def load_player_sprites():
        """Load all player sprites from the assets directory"""
        sprites = {
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
        
        # Check for Pink Monster sprites in the sprites directory
        pink_monster_path = os.path.join('assets', 'sprites', '1 Pink_Monster')
        
        # Define sprite mappings
        sprite_files = {
            'idle': ('Pink_Monster_Idle_4.png', 4),
            'run': ('Pink_Monster_Run_6.png', 6),
            'jump': ('Pink_Monster_Jump_8.png', 8),
            'walk': ('Pink_Monster_Walk_6.png', 6),
        }
        
        # Try to load sprites from the Pink Monster directory
        if os.path.exists(pink_monster_path):
            # Get the first sprite to determine dimensions
            first_sprite_path = os.path.join(pink_monster_path, 'Pink_Monster.png')
            try:
                first_sprite = pygame.image.load(first_sprite_path).convert_alpha()
                sprite_width = first_sprite.get_width()
                sprite_height = first_sprite.get_height()
                
                # Load each sprite sheet
                for sprite_type, (filename, num_frames) in sprite_files.items():
                    sprite_path = os.path.join(pink_monster_path, filename)
                    if os.path.exists(sprite_path):
                        # Load the spritesheet
                        frames = SpriteLoader.load_spritesheet(
                            sprite_path, 
                            sprite_width, 
                            sprite_height, 
                            num_frames
                        )
                        
                        if frames:
                            # Map to appropriate animation states
                            if sprite_type == 'idle':
                                sprites['idle_right'] = frames
                                # Create flipped versions for left-facing animations
                                sprites['idle_left'] = [pygame.transform.flip(frame, True, False) for frame in frames]
                            
                            elif sprite_type == 'run':
                                sprites['run_right'] = frames
                                sprites['run_left'] = [pygame.transform.flip(frame, True, False) for frame in frames]
                            
                            elif sprite_type == 'walk':
                                # Use walk animation as fallback for wall slide
                                sprites['wall_slide_right'] = frames
                                sprites['wall_slide_left'] = [pygame.transform.flip(frame, True, False) for frame in frames]
                            
                            elif sprite_type == 'jump':
                                # Use first half of jump animation for jump
                                half = num_frames // 2
                                sprites['jump_right'] = frames[:half]
                                sprites['jump_left'] = [pygame.transform.flip(frame, True, False) for frame in frames[:half]]
                                
                                # Use second half of jump animation for fall
                                sprites['fall_right'] = frames[half:]
                                sprites['fall_left'] = [pygame.transform.flip(frame, True, False) for frame in frames[half:]]
                
                # Scale sprites to match player size
                for state in sprites:
                    sprites[state] = [pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT)) 
                                     for frame in sprites[state]]
                
                print("Successfully loaded Pink Monster sprites")
                return sprites
            
            except pygame.error as e:
                print(f"Error loading Pink Monster sprites: {e}")
        
        # If we get here, either the sprites don't exist or there was an error loading them
        # Create placeholder sprites
        print("Using placeholder sprites")
        return SpriteLoader.create_placeholder_sprites()
    
    @staticmethod
    def create_placeholder_sprites():
        """Create placeholder sprites if actual sprites can't be loaded"""
        sprites = {
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
        
        # Create 4 frames for each animation state
        for state in sprites:
            for i in range(4):
                # Create a surface for the frame
                frame = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
                
                # Different colors for different states
                if 'idle' in state:
                    frame.fill(PLAYER_COLOR)
                elif 'run' in state:
                    frame.fill((0, 200, 0))
                elif 'jump' in state:
                    frame.fill((0, 255, 100))
                elif 'fall' in state:
                    frame.fill((0, 150, 0))
                elif 'wall_slide' in state:
                    frame.fill((0, 100, 0))
                
                # Add a visual indicator for direction
                if 'right' in state:
                    pygame.draw.rect(frame, (255, 255, 255), (PLAYER_WIDTH - 10, 10, 5, 5))
                else:
                    pygame.draw.rect(frame, (255, 255, 255), (5, 10, 5, 5))
                
                # Add animation frame indicator
                pygame.draw.rect(frame, (255, 255, 255), (10 + i*5, PLAYER_HEIGHT - 10, 5, 5))
                
                # Add the frame to the list
                sprites[state].append(frame)
        
        return sprites
