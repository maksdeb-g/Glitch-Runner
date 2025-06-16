import pygame
import os
import sys

# Try to import the resource_path function
try:
    from resource_path import resource_path
except ImportError:
    # If not available, define it here
    def resource_path(relative_path):
        """Get absolute path to resource, works for dev and for PyInstaller"""
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        
        return os.path.join(base_path, relative_path)

class SpriteLoader:
    """Utility class for loading and managing sprites"""
    
    @staticmethod
    def load_player_sprites():
        """Load player sprites from assets directory"""
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
        
        # Try to load sprites from assets directory
        try:
            # Check if player sprites directory exists
            player_dir = resource_path(os.path.join('assets', 'images', 'player'))
            print(f"Looking for player sprites in: {player_dir}")
            
            if os.path.exists(player_dir):
                print(f"Player directory exists: {player_dir}")
                # List all files in the directory to debug
                try:
                    files = os.listdir(player_dir)
                    print(f"Files in player directory: {files}")
                except Exception as e:
                    print(f"Error listing directory: {e}")
                
                # Load sprites from files
                SpriteLoader._load_sprites_from_directory(sprites, player_dir)
            else:
                print(f"Player directory does not exist: {player_dir}")
                # Create placeholder sprites
                SpriteLoader._create_placeholder_sprites(sprites)
                
        except Exception as e:
            print(f"Error loading player sprites: {e}")
            # Create placeholder sprites as fallback
            SpriteLoader._create_placeholder_sprites(sprites)
        
        # Verify that sprites were loaded
        for key, frames in sprites.items():
            print(f"Sprite {key}: {len(frames)} frames")
            
        return sprites
    
    @staticmethod
    def _load_sprites_from_directory(sprites, directory):
        """Load sprites from files in the given directory"""

        # For each animation type, look for sprite sheets or individual frames
        sprite_files = {
            'idle': 'Pink_Monster_Idle_4.png',
            'run': 'Pink_Monster_Run_6.png',
            'jump': 'Pink_Monster_Jump_8.png',
            'fall': 'Pink_Monster_Jump_8.png',  # Use jump for fall animation
            'wall_slide': 'Pink_Monster_Climb_4.png'  # Use climb for wall slide
        }

        # Try to load each sprite type
        for anim_type, filename in sprite_files.items():
            full_path = os.path.join(directory, filename)
            print(f"Checking for sprite file: {full_path}")
            
            if os.path.exists(full_path):
                print(f"Loading sprite file: {full_path}")
                try:
                    # Load the sprite sheet
                    sprite_sheet = pygame.image.load(full_path).convert_alpha()

                    # Get frame count from filename (e.g., "Pink_Monster_Run_6.png" has 6 frames)
                    frame_count = int(filename.split('_')[-1].split('.')[0])

                    # Calculate frame width
                    frame_width = sprite_sheet.get_width() // frame_count
                    frame_height = sprite_sheet.get_height()

                    # Extract individual frames
                    frames = []
                    for i in range(frame_count):
                        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                        frame.blit(sprite_sheet, (0, 0), (i * frame_width, 0, frame_width, frame_height))
                        frames.append(frame)

                    # Assign frames to appropriate animation states
                    sprites[f'{anim_type}_right'] = frames
                    # Create flipped versions for left-facing animations
                    sprites[f'{anim_type}_left'] = [pygame.transform.flip(frame, True, False) for frame in frames]
                    
                    print(f"Successfully loaded {len(frames)} frames for {anim_type}")
                except Exception as e:
                    print(f"Error loading sprite {filename}: {e}")
            else:
                print(f"Sprite file not found: {full_path}")
    @staticmethod
    def _create_placeholder_sprites(sprites):
        """Create placeholder sprites when assets are not available"""
        from src.constants import PLAYER_WIDTH, PLAYER_HEIGHT
        
        # Create a simple rectangle for the player
        right_sprite = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT), pygame.SRCALPHA)
        right_sprite.fill((0, 255, 0))  # Green rectangle
        
        # Add some details to distinguish different states
        pygame.draw.rect(right_sprite, (0, 200, 0), (0, 0, PLAYER_WIDTH, PLAYER_HEIGHT), 2)
        pygame.draw.line(right_sprite, (0, 200, 0), (0, 0), (PLAYER_WIDTH, PLAYER_HEIGHT), 2)
        pygame.draw.line(right_sprite, (0, 200, 0), (0, PLAYER_HEIGHT), (PLAYER_WIDTH, 0), 2)
        
        # Create left-facing sprite by flipping the right one
        left_sprite = pygame.transform.flip(right_sprite, True, False)
        
        # Create variations for different states
        jump_right = right_sprite.copy()
        pygame.draw.polygon(jump_right, (0, 200, 0), [(0, PLAYER_HEIGHT), (PLAYER_WIDTH//2, PLAYER_HEIGHT//2), (PLAYER_WIDTH, PLAYER_HEIGHT)], 2)
        jump_left = pygame.transform.flip(jump_right, True, False)
        
        run_right = right_sprite.copy()
        pygame.draw.rect(run_right, (0, 200, 0), (PLAYER_WIDTH//4, PLAYER_HEIGHT//4, PLAYER_WIDTH//2, PLAYER_HEIGHT//2), 2)
        run_left = pygame.transform.flip(run_right, True, False)
        
        # Assign sprites to each animation state
        sprites['idle_right'] = [right_sprite]
        sprites['idle_left'] = [left_sprite]
        sprites['run_right'] = [run_right]
        sprites['run_left'] = [run_left]
        sprites['jump_right'] = [jump_right]
        sprites['jump_left'] = [jump_left]
        sprites['fall_right'] = [jump_right]
        sprites['fall_left'] = [jump_left]
        sprites['wall_slide_right'] = [right_sprite]
        sprites['wall_slide_left'] = [left_sprite]
