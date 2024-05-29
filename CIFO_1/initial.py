from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import copy
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation
from charles.xo import cycle_xo
import math

d0 = ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0']
data = [
    
    #1
    ['S0', 'f', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #2
    ['S15', 'f', '39.0', '26.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #3
    ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
    #4
    ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '180.0', 'C65'],
    #5
    ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1063.0', '90.0', 'C98'],
    #6
    ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
    #7
    ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
    #8
    ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
]


    
def get_fitness_time(self):

    time_error = False
    current_time = 0.0
    delivery_first = 100000
    battery = 77.75
    
    
    for idx, rep in enumerate(self.representation):
        ready_time = float(data[rep][5])
        due_date = float(data[rep][6])
        service_time = float(data[rep][7])
        
        d = 0

        if delivery_first != 100000:
            distance = (float(data[rep][2])-float(data[delivery_first][2]))**2 
            distance += (float(data[rep][3])-float(data[delivery_first][3]))**2
            distance = math.sqrt(distance)
            d = distance
            battery -= distance
            current_time += distance

        else: 
            distance = (float(data[rep][2])-float(d0[2]))**2 
            distance += (float(data[rep][3])-float(d0[3]))**2
            distance = math.sqrt(distance)
            d = distance
            battery -= distance
            current_time += distance

        if ready_time > current_time:
            current_time = ready_time

        if due_date < current_time:
            time_error = True

        delivery_first = rep

        if service_time != 0.0:
            current_time += service_time

        time_charging = 0

        if 'S' in data[rep][0]:
            time_charging = (77.75 - battery)*3.47
            current_time += time_charging
        
        #print(rep,' ', delivery_first, ' ', d, ' ', current_time, ' ', time_charging, ' ', service_time, ' ', ready_time)
    
    
    distance = (float(data[rep][2])-float(d0[2]))**2 
    distance += (float(data[rep][3])-float(d0[3]))**2
    distance = math.sqrt(distance)
    d = distance
    battery -= distance
    current_time += distance

    if float(d0[6]) < current_time:
        time_error = True

    if time_error:
        return 1000000000
    
    else:
        return current_time
    

def get_fitness_vehicle_battery(self):

    battery = 77.75
    battery_consume = 0
    delivery_first = 1000
    battery_consumption = 1
    battery_error =False
    battery_now = battery

    for idx, rep in enumerate(self.representation):
        distance = 0
        if battery_consume !=0 :
            distance = (float(data[rep][2])-float(data[delivery_first][2]))**2 
            distance += (float(data[rep][3])-float(data[delivery_first][3]))**2
            distance = math.sqrt(distance)
            battery_now -= distance*battery_consumption
        else:
            distance = (float(data[rep][2])-float(d0[2]))**2 
            distance += (float(data[rep][3])-float(d0[3]))**2
            distance = math.sqrt(distance)
            battery_now -= distance*battery_consumption
        
        if battery_now < 0 :
            battery_error = True
            
            break
        station_type = data[rep][0]
       
        if 'S' in station_type:
            battery_now = battery
            
        delivery_first = rep
    
    
    distance = (float(data[rep][2])-float(d0[2]))**2 
    distance += (float(data[rep][3])-float(d0[3]))**2
    distance = math.sqrt(distance)
    battery_now -= distance*battery_consumption
    
    if battery_now< 0:
        battery_error = True

    if battery_error:
        
        return 100000000

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
        return 1000000

    return 1



def get_fitness(self):
    # Define weights for each objective
    weight_battery = 0.4
    weight_time = 0.3
    weight_order = 0.3

    # Calculate individual fitness values
    fitness_battery = get_fitness_vehicle_battery(self)
    fitness_time = get_fitness_time(self)
    fitness_order = get_fitness_pickup_delivery_order(self)

    # Weighted sum of fitness values
    total_fitness = (weight_battery * fitness_battery +
                     weight_time * fitness_time +
                     weight_order * fitness_order)

    # Penalize if the first point is not the depot
    if self.representation[0] != 0:
        return -1000

    return total_fitness


def get_neighbours(self):
    """A neighbourhood function for the TSP problem. Switch
    indexes around in pairs.

    Returns:
        list: a list of individuals
    """
    n = [copy(self.representation) for _ in range(len(self.representation)-1)]

    for i, ne in enumerate(n):
        ne[i], ne[i+1] = ne[i+1], ne[i]

    n = [Individual(ne) for ne in n]
    return n

# Monkey patching
Individual.get_fitness = get_fitness
Individual.get_neighbours = get_neighbours

P = Population(size=40, optim="min", sol_size=len(data),
                 valid_set=[i for i in range(len(data))], repetition = False)

P.evolve(gens=100, xo_prob=0.9, mut_prob=0.15, select=tournament_sel,
         xo=cycle_xo, mutate=swap_mutation, elitism=True)



#hill_climb(pop)
#sim_annealing(pop)

