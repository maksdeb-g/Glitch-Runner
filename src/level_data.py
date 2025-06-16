"""
Level data for Glitch Runner

Format:
Each level is a dictionary with the following keys:
- platforms: List of platform data (x, y, width, height)
- enemies: List of enemy data (x, y, patrol_distance, enemy_type)
- player_start: Tuple of player starting position (x, y)
- exit_pos: Tuple of level exit position (x, y)
- background_color: RGB tuple for level background color
- lives: Number of lives for this level
"""

from src.constants import *

# Level 1 - Tutorial level
LEVEL_1 = {
    "name": "Level 1: First Glitches",
    "background_color": (30, 30, 50),
    "player_start": (100, SCREEN_HEIGHT - 150),
    "exit_pos": (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 150),
    "lives": 2,
    "platforms": [
        # Ground
        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
        # Tutorial platforms
        (200, SCREEN_HEIGHT - 200, 200, 20),
        (500, SCREEN_HEIGHT - 300, 200, 20),
        (100, SCREEN_HEIGHT - 400, 200, 20),
        # Wall for wall jumping
        (400, SCREEN_HEIGHT - 250, 20, 150),
    ],
    "enemies": [
        # Basic enemy patrolling the ground
        (300, SCREEN_HEIGHT - 90, 150, "basic"),
        # Basic enemy on a platform
        (550, SCREEN_HEIGHT - 340, 100, "basic"),
    ]
}

# Level 2 - More complex level with more enemies
LEVEL_2 = {
    "name": "Level 2: Glitch Intensifies",
    "background_color": (40, 20, 60),
    "player_start": (50, SCREEN_HEIGHT - 150),
    "exit_pos": (SCREEN_WIDTH - 50, 100),
    "lives": 3,
    "platforms": [
        # Ground
        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
        # Left side platforms
        (0, SCREEN_HEIGHT - 200, 150, 20),
        (200, SCREEN_HEIGHT - 300, 150, 20),
        (0, SCREEN_HEIGHT - 400, 150, 20),
        # Middle platforms
        (300, SCREEN_HEIGHT - 250, 200, 20),
        (350, SCREEN_HEIGHT - 400, 100, 20),
        # Right side platforms
        (600, SCREEN_HEIGHT - 200, 200, 20),
        (550, SCREEN_HEIGHT - 350, 150, 20),
        (650, SCREEN_HEIGHT - 500, 150, 20),
        # Walls
        (300, SCREEN_HEIGHT - 350, 20, 100),
        (530, SCREEN_HEIGHT - 500, 20, 150),
    ],
    "enemies": [
        # Ground enemies
        (200, SCREEN_HEIGHT - 90, 200, "basic"),
        (500, SCREEN_HEIGHT - 90, 200, "basic"),
        # Platform enemies
        (650, SCREEN_HEIGHT - 240, 150, "jumper"),
        (400, SCREEN_HEIGHT - 440, 50, "shooter"),
    ]
}

# Level 3 - Hard level with many enemies and complex layout
LEVEL_3 = {
    "name": "Level 3: Glitch Nightmare",
    "background_color": (60, 10, 30),
    "player_start": (50, SCREEN_HEIGHT - 150),
    "exit_pos": (SCREEN_WIDTH - 50, 50),
    "lives": 5,
    "platforms": [
        # Ground
        (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
        # Left side
        (0, SCREEN_HEIGHT - 200, 100, 20),
        (150, SCREEN_HEIGHT - 300, 100, 20),
        (0, SCREEN_HEIGHT - 400, 100, 20),
        # Middle section - obstacle course
        (200, SCREEN_HEIGHT - 150, 50, 20),
        (300, SCREEN_HEIGHT - 250, 50, 20),
        (400, SCREEN_HEIGHT - 350, 50, 20),
        (300, SCREEN_HEIGHT - 450, 50, 20),
        (200, SCREEN_HEIGHT - 550, 50, 20),
        # Right side - final ascent
        (500, SCREEN_HEIGHT - 200, 100, 20),
        (650, SCREEN_HEIGHT - 300, 100, 20),
        (500, SCREEN_HEIGHT - 400, 100, 20),
        (650, SCREEN_HEIGHT - 500, 150, 20),
        # Walls
        (450, SCREEN_HEIGHT - 300, 20, 250),
        (600, SCREEN_HEIGHT - 500, 20, 200),
    ],
    "enemies": [
        # Ground enemies
        (300, SCREEN_HEIGHT - 90, 150, "basic"),
        (600, SCREEN_HEIGHT - 90, 150, "jumper"),
        # Platform enemies
        (150, SCREEN_HEIGHT - 340, 50, "shooter"),
        (500, SCREEN_HEIGHT - 240, 100, "basic"),
        (650, SCREEN_HEIGHT - 340, 100, "jumper"),
        (500, SCREEN_HEIGHT - 440, 100, "shooter"),
        (700, SCREEN_HEIGHT - 540, 100, "basic"),
    ]
}

# List of all levels
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3]
