from random import randint, sample, randrange


def swap_mutation(individual):
    """Swap mutation for a GA individual. Swaps elements within each sublist.

    Args:
        individual (list of lists): A GA individual represented as a list of lists.

    Returns:
        list of lists: Mutated individual.
    """
    mut_list_index = randrange(len(individual))
    chosen_list = individual[mut_list_index]

    # Ensure chosen_list has more than 1 element for a meaningful swap
    while len(chosen_list) <= 1:
        mut_list_index = randrange(len(individual))
        chosen_list = individual[mut_list_index]

    # Perform the swap mutation on the chosen list
    mut_indexes = sample(range(len(chosen_list)), 2)
    chosen_list[mut_indexes[0]], chosen_list[mut_indexes[1]] = chosen_list[mut_indexes[1]], chosen_list[mut_indexes[0]]

    return individual


    """
    mut_list_index = randrange(len(individual))
    chosen_list = individual[mut_list_index]
    if len(chosen_list) == 0:
        mut_indexes = sample(range(len(chosen_list)), 2)
        chosen_list[mut_indexes[0]], chosen_list[mut_indexes[1]] = chosen_list[mut_indexes[1]], chosen_list[mut_indexes[0]]
    return individual
"""

def inversion_mutation(individual):
    """Inversion mutation for a GA individual. Reverts a portion of the representation.

    Args:
        individual (Individual): A GA individual from charles.py

    Returns:
        Individual: Mutated Individual
    """
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]
    return individual


if __name__ == "__main__":
    test = [[0,1,9,7,5,4], [], [4,6,7], [4,2,6]]
    swap_mutation(test)