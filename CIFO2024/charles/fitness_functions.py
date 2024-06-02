from CIFO2024.utils import euclidean_distance
from CIFO2024.read_data import *
from copy import copy


def get_fitness(data, charge):
    """
    Calculates the fitness function for the given data and charging stations.

    Args:
        data (list): List of data representing each locality.
        charge (list): List of charging stations.

    Returns:
        function: A fitness function that takes an individual as input and returns its fitness value.
    """
    def get_overall_fitness(individual):
        """
        Calculates the overall fitness of an individual.

        Args:
            individual: An individual solution representation.

        Returns:
            float: The overall fitness value of the individual.
        """
        fitness_time = 0
        number_of_cars_used = len(individual.representation)
        fitness_capacity = 0
        for route in individual.representation:
            
            if not route:
                number_of_cars_used -= 1
                continue

            fitness_time += get_fitness_time(route, data, charge)
            fitness_capacity += get_fitness_capacity(route, data)
            
        return ((fitness_time * number_of_cars_used) / 1000) + fitness_capacity

    return get_overall_fitness


def get_fitness_capacity(route, data):
    """
    Calculates the fitness related to the capacity of a route.

    Args:
        route (list): List of localities in a route.
        data (list): List of data representing each locality.

    Returns:
        float: The fitness related to the capacity of the route.
    """
    car_max_capacity = vehicle_params['Vehicle freight capacity']
    current_route_capacity = 0
    max_capacity = False

    for rep in route:
        current_route_capacity += float(data[rep][4])
        if current_route_capacity > car_max_capacity:
            max_capacity = True
            break

    if max_capacity:
        return 10000000000000000000
    else:
        return 1
    

def get_fitness_time(route, data, charging_stations):
    """
    Calculates the fitness related to the time for a route.

    Args:
        route (list): List of localities in a route.
        data (list): List of data representing each locality.
        charging_stations (list): List of charging stations.

    Returns:
        float: The fitness related to the time for the route.
    """
    # Copy route and inset 0 in the beginning and end of the route,
    # to make calculations easier without any special case
    route = copy(route)
    route.insert(0, 0)
    route.append(0)

    delay = 0
    current_time = 0
    previous_locality = -1
    battery = vehicle_params['Vehicle battery capacity']
    
    for i, rep in enumerate(route):
        ready_time = float(data[rep][5])
        due_date = float(data[rep][6])
        service_time = float(data[rep][7])

        distance = euclidean_distance(data[rep], data[previous_locality])
        battery -= distance

        # If we're already in the depot (last stop), do nothing
        if i == len(route) - 1:
            continue

        # Calculate the distance to the next locality to check if
        # the car needs to be charged or not before next locality
        next_locality = data[route[i+1]]
        next_distance = euclidean_distance(data[rep], next_locality)
        if (battery - next_distance) < 0:
            min_distance = 10000

            for charge_station in charging_stations:
                d = euclidean_distance(data[rep], charge_station)
                d += euclidean_distance(charge_station, next_locality)

                if d < min_distance:
                    min_distance = d

            distance += min_distance
            battery = vehicle_params['Vehicle battery capacity']

        current_time += distance

        # Cases where there's waiting time
        if ready_time > current_time:
            current_time = ready_time

        current_time += service_time

        # Cases where there's delay
        if due_date < current_time:
            delay += current_time - due_date

        previous_locality = rep

    return current_time * 0.3 + delay * 0.7
