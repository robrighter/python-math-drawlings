import matplotlib.pyplot as plt
import numpy as np

def koch_curve(points, depth):
    """
    Recursively generates points for the Koch Curve.

    Parameters:
    points (list): A list of two points representing the initial line segment [(x0, y0), (x1, y1)].
    depth (int): The recursion depth, controlling the level of detail of the curve.

    Returns:
    list: A list of points representing the Koch Curve at the given depth.
    """
    if depth == 0:
        return points

    start_point = np.array(points[0])
    end_point = np.array(points[1])

    delta = end_point - start_point

    point1 = start_point + delta / 3
    point2 = end_point - delta / 3

    # Calculate the coordinates of the triangle point using rotation
    v = point2 - point1
    rotation_matrix = np.array([[np.cos(np.pi/3), -np.sin(np.pi/3)],
                                [np.sin(np.pi/3), np.cos(np.pi/3)]]) # 60 degrees rotation
    point_triangle = point1 + rotation_matrix @ v


    segment1 = [start_point, point1]
    segment2 = [point1, point_triangle]
    segment3 = [point_triangle, point2]
    segment4 = [point2, end_point]

    # Recursively generate Koch Curve for each segment
    koch_segment1 = koch_curve(segment1, depth-1)
    koch_segment2 = koch_curve(segment2, depth-1)
    koch_segment3 = koch_curve(segment3, depth-1)
    koch_segment4 = koch_curve(segment4, depth-1)

    # Combine the points, excluding the repeated endpoints to form a continuous curve
    return koch_segment1[:-1] + koch_segment2[:-1] + koch_segment3[:-1] + koch_segment4


def display_koch_curve(depth):
    """
    Displays the Koch Curve using matplotlib.

    Parameters:
    depth (int): The recursion depth for the Koch Curve.
    """
    initial_points = [(0, 0), (1, 0)] # Start with a horizontal line from (0,0) to (1,0)
    koch_points = koch_curve(initial_points, depth)

    x_coords = [point[0] for point in koch_points]
    y_coords = [point[1] for point in koch_points]

    plt.figure(figsize=(8, 8)) # Adjust figure size for better visualization
    plt.plot(x_coords, y_coords, linewidth=1) # Adjust linewidth for line thickness
    plt.title(f'Koch Curve - Depth {depth}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.gca().set_aspect('equal', adjustable='box') # Ensure equal aspect ratio for correct shape
    plt.grid(False) # Turn off grid for cleaner look
    plt.show()


if __name__ == '__main__':
    curve_depth = 14  # You can change the depth to control the complexity
    display_koch_curve(curve_depth)