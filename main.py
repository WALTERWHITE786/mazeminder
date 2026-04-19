# src/main.py
"""
The main entry point for the playable MazeMinder game.
This final version integrates the pre-trained RL agent to dynamically
adjust the maze difficulty based on player performance.
"""
import pygame
import time
import sys
import numpy as np 
import random # For key placement

# Use relative imports
from .settings import *
from .maze import Maze
from .player import Player
from .agent import MazeMinderAgent
from .transformations import transformations
from .visuals import create_win_particles 

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.game_res = (GRID_WIDTH + (WIDTH - GRID_WIDTH), GRID_HEIGHT) 
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.game_surface = pygame.Surface(self.game_res) 

        self.current_maze_pixel_width = GRID_WIDTH
        self.current_maze_pixel_height = GRID_HEIGHT

        # Load font safely
        try:
            self.font = pygame.font.Font(FONT_PATH, 24)
            self.small_font = pygame.font.Font(FONT_PATH, 18)
        except FileNotFoundError:
            print(f"Warning: Font file not found at {FONT_PATH}. Using default.")
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        except pygame.error as e:
            print(f"Warning: Pygame error loading font: {e}. Using default.")
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)

        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()

        self.all_sprites = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.load_assets()
        self.agent = MazeMinderAgent(load_q_table=True) 

        self.previous_state = 1 
        self.current_state = 1
        self.last_action_name = "Begin"
        self.level_num = 1
        self.running = True

    def load_assets(self):
        """Loads all game sounds safely."""
        self.sounds = {}
        sound_files = {
            'step': STEP_SOUND,
            'collect': COLLECT_SOUND,
            'win': WIN_SOUND,
            'transform': TRANSFORM_SOUND
        }
        for name, path in sound_files.items():
            try:
                self.sounds[name] = pygame.mixer.Sound(path)
            except pygame.error as e:
                print(f"Warning: Could not load sound '{name}' at {path}. Error: {e}")
                self.sounds[name] = None 

    # --- THIS IS THE UPDATED AND CORRECTED METHOD ---
    def new_level(self):
        """Sets up a new, solvable, and transformed level."""
        if self.sounds.get('transform'): self.sounds['transform'].play()
        self.all_sprites.empty()
        self.particles.empty()

        action = self.agent.choose_action(self.current_state)
        
        # 1. Check state and create the appropriate maze
        if self.current_state == 0: # State 0 is "Struggling"
            print("Player is Struggling. Generating a simple maze.")
            self.maze = Maze(width=SIMPLE_MAZE_WIDTH, height=SIMPLE_MAZE_HEIGHT)
            self.current_maze_pixel_width = SIMPLE_MAZE_WIDTH * TILE_SIZE
            self.current_maze_pixel_height = SIMPLE_MAZE_HEIGHT * TILE_SIZE
        else:
            # Player is Learning (1) or has Mastery (2)
            print("Player is Learning/Mastery. Generating a standard maze.")
            self.maze = Maze() # Uses default MAZE_WIDTH/MAZE_HEIGHT
            self.current_maze_pixel_width = GRID_WIDTH
            self.current_maze_pixel_height = GRID_HEIGHT

        # 2. Apply the agent's chosen transformation
        # The transformation function now correctly updates the grid AND all object coordinates.
        (
            self.maze.grid, 
            self.maze.start_pos, 
            self.maze.key_pos, 
            self.maze.end_pos
        ) = transformations[action](
            self.maze.grid, 
            self.maze.start_pos, 
            self.maze.key_pos, 
            self.maze.end_pos
        )
        
        self.last_action_name = transformations[action].__name__.replace('_maze', '').capitalize()

        # 3. Create the player at the new, correct start position
        self.player = Player(self.maze.start_pos[0], self.maze.start_pos[1])
        self.all_sprites.add(self.player)

        self.run_level()

    def run_level(self):
        """The main game loop for a single level."""
        self.playing = True
        start_time = time.time()

        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events()
            self.update()
            self.draw()

        end_time = time.time()
        time_taken = end_time - start_time
        
        # Pass the maze width to the update function for fair evaluation
        self.update_player_state(time_taken, self.player.move_count, self.maze.width)
        self.level_num += 1

    def update_player_state(self, time_taken, moves, current_maze_width):
        """Determines the player's new cognitive state based on dynamic, demonstratable thresholds."""
        self.previous_state = self.current_state
        
        if current_maze_width == SIMPLE_MAZE_WIDTH:
            # --- Thresholds for 10x10 maze ---
            struggling_threshold = 25
            mastery_threshold = 15
        else:
            # --- EASIER THRESHOLDS for standard 24x24 maze (for demonstration) ---
            struggling_threshold = 60
            mastery_threshold = 45
        
        # Apply the new dynamic logic
        if time_taken > struggling_threshold:
             self.current_state = 0 # Struggling
        elif time_taken < mastery_threshold:
             self.current_state = 2 # Mastery
        else:
             self.current_state = 1 # Learning
             
        print(f"Level {self.level_num} stats: Time={time_taken:.2f}s, Moves={moves}")
        print(f"New player state: {self.current_state} ({['Struggling', 'Learning', 'Mastery'][self.current_state]})")

    def events(self):
        """Handles all user input (keyboard, window close)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_ESCAPE: 
                     self.playing = False
                     self.running = False
                if event.key == pygame.K_LEFT: moved = self.player.move(-1, 0, self.maze)
                if event.key == pygame.K_RIGHT: moved = self.player.move(1, 0, self.maze)
                if event.key == pygame.K_UP: moved = self.player.move(0, -1, self.maze)
                if event.key == pygame.K_DOWN: moved = self.player.move(0, 1, self.maze)
                if moved and self.sounds.get('step'): self.sounds['step'].play()

    def update(self):
        """Updates game state (sprite positions, check win conditions)."""
        self.all_sprites.update() 
        self.particles.update() 

        # Check for key collection
        if self.maze.key_pos and (self.player.x, self.player.y) == self.maze.key_pos:
            self.player.has_key = True
            self.maze.key_pos = None 
            if self.sounds.get('collect'): self.sounds['collect'].play()
            # create_win_particles(self.player.x, self.player.y, self.particles) # Disabled

        # Check for win condition (Player reached goal AND has key)
        if (self.player.x, self.player.y) == self.maze.end_pos and self.player.has_key:
            if self.sounds.get('win'): self.sounds['win'].play()
            # create_win_particles(self.player.x, self.player.y, self.particles) # Disabled
            self.playing = False 

    def draw_grid_and_ui(self):
        """Draws the maze, player, and UI panel onto the internal game_surface."""
        self.game_surface.fill(UI_BG_COLOR)

        # 1. Create maze_surf with CURRENT dynamic dimensions
        maze_surf = pygame.Surface((self.current_maze_pixel_width, self.current_maze_pixel_height))
        maze_surf.fill(BLACK) 
        self.maze.draw(maze_surf) 
        self.all_sprites.draw(maze_surf) 
        self.particles.draw(maze_surf) 
        # Blit the (potentially smaller) maze surface at (0,0)
        self.game_surface.blit(maze_surf, (0, 0)) 

        # 2. Draw UI panel starting *immediately after* the current maze
        ui_panel_start_x = self.current_maze_pixel_width
        ui_panel_width = self.game_res[0] - ui_panel_start_x
        
        ui_panel_rect = pygame.Rect(ui_panel_start_x, 0, ui_panel_width, self.game_res[1])
        pygame.draw.rect(self.game_surface, UI_BORDER_COLOR, ui_panel_rect) 

        # 3. Draw UI text centered *within the new dynamic UI panel*
        ui_panel_center_x = ui_panel_start_x + (ui_panel_width // 2)
        
        state_map = {0: "Struggling", 1: "Learning", 2: "Mastery"}
        state_str = state_map.get(self.current_state, "Unknown") 

        self.draw_text(f"Level: {self.level_num}", self.font, UI_TEXT_COLOR, ui_panel_center_x, 50)
        self.draw_text("Status:", self.small_font, UI_TEXT_COLOR, ui_panel_center_x, 150)
        self.draw_text(state_str, self.font, UI_HIGHLIGHT_COLOR, ui_panel_center_x, 180)
        self.draw_text("Guardian's Action:", self.small_font, UI_TEXT_COLOR, ui_panel_center_x, 250)
        self.draw_text(self.last_action_name, self.font, UI_HIGHLIGHT_COLOR, ui_panel_center_x, 280)

    def draw_text(self, text, font, color, center_x, center_y):
        """Helper function to draw centered text onto the game_surface."""
        try:
            text_surface = font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(center_x, center_y))
            self.game_surface.blit(text_surface, text_rect)
        except Exception as e:
            print(f"Error rendering text '{text}': {e}")

    def draw(self):
        """Renders the complete scene to the main screen."""
        self.draw_grid_and_ui()
        self.screen.blit(pygame.transform.scale(self.game_surface, self.screen.get_size()), (0, 0))
        pygame.display.flip()

    def run(self):
        """Main game execution loop that runs level after level."""
        while self.running:
            self.new_level() 
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()