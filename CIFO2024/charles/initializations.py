import random
from random import sample


def random_initialization(data, max_vehicles):
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
