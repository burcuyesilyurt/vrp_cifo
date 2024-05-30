import random
from random import sample

from charles.charles import Population, Individual
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, inversion_mutation
from charles.xo import cycle_xo, pmx, vrp_pmx, vrp_single_point_xo
from fitness_functions import get_fitness
from initializations import random_initialization

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

data = [
    #0
    ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
    #1
    ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
    #2
    ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
    #3
    ['C57', 'cd', '40.0', '15.0', '-60.0', '20.0', '1069.0', '90.0', 'C98'],
    #4
    ['C65', 'cp', '48.0', '40.0', '20.0', '20.0', '139.0', '90.0', 'C24'],
    #5
    ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
    #6
    ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
]

# Max number of vehicles = number of pick ups
#max_vehicles = len(list(filter(lambda e: e[1] == "cp", data)))
max_vehicles = 4

# Monkey patching
Individual.get_fitness = get_fitness(data)

if __name__ == "__main__":
    P = Population(size=20, optim="min", init_func=random_initialization(data, max_vehicles))

    # TODO change mut prob when mutation is implemented for our structure
    P.evolve(gens=100,
             xo_prob=1,
             mut_prob=0,
             select=tournament_sel,
             xo=vrp_single_point_xo(data),
             mutate=swap_mutation,
             elitism=True)
