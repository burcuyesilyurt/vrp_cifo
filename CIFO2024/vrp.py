from charles.charles import Population, Individual
from data.tsp_data import cities, distance_matrix
from charles.selection import fps, tournament_sel
from charles.mutation import swap_mutation, inversion_mutation
from charles.xo import cycle_xo, pmx


def get_fitness_capacity(self):
    pass

def get_fitness_distance(self):
    pass

def get_fitness_number_of_vehicles(self):
    pass

def get_fitness_time(self):
    pass

def get_fitness_vehicle_battery(self):
    pass

def get_fitness(self):
    #TODO implement the fitness function considering the different objectives
    # We can try weighted sum or pareto front here
    pass

# Monkey patching
Individual.get_fitness = get_fitness

def init_func():
    pass

P = Population(size=20, optim="min", sol_size=len(cities), init_func=init_func)

P.evolve(gens=100, xo_prob=1, mut_prob=0.15, select=tournament_sel,
         xo=pmx, mutate=inversion_mutation, elitism=True)


#hill_climb(pop)
#sim_annealing(pop)

