import turtle as t
import math

start_point = (0, 0)
end_point = (200, 165)

def draw_bell_curve(start, end, magnitude, turt, steps=100):
    x0, y0 = start
    x1, y1 = end
    for i in range(steps + 1):
        t_ = i / steps
        # Linear interpolation for x and y
        x = x0 + (x1 - x0) * t_
        y = y0 + (y1 - y0) * t_
        # Bell curve offset (Gaussian)
        bell = magnitude * math.exp(-((t_ - 0.5) ** 2) / 0.02)
        # Perpendicular direction
        dx = x1 - x0
        dy = y1 - y0
        length = math.hypot(dx, dy)
        if length == 0:
            perp_x, perp_y = 0, 0
        else:
            perp_x = -dy / length
            perp_y = dx / length
        x += bell * perp_x
        y += bell * perp_y
        if i == 0:
            turt.penup()
            turt.goto(x, y)
            turt.pendown()
        else:
            turt.goto(x, y)
    
def draw(turt):
    n = 20
    c1 = 2
    c2 = 0.8
    c3 = 5
    a = 1.06
    b = -1.3
    d = 10
    function1 = lambda x: a * math.pow(x, c1)
    function2 = lambda x: b * math.pow(c2, x)
    function3 = lambda x: d * math.sin(x + c3)
    combination = lambda x: function1(x) + function2(x)
    for i in range(1, n, 1):
        draw_bell_curve(start_point, end_point, combination(i), turt, steps=100*i)
        draw_bell_curve(start_point, end_point, -1 * combination(i), turt, steps=100*i)