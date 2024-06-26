import random
from random import randint, sample, uniform
from CIFO2024.charles.xo_utils import flatten_routes, reconstruct_routes, fill_missing_pickups, fill_missing_deliveries, remove_duplicates, repair_pickup, repair_routes_random


def single_point_xo(parent1, parent2):
    """Implementation of single point crossover.

    Args:
        parent1 (Individual): First parent for crossover.
        parent2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_point = randint(1, len(parent1)-1)
    offspring1 = parent1[:xo_point] + parent2[xo_point:]
    offspring2 = parent2[:xo_point] + parent1[xo_point:]
    return offspring1, offspring2


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        count = 0
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)
            count += 1
            if count >30:
                break

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2

def pmx(p1, p2):
    """Implementation of partially matched/mapped crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    xo_points = sample(range(len(p1)), 2)
    xo_points.sort()

    def pmx_offspring(x, y):
       
        o = [None] * len(x)
        # offspring2
        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]]
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])

        # numbers that exist in the segment
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])
            count = 0
            while o[index] is not None and count < 50:
                temp = index
                index = y.index(x[temp])
                count += 1
            o[index] = i

        # numbers that doesn't exist in the segment

        
        while None in o:
            index = o.index(None)
            o[index] = y[index]
        return o
    
    o1, o2 = pmx_offspring(p1, p2), pmx_offspring(p2, p1)
    return o1, o2


def vrp_xo(data, max_vehicles, xo_operation):
    """
    Applies a crossover operation to two parents to produce two offspring, ensuring the offspring are valid VRP solutions by performing repairs.

    Args:
        data (list): List of data representing each locality.
        max_vehicles (int): The maximum number of vehicles available.
        xo_operation (function): The crossover operation to be applied to the parents.

    Returns:
        function: The crossover function that takes two parents and returns two offspring.
    """
    def xo(parent1, parent2):
        """
        The crossover function that takes two parents and returns two offspring.

        Args:
            parent1 (list): The first parent.
            parent2 (list): The second parent.

        Returns:
            tuple: Two offspring generated from the parents.
        """
        # Flatten the routes of the parents, converts lists inside a list to just a list 
        #[[],[],[]] to []
        flat_parent1 = flatten_routes(parent1)
        flat_parent2 = flatten_routes(parent2)
        #Verifies same length after conversion
        flat_parent1, flat_parent2 = same_size_flat(flat_parent1,flat_parent2)
        # Apply the crossover operation
        flat_offspring1, flat_offspring2 = xo_operation(flat_parent1, flat_parent2)
        # Repair the offspring to ensure they are valid VRP solutions
        flat_offspring1 = repair_pickup(flat_offspring1, data)
        flat_offspring1 = fill_missing_pickups(flat_offspring1, data)
        flat_offspring1 = fill_missing_deliveries(flat_offspring1, data)
        flat_offspring1 = remove_duplicates(flat_offspring1)

        flat_offspring2 = repair_pickup(flat_offspring2, data)
        flat_offspring2 = fill_missing_pickups(flat_offspring2, data)
        flat_offspring2 = fill_missing_deliveries(flat_offspring2, data)
        flat_offspring2 = remove_duplicates(flat_offspring2)
        # Reconstruct the routes
        #from [] to [[],[]]
        offspring1 = reconstruct_routes(flat_offspring1)
        offspring2 = reconstruct_routes(flat_offspring2)
        # Ensure the offspring have the correct number of routes, have the same size. 
        offspring1, offspring2 = same_size(offspring1, offspring2, max_vehicles)
        
        return offspring1, offspring2

    return xo


def vrp_xo_random(data, max_vehicles, xo_operation):
    """
    Applies a crossover operation to two parents to produce two offspring, ensuring the offspring are valid VRP solutions by performing random repairs.

    Args:
        data (list): List of data representing each locality.
        max_vehicles (int): The maximum number of vehicles available.
        xo_operation (function): The crossover operation to be applied to the parents.

    Returns:
        function: The crossover function that takes two parents and returns two offspring.
    """

    def xo(parent1, parent2):
        # Flatten the routes of the parents
        flat_parent1 = flatten_routes(parent1)
        flat_parent2 = flatten_routes(parent2)
        flat_parent1, flat_parent2 = same_size_flat(flat_parent1, flat_parent2)

        flat_offspring1, flat_offspring2 = xo_operation(flat_parent1, flat_parent2)

        # Repair the offspring using random repair functions, 
        flat_offspring1 = repair_routes_random(flat_offspring2, data)
        flat_offspring2 = repair_routes_random(flat_offspring2, data)
        # Reconstruct the routes from the flattened routes before
        offspring1 = reconstruct_routes(flat_offspring1)
        offspring2 = reconstruct_routes(flat_offspring2)
        # Ensure the offspring have the correct number of routes
        offspring1, offspring2 = same_size(offspring1, offspring2, max_vehicles)

        return offspring1, offspring2

    return xo

def sequential_constructive_xo(data):
    """
    Implements the Sequential Constructive Crossover (SCX) operation for the Vehicle Routing Problem (VRP).

    Args:
        data (list): List of data representing each locality.

    Returns:
        function: The crossover function that takes two parents and returns two offspring.
    """
    def add_to_offspring(offspring, parents, parent_to_inherit, main_parent_index, i):
        """
        Adds elements to the offspring based on the parent routes and the inheritance strategy.

        Args:
            offspring (list): The current offspring being constructed.
            parents (list): The parent routes.
            parent_to_inherit (bool): Boolean indicating which parent to inherit from.
            main_parent_index (int): Index of the main parent (0 or 1).
            i (int): Current index in the parent routes.
        """
        # "main" delimiter have precedence in order to maintain route sizes
        if parents[main_parent_index][i] == 0:
            offspring.append(0)
            return

        # not "main" parent delimiter have low precedence, so we don't want to inherit it.
        if parents[not main_parent_index][i] == 0:
            offspring.append(parents[main_parent_index][i])
            return

        offspring.append(parents[parent_to_inherit][i])

    def seq_xo(parent1, parent2):
        """
        Applies the sequential constructive crossover to two parents to produce two offspring.

        Args:
            parent1 (list): The flattened route representation of the first parent.
            parent2 (list): The flattened route representation of the second parent.

        Returns:
            tuple: Two offspring generated from the parents.
        """
        assert len(parent1) == len(parent2)

        offspring1 = []
        offspring2 = []
        parents = [parent1, parent2]

        for i in range(len(parent1)):
            parent_to_inherit = bool(random.randint(0, 1))

            add_to_offspring(offspring1, parents, parent_to_inherit, 0, i)
            add_to_offspring(offspring2, parents, not parent_to_inherit, 1, i)

        return offspring1, offspring2

    def xo(parent1, parent2):
        flat_parent1 = flatten_routes(parent1)
        flat_parent2 = flatten_routes(parent2)

        flat_offspring1, flat_offspring2 = seq_xo(flat_parent1, flat_parent2)

        flat_offspring1 = repair_pickup(flat_offspring1, data)
        flat_offspring1 = fill_missing_pickups(flat_offspring1, data)
        flat_offspring1 = fill_missing_deliveries(flat_offspring1, data)
        flat_offspring1 = remove_duplicates(flat_offspring1)

        flat_offspring2 = repair_pickup(flat_offspring2, data)
        flat_offspring2 = fill_missing_pickups(flat_offspring2, data)
        flat_offspring2 = fill_missing_deliveries(flat_offspring2, data)
        flat_offspring2 = remove_duplicates(flat_offspring2)

        offspring1 = reconstruct_routes(flat_offspring1)
        offspring2 = reconstruct_routes(flat_offspring2)

        return offspring1, offspring2

    return xo


def same_size_flat(f_parent1, f_parent2):
    """
    Ensures that two flattened parent routes have the same length by padding the shorter one with zeros.

    Args:
        f_parent1 (list): The flattened route representation of the first parent.
        f_parent2 (list): The flattened route representation of the second parent.

    Returns:
        tuple: The adjusted parent routes of the same length.
    """
    while len(f_parent1)!= len(f_parent2):
        if len(f_parent1)< len(f_parent2):
            f_parent1.append(0)
        else:
            f_parent2.append(0)

    return f_parent1, f_parent2
def same_size(parent1, parent2, max_v):
    """
    Ensures that two parent routes have the same number of routes and do not exceed the maximum number of vehicles.

    Args:
        parent1 (list): The route representation of the first parent.
        parent2 (list): The route representation of the second parent.
        max_v (int): The maximum number of vehicles allowed.

    Returns:
        tuple: The adjusted parent routes of the same size.
    """
    count = 0
    while len(parent1) != len(parent2):
        if len(parent1)>max_v and len(parent1)>0:
            ver = True
            for i in range(0,len(parent1)):
                if len(parent1[len(parent1)-i-1]) ==0:
                    parent1.pop(len(parent1)-i-1)
                    ver = False
                    break
            if ver:
                for j in parent1[len(parent1)-1]:
                    parent1[len(parent1)-2].append(j)
                parent1.pop(len(parent1)-1)
                
        if len(parent2)>max_v and len(parent2)>0:
            ver = True
            for i in range(0,len(parent2)):
                if len(parent2[len(parent2)-i-1]) ==0:
                    parent2.pop(len(parent2)-i-1)
                    ver = False
                    break
            if ver:
                for j in (parent2[len(parent2)-1]):
                    parent2[len(parent2)-2].append(j)
                parent2.pop(len(parent2)-1)
                
        else:
            if len(parent1)< len(parent2):
                parent1.append([])
            else:
                parent2.append([])
        count += 1
    return parent1, parent2

if __name__ == "__main__":
    #p1, p2 = [9,8,2,1,7,4,5,10,6,3], [1,2,3,4,5,6,7,8,9,10]
    #p1, p2 = [2,7,4,3,1,5,6,9,8], [1,2,3,4,5,6,7,8,9]
    #p1, p2 = [9,8,4,5,6,7,1,3,2,10], [8,7,1,2,3,10,9,5,4,6]
    #o1, o2 = pmx(p1, p2)

    #p1 = [0, 5, 4, 3, 0, 2, 0, 1, 6, 0]
    #p2 = [0, 1, 0, 3, 2, 0, 5, 4, 6, 0]
    #o1, o2 = pmx(p1, p2)

    data = [
        # 0
        ['D0', 'd', '40.0', '50.0', '0.0', '0.0', '1236.0', '0.0', '0'],
        # 1
        ['C20', 'cd', '30.0', '50.0', '-10.0', '0.0', '1136.0', '90.0', 'C99'],
        # 2
        ['C24', 'cd', '25.0', '50.0', '-20.0', '0.0', '1131.0', '90.0', 'C65'],
        # 3
        ['C57', 'cd', '40.0', '15.0', '-60.0', '989.0', '1069.0', '90.0', 'C98'],
        # 4
        ['C65', 'cp', '48.0', '40.0', '20.0', '67.0', '139.0', '90.0', 'C24'],
        # 5
        ['C98', 'cp', '58.0', '75.0', '60.0', '0.0', '1115.0', '90.0', 'C57'],
        # 6
        ['C99', 'cp', '30.0', '50.0', '10.0', '0.0', '1136.0', '0.0', 'C20']
    ]

    offspring1 = [0, 6, 5, 0, 0, 4, 2, 0, 0, 1, 3, 0]

    rp = repair_pickup(offspring1, data)
    offspring = [2, 3, 0, 5, 4, 0, 2, 5, 0]
    # Todo this doesn't work if both pickup and delivery is missing in the offspring
    print(fill_missing_deliveries(fill_missing_pickups(offspring, data), data))

def check_if(parent, flat):
    num = 7 
    val = 0
    for i in range(1, num):
        yes = False
        for j in parent:
            if len(j)!=0:
                if i in j:
                    yes=True
                    
        if yes==False:
            print('error', parent, i, flat)   