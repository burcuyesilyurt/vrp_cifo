"""
VEHICLE ROUTING PROBLEM (VRP)
"""
import random
from vrp_data import depot, charging_stations, customers, locations, max_battery_capacity

"""
Population representation
"""
def distance(point1, point2): # euclidean distance
    return ((locations[point1][0] - locations[point2][0]) ** 2 + (
                locations[point1][1] - locations[point2][1]) ** 2) ** 0.5

def generate_population(pop_size, num_vehicles, customers):
    population = []
    for _ in range(pop_size):
        routes = []
        customer_assignments = random.sample(customers, len(customers)) # shuffle the customers
        assigned_customers = [[] for _ in range(num_vehicles)]

        for i, customer in enumerate(customer_assignments): # distribute the customer on the cars
            assigned_customers[i % num_vehicles].append(customer)

        for vehicle_customers in assigned_customers: # create the route
            pickups = [c for c in vehicle_customers]
            route = [depot]
            current_battery = max_battery_capacity

            for pickup in pickups:
                # calculate distance to pickup
                if current_battery < distance(route[-1], pickup["id"]):
                    # Find the nearest charging station and add it to the route
                    nearest_station = min(charging_stations, key=lambda s: distance(route[-1], s))
                    route.append(nearest_station)
                    current_battery = max_battery_capacity - distance(route[-1], pickup["id"])
                else:
                    current_battery -= distance(route[-1], pickup["id"])

                route.append(pickup["id"])

                dropout = pickup["dropout"]

                if current_battery < distance(route[-1], dropout):
                    # check if the car has enough battery
                    nearest_station = min(charging_stations, key=lambda s: distance(route[-1], s))
                    route.append(nearest_station)
                    current_battery = max_battery_capacity - distance(route[-1], dropout) # not enough, go charge
                else:
                    current_battery -= distance(route[-1], dropout) # update battery level, after trip

                route.append(dropout)

            if current_battery < distance(route[-1], depot): # battery after dropout to return to depot
                nearest_station = min(charging_stations, key=lambda s: distance(route[-1], s))
                route.append(nearest_station) # not enough go charge
                current_battery = max_battery_capacity - distance(route[-1], depot)

            route.append(depot)
            routes.append(route)

        population.append(routes)
    return population


# example
population_size = 3
num_vehicles = 2
population = generate_population(population_size, num_vehicles, customers)

# initial population
for individual in population:
    print(individual)

"""
# init P with N individuals
pop = Population(size=20,
                 optim="max",
                 sol_size=len(values), #size of my representation
                 valid_set=[0,1],
                 replacement=True)

pop.evolve(gens=100, xo_prob=0.9, mut_prob=0.15, select=fps, xo=single_point_xo, mutate=binary_mutation, elitism=True)
"""