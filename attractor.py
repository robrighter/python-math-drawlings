import turtle
import math

# --- Configuration ---
# Screen dimensions
WIDTH, HEIGHT = 800, 600
# Number of steps to calculate and draw
NUM_STEPS = 15000
# Drawing scale factor
SCALE = 10
# Time step for the simulation. Smaller values are more accurate but slower.
DT = 0.005

# --- Lorenz Attractor Parameters ---
# These are the classic values that produce the butterfly-wing shape.
# Feel free to experiment with them.
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0


# --- Setup the Turtle Environment ---
def setup_screen():
    """Sets up the turtle screen."""
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Lorenz Attractor")
    # Turn off tracer for maximum drawing speed
    screen.tracer(0)
    return screen


def setup_turtle():
    """Sets up the turtle and its initial position."""
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    # t.color("#FF5733")  # A nice fiery orange color
    t.penup()
    # Initial position of the point in 3D space
    t.x, t.y, t.z = 0.1, 0.0, 0.0
    # Move the turtle to the projected 2D starting point
    t.goto(t.x * SCALE, t.z * SCALE - 250)  # Project onto X-Z plane and center
    t.pendown()
    return t


# --- Attractor Logic ---
def draw_lorenz_attractor(t):
    """Calculates and draws the Lorenz attractor."""
    print(f"Generating {NUM_STEPS} steps... This may take a moment.")

    # We will use a simple list to create a color gradient effect
    colors = ["#FF5733", "#FF8C00", "#FFD700", "#FFFF00"]
    color_index = 0

    for i in range(NUM_STEPS):
        # Lorenz system differential equations
        # These equations describe how the 3D point (x, y, z) moves over time.
        dx = SIGMA * (t.y - t.x)
        dy = t.x * (RHO - t.z) - t.y
        dz = t.x * t.y - BETA * t.z

        # Update the coordinates using Euler's method
        # This is a simple way to approximate the next point in the system.
        t.x += dx * DT
        t.y += dy * DT
        t.z += dz * DT

        # --- Drawing Logic ---
        # We are projecting the 3D system onto a 2D plane by using x and z.
        # The y-coordinate influences the path but is not directly plotted.
        # We also shift the drawing down to center it better.
        t.goto(t.x * SCALE, t.z * SCALE - 250)

        # Change color periodically to create a nice visual effect
        if i % 100 == 0:
            color_index = (color_index + 1) % len(colors)
            # t.pencolor(colors[color_index])

        # Update the screen in batches to speed up the drawing
        if i % 500 == 0:
            turtle.update()

    # Final update to show the complete drawing
    turtle.update()
    print("Attractor drawing complete.")


# --- Main Execution ---
if __name__ == "__main__":
    try:
        screen = setup_screen()
        pen = setup_turtle()
        draw_lorenz_attractor(pen)
        # Keep the window open until it's clicked
        screen.exitonclick()
    except turtle.Terminator:
        print("Turtle graphics window was closed.")
    except Exception as e:
        print(f"An error occurred: {e}")
