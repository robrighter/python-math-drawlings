import turtle

def create_l_system(iterations, axiom, rules):
    """
    Generates the final string for the L-system.

    Args:
        iterations (int): The number of times to apply the rules.
        axiom (str): The starting string.
        rules (dict): A dictionary of rules to apply.

    Returns:
        str: The final generated string after all iterations.
    """
    start_string = axiom
    if iterations == 0:
        return axiom
    end_string = ""
    for _ in range(iterations):
        end_string = "".join(rules.get(character, character) for character in start_string)
        start_string = end_string

    return end_string


def draw_l_system(t, instructions, angle, distance):
    """
    Instructs the turtle to draw the L-system fractal based on an instruction string.

    Args:
        t (turtle.Turtle): The turtle object.
        instructions (str): The string generated by the L-system.
        angle (float): The angle to turn for '+' and '-' commands.
        distance (float): The distance to move for 'F' commands.
    """
    # Stack to save turtle's position and heading
    stack = []
    for cmd in instructions:
        if cmd == 'F':
            # Move turtle forward
            t.forward(distance)
        elif cmd == 'B':
            # Move turtle backward
            t.backward(distance)
        elif cmd == '+':
            # Turn turtle right
            t.right(angle)
        elif cmd == '-':
            # Turn turtle left
            t.left(angle)
        elif cmd == '[':
            # Push current state (position and heading) onto the stack
            pos = t.position()
            head = t.heading()
            stack.append((pos, head))
        elif cmd == ']':
            # Pop state from the stack and restore it
            pos, head = stack.pop()
            t.penup()
            t.setposition(pos)
            t.setheading(head)
            t.pendown()

def draw(t):
    """
    Defines the L-system and draws the fractal.

    Args:
        t (turtle.Turtle): The turtle object to draw with.
    """
    # --- Define L-System Parameters ---
    # You can change these to create different fractals!
    axiom = "F"
    rules = {
        "F": "F[+F]F[-F]F"
    }
    iterations = 4
    angle = 25
    distance = 5

    # --- Position the Turtle ---
    screen = t.getscreen()
    t.penup()
    t.left(90) # Point the turtle upwards
    t.setposition(0, -screen.window_height() / 2 + 50)
    t.pendown()

    # --- Generate and Draw ---
    # 1. Generate the full instruction string
    instructions = create_l_system(iterations, axiom, rules)

    # 2. Draw the fractal based on the instructions
    print(f"Drawing L-System with {len(instructions)} commands...")
    draw_l_system(t, instructions, angle, distance)
    print("Drawing complete.")


def main():
    """Main function to set up the window and turtle, then start the drawing."""
    # --- Setup Turtle ---
    screen = turtle.Screen()
    screen.setup(width=800, height=800)
    #screen.bgcolor("black")

    t = turtle.Turtle()
    t.speed(0)  # 0 is the fastest speed
    #t.color("green")
    t.hideturtle()
    t.pensize(1)

    # --- Start Drawing ---
    draw(t)

    # Keep the window open until it's clicked
    screen.exitonclick()


if __name__ == "__main__":
    main()
