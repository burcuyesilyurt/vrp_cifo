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


def repair_pickup(offspring, data):
    """
    This function repairs the offspring by putting the delivery right after the pickup.

    :param offspring:
    :param data:
    :return:
    """
    for i in offspring:
        if data[i][1] == 'cp':
            for j in range(len(offspring)):
                if data[offspring[j]][1] == 'cd' and data[offspring[j]][8] == data[i][0]:
                    # Put the delivery right after the pickup
                    offspring.insert(offspring.index(i)+1, offspring[j])
                    del offspring[j+1]
                    break

    return offspring

def repair_pickup_randomly(offspring, data):
    pass

def fill_missing_pickups(offspring, data):
    pass

def fill_missing_pickups_randomly(offspring, data):
    pass

def fill_missing_deliveries(offspring, data):
    pass

def fill_missing_deliveries_randomly(offspring, data):
    pass
