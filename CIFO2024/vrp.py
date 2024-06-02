from charles.charles import Population, Individual
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, inversion_mutation
from charles.xo import cycle_xo, pmx, vrp_xo, single_point_xo, vrp_xo_random, sequential_constructive_xo
from CIFO2024.charles.fitness_functions import get_fitness
from CIFO2024.charles.initializations import random_initialization
from read_data import *

charge = []
for i in data:
    if 'S' in i:
        charge.append(i)

# Max number of vehicles = number of pick-ups
max_vehicles = 45

# Monkey patching
Individual.get_fitness = get_fitness(data, charge)

if __name__ == "__main__":
    # Mutation operators
    mutation = [swap_mutation, inversion_mutation]
    # Crossover operators
    xo = [
        (lambda: sequential_constructive_xo(data), "sequential_constructive_xo"),
        (lambda: vrp_xo(data, max_vehicles, cycle_xo), "vrp_xo(cycle_xo)"),
        (lambda: vrp_xo(data, max_vehicles, pmx), "vrp_xo(pmx)"),
        (lambda: vrp_xo(data, max_vehicles, single_point_xo), "vrp_xo(single_point_xo)"),
        (lambda: vrp_xo_random(data, max_vehicles, cycle_xo), "vrp_xo_random(cycle_xo)"),
        (lambda: vrp_xo_random(data, max_vehicles, pmx), "vrp_xo_random(pmx)"),
        (lambda: vrp_xo_random(data, max_vehicles, single_point_xo), "vrp_xo_random(single_point_xo)")
        ]
    # Selection operators
    selection = [fps, tournament_sel]
    # Iterate over operators
    for s in selection:
        for x_func, x_name in xo:
            for m in mutation:
                # Print teh configurations
                for iter in range(2):
                    print(f"Selection: {s.__name__}, Crossover: {x_name}, Mutation: {m.__name__}")
                    # Initiate the population
                    P = Population(size=20, optim="min", init_func=random_initialization(data, max_vehicles))
                    # Evolve
                    P.evolve(gens=50,
                            xo_prob=1,
                            mut_prob=0.20,
                            select=s,
                            xo=x_func(),
                            mutate=m,
                            elitism=False,
                            iter=iter,
                            x_name = x_name
                            )
                    print("\n")