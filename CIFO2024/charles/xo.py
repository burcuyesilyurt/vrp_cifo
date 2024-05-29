import random
from copy import copy
from random import randint, sample, uniform

from CIFO2024.charles.xo_utils import flatten_routes, reconstruct_routes


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
            count = 0
            while o[index] is not None and count < 50:
                temp = index
                index = y.index(x[temp])
                count += 1
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

    # Flatten the routes of both parents
    flat_parent1 = flatten_routes2(parent1)
    flat_parent2 = flatten_routes2(parent2)

    flat_offspring1, flat_offspring2 = pmx(flat_parent1, flat_parent2)

    # Reconstruct routes for both offspring
    #offspring1 = reconstruct_routes(flat_offspring1)
    #offspring2 = reconstruct_routes(flat_offspring2)

    offspring1 = unflatten2(flat_offspring1)
    offspring2 = unflatten2(flat_offspring2)

    offspring1_c, offspring2_c = correct_routes2(offspring1, offspring2)
    print(offspring1_c)
    print(offspring2_c)

    return offspring1_c, offspring2_c

if __name__ == "__main__":
    #p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    #p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    #p1, p2 = [9,8,4,5,6,7,1,3,2,10], [8,7,1,2,3,10,9,5,4,6]
    #o1, o2 = pmx(p1, p2)

    #p1 = [0, 5, 4, 3, 0, 2, 0, 1, 6, 0]
    #p2 = [0, 1, 0, 3, 2, 0, 5, 4, 6, 0]
    #o1, o2 = pmx(p1, p2)

    data = [
        # 0
        ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
        # 1
        ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
        # 2
        ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
        # 3
        ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1069.0', '90.0', 'C98'],
        # 4
        ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
        # 5
        ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
        # 6
        ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
    ]

    offspring1 = [0, 6, 5, 0, 0, 4, 2, 0, 0, 1, 3, 0]

    rp = repair_pickup(offspring1, data)


def flatten_routes2(parent):
    result = []
    for i in range(len(parent)):
        par = parent[i]
        if len(par) == 0:
            result.append(0)
        else:
            for j in par:
                result.append(j)
            result.append(0)
    return result


def unflatten2(parent):
    result = []

    par = parent
    r = []
    for i in range(len(par)):
        if i == 0:
            if par[i] != 0:
                r.append(par[i])
        if par[i] == 0:
            result.append(r)
            r = []
        else:
            r.append(par[i])

    return result


def correct_routes2(parent1, parent2):
    p1 = []
    p2 = []
    for j in range(len(parent1)):
        if len(parent1[j]) != 0:
            p1.append(parent1[j])
    for j in range(len(parent2)):
        if len(parent2[j]) != 0:
            p2.append(parent2[j])
    while (len(p1) != len(p2)):
        if len(p1) > len(p2):
            p2.append([])
        elif len(p2) > len(p1):
            p1.append([])
    return p1, p2