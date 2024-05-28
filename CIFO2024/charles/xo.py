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


def order_xo(parent1, parent2):
    def flatten_routes(parent):
        return [customer for route in parent for customer in route if customer != 0]

    def can_add_to_route(route, customer):
        # Assuming this function checks capacity and time windows
        return True

    def order_crossover(flat_parent1, flat_parent2):
        # Choose crossover points
        pt1, pt2 = sorted(random.sample(range(len(flat_parent1)), 2))

        # Create offspring with None placeholders
        offspring_flat = [None] * len(flat_parent1)

        # Copy segment from the first parent to the offspring
        offspring_flat[pt1:pt2+1] = flat_parent1[pt1:pt2+1]

        # Fill the remaining positions with customers from the second parent in order
        current_pos = (pt2 + 1) % len(flat_parent1)
        for customer in flat_parent2:
            if customer not in offspring_flat:
                while offspring_flat[current_pos] is not None:
                    current_pos = (current_pos + 1) % len(flat_parent1)
                offspring_flat[current_pos] = customer

        return offspring_flat

    def reconstruct_routes(flat_offspring):
        offspring = []
        route = [0]
        for customer in flat_offspring:
            if can_add_to_route(route, customer):  # Assuming can_add_to_route checks capacity and time windows
                route.append(customer)
            else:
                route.append(0)
                offspring.append(route)
                route = [0, customer]
        route.append(0)
        offspring.append(route)

        return offspring

    # Flatten the routes of both parents
    flat_parent1 = flatten_routes(parent1)
    flat_parent2 = flatten_routes(parent2)

    # Create two offspring using the order crossover technique
    #flat_offspring1 = order_crossover(flat_parent1, flat_parent2)
    #flat_offspring2 = order_crossover(flat_parent2, flat_parent1)

    flat_offspring1, flat_offspring2 = single_point_xo(flat_parent1, flat_parent2)

    # Reconstruct routes for both offspring
    offspring1 = reconstruct_routes(flat_offspring1)
    offspring2 = reconstruct_routes(flat_offspring2)

    return offspring1, offspring2

if __name__ == "__main__":
    #p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    #p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    #p1, p2 = [9,8,4,5,6,7,1,3,2,10], [8,7,1,2,3,10,9,5,4,6]
    #o1, o2 = pmx(p1, p2)
    p1 = [[1, 2], [4, 3], []]
    p2 = [[4, 2], [3], [1]]

    o1, o2 = order_xo(p1, p2)
    print(o1)
    print(o2)