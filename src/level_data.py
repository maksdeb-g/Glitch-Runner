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

# Level 4 - Constant screen shaking level
LEVEL_4 = {
    "name": "Level 4: Reality Breakdown",
    "background_color": (45, 15, 45),  # Purple-red mix
    "player_start": (50, SCREEN_HEIGHT - 150),
    "exit_pos": (SCREEN_WIDTH - 50, 50),
    "lives": 6,
    "shake_enabled": True,  # Enable constant screen shaking
    "platforms": [
        # Ground - broken into segments to represent unstable reality
        (0, SCREEN_HEIGHT - 50, 150, 50),
        (200, SCREEN_HEIGHT - 50, 150, 50),
        (400, SCREEN_HEIGHT - 50, 150, 50),
        (600, SCREEN_HEIGHT - 50, 200, 50),
        
        # Floating platforms - more chaotic arrangement
        (100, SCREEN_HEIGHT - 180, 80, 20),
        (250, SCREEN_HEIGHT - 250, 80, 20),
        (150, SCREEN_HEIGHT - 320, 80, 20),
        (300, SCREEN_HEIGHT - 390, 80, 20),
        
        # Middle section - moving upward
        (400, SCREEN_HEIGHT - 200, 70, 20),
        (500, SCREEN_HEIGHT - 280, 70, 20),
        (400, SCREEN_HEIGHT - 360, 70, 20),
        (500, SCREEN_HEIGHT - 440, 70, 20),
        
        # Final approach
        (600, SCREEN_HEIGHT - 300, 100, 20),
        (650, SCREEN_HEIGHT - 400, 100, 20),
        (600, SCREEN_HEIGHT - 500, 200, 20),
        
        # Walls - more scattered
        (350, SCREEN_HEIGHT - 300, 20, 200),
        (550, SCREEN_HEIGHT - 500, 20, 150),
        (250, SCREEN_HEIGHT - 400, 20, 100),
    ],
    "enemies": [
        # More enemies with varied types
        (250, SCREEN_HEIGHT - 90, 100, "basic"),
        (500, SCREEN_HEIGHT - 90, 150, "jumper"),
        
        # Platform enemies - more aggressive placement
        (100, SCREEN_HEIGHT - 220, 80, "shooter"),
        (250, SCREEN_HEIGHT - 290, 80, "basic"),
        (300, SCREEN_HEIGHT - 430, 80, "jumper"),
        
        # Higher level enemies
        (400, SCREEN_HEIGHT - 240, 70, "shooter"),
        (500, SCREEN_HEIGHT - 320, 70, "basic"),
        (400, SCREEN_HEIGHT - 400, 70, "jumper"),
        
        # Final approach - gauntlet of enemies
        (600, SCREEN_HEIGHT - 340, 100, "shooter"),
        (650, SCREEN_HEIGHT - 440, 100, "jumper"),
        (700, SCREEN_HEIGHT - 540, 100, "shooter"),
    ]
}

# Level 5 - Advanced glitches with screen shaking
LEVEL_5 = {
    "name": "Level 5: System Collapse",
    "background_color": (50, 10, 20),  # Darker red
    "player_start": (50, SCREEN_HEIGHT - 150),
    "exit_pos": (SCREEN_WIDTH - 50, 50),
    "lives": 8,
    "shake_enabled": True,  # Enable constant screen shaking (more intense)
    "advanced_glitches": True,  # Enable advanced glitch effects
    "platforms": [
        # Ground - very broken to represent collapsing system
        (0, SCREEN_HEIGHT - 50, 100, 50),
        (150, SCREEN_HEIGHT - 50, 100, 50),
        (300, SCREEN_HEIGHT - 50, 100, 50),
        (450, SCREEN_HEIGHT - 50, 100, 50),
        (600, SCREEN_HEIGHT - 50, 100, 50),
        (750, SCREEN_HEIGHT - 50, 50, 50),
        
        # Left side - chaotic ascent
        (50, SCREEN_HEIGHT - 150, 60, 20),
        (150, SCREEN_HEIGHT - 220, 60, 20),
        (50, SCREEN_HEIGHT - 290, 60, 20),
        (150, SCREEN_HEIGHT - 360, 60, 20),
        (50, SCREEN_HEIGHT - 430, 60, 20),
        
        # Middle section - complex obstacle course
        (250, SCREEN_HEIGHT - 180, 50, 20),
        (350, SCREEN_HEIGHT - 240, 50, 20),
        (450, SCREEN_HEIGHT - 300, 50, 20),
        (350, SCREEN_HEIGHT - 360, 50, 20),
        (250, SCREEN_HEIGHT - 420, 50, 20),
        (350, SCREEN_HEIGHT - 480, 50, 20),
        
        # Right side - final difficult ascent
        (550, SCREEN_HEIGHT - 200, 70, 20),
        (650, SCREEN_HEIGHT - 270, 70, 20),
        (550, SCREEN_HEIGHT - 340, 70, 20),
        (650, SCREEN_HEIGHT - 410, 70, 20),
        (550, SCREEN_HEIGHT - 480, 70, 20),
        (650, SCREEN_HEIGHT - 550, 150, 20),
        
        # Walls - scattered throughout
        (200, SCREEN_HEIGHT - 250, 20, 150),
        (500, SCREEN_HEIGHT - 350, 20, 200),
        (300, SCREEN_HEIGHT - 450, 20, 150),
        (600, SCREEN_HEIGHT - 500, 20, 250),
    ],
    "enemies": [
        # Ground level - gauntlet of enemies
        (100, SCREEN_HEIGHT - 90, 100, "basic"),
        (250, SCREEN_HEIGHT - 90, 100, "jumper"),
        (400, SCREEN_HEIGHT - 90, 100, "shooter"),
        (550, SCREEN_HEIGHT - 90, 100, "basic"),
        (700, SCREEN_HEIGHT - 90, 100, "jumper"),
        
        # Left side ascent
        (50, SCREEN_HEIGHT - 190, 60, "shooter"),
        (150, SCREEN_HEIGHT - 260, 60, "basic"),
        (50, SCREEN_HEIGHT - 330, 60, "jumper"),
        (150, SCREEN_HEIGHT - 400, 60, "shooter"),
        
        # Middle obstacle course
        (250, SCREEN_HEIGHT - 220, 50, "basic"),
        (350, SCREEN_HEIGHT - 280, 50, "jumper"),
        (450, SCREEN_HEIGHT - 340, 50, "shooter"),
        (350, SCREEN_HEIGHT - 400, 50, "basic"),
        (250, SCREEN_HEIGHT - 460, 50, "jumper"),
        
        # Right side - final ascent
        (550, SCREEN_HEIGHT - 240, 70, "shooter"),
        (650, SCREEN_HEIGHT - 310, 70, "basic"),
        (550, SCREEN_HEIGHT - 380, 70, "jumper"),
        (650, SCREEN_HEIGHT - 450, 70, "shooter"),
        (550, SCREEN_HEIGHT - 520, 70, "basic"),
        (700, SCREEN_HEIGHT - 590, 100, "jumper"),
    ]
}

# List of all levels
LEVELS = [LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4, LEVEL_5]
