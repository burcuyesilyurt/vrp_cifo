
#import matplotlib.pyplot as plt
#from read_data import data, d0
#import matplotlib.image as mpimg
#from matplotlib.offsetbox import OffsetImage, AnnotationBbox

import math



def euclidean_distance(a, b):
    ax, ay = float(a[2]), float(a[3])
    bx, by = float(b[2]), float(b[3])
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)


def plot_vrp_solution(solution, all_points):
    x_coords = [all_points[i][2] for i in solution]
    y_coords = [all_points[i][3] for i in solution]

    fig, ax = plt.subplots(figsize=(12, 8))

    ax.plot(x_coords, y_coords, 'o--', linewidth=2, markersize=8, label='Path', color='black')

    def add_image(ax, img, xy, zoom=0.1):
        imagebox = OffsetImage(img, zoom=zoom)
        ab = AnnotationBbox(imagebox, xy, frameon=False)
        ax.add_artist(ab)

    depot_img = plt.imread('depot.png')
    battery_img = plt.imread('battery.png')
    box_img = plt.imread('box.png')

    def get_image_type(point):
        if point[1] == 'f':
            return battery_img
        elif point[1] == 'd':
            return depot_img
        else:
            return box_img

    for i, (x, y) in enumerate(zip(x_coords, y_coords)):
        img = get_image_type(all_points[solution[i]])
        if img is not depot_img:
            add_image(ax, img, (x, y), zoom=0.1)

    for i in range(len(x_coords)-1):
        ax.annotate('', xy=(x_coords[i+1], y_coords[i+1]), xytext=(x_coords[i], y_coords[i]),
                    arrowprops=dict(arrowstyle='->', color='black', lw=2))

    for i, (x, y) in enumerate(zip(x_coords, y_coords)):
        img = get_image_type(all_points[solution[i]])
        if img is depot_img:
            add_image(ax, img, (x, y), zoom=0.1)

    for i, (x, y) in enumerate(zip(x_coords, y_coords)):
        ax.text(x, y, f'{solution[i]}', fontsize=12, ha='right', va='bottom')

    ax.set_title('VRP Solution Path', fontsize=16)
    ax.set_xlabel('X Coordinate', fontsize=14)
    ax.set_ylabel('Y Coordinate', fontsize=14)

    ax.legend()
    ax.grid(True)
    ax.set_facecolor('#f7f7f7')

    plt.show()




# solution = [0, 7, 3, 1, 6, 5, 2, 8, 4]
# all_points =  [d0] + data
#
# plot_vrp_solution(solution, all_points)

