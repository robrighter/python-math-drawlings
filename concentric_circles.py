import turtle as t
import math as m

CIRCLES = 60
BASE_RADIUS = 20
INCREMENT = 5
PATH_CIRCLE_RADIUS = 10

def draw(turt):
    radius = BASE_RADIUS
    meta_radius = 0
    phase = 3
    for i in range(CIRCLES):
        turt.penup()
        turt.goto(0, -radius - meta_radius)
        turt.pendown()
        turt.circle(radius, steps=1000)
        radius += INCREMENT
        if meta_radius > PATH_CIRCLE_RADIUS:
            phase = -phase
        elif meta_radius < -PATH_CIRCLE_RADIUS:
            phase = -phase
        meta_radius += phase

def main():
    t.setup(600, 600)
    t.title("Circles")
    t.speed(0)
    t.delay(0)
    draw(t)
    t.done()

if __name__ == "__main__":
    main()