from operator import attrgetter
from random import choice, sample, random
from copy import copy
import csv
import os

class Individual:
    # we always initialize
    def __init__(self, representation=None, size=None, valid_set=None, repetition=True, init_func=None):

        if representation is None:
            if init_func is None:
                if repetition:
                    # individual will be chosen from the valid_set with a specific size
                    self.representation = [choice(valid_set) for i in range(size)]
                else:
                    self.representation = sample(valid_set, size)
            else:
                self.representation = init_func()

        # if we pass an argument like Individual(my_path)
        else:
            if type(representation) is Individual:
                self.representation = representation.representation
            elif type(representation) is list:
                self.representation = representation
            else:
                raise Exception("Invalid representation type")

        # fitness will be assigned to the individual

        self.fitness = self.get_fitness()

    # methods for the class
    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness function.")

    def get_neighbours(self):
        raise Exception("You need to monkey patch the neighbourhood function.")

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        return f" Fitness: {self.fitness}, Rep: {self.representation}"


class Population:
    def __init__(self, size, optim, **kwargs):

        # population size
        self.size = size

        # defining the optimization problem as a minimization or maximization problem
        self.optim = optim

        self.individuals = []
        
        # appending the population with individuals
        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs.get("sol_size"),
                    valid_set=kwargs.get("valid_set"),
                    repetition=kwargs.get("repetition"),
                    init_func=kwargs.get("init_func")
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, xo, mutate, elitism,iter,x_name):
         
        with open(os.path.join('evolution_data.csv'), mode='a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            if csv_file.tell() == 0:  # Check if file is empty
                writer.writerow(['Iteration','Generation', 'Max Vehicles', 'Fitness',  'Selection', 'Crossover', 'Mutation'])

        # gens = 100
            for i in range(gens):
                new_pop = []

                if elitism:
                    if self.optim == "max":
                        elite = copy(max(self.individuals, key=attrgetter('fitness')))
                    elif self.optim == "min":
                        elite = copy(min(self.individuals, key=attrgetter('fitness')))

                    #new_pop.append(elite)

                while len(new_pop) < self.size:
                    # selection
                    parent1, parent2 = select(self), select(self)
                    # xo with prob
                    if random() < xo_prob:
                        offspring1, offspring2 = xo(parent1, parent2)
                    # replication
                    else:
                        offspring1, offspring2 = parent1, parent2
                    # mutation with prob
                    if random() < mut_prob:
                        offspring1 = mutate(offspring1)
                    if random() < mut_prob:
                        offspring2 = mutate(offspring2)

                    new_pop.append(Individual(representation=offspring1))
                    if len(new_pop) < self.size:
                        new_pop.append(Individual(representation=offspring2))

                if elitism:
                    if self.optim == "max":
                        worst = min(new_pop, key=attrgetter('fitness'))
                        if elite.fitness > worst.fitness:
                            new_pop.pop(new_pop.index(worst))
                            new_pop.append(elite)
                    if self.optim == "min":
                        worst = max(new_pop, key=attrgetter('fitness'))
                        if elite.fitness < worst.fitness:
                            new_pop.pop(new_pop.index(worst))
                            new_pop.append(elite)


                self.individuals = new_pop

                               
                if self.optim == "max":
                    print(f"Best individual of gen #{i + 1}: {max(self, key=attrgetter('fitness'))}")
                elif self.optim == "min":
                    minimum = min(self, key=attrgetter('fitness'))
                    number_rep = 0
                    for m in minimum.representation:
                        if len(m) != 0:
                            number_rep += 1

                    # Write data to CSV
                    writer.writerow([iter,i + 1, number_rep, minimum.fitness,  select.__name__, x_name, mutate.__name__])
                    
                    print(f"Best individual of gen #{i + 1}: {number_rep, minimum.representation, minimum.fitness}")


    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]