# src/player.py
"""
Contains the Player class, responsible for player movement,
collision detection, and rendering.
"""
import pygame
# Use relative import
from .settings import TILE_SIZE, PLAYER_SPRITE, PLAYER_SPEED_MS

class Player(pygame.sprite.Sprite):
    """Represents the user-controlled character in the maze."""
    def __init__(self, x, y):
        super().__init__()
        
        # Load asset safely
        try:
            self.image = pygame.image.load(PLAYER_SPRITE).convert_alpha()
            self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        except pygame.error as e:
            print(f"Error loading Player asset: {e}")
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE)); self.image.fill((0, 0, 255))

        self.rect = self.image.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
        self.x = x
        self.y = y
        
        self.last_move_time = 0
        self.move_count = 0
        self.has_key = False

    def move(self, dx, dy, maze):
        """
        Attempts to move the player by (dx, dy) grid units, respecting cooldown.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < PLAYER_SPEED_MS:
            return False

        new_x = self.x + dx
        new_y = self.y + dy

        if not maze.is_wall(new_x, new_y):
            self.x = new_x
            self.y = new_y
            self.rect.topleft = (self.x * TILE_SIZE, self.y * TILE_SIZE)
            self.move_count += 1
            self.last_move_time = current_time
            return True
        return False

    def reset(self, x, y):
        """Resets the player's position and state."""
        self.x = x
        self.y = y
        self.rect.topleft = (x * TILE_SIZE, y * TILE_SIZE)
        self.move_count = 0
        self.has_key = False