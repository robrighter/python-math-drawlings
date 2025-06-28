import turtle

def hilbert_A(level, angle, step, t):
    """
    Draws a Hilbert curve with a '|_|' orientation.
    This corresponds to one of the two recursive rules for the curve.
    It ensures the drawing expands upwards and sideways from the start.

    Args:
        level (int): The recursion level.
        angle (int): The angle to turn (always 90).
        step (int): The length of each segment.
        t (turtle.Turtle): The turtle object to draw with.
    """
    # Base case: at level 0, we do nothing.
    if level == 0:
        return

    t.left(angle)
    hilbert_B(level - 1, angle, step, t) # First sub-curve
    t.forward(step)
    t.right(angle)
    hilbert_A(level - 1, angle, step, t) # Second sub-curve
    t.forward(step)
    hilbert_A(level - 1, angle, step, t) # Third sub-curve
    t.right(angle)
    t.forward(step)
    hilbert_B(level - 1, angle, step, t) # Fourth sub-curve
    t.left(angle)

def hilbert_B(level, angle, step, t):
    """
    Draws a Hilbert curve with a '|-|' orientation.
    This is the second of the two mutually recursive rules.

    Args:
        level (int): The recursion level.
        angle (int): The angle to turn (always 90).
        step (int): The length of each segment.
        t (turtle.Turtle): The turtle object to draw with.
    """
    # Base case: at level 0, we do nothing.
    if level == 0:
        return

    t.right(angle)
    hilbert_A(level - 1, angle, step, t) # First sub-curve
    t.forward(step)
    t.left(angle)
    hilbert_B(level - 1, angle, step, t) # Second sub-curve
    t.forward(step)
    hilbert_B(level - 1, angle, step, t) # Third sub-curve
    t.left(angle)
    t.forward(step)
    hilbert_A(level - 1, angle, step, t) # Fourth sub-curve
    t.right(angle)


def draw(t):
    # --- Curve Parameters ---
    level = 4
    size = 500  # Overall size of the curve's bounding box
    # Calculate the step size based on the level and overall size
    step = size / (2 ** level - 1)
    angle = 90

    # --- Initial Positioning ---
    t.penup()
    # Position the turtle at the lower-left corner of the drawing area.
    # The turtle starts facing East (0 degrees) by default.
    t.goto(-size / 2, -size / 2)
    t.pendown()

    # --- Start Drawing ---
    # We start with hilbert_A to get the upward-opening curve.
    hilbert_A(level, angle, step, t)

def main():
    """
    Main function to set up the turtle environment and start the drawing.
    """
    # --- Screen Setup ---
    screen = turtle.Screen()
    screen.setup(width=600, height=600)


    # --- Turtle Setup ---
    t = turtle.Turtle()
    t.speed(0)  # Set speed to maximum
    t.hideturtle()
    t.pensize(1)

    # --- Curve Parameters ---
    level = 4
    size = 500 # Overall size of the curve's bounding box
    # Calculate the step size based on the level and overall size
    step = size / (2**level - 1)
    angle = 90

    # --- Initial Positioning ---
    t.penup()
    # Position the turtle at the lower-left corner of the drawing area.
    # The turtle starts facing East (0 degrees) by default.
    t.goto(-size / 2, -size / 2)
    t.pendown()

    # --- Start Drawing ---
    # We start with hilbert_A to get the upward-opening curve.
    hilbert_A(level, angle, step, t)

    # --- Finish ---
    screen.exitonclick()

if __name__ == "__main__":
    main()
