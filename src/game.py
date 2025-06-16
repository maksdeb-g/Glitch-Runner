import pygame
import os
import time
from src.player import Player
from src.level import Level
from src.glitch_engine import GlitchEngine
from src.level_data import LEVELS
from src.sound_manager import SoundManager
from src.constants import *

class Game:
    def __init__(self):
        # Set up the display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Glitch Runner")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Game state
        self.running = True
        self.game_state = "menu"  # menu, playing, game_over, level_complete
        self.current_level_index = 0
        self.lives = 0  # Will be set based on level data
        self.max_lives = 0  # Maximum lives for current level
        self.score = 0
        self.level_start_time = 0
        
        # Create player
        self.player = Player()
        
        # Load levels
        self.levels = []
        for level_data in LEVELS:
            self.levels.append(Level(level_data))
        
        # Set current level
        self.current_level = self.levels[self.current_level_index]
        
        # Create glitch engine
        self.glitch_engine = GlitchEngine(self)
        
        # Initialize font for text
        pygame.font.init()
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 48)
        
        # Create asset directories if they don't exist
        self.create_asset_directories()
        
        # Create a render surface for post-processing
        self.render_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Game over timer
        self.game_over_timer = 0
        self.level_complete_timer = 0
        
        # Start background music
        self.sound_manager.play_music('background')
        
    def create_asset_directories(self):
        # Create asset directories
        directories = [
            os.path.join('assets', 'images', 'player'),
            os.path.join('assets', 'sounds'),
            os.path.join('assets', 'fonts')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def reset_level(self, reset_lives=True):
        # Reset player position
        self.current_level.reset_player_position(self.player)
        self.level_start_time = time.time()
        
        # Set lives based on current level, but only if reset_lives is True
        if reset_lives:
            level_data = LEVELS[self.current_level_index]
            self.max_lives = level_data.get("lives", 3)  # Default to 3 if not specified
            self.lives = self.max_lives
    
    def next_level(self):
        self.current_level_index += 1
        if self.current_level_index < len(self.levels):
            self.current_level = self.levels[self.current_level_index]
            self.reset_level(reset_lives=True)  # Reset lives for new level
            self.game_state = "playing"
        else:
            # Game completed
            self.game_state = "game_completed"
            self.sound_manager.play_sound('game_completed')
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Toggle debug mode with F3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
                global DEBUG_MODE
                DEBUG_MODE = not DEBUG_MODE
            
            # Menu controls
            if self.game_state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.game_state = "playing"
                    self.reset_level(reset_lives=True)  # Reset lives when starting from menu
                    self.sound_manager.play_sound('level_complete')
            
            # Game over / level complete controls
            elif self.game_state in ["game_over", "level_complete", "game_completed"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    if self.game_state == "game_over":
                        if self.lives > 0:
                            self.game_state = "playing"
                            self.reset_level(reset_lives=False)  # Don't reset lives when continuing
                        else:
                            self.game_state = "menu"
                            self.score = 0
                            self.current_level_index = 0
                            self.current_level = self.levels[self.current_level_index]
                            self.reset_level()
                    elif self.game_state == "level_complete":
                        self.next_level()
                    elif self.game_state == "game_completed":
                        self.game_state = "menu"
                        self.score = 0
                        self.current_level_index = 0
                        self.current_level = self.levels[self.current_level_index]
                        self.reset_level()
            
            # Playing controls
            elif self.game_state == "playing":
                # Process event through glitch engine for input lag
                processed_event = self.glitch_engine.process_input(event)
                if processed_event:
                    # Handle player input
                    self.player.handle_event(processed_event)
        
        # Process any lagged inputs
        if self.game_state == "playing":
            lagged_events = self.glitch_engine.get_lagged_input()
            for event in lagged_events:
                self.player.handle_event(event)
    
    def update(self):
        if self.game_state == "playing":
            # Update glitch engine
            self.glitch_engine.update()
            
            # Update current level (which updates player and enemies)
            self.current_level.update(self.player)
            
            # Check for level exit collision
            if self.current_level.check_exit_collision(self.player):
                self.game_state = "level_complete"
                self.level_complete_timer = time.time()
                self.score += 1000  # Base score for completing level
                self.sound_manager.play_sound('level_complete')
                
                # Bonus for speed
                time_bonus = max(0, 60 - int(time.time() - self.level_start_time)) * 10
                self.score += time_bonus
            
            
            # Check for enemy collision
            if self.current_level.check_enemy_collision(self.player):
                self.lives -= 1
                self.game_state = "game_over"
                self.game_over_timer = time.time()
                
                # Play different sounds based on lives remaining
                if self.lives <= 0:
                    self.sound_manager.play_sound('final_death')
                else:
                    self.sound_manager.play_sound('game_over')
            
            # Check if player fell off the level
            if self.player.rect.top > SCREEN_HEIGHT:
                self.lives -= 1
                self.game_state = "game_over"
                self.game_over_timer = time.time()
                
                # Play different sounds based on lives remaining
                if self.lives <= 0:
                    self.sound_manager.play_sound('final_death')
                else:
                    self.sound_manager.play_sound('game_over')
        
        # Handle timers for game states
        current_time = time.time()
        
        if self.game_state == "game_over" and current_time - self.game_over_timer > 2:
            if self.lives > 0:
                self.game_state = "playing"
                self.reset_level(reset_lives=False)  # Don't reset lives when continuing after death
        
        if self.game_state == "level_complete" and current_time - self.level_complete_timer > 2:
            self.next_level()
    
    def render_menu(self):
        # Clear the screen
        self.screen.fill((0, 0, 0))
        
        # Draw title
        title_text = self.title_font.render("GLITCH RUNNER", True, GLITCH_COLOR)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Draw instructions
        instructions = [
            "Navigate through glitchy levels to reach the exit portal",
            "Watch out for enemies and random glitches!",
            "",
            "Controls:",
            "Arrow Keys: Move",
            "Space: Jump/Double Jump",
            "F3: Toggle Debug Mode",
            "",
            "Press ENTER to Start"
        ]
        
        for i, line in enumerate(instructions):
            text = self.font.render(line, True, (255, 255, 255))
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 200 + i * 30))
    
    def render_game_over(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text
        game_over_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        if self.lives > 0:
            # Draw lives remaining
            lives_text = self.font.render(f"Lives remaining: {self.lives}/{self.max_lives}", True, (255, 255, 255))
            self.screen.blit(lives_text, (SCREEN_WIDTH // 2 - lives_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            # Draw continue text
            continue_text = self.font.render("Continuing...", True, (255, 255, 255))
            self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
        else:
            # Draw game over message
            message_text = self.font.render("Press ENTER to return to menu", True, (255, 255, 255))
            self.screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    
    def render_level_complete(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw level complete text
        level_complete_text = self.title_font.render("LEVEL COMPLETE!", True, (0, 255, 0))
        self.screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        # Draw continue text
        continue_text = self.font.render("Continuing to next level...", True, (255, 255, 255))
        self.screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    
    def render_game_completed(self):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game completed text
        completed_text = self.title_font.render("GAME COMPLETED!", True, (0, 255, 255))
        self.screen.blit(completed_text, (SCREEN_WIDTH // 2 - completed_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
        
        # Draw final score
        score_text = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        
        # Draw return to menu text
        menu_text = self.font.render("Press ENTER to return to menu", True, (255, 255, 255))
        self.screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
    
    def render_playing(self):
        # Clear the render surface with the level background color
        self.render_surface.fill((0, 0, 0))  # Black background for the procedural background
        
        # Only draw sprites if not flickering
        if self.glitch_engine.flicker_state:
            # Draw level
            self.current_level.draw(self.render_surface)
            
            # Draw player
            self.player.draw(self.render_surface)
        
        # Apply glitch effects to the render surface
        self.glitch_engine.apply_screen_effects(self.render_surface)
        
        # Copy the processed render surface to the screen
        self.screen.blit(self.render_surface, (0, 0))
        
        # Draw HUD (not affected by glitches)
        self.render_hud()
    
    def render_hud(self):
        # Draw level name
        level_text = self.font.render(f"Level {self.current_level_index + 1}: {self.current_level.name}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 10))
        
        # Draw lives
        lives_text = self.font.render(f"Lives: {self.lives}/{self.max_lives}", True, (255, 255, 255))
        self.screen.blit(lives_text, (10, 40))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 70))
        
        # Draw active glitches
        if self.glitch_engine.active_glitches:
            active_glitches = [g['effect'].__name__.replace('_', ' ').upper() for g in self.glitch_engine.active_glitches]
            glitch_text = self.font.render(f"Active Glitches: {', '.join(active_glitches)}", True, GLITCH_COLOR)
            self.screen.blit(glitch_text, (10, SCREEN_HEIGHT - 30))
        
        # Draw debug info
        if DEBUG_MODE:
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
            self.screen.blit(fps_text, (SCREEN_WIDTH - 100, 10))
            
            # Draw controls help
            controls = [
                "Controls:",
                "Arrow Keys: Move",
                "Space: Jump/Double Jump",
                "Wall Slide: Touch wall while falling",
                "F3: Toggle Debug Mode"
            ]
            
            for i, text in enumerate(controls):
                help_text = self.font.render(text, True, (255, 255, 255))
                self.screen.blit(help_text, (SCREEN_WIDTH - 250, 40 + i * 20))
    
    def render(self):
        if self.game_state == "menu":
            self.render_menu()
        elif self.game_state == "playing":
            self.render_playing()
        elif self.game_state == "game_over":
            self.render_playing()  # Draw the game in the background
            self.render_game_over()
        elif self.game_state == "level_complete":
            self.render_playing()  # Draw the game in the background
            self.render_level_complete()
        elif self.game_state == "game_completed":
            self.render_playing()  # Draw the game in the background
            self.render_game_completed()
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        # Game loop
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
