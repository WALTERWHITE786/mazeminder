# src/settings.py
"""
Centralized configuration file for the MazeMinder project.
Contains all constants for screen dimensions, colors, game properties,
and agent training parameters.
"""
import os, numpy

# --- Project Setup ---
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "MazeMinder: The Adaptive Labyrinth"

# --- Maze Geometry ---
TILE_SIZE = 32 
MAZE_WIDTH = 24  # Set to 24 (Even) to be divisible by 2 for 'warp_maze'
MAZE_HEIGHT = 24 # Set to 24 (Even) to be divisible by 2 for 'warp_maze'
GRID_WIDTH = MAZE_WIDTH * TILE_SIZE
GRID_HEIGHT = MAZE_HEIGHT * TILE_SIZE

# --- Dimensions for the "Struggling" state ---
SIMPLE_MAZE_WIDTH = 10
SIMPLE_MAZE_HEIGHT = 10

# --- Player Settings ---
PLAYER_SPEED_MS = 150 # Milliseconds per tile move (cooldown)

# --- RL Agent Parameters ---
ALPHA = 0.1             # Learning rate
GAMMA = 0.9             # Discount factor
EPSILON_START = 1.0     
EPSILON_DECAY = 0.9998  
EPSILON_MIN = 0.05      

NUM_EPISODES = 15000
MAX_STEPS_PER_EPISODE = 150
NUM_STATES = 3
NUM_ACTIONS = 4 # No Change, Rotate, Mirror, Warp

# --- Colors (FIX IS HERE) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) # <-- THIS LINE WAS MISSING
UI_BG_COLOR = (10, 5, 20) 
UI_BORDER_COLOR = (80, 70, 100)
UI_TEXT_COLOR = (230, 220, 255)
UI_HIGHLIGHT_COLOR = (255, 220, 100) 

# --- Paths (Assumes running from project root) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Q_TABLE_PATH = 'q_table.pkl'
FONT_PATH = os.path.join(BASE_DIR, 'assets', 'fonts', 'medieval_font.ttf')
PLAYER_SPRITE = os.path.join(BASE_DIR, 'assets', 'sprites', 'player.png')
GOAL_SPRITE = os.path.join(BASE_DIR, 'assets', 'sprites', 'goal.png')
WALL_TILESET = os.path.join(BASE_DIR, 'assets', 'sprites', 'wall_tileset.png')
PARTICLE_SPRITE = os.path.join(BASE_DIR, 'assets', 'sprites', 'vfx', 'particle.png')
KEY_SPRITE = os.path.join(BASE_DIR, 'assets', 'sprites', 'key.png')

STEP_SOUND = os.path.join(BASE_DIR, 'assets', 'sounds', 'step.wav')
COLLECT_SOUND = os.path.join(BASE_DIR, 'assets', 'sounds', 'collect.wav')
WIN_SOUND = os.path.join(BASE_DIR, 'assets', 'sounds', 'win.wav')
TRANSFORM_SOUND = os.path.join(BASE_DIR, 'assets', 'sounds', 'transform.wav')