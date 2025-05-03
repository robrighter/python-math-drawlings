import matplotlib.pyplot as plt
import numpy as np
import random

def initialize_grid(grid_size):
    """
    Initializes the grid for DLA simulation with a seed particle at the center.

    Parameters:
    grid_size (int): Size of the square grid.

    Returns:
    tuple: (grid, occupied_cells) - grid is a NumPy array, occupied_cells is a set of occupied coordinates.
    """
    grid = np.zeros((grid_size, grid_size), dtype=int) # 0: empty, 1: occupied
    center = grid_size // 2
    grid[center, center] = 1 # Seed particle at the center
    occupied_cells = {(center, center)}
    return grid, occupied_cells

def get_random_start_position(grid_size):
    """
    Gets a random starting position for a walker at the grid boundary.

    Parameters:
    grid_size (int): Size of the grid.

    Returns:
    tuple: (x, y) - Random starting coordinates at the boundary.
    """
    side = random.randint(0, 3) # 0: top, 1: right, 2: bottom, 3: left
    if side == 0: # Top
        return random.randint(0, grid_size - 1), 0
    elif side == 1: # Right
        return grid_size - 1, random.randint(0, grid_size - 1)
    elif side == 2: # Bottom
        return random.randint(0, grid_size - 1), grid_size - 1
    else: # Left
        return 0, random.randint(0, grid_size - 1)

def random_walk(grid, occupied_cells, grid_size):
    """
    Simulates a random walk until the particle sticks to the cluster.

    Parameters:
    grid (np.array): The grid.
    occupied_cells (set): Set of occupied cell coordinates.
    grid_size (int): Size of the grid.

    Returns:
    tuple: (x, y) - Coordinates where the particle stuck.
    """
    start_x, start_y = get_random_start_position(grid_size)
    x, y = start_x, start_y

    while True:
        direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)]) # right, left, down, up
        x_new, y_new = x + direction[0], y + direction[1]

        # Stay within grid boundaries
        if 0 <= x_new < grid_size and 0 <= y_new < grid_size:
            x, y = x_new, y_new

            # Check for sticking to occupied neighbors
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]: # Check neighbors
                neighbor_x, neighbor_y = x + dx, y + dy
                if (0 <= neighbor_x < grid_size and 0 <= neighbor_y < grid_size and
                        (neighbor_x, neighbor_y) in occupied_cells):
                    return x, y # Stick!

def display_dla_fractal(grid):
    """
    Displays the DLA fractal grid using matplotlib.

    Parameters:
    grid (np.array): The DLA grid.
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(grid, cmap='viridis', interpolation='none') # 'viridis' for visualization
    plt.title('Diffusion-Limited Aggregation (DLA) Fractal')
    plt.axis('off') # Hide axes
    plt.colorbar(label='Occupied (1) / Empty (0)') # Colorbar to indicate occupied/empty
    plt.show()

def run_dla_simulation(grid_size, num_particles):
    """
    Runs the DLA simulation and displays the resulting fractal.

    Parameters:
    grid_size (int): Size of the grid.
    num_particles (int): Number of particles to aggregate.
    """
    grid, occupied_cells = initialize_grid(grid_size)

    for _ in range(num_particles):
        stick_x, stick_y = random_walk(grid, occupied_cells, grid_size)
        grid[stick_y, stick_x] = 1 # Mark as occupied in grid (y, x because of numpy array indexing)
        occupied_cells.add((stick_x, stick_y)) # Add to set of occupied cells

    display_dla_fractal(grid)


if __name__ == '__main__':
    grid_size = 2*100  # Adjust grid size for resolution
    num_particles = 2*5000 # Adjust number of particles for fractal size/density
    run_dla_simulation(grid_size, num_particles)