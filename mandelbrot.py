import matplotlib.pyplot as plt
import numpy as np

def mandelbrot(c, max_iter):
    """
    Checks if a complex number c is in the Mandelbrot set.

    Parameters:
    c (complex): The complex number to check.
    max_iter (int): The maximum number of iterations.

    Returns:
    int: The number of iterations before the sequence escapes, or max_iter if it doesn't escape.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n

def display_mandelbrot(width, height, max_iter):
    """
    Displays the Mandelbrot set using matplotlib.

    Parameters:
    width (int): The width of the image in pixels.
    height (int): The height of the image in pixels.
    max_iter (int): The maximum number of iterations for the Mandelbrot calculation.
    """
    image = np.zeros((height, width))
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5

    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_max, y_min, height) # y_max to y_min to orient the image correctly

    for i in range(height):
        for j in range(width):
            c = complex(x[j], y[i])
            iteration_count = mandelbrot(c, max_iter)
            image[i, j] = iteration_count

    plt.imshow(image, extent=[x_min, x_max, y_min, y_max], cmap='magma') # 'magma' colormap for visualization
    plt.title('Mandelbrot Set')
    plt.xlabel('Re(c)')
    plt.ylabel('Im(c)')
    plt.colorbar(label='Iteration Count') # Add a colorbar to show iteration count meaning
    plt.show()

if __name__ == '__main__':
    image_width = 500
    image_height = 500
    max_iterations = 100
    display_mandelbrot(image_width, image_height, max_iterations)