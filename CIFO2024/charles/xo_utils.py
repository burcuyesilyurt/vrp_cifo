from copy import copy, deepcopy
from random import randint


def flatten_routes(individual):
    """
    Flat the individual representation from 2D-array to 1D-array,
    splitting the routes around 0s.

     For instance, the individual [[1,2][3,4]] will be flattened to [0,1,2,0,0,3,4,0]
    """
    flattened_parent = []
    for route in individual:
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

    current_route = []
    for i in flat_offspring:
        if i == 0:
            offspring.append(current_route)
            current_route = []
        else:
            current_route.append(i)

    return offspring


def repair_pickup(offspring, data):
    """
    This function repairs the offspring by putting the delivery right after the pickup.

    :param offspring:
    :param data:
    :return:
    """
    result = []
    for idx, e in enumerate(offspring):
        if data[e][1] != 'cp' and data[e][1] != 'cd':
            result.append(e)
        else:
            for j in range(len(offspring)):
                if data[offspring[j]][1] == 'cd' and data[offspring[j]][8] == data[e][0]:
                    # Put the delivery right after the pickup
                    result.append(e)
                    result.append(offspring[j])
                    break

    return result



def repair_pickup_randomly(offspring, data):
    pass


def fill_missing_pickups(offspring, data):
    pickups_by_id = {data[i][0]: i for i in offspring if data[i][1] == 'cp'}
    all_pickups_by_id = {data[i][0]: i for i in range(len(data)) if data[i][1] == 'cp'}

    result = deepcopy(offspring)
    for idx, i in enumerate(offspring):
        if data[i][1] == 'cd' and data[i][8] not in pickups_by_id.keys():
            result.insert(idx, all_pickups_by_id[data[i][8]])
        else:
            # Both pickup and delivery are missing, add the pickup randomly.
            # The deliveries will be added next in the fill_missing_deliveries function
            if idx == len(offspring) - 1:
                missing_pickups = set(all_pickups_by_id.values()).difference(set(pickups_by_id.values()))
                for pickup in missing_pickups:
                    random_index = randint(0, len(offspring) - 1)
                    result.insert(random_index, pickup)

    return result


def fill_missing_deliveries(offspring, data):
    deliveries_by_id = {data[i][0]: i for i in offspring if data[i][1] == 'cd'}
    all_deliveries_by_id = {data[i][0]: i for i in range(len(data)) if data[i][1] == 'cd'}

    result = deepcopy(offspring)
    for i in offspring:
        if data[i][1] == 'cp' and data[i][8] not in deliveries_by_id.keys():
            result.insert(offspring.index(i)+1, all_deliveries_by_id[data[i][8]])

    return result

def fill_missing_pickups_randomly(offspring, data):
    pass


def fill_missing_deliveries_randomly(offspring, data):
    pass


def remove_duplicates(offspring):
    """
    Remove duplicates of the offspring, only keeping the first occurence
    of each element. Zeroes are not considered and all zeroes are kept.
    """
    visited_elements = set()
    result = []
    for i in offspring:
        if i not in visited_elements or i == 0:
            result.append(i)
            visited_elements.add(i)

    return result
