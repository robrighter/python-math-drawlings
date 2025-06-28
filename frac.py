import turtle

def draw_fractal_star(size, t):
    """
    Recursively draws a fractal star.

    Args:
        size (int): The size of the current star's side.
        t (turtle.Turtle): The turtle object to draw with.
    """
    if size < 10:
        # Base case: if the size is too small, just draw a line and stop
        t.forward(size)
        return

    # A star has 5 points
    for _ in range(5):
        # Move forward to draw one side of the point
        t.forward(size)

        # Recursively call the function to draw a smaller star at the tip
        # We reduce the size by a factor (e.g., 2.5) for the next level
        draw_fractal_star(size / 2.5, t)

        # Move back to the center of the current star
        t.backward(size)

        # Turn to draw the next point of the star.
        # 144 degrees is the external angle of a 5-pointed star.
        t.right(144)


def main():
    """
    Main function to set up the turtle environment and start the drawing.
    """
    # --- Screen Setup ---
    screen = turtle.Screen()
    screen.bgcolor("black")
    screen.title("Fractal Star")

    # --- Turtle Setup ---
    t = turtle.Turtle()
    t.speed(0)  # Set speed to maximum
    t.color("yellow")
    t.hideturtle()

    # --- Initial Positioning ---
    t.penup()
    t.goto(-100, 50) # Position the turtle to start
    t.pendown()

    # --- Start Drawing ---
    initial_size = 200
    draw_fractal_star(initial_size, t)

    # --- Finish ---
    screen.exitonclick()

if __name__ == "__main__":
    main()
