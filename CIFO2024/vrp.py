from charles.charles import Population, Individual
from data.tsp_data import cities, distance_matrix
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, inversion_mutation
from charles.xo import cycle_xo, pmx
import math

data = [
    #0
    ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #1
    ['S0', 'f', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #2
    ['S15', 'f', '39.0', '26.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #3
    ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
    #4
    ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
    #5
    ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1063.0', '90.0', 'C98'],
    #6
    ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
    #7
    ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
    #8
    ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
]

# Max number of vehicles = number of pick ups
max_vehicles = len(list(filter(lambda e: e[1] == "cp", data)))

def get_fitness_capacity(self):
    pass

def get_fitness_number_of_vehicles(self):
    pass

def get_fitness_time(self):
    time_error = False
    current_time = 0.0
    delivery_first = 1000
    for idx, rep in enumerate(self.representation):
        ready_time = float(data[rep][5])
        due_date = float(data[rep][6])
        service_time = float(data[rep][7])
        

        if delivery_first != 1000:
            distance = (float(data[rep][2])-float(data[delivery_first][2]))**2 
            distance += (float(data[rep][3])-float(data[delivery_first][3]))**2
            distance = math.sqrt(distance)
            current_time += distance

        if ready_time > current_time:
            current_time = ready_time

        if due_date < current_time:
            time_error = True
            print(self.representation)
            print('error')
            print(ready_time, service_time, due_date)
            print(current_time)

        delivery_first = rep

        if service_time != 0.0:
            current_time += service_time

    if time_error:
        return -500
    
    else:
        return 1
    

def get_fitness_vehicle_battery(self):
    battery = 77.75
    battery_consume = 0
    delivery_first = 1000
    battery_consumption = 1
    battery_error =False
    battery_now = battery

    for idx, rep in enumerate(self.representation):
        if battery_consume !=0 :
            distance = (float(data[rep][2])-float(data[delivery_first][2]))**2 
            distance += (float(data[rep][3])-float(data[delivery_first][3]))**2
            distance = math.sqrt(distance)
            battery_consume += distance*battery_consumption
        if battery_now-battery_consume < 0 :
            battery_error = True
            break
        station_type = data[rep][0]
        if 'S' in station_type:
            battery_now = battery

        delivery_first = rep

    if battery_error:
        return -500

    return 1


def get_fitness_pickup_delivery_order(self):
    
    pickup_violation = False
    for idx, rep in enumerate(self.representation):
        if data[rep][0] == "cp":
            for j in self.representation[idx+0:]:
                if data[j][0] == "cd" and data[j][8] == data[rep][0]:
                    break
                elif j == self.representation[-2]:
                    pickup_violation = True

    if pickup_violation:
        return -500

    return 1

def get_fitness(self):
    #TODO implement the fitness function considering the different objectives
    # We can try weighted sum or pareto front here
    # Penalize if the first point is not the depot
    if self.representation[0] != 0:
        return -1000

    return get_fitness_vehicle_battery(self)

# Monkey patching
Individual.get_fitness = get_fitness

def init_func():
    pass

P = Population(size=20, optim="max", sol_size=len(data), valid_set=[i for i in range(len(data))], repetition=False)

P.evolve(gens=100, xo_prob=1, mut_prob=0.15, select=tournament_sel,
         xo=cycle_xo, mutate=inversion_mutation, elitism=True)


#hill_climb(pop)
#sim_annealing(pop)

