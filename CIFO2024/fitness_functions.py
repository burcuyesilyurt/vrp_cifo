from utils import euclidean_distance
from restrictions import has_pickup_violation, has_capacity_violation, has_battery_violation

def get_fitness(data):
    # Define weights for each objective
    vehicle_capacity = 200.0
    battery_capacity = 77.5

    weight_battery = 0.5
    weight_time = 0.25
    weight_order = 0.25

    def get_overall_fitness(individual):
        fitness_time = 0
        fitness_capacity = 0
        fitness_battery = 0
        for route in individual.representation:
            if not route:
                continue

            if has_pickup_violation(route, data):
                return 500000000

            fitness_time += get_fitness_time(route, data)

            if has_capacity_violation(route, data, vehicle_capacity):
                return 500000000

            fitness_capacity += get_fitness_vehicle_capacity(route,data)

            if has_battery_violation(route, data, battery_capacity):
                return 500000000

            fitness_battery += get_fitness_vehicle_battery(route, data)

        total_fitness = (weight_battery * fitness_battery +
                         weight_time * fitness_time +
                         weight_order * fitness_capacity)

        return total_fitness

    return get_overall_fitness


def get_fitness_time(route, data):
    # Assign d0 to be equals the depot
    d0 = data[0]

    time_error = False
    current_time = 0.0
    delivery_first = 100000

    battery_capacity = 77.5
    battery = battery_capacity
    recharging_rate = 3.47

    for rep in route:
        ready_time = float(data[rep][5])
        due_date = float(data[rep][6])
        service_time = float(data[rep][7])

        if delivery_first != 100000:
            distance = euclidean_distance(data[rep], data[delivery_first])
            battery -= distance
            current_time += distance

        else:
            distance = euclidean_distance(data[rep], d0)
            battery -= distance
            current_time += distance

        if ready_time > current_time:
            current_time = ready_time

        if due_date < current_time:
            time_error = True

        delivery_first = rep

        current_time += service_time

        if 'S' in data[rep][0]:
            time_charging = (battery_capacity - battery) * recharging_rate
            current_time += time_charging

        # print(rep,' ', delivery_first, ' ', d, ' ', current_time, ' ', time_charging, ' ', service_time, ' ', ready_time)

    distance = euclidean_distance(data[rep], d0)
    battery -= distance
    current_time += distance

    if float(d0[6]) < current_time:
        time_error = True

    if time_error:
        return 1000000

    else:
        return current_time


def get_fitness_vehicle_battery(route, data):
    # Assign d0 to be equals the depot
    d0 = data[0]

    battery = 77.75
    battery_consume = 0
    delivery_first = 1000
    battery_consumption = 1
    battery_error = False
    battery_now = battery

    for rep in route:
        if battery_consume != 0:
            distance = euclidean_distance(data[rep], data[delivery_first])
            battery_now -= distance * battery_consumption
        else:
            distance = euclidean_distance(data[rep], d0)
            battery_now -= distance * battery_consumption

        if battery_now < 0:
            battery_error = True

            break
        station_type = data[rep][0]

        if 'S' in station_type:
            battery_now = battery

        delivery_first = rep

    distance = euclidean_distance(data[rep], d0)
    battery_now -= distance * battery_consumption

    if battery_now < 0:
        battery_error = True

    if battery_error:
        return 100000000

    return 1


def get_fitness_vehicle_capacity(route, data):
    capacity = 200.0
    capacity_error = False
    capacity_now = capacity

    for rep in route:
        route = rep
        capacity_now += float(data[rep][4])

    if capacity_now < 0:
        capacity_error = True

    if capacity_error:
        return 100000000

    return 1