import random
from random import sample


def random_initialization(data, max_vehicles):
    def init():
        localities = [i for i in range(1, len(data))]
        representation = [[] for _ in range(max_vehicles)]
        num_charging_stations = len(list(filter(lambda e: e[1] == "f", data)))

        while len(localities) > num_charging_stations:
            route_idx = random.randint(0, max_vehicles-1)
            locality_idx = sample(localities, 1)[0]

            representation[route_idx].append(locality_idx)

            if data[locality_idx][1] != "f":
                localities.remove(locality_idx)

        return representation

    return init
