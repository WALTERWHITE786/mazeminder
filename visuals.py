# src/visuals.py
"""
Contains functions for visual effects. 
NOTE: The actual particle drawing is disabled to prevent asset errors.
"""
import pygame
import random
# Use relative import
from .settings import TILE_SIZE, PARTICLE_SPRITE

# We define a dummy class and function to prevent crashes on missing asset
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Dummy initialization to prevent crashing on image load
        self.image = pygame.Surface([1, 1])
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = pygame.math.Vector2(0, 0)
        self.lifetime = 1

    def update(self):
        # The original particle logic is disabled
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()

def create_win_particles(x, y, particle_group):
    """Placeholder: Does nothing since particle assets are explicitly excluded."""
    pass 
    # To re-enable particles, uncomment the code below and ensure PARTICLE_SPRITE is a valid 8x8 image
    """
    for _ in range(30):
        particle_group.add(Particle(x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2))
    """