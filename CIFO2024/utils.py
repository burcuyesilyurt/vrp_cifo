import math


def euclidean_distance(a, b):
    ax, ay = float(a[2]), float(a[3])
    bx, by = float(b[2]), float(b[3])
    return math.sqrt((ax - bx) ** 2 + (ay - by) ** 2)
