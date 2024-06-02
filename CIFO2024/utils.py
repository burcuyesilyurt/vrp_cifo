
import matplotlib.pyplot as plt
from read_data import data
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import math
import os



def euclidean_distance(a, b):
    ax, ay = float(a[2]), float(a[3])
    bx, by = float(b[2]), float(b[3])
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def plot_vrp_solution(routes, all_points):
    fig, ax = plt.subplots(figsize=(12, 8))

    colors = ['black', 'red', 'blue', 'green', 'orange', 'purple']  # Lista de colores para diferentes rutas
    depot_img = plt.imread(os.path.join('CIFO2024', 'images/depot.png'))
    battery_img = plt.imread(os.path.join('CIFO2024', 'images/battery.png'))
    box_img = plt.imread(os.path.join('CIFO2024', 'images/box.png'))

    def add_image(ax, img, xy, zoom=0.1):
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, xy, frameon=False)
        ax.add_artist(ab)

    def get_image_type(point):
        if point[1] == 'f':
            return battery_img
        elif point[1] == 'd':
            return depot_img
        else:
            return box_img

    for route_idx, route in enumerate(routes):
        if not route:
            continue
        route = [0] + route + [0]  # Añadir el depósito al inicio y al final de cada ruta
        x_coords = [all_points[i][2] for i in route]
        y_coords = [all_points[i][3] for i in route]

        color = colors[route_idx % len(colors)]  # Seleccionar color para la ruta

        ax.plot(x_coords, y_coords, 'o--', linewidth=2, markersize=8, linestyle='--', label=f'Ruta {route_idx+1}', color=color)

        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            img = get_image_type(all_points[route[i]])
            if img is not depot_img:
                add_image(ax, img, (x, y), zoom=0.1)

        for i in range(len(x_coords) - 1):
            ax.annotate('', xy=(x_coords[i + 1], y_coords[i + 1]), xytext=(x_coords[i], y_coords[i]),
                        arrowprops=dict(arrowstyle='->', color=color, lw=2))

        for i, (x, y) in enumerate(zip(x_coords, y_coords)):
            img = get_image_type(all_points[route[i]])
            if img is depot_img:
                add_image(ax, img, (x, y), zoom=0.1)

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
    #all_points = [d0] + data
    all_points = data

    plot_vrp_solution(routes, all_points)
