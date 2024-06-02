from copy import deepcopy
from random import randint

def flatten_routes(individual):
    """
    Flattens an individual's representation from a 2D-array to a 1D-array, splitting routes around 0s.
    For example, [[1, 2], [3, 4]] will be flattened to [0, 1, 2, 0, 0, 3, 4, 0].

    Args:
        individual (list): The individual representation as a 2D-array.

    Returns:
        list: The flattened representation as a 1D-array.
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
    """
    Reconstructs an individual's representation from a flattened array back to a 2D-array.

    Args:
        flat_offspring (list): The flattened representation as a 1D-array.

    Returns:
        list: The reconstructed representation as a 2D-array.
    """
    offspring = []

    current_route = []
    for i in flat_offspring:
        if i == 0:
            offspring.append(current_route)
            current_route = []
        else:
            current_route.append(i)

    return offspring

def repair_routes(flat_offspring, data):
    """
    Repairs the offspring by placing deliveries immediately after pickups.

    Args:
        flat_offspring (list): The flattened representation of the offspring.
        data (list): List of data representing each locality.

    Returns:
        list: The repaired offspring representation.
    """
    offspring_repaired = repair_pickup(flat_offspring, data)

    offspring_w_pickups = fill_missing_pickups(offspring_repaired, data)
    offspring_w_deliveries = fill_missing_deliveries(offspring_w_pickups, data)
    offspring_no_duplicates = remove_duplicates(offspring_w_deliveries)

    return offspring_no_duplicates

def repair_routes_random(flat_offspring, data):
    """
    Repairs the offspring by placing deliveries randomly after pickups.

    Args:
        flat_offspring (list): The flattened representation of the offspring.
        data (list): List of data representing each locality.

    Returns:
        list: The repaired offspring representation.
    """
    offspring_w_pickups = fill_missing_pickups_with_random(flat_offspring, data)
    offspring_w_deliveries = fill_missing_deliveries_with_random(offspring_w_pickups, data)
    offspring_repaired = repair_pickup_with_random(offspring_w_deliveries, data)
    offspring_no_duplicates = remove_duplicates(offspring_repaired)

    return offspring_no_duplicates


def repair_pickup(offspring, data):
    """
    Repairs the offspring by placing the delivery right after the pickup.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The repaired offspring representation.
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

def repair_pickup_with_random(offspring, data):
    """
    Repairs the offspring by putting the delivery in a random position after the pickup.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The repaired offspring representation.
    """
    for i in range(len(offspring)):
        locality = offspring[i]

        if data[locality][1] == "cp":
            for j in range(i+1, len(offspring)):
                potential_delivery = offspring[j]

                if data[potential_delivery][1] == 'cd' and data[potential_delivery][8] == data[locality][0]:
                    # Find next occurrence of zero, which indicate end of current route
                    end_of_route = i + offspring[i:].index(0)

                    # if j is already in the route, do nothing
                    if i < j < end_of_route:
                        continue

                    if i+1 == end_of_route:
                        index_to_add_delivery = i+1
                    else:
                        index_to_add_delivery = randint(i+1, end_of_route)

                    offspring.insert(index_to_add_delivery, potential_delivery)
                    del offspring[j+1]

    for i in range(len(offspring)):
        locality = offspring[i]

        if data[locality][1] == "cd":
            for j in range(i + 1, len(offspring)):
                potential_pickup = offspring[j]

                if data[potential_pickup][1] == 'cp' and data[potential_pickup][8] == data[locality][0]:
                    # Find next occurrence of zero, which indicate end of current route
                    end_of_route = j + offspring[j:].index(0)

                    if j + 1 == end_of_route:
                        index_to_add_delivery = j + 1
                    else:
                        index_to_add_delivery = randint(j + 1, end_of_route)

                    offspring.insert(index_to_add_delivery, locality)
                    offspring[i] = None

    return [i for i in offspring if i is not None]

def fill_missing_pickups(offspring, data):
    """
    Fills in missing pickups in the offspring.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The offspring representation with missing pickups filled.
    """
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

def fill_missing_pickups_with_random(offspring, data):
    """
    Fills in missing pickups in the offspring with random positions.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The offspring representation with missing pickups filled randomly.
    """
    pickups_by_id = {data[i][0]: i for i in offspring if data[i][1] == 'cp'}
    all_pickups_by_id = {data[i][0]: i for i in range(len(data)) if data[i][1] == 'cp'}

    result = deepcopy(offspring)
    for idx, i in enumerate(offspring):
        if data[i][1] == 'cd' and data[i][8] not in pickups_by_id.keys():
            # NOTE: the trick here is to add it to an invalid position, so the repair will replace it randomly later
            result.insert(idx+1, all_pickups_by_id[data[i][8]])
        else:
            # Both pickup and delivery are missing, add the pickup randomly.
            # The deliveries will be added next in the fill_missing_deliveries function
            if idx == len(offspring) - 1:
                missing_pickups = set(all_pickups_by_id.values()).difference(set(pickups_by_id.values()))
                for pickup in missing_pickups:
                    random_index = randint(0, len(offspring) - 1)
                    result.insert(random_index, pickup)

    return result

def fill_missing_deliveries_with_random(offspring, data):
    """
    Fills in missing deliveries in the offspring with random positions.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The offspring representation with missing deliveries filled randomly.
    """
    deliveries_by_id = {data[i][0]: i for i in offspring if data[i][1] == 'cd'}
    all_deliveries_by_id = {data[i][0]: i for i in range(len(data)) if data[i][1] == 'cd'}

    result = deepcopy(offspring)
    for i in offspring:
        if data[i][1] == 'cp' and data[i][8] not in deliveries_by_id.keys():
            # NOTE: the trick here is to add it to an invalid position, so the repair will replace it randomly later
            result.insert(offspring.index(i), all_deliveries_by_id[data[i][8]])

    return result


def fill_missing_deliveries(offspring, data):
    """
    Fills in missing deliveries in the offspring.

    Args:
        offspring (list): The offspring representation.
        data (list): List of data representing each locality.

    Returns:
        list: The offspring representation with missing deliveries filled.
    """
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
    Removes duplicates from the offspring while keeping the first occurrence of each element.
    Zeros are not considered, and all zeroes are kept.

    Args:
        offspring (list): The offspring representation.

    Returns:
        list: The offspring representation with duplicates removed.
    """
    visited_elements = set()
    result = []
    for i in offspring:
        if i not in visited_elements or i == 0:
            result.append(i)
            visited_elements.add(i)

    return result
