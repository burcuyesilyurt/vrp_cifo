from utils import euclidean_distance
from restrictions import has_pickup_violation, has_capacity_violation
from read_data import *


def get_fitness(data, charge):
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

            fitness_time += get_fitness_time(route, data, charge)
            fitness_capacity += get_fitness_capacity(route,data)
            
                
        return ((fitness_time)*(size))/1000+fitness_capacity

    return get_overall_fitness

def get_fitness_capacity(route, data):
    
    cars_capacity = vehicle_params['Vehicle battery capacity']
    car = 0
    max_capacity = False
    for rep in route:
       car = car + float(data[rep][4])
       if car > cars_capacity:
           max_capacity = True
           break
    if max_capacity:
        
        return 10000000000000000000
    else:
        return 1
    

def get_fitness_time(route, data,charge):
    # Assign d0 to be equals the depot
    d0 = data[0]
    delay = 0
    time_error = False
    current_time = 0
    delivery_first = 100000
    battery = vehicle_params['Vehicle battery capacity']
    return_time = 0
    
    for rep in route:
        ready_time = float(data[rep][5])
        due_date = float(data[rep][6])
        service_time = float(data[rep][7])

        if delivery_first != 100000:

            distance = euclidean_distance(data[rep], data[delivery_first])
            battery -= distance
            

            if rep == len(data)-1:
                next_distance = euclidean_distance(data[rep], d0)

                if (battery-next_distance) < 0:
                    min_distance = 10000
                    
                    for i in range(0, len(charge)):

                        charge_station = charge[i]

                        d = euclidean_distance(data[rep], charge_station)
                        d=+ euclidean_distance(d0, charge_station)

                        if d < min_distance:
                            min_distance = d
                            
                    distance += min_distance
                    battery = vehicle_params['Vehicle battery capacity']
                else:
                    next_distance = euclidean_distance(data[rep], data[rep+1])
                    if (battery-next_distance) < 0:
                        min_distance = 10000
                        station_name = ''
                        for i in range(0, len(charge)):
                            charge_station = charge[i]
                            d = euclidean_distance(data[rep], charge_station)
                            d=+ euclidean_distance(data[rep+1], charge_station)
                            if d < min_distance:
                                min_distance = d
                                station_name = charge_station[0]
                        distance += min_distance
                        battery = vehicle_params['Vehicle battery capacity']
            current_time += distance
        else:

            distance = euclidean_distance(data[rep], d0)
            battery -= distance
            current_time += distance



        if ready_time > current_time:
            current_time = ready_time

        if due_date < current_time:

            delay += (current_time-due_date)

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
        
   
    
    return (current_time*0.3 + delay*0.7)


def get_fitness_vehicle_battery(route, data):
    # Assign d0 to be equals the depot
    d0 = data[0]

    battery = vehicle_params['Vehicle battery capacity']
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
