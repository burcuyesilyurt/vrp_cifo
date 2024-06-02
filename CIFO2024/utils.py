import matplotlib.pyplot as plt
from read_data import data
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import math
import os

def euclidean_distance(a, b):
    """
    Calculates the Euclidean distance between two points.

    Args:
        a (tuple): Tuple containing information about the first point (id, type, x, y).
        b (tuple): Tuple containing information about the second point (id, type, x, y).

    Returns:
        float: The Euclidean distance between the two points.
    """
    ax, ay = float(a[2]), float(a[3])
    bx, by = float(b[2]), float(b[3])
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)

def plot_vrp_solution(routes, all_points):
    """
    Plots the VRP solution paths.

    Args:
        routes (list): List of routes, where each route is represented as a list of point IDs.
        all_points (list): List of all points, each represented as a tuple (id, type, x, y).
    """
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = ['black', 'red', 'blue', 'green', 'orange', 'purple']  # Colors for the routes
    # add images for depot, battery and box
    depot_img = plt.imread(os.path.join('CIFO2024', 'images/depot.png'))
    battery_img = plt.imread(os.path.join('CIFO2024', 'images/battery.png'))
    box_img = plt.imread(os.path.join('CIFO2024', 'images/box.png'))

    def add_image(ax, img, xy, zoom=0.1):
        """
        Adds an image to the plot at specified coordinates.

        Args:
            ax: The Axes object to which the image will be added.
            img: The image to be added.
            xy (tuple): Coordinates (x, y) where the image will be placed.
            zoom (float): Zoom factor for the image (default is 0.1).
        """
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, xy, frameon=False)
        ax.add_artist(ab)

    def get_image_type(point):
        """
        Determines the image type based on the point type.

        Args:
            point (tuple): Tuple containing information about a point (id, type, x, y).

        Returns:
            numpy.ndarray: The image corresponding to the point type.
        """
        if point[1] == 'f':
            return battery_img
        elif point[1] == 'd':
            return depot_img
        else:
            return box_img
    # plot the routes
    for route_idx, route in enumerate(routes):
        if not route:
            continue
        route = [0] + route + [0]  # Add depot to the beginning and end of the routes
        x_coords = [all_points[i][2] for i in route]
        y_coords = [all_points[i][3] for i in route]

        color = colors[route_idx % len(colors)]  # select color for the route

        ax.plot(x_coords, y_coords, 'o--', linewidth=2, markersize=8, linestyle='--', label=f'Ruta {route_idx+1}', color=color)
        # add images (except depot)
        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            img = get_image_type(all_points[route[i]])
            if img is not depot_img:
                add_image(ax, img, (x, y), zoom=0.1)
        # add arrows
        for i in range(len(x_coords) - 1):
            ax.annotate('', xy=(x_coords[i + 1], y_coords[i + 1]), xytext=(x_coords[i], y_coords[i]),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))
        # add depot image
        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            img = get_image_type(all_points[route[i]])
            if img is depot_img:
                add_image(ax, img, (x, y), zoom=0.1)
        # add ids
        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            ax.text(x, y, f'{route[i]}', fontsize=12, ha='right', va='bottom')

    ax.set_title('VRP Solution Paths', fontsize=16)
    ax.set_xlabel('X Coordinate', fontsize=14)
    ax.set_ylabel('Y Coordinate', fontsize=14)

    ax.legend()
    ax.grid(True)
    ax.set_facecolor('#f7f7f7')

    plt.show()

if __name__ == "__main__":
    routes = [[], [], [], [12, 15], [], [], [], [], [], [], [19, 8], [], [], [], [], [], [], [], [], [9, 10], [], [], [], [], [], [7, 20], [], [], [], [], [21, 14, 13, 18, 16, 17], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [6, 11], [], [], [], [], [], [], [], [], [], []]
    all_points = data

    plot_vrp_solution(routes, all_points)
