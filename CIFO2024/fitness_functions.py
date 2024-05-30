from utils import euclidean_distance
from restrictions import has_pickup_violation, has_capacity_violation


def get_fitness(data):
    def get_overall_fitness(individual):
        #TODO implement the fitness function considering the different objectives
        # We can try weighted sum or pareto front here
        # Penalize if the first point is not the depot
        fitness_time = 0
        size = len(individual.representation)
        fitness_capacity = 0
        for route in individual.representation:
            
            if not route:
                size -= 1
                continue

            #if has_pickup_violation(route, data):
             #   return 500000000

            fitness_time += get_fitness_time(route, data)
            fitness_capacity += get_fitness_capacity(route,data)
            
                
        return (fitness_time/size)+fitness_capacity

    return get_overall_fitness

def get_fitness_capacity(route, data):
    
    cars_capacity = 100
    car = 0
    max_capacity = False
    for rep in route:
       car = car + float(data[rep][4])
       print(car)
       if car > cars_capacity:
           max_capacity = True
           break
    if max_capacity:
        print("a")
        return 1000000
    else:
        return 0
def get_fitness_time(route, data):
    # Assign d0 to be equals the depot
    d0 = data[0]

    time_error = False
    current_time = 0
    delivery_first = 100000
    battery = 77.75

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

        #current_time += service_time

        #if 'S' in data[rep][0]:
         #   time_charging = (77.75 - battery) * 3.47
          #  current_time += time_charging

        # print(rep,' ', delivery_first, ' ', d, ' ', current_time, ' ', time_charging, ' ', service_time, ' ', ready_time)

    distance = euclidean_distance(data[rep], d0)
    battery -= distance
    current_time += distance
    
    #if float(d0[6]) < current_time:
     #   time_error = True
        
    #if time_error:
        
     #   return 1000000

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
