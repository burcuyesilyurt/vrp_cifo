import random
from copy import copy
from random import randint, sample, uniform


def single_point_xo(parent1, parent2):
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1)-1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2


def pmx(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(p1)), 2)
    #xo_points = [3,6]
    xo_points.sort()

    def pmx_offspring(x, y):
        o = [None] * len(x)
        # offspring2
        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]]
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            while o[index] is not None:
                temp = index
                index = y.index(x[temp])
            o[index] = i

        # numbers that doesn't exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o

    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2


def geo_xo(p1,p2):
    """Implementation of arithmetic crossover/geometric crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individual: Offspring, resulting from the crossover.
    """
    o = [None] * len(p1)
    for i in range(len(p1)):
        r = uniform(0,1)
        o[i] = p1[i] * r + (1-r) * p2[i]
    return o


def vrp_pmx(parent1, parent2):
    def flatten_routes(parent):
        flattened_parent = []
        for route in parent:
            flattened_parent.append(0)
            if len(route) == 0:
                flattened_parent.append(0)
            else:
                for i, locality in enumerate(route):
                    flattened_parent.append(locality)
                    if i == len(route) - 1:
                        flattened_parent.append(0)

        return flattened_parent

    def reconstruct_routes(flat_offspring):
        offspring = []

        current_route = None
        for i in flat_offspring:
            if i == 0:
                if current_route is None:
                    current_route = []
                else:
                    offspring.append(current_route)
                    current_route = None
            else:
                current_route.append(i)

        return offspring

    # Flatten the routes of both parents
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)

    flat_offspring1, flat_offspring2 = cycle_xo(flat_parent1, flat_parent2)

    # Reconstruct routes for both offspring
    offspring1 = reconstruct_routes(flat_offspring1)
    offspring2 = reconstruct_routes(flat_offspring2)

    return offspring1, offspring2

if __name__ == "__main__":
    #p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    #p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    #p1, p2 = [9,8,4,5,6,7,1,3,2,10], [8,7,1,2,3,10,9,5,4,6]
    #o1, o2 = pmx(p1, p2)

    #p1 = [0, 5, 4, 3, 0, 2, 0, 1, 6, 0]
    #p2 = [0, 1, 0, 3, 2, 0, 5, 4, 6, 0]
    #o1, o2 = pmx(p1, p2)

    p1 = [[1, 2], [4, 3], []]
    p2 = [[4, 2], [3], [1]]
    o1, o2 = vrp_pmx(p1, p2)
    print(o1)
    print(o2)