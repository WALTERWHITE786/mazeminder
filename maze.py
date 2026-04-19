# src/maze.py
"""
Contains the Maze class, responsible for generating, storing,
and drawing the maze structure using the Recursive Backtracking algorithm.
"""
import pygame
import random
import numpy as np
# Use relative imports
from .settings import TILE_SIZE, MAZE_WIDTH, MAZE_HEIGHT, WALL_TILESET, GOAL_SPRITE, KEY_SPRITE, BLACK, WHITE

class Maze:
    """
    Generates and manages a perfect maze.
    The maze is represented as a NumPy array where 1 is a path and 0 is a wall.
    """
    def __init__(self, width=MAZE_WIDTH, height=MAZE_HEIGHT):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=int)
        
        # Load assets safely
        try:
            self.tileset = pygame.image.load(WALL_TILESET).convert_alpha()
            self.tileset = pygame.transform.scale(self.tileset, (TILE_SIZE, TILE_SIZE))
            self.goal_img = pygame.image.load(GOAL_SPRITE).convert_alpha()
            self.goal_img = pygame.transform.scale(self.goal_img, (TILE_SIZE, TILE_SIZE))
            self.key_img = pygame.image.load(KEY_SPRITE).convert_alpha()
            self.key_img = pygame.transform.scale(self.key_img, (TILE_SIZE, TILE_SIZE))
        except pygame.error:
            # Fallback surfaces if assets are missing
            self.tileset = pygame.Surface((TILE_SIZE, TILE_SIZE)); self.tileset.fill((100, 100, 100))
            self.goal_img = pygame.Surface((TILE_SIZE, TILE_SIZE)); self.goal_img.fill((255, 0, 0))
            self.key_img = pygame.Surface((TILE_SIZE, TILE_SIZE)); self.key_img.fill((255, 255, 0))

        # --- THIS IS THE CORRECTED LOGIC ---
        # 1. Generate the connected path
        self.generate_path()
        # 2. Place start, end, and key on that guaranteed path
        self.place_objects()
        # --- END CORRECTION ---

    def generate_path(self):
        """Generates the maze structure using Recursive Backtracking."""
        stack = [(0, 0)]
        self.grid[0, 0] = 1 # Start cell is a path

        # Recursive Backtracking Algorithm
        while stack:
            cx, cy = stack[-1]
            neighbors = []
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = cx + dx * 2, cy + dy * 2
                if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny, nx] == 0:
                    neighbors.append((nx, ny, dx, dy))
            
            if neighbors:
                nx, ny, dx, dy = random.choice(neighbors)
                self.grid[ny, nx] = 1
                self.grid[cy + dy, cx + dx] = 1 # Carve the path
                stack.append((nx, ny))
            else:
                stack.pop()

    def place_objects(self):
        """Places start, end, and key on the generated path."""
        # Get ALL cells that are part of the connected path
        path_cells = np.argwhere(self.grid == 1)
        
        # Start is always where the algorithm started
        start_cell = path_cells[0]
        self.start_pos = (start_cell[1], start_cell[0]) # (x, y) format
        
        # Goal is the last cell the algorithm visited (farthest from start)
        end_cell = path_cells[-1]
        self.end_pos = (end_cell[1], end_cell[0]) # (x, y) format

        # Key is a random cell on the path that is NOT the start or end
        valid_key_cells = [
            cell for cell in path_cells 
            if not np.array_equal(cell, start_cell) and not np.array_equal(cell, end_cell)
        ]
        
        if valid_key_cells:
            key_cell = random.choice(valid_key_cells)
            self.key_pos = (key_cell[1], key_cell[0]) # (x, y) format
        else:
            # Fallback if maze is tiny, just put key on goal
            self.key_pos = self.end_pos


    def draw(self, screen):
        """Draws the maze walls, key, and goal."""
        for y in range(self.height):
            for x in range(self.width):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(screen, BLACK, rect) # Background path color

                if self.grid[y, x] == 0: # If it's a wall
                    screen.blit(self.tileset, rect.topleft)
        
        # Draw the goal and key
        screen.blit(self.goal_img, (self.end_pos[0] * TILE_SIZE, self.end_pos[1] * TILE_SIZE))
        
        if self.key_pos is not None:
             screen.blit(self.key_img, (self.key_pos[0] * TILE_SIZE, self.key_pos[1] * TILE_SIZE))

    def is_wall(self, x, y):
        """Checks if a given grid coordinate is a wall."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x] == 0
        return True