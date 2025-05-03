import matplotlib.pyplot as plt
import numpy as np

def trigonometric_fractal(c, max_iter):
    """
    Checks if a complex number c belongs to the Trigonometric Fractal set.

    Parameters:
    c (complex): The complex number to check.
    max_iter (int): Maximum iterations.

    Returns:
    int: Iteration count before escape, or max_iter if bounded.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = np.sin(z) + np.cos(c)  # Trigonometric iteration
        n += 1
    return n

def display_trigonometric_fractal(width, height, max_iter):
    """
    Displays the Trigonometric Fractal using matplotlib, zoomed in to the specified range.

    Parameters:
    width (int): Image width.
    height (int): Image height.
    max_iter (int): Maximum iterations.
    """
    image = np.zeros((height, width))
    x_min, x_max = 1.0, 2.0  # Zoomed in Real axis range
    y_min, y_max = -0.5, 0.5  # Zoomed in Imaginary axis range

    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_max, y_min, height)

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            iteration_count = trigonometric_fractal(c, max_iter)
            image[i, j] = iteration_count

    plt.figure(figsize=(8, 8))
    plt.imshow(image, extent=[x_min, x_max, y_min, y_max], cmap='viridis')
    plt.title('Trigonometric Fractal Set (Zoomed In)')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.colorbar(label='Iteration Count')
    plt.show()

if __name__ == '__main__':
    image_width = 500
    image_height = 500
    max_iterations = 100
    display_trigonometric_fractal(image_width, image_height, max_iterations)