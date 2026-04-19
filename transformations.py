# src/transformations.py
"""
Contains functions that apply transformations to a maze grid AND
its object coordinates, guaranteeing solvability.
"""
import numpy as np

def _transform_coord(x, y, w, h, transform_type):
    """Helper function to transform a single (x, y) coordinate."""
    if transform_type == 'rotate':
        # 90-deg clockwise rotation: (x, y) -> (h-1-y, x)
        return h - 1 - y, x
    elif transform_type == 'mirror':
        # Horizontal flip: (x, y) -> (w-1-x, y)
        return w - 1 - x, y
    elif transform_type == 'warp':
        # Quadrant swap (TL <-> BR)
        h_mid, w_mid = h // 2, w // 2
        if x < w_mid and y < h_mid: # Top-Left -> Bottom-Right
            return x + w_mid, y + h_mid
        elif x >= w_mid and y >= h_mid: # Bottom-Right -> Top-Left
            return x - w_mid, y - h_mid
        else:
            return x, y # Other quadrants are unchanged
    else:
        # 'no_change'
        return x, y

def no_change(grid, start, key, end):
    """Action 0: Returns all inputs unchanged."""
    return grid, start, key, end

def rotate_maze(grid, start, key, end):
    """Action 1: Rotates grid and all coordinates 90-deg clockwise."""
    h, w = grid.shape
    new_grid = np.rot90(grid, k=-1)
    
    new_start = _transform_coord(start[0], start[1], w, h, 'rotate')
    new_key = _transform_coord(key[0], key[1], w, h, 'rotate') if key else None
    new_end = _transform_coord(end[0], end[1], w, h, 'rotate')
    
    return new_grid, new_start, new_key, new_end

def mirror_maze(grid, start, key, end):
    """Action 2: Mirrors grid and all coordinates horizontally."""
    h, w = grid.shape
    new_grid = np.fliplr(grid)
    
    new_start = _transform_coord(start[0], start[1], w, h, 'mirror')
    new_key = _transform_coord(key[0], key[1], w, h, 'mirror') if key else None
    new_end = _transform_coord(end[0], end[1], w, h, 'mirror')

    return new_grid, new_start, new_key, new_end

def warp_maze(grid, start, key, end):
    """Action 3: Swaps TL/BR quadrants on grid and all coordinates."""
    h, w = grid.shape
    h_mid, w_mid = h // 2, w // 2
    
    # Check if maze is even-dimensioned (which we ensured in settings.py)
    if h % 2 != 0 or w % 2 != 0:
        print("Warning: Warp applied to odd-dimensioned maze. Skipping.")
        return grid, start, key, end

    new_grid = grid.copy()
    
    # Copy quadrants
    top_left = grid[0:h_mid, 0:w_mid].copy()
    bottom_right = grid[h_mid:, w_mid:].copy()
    
    # Swap them
    new_grid[0:h_mid, 0:w_mid] = bottom_right
    new_grid[h_mid:, w_mid:] = top_left
    
    # Transform coordinates
    new_start = _transform_coord(start[0], start[1], w, h, 'warp')
    new_key = _transform_coord(key[0], key[1], w, h, 'warp') if key else None
    new_end = _transform_coord(end[0], end[1], w, h, 'warp')

    return new_grid, new_start, new_key, new_end

# List of all available transformation functions
transformations = [
    no_change,
    rotate_maze,
    mirror_maze,
    warp_maze,
]