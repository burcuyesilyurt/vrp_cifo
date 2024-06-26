from random import sample, randrange


def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps elements within each sublist.

    Args:
        individual (list of lists): A GA individual represented as a list of lists.

    Returns:
        list of lists: Mutated individual.
    """
    mut_list_index = randrange(len(individual))
    chosen_list = individual[mut_list_index]

    while len(chosen_list) <= 1:
        mut_list_index = randrange(len(individual))
        chosen_list = individual[mut_list_index]

    mut_indexes = sample(range(len(chosen_list)), 2)
    chosen_list[mut_indexes[0]], chosen_list[mut_indexes[1]] = chosen_list[mut_indexes[1]], chosen_list[mut_indexes[0]]

    return individual

def inversion_mutation(individual):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (list of lists): A GA individual represented as a list of lists.

    Returns:
        list of lists: Mutated Individual
    """
    mut_list_index = randrange(len(individual))
    chosen_list = individual[mut_list_index]

    while len(chosen_list) <= 1:
        mut_list_index = randrange(len(individual))
        chosen_list = individual[mut_list_index]

    mut_indexes = sample(range(0, len(chosen_list)), 2)
    mut_indexes.sort()
    chosen_list[mut_indexes[0]:mut_indexes[1]] = chosen_list[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


if __name__ == "__main__":
    test = [[0,1,9,7,5,4], [], [4,6,7], [4,2,6]]
    inversion_mutation(test)