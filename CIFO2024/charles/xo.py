import random
from copy import copy, deepcopy
from random import randint, sample, uniform

from CIFO2024.charles.xo_utils import flatten_routes, reconstruct_routes, fill_missing_pickups, fill_missing_deliveries, remove_duplicates, repair_pickup


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
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)

    flat_offspring1, flat_offspring2 = cycle_xo(flat_parent1, flat_parent2)

    # Reconstruct routes for both offspring
    offspring1 = reconstruct_routes(flat_offspring1)
    offspring2 = reconstruct_routes(flat_offspring2)

    return offspring1, offspring2

def vrp_single_point_xo(data):

    def my_single_point_xo(parent1, parent2):
        assert len(parent1) == len(parent2)
        crossover_point = randint(0, len(parent1)-1)
        p1 = deepcopy(parent1)
        p2 = deepcopy(parent2)
        offspring1 = p1[:crossover_point] + p2[crossover_point:]
        offspring2 = p2[:crossover_point] + p1[crossover_point:]

        return offspring1, offspring2

    def xo(parent1, parent2):
        offspring1, offspring2 = my_single_point_xo(parent1, parent2)

        flat_offspring1 = flatten_routes(offspring1)
        flat_offspring2 = flatten_routes(offspring2)

        offspring1_repaired = repair_pickup(flat_offspring1, data)
        offspring1_w_pickups = fill_missing_pickups(offspring1_repaired, data)
        offspring1_w_deliveries = fill_missing_deliveries(offspring1_w_pickups, data)
        offspring1_no_duplicates = remove_duplicates(offspring1_w_deliveries)

        offspring2_repaired = repair_pickup(flat_offspring2, data)
        offspring2_w_pickups = fill_missing_pickups(offspring2_repaired, data)
        offspring2_w_deliveries = fill_missing_deliveries(offspring2_w_pickups, data)
        offspring2_no_duplicates = remove_duplicates(offspring2_w_deliveries)

        offspring1_final = reconstruct_routes(offspring1_no_duplicates)
        offspring2_final = reconstruct_routes(offspring2_no_duplicates)

        return offspring1_final, offspring2_final

    return xo


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
    offspring = [2, 3, 0, 5, 4, 0, 2, 5, 0]
    # Todo this doesn't work if both pickup and delivery is missing in the offspring
    print(fill_missing_deliveries(fill_missing_pickups(offspring, data), data))

