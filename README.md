# Glitch Runner

A 2D platformer game built with Pygame where you navigate through glitchy environments.

## Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Space: Jump (double jump available)
- F3: Toggle debug mode
- Enter: Select menu options

## Game Features

- **Multiple Levels**: Progress through 3 increasingly difficult levels
- **Enemy Types**:
  - Basic enemies that patrol platforms
  - Jumper enemies that can jump between platforms
  - Shooter enemies that fire projectiles at you
- **Lives System**: You have 3 lives to complete all levels
- **Score System**: Earn points by completing levels quickly

## Glitch System

The game features a glitch system that randomly triggers various effects every 10 seconds:

- **Reversed Gravity**: Flips gravity upside down
- **Flickering Sprites**: Makes game objects flicker in and out
- **Input Lag**: Delays your control inputs
- **Color Distortion**: Shifts the color palette of the game
- **Screen Shake**: Makes the screen shake violently
- **Disappearing Platforms**: Makes random platforms fade away
- **Speed Change**: Alters your movement speed
- **Pixelation**: Pixelates the screen

Each glitch lasts for 5 seconds before returning to normal.

## Project Structure

```
glitch_runner/
├── assets/
│   ├── images/     # Game sprites and images
│   ├── sounds/     # Sound effects and music
│   └── fonts/      # Game fonts
├── src/
│   ├── __init__.py
│   ├── constants.py    # Game constants and settings
│   ├── game.py         # Main game class
│   ├── player.py       # Player character class
│   ├── enemy.py        # Enemy classes
│   ├── level.py        # Level management
│   ├── level_data.py   # Level definitions
│   ├── platform.py     # Platform objects
│   └── glitch_engine.py # Handles glitch effects
├── main.py         # Entry point
└── requirements.txt
```


