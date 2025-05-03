import turtle
import math


def draw_square(t, size):
    """Draw a square with given side length"""
    for _ in range(4):
        t.forward(size)
        t.right(90)


def draw_circle(t, radius):
    """Draw a circle with given radius"""
    # Circle is drawn using 360 small steps
    t.circle(radius)

def poly(t, side, angle):
    turn=0
    while True:
        t.forward(side)
        t.right(angle)
        turn=turn+angle
        if turn%360==0:
            break


def new_poly(t, side, angle):
    turn=0
    while True:
        t.forward(side)
        t.right(angle)
        t.forward(side)
        t.right(2 * angle)
        turn = turn + (angle *3)
        if turn%360 == 0:
            break

def poly_roll(t, side, angle1, angle2):
    turn=0
    while True:
        poly(t, side, angle1)
        t.right(angle2)
        turn = turn + angle2
        if turn%360==0:
            break


def poly_spi(t, side, angle, inc ):
    t.forward(side)
    dot(t)
    t.right(angle)
    poly_spi(t, side+inc, angle, inc)


def dot(t):
    t.pendown()
    t.dot(6)
    t.penup()

def main():
    # Create and set up the turtle
    t = turtle.Turtle()
    t.speed(20)  # Slightly faster than before



    #t.penup()
    #poly_spi(t,5,456, 5)
    #poly(t, 1, 1)
    # Move to a new position without drawing
    t.penup()
    t.goto(-150, 0)
    t.pendown()

    poly_roll(t, 100, 85, 20)

    # Keep the window open
    turtle.done()


if __name__ == "__main__":
    main()