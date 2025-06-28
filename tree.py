import turtle
import random

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("white")

# Create turtle
tree = turtle.Turtle()
tree.hideturtle()
tree.speed(0)
tree.left(90)  # Point upwards
tree.up()
tree.goto(0, -250)
tree.down()
tree.color("black")

# Recursive function to draw tree
def draw_branch(t, branch_length, thickness):
    if branch_length < 5:
        # Draw a leaf
        t.color("pink")
        t.begin_fill()
        t.circle(2 + random.random() * 2)
        t.end_fill()
        t.color("black")
        return

    angle = random.randint(15, 30)
    shrink = random.uniform(0.65, 0.85)

    t.pensize(thickness)
    t.forward(branch_length)

    # Right branch
    t.right(angle)
    draw_branch(t, branch_length * shrink, thickness * 0.7)
    t.left(angle)

    # Left branch
    t.left(angle)
    draw_branch(t, branch_length * shrink, thickness * 0.7)
    t.right(angle)

    t.penup()
    t.backward(branch_length)
    t.pendown()

# Draw the tree
draw_branch(tree, 5, 1)

# Keep window open
screen.mainloop()
