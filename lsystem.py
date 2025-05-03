import matplotlib.pyplot as plt
import numpy as np

def create_l_system(axiom, rules, iterations):
    """
    Generates an L-System string based on the axiom, rules, and number of iterations.

    Parameters:
    axiom (str): The initial string.
    rules (dict): A dictionary of replacement rules (e.g., {'F': 'F+F-F-F+F'}).
    iterations (int): The number of iterations to apply the rules.

    Returns:
    str: The generated L-System string.
    """
    string = axiom
    for _ in range(iterations):
        next_string = ""
        for char in string:
            next_string += rules.get(char, char) # Apply rule if it exists, otherwise keep the character
        string = next_string
    return string

def draw_l_system(string, angle, step):
    """
    Draws an L-System fractal based on the L-System string using turtle-like graphics in matplotlib.

    Parameters:
    string (str): The L-System string to interpret.
    angle (float): The angle of rotation in degrees.
    step (int): The step size for forward movements.
    """
    x, y = 0, 0 # Starting position
    angle_rad = np.radians(angle) # Convert angle to radians for numpy functions
    current_angle = 0 # Initial direction (east)
    stack = [] # Stack for saving position and angle during branching
    segments = [] # List to store line segments for plotting

    for command in string:
        if command == 'F': # Move forward and draw line
            x_new = x + step * np.cos(current_angle)
            y_new = y + step * np.sin(current_angle)
            segments.append([(x, y), (x_new, y_new)]) # Store segment
            x, y = x_new, y_new # Update current position
        elif command == '+': # Turn right
            current_angle -= angle_rad
        elif command == '-': # Turn left
            current_angle += angle_rad
        elif command == '[': # Save current position and angle to stack
            stack.append((x, y, current_angle))
        elif command == ']': # Restore position and angle from stack (branch end)
            x, y, current_angle = stack.pop()

    # Plotting using matplotlib
    plt.figure(figsize=(8, 8))
    ax = plt.gca()
    for start_point, end_point in segments:
        x_coords, y_coords = zip(start_point, end_point)
        ax.plot(x_coords, y_coords, 'black', linewidth=1) # Plot each segment

    ax.set_aspect('equal', adjustable='box') # Equal aspect ratio
    ax.axis('off') # Hide axes for cleaner fractal view
    plt.title('L-System Fractal')
    plt.show()


if __name__ == '__main__':
    # Example: Fractal Plant (Barnsley Fern variation)
    axiom = "X"
    rules = {
        "F": "FF",
        "X": "F+[[X]-X]-F[-FX]+X",
    }
    iterations = 6
    angle = 25 # Branching angle
    step_size = 5

    l_system_string = create_l_system(axiom, rules, iterations)
    draw_l_system(l_system_string, angle, step_size)