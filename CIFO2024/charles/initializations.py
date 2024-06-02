import random
from random import sample


def random_initialization(data, max_vehicles):
    """
    Generates a random initialization for the population.

    Args:
        data (list): List of data representing each locality.
        max_vehicles (int): Maximum number of vehicles.

    Returns:
        function: A function that generates a random solution representation.
    """
    def init():
        localities = [i for i in range(1, len(data)) if data[i][1] != 'f']
        representation = [[] for _ in range(max_vehicles)]

        while len(localities) > 0:
            route_idx = random.randint(0, max_vehicles-1)
            locality_idx = sample(localities, 1)[0]

            representation[route_idx].append(locality_idx)

            localities.remove(locality_idx)

        return representation

    return init
