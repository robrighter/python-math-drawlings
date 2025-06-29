import turtle
import math

# --- Configuration ---
# You can change these values to alter the appearance of the drawing.

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PEN_SIZE = 1
LINE_SPACING = 5       # Distance between each horizontal line
AMPLITUDE = 35         # The height of the wave in the middle
FREQUENCY = 0.02       # How tight or loose the wave is
WAVE_WIDTH_FACTOR = 0.47 # The portion of the screen width the wave will cover (0.0 to 1.0)
PHASE_SHIFT = math.pi / 2         # Horizontal shift of the wave. Try math.pi / 2 for a 90-degree shift.


# --- Drawing Function ---
def draw(pen):
    """Draws the wavy line pattern using the provided turtle object."""
    # 1. Calculate drawing boundaries
    start_y = (SCREEN_HEIGHT // 2) - 50
    end_y = -((SCREEN_HEIGHT // 2) - 50)
    wave_zone_width = SCREEN_WIDTH * WAVE_WIDTH_FACTOR
    wave_start_x = -wave_zone_width / 2
    wave_end_x = wave_zone_width / 2

    # 2. Main drawing loop
    # Iterate from the top to the bottom of the canvas
    current_y = start_y
    while current_y >= end_y:
        pen.penup()
        # Start each line at the left edge.
        # Calculate the y-offset at the start of the wave to connect the first straight line segment.
        start_y_offset = AMPLITUDE * math.sin((wave_start_x - wave_start_x) * FREQUENCY + PHASE_SHIFT)
        start_y_level = current_y + start_y_offset
        pen.goto(-SCREEN_WIDTH / 2, start_y_level)
        pen.pendown()

        # Calculate the y-offset at the very end of the wave section.
        # This will be the new straight line level after the wave.
        end_y_offset = AMPLITUDE * math.sin((wave_end_x - wave_start_x) * FREQUENCY + PHASE_SHIFT)
        final_y_level = current_y + end_y_offset

        # Draw a single continuous line across the screen
        for x in range(-SCREEN_WIDTH // 2, SCREEN_WIDTH // 2):
            # Check which part of the line we are drawing
            if x <= wave_start_x:
                # Part 1: The straight line leading up to the wave.
                # This line connects to the first point of the wave.
                pen.goto(x, start_y_level)
            elif wave_start_x < x < wave_end_x:
                # Part 2: The sine wave itself.
                # Calculate the sine wave offset from the base y-level, including the phase shift.
                y_offset = AMPLITUDE * math.sin((x - wave_start_x) * FREQUENCY + PHASE_SHIFT)
                pen.goto(x, current_y + y_offset)
            else: # x >= wave_end_x
                # Part 3: The straight line after the wave.
                # This line is drawn at the same y-level as the wave's last point.
                pen.goto(x, final_y_level)

        # Move to the next line position
        current_y -= LINE_SPACING

def main():
    """Sets up the screen and turtle, then runs the drawing."""
    # 1. Set up the screen
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Wavy Lines Pattern")

    # Turn off automatic screen updates for maximum drawing speed
    screen.tracer(0)

    # 2. Set up the turtle (the pen)
    pen = turtle.Turtle()
    pen.hideturtle()  # We don't need to see the turtle icon
    pen.pensize(PEN_SIZE)
    pen.speed(0)      # Set speed to fastest

    # 3. Execute the drawing
    draw(pen)

    # 4. Update the screen to show the final drawing
    screen.update()

    # 5. Keep the window open until it's closed manually
    turtle.done()

# --- Main Program Execution ---
if __name__ == "__main__":
    main()
