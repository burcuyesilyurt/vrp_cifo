import numpy as np
import os
import math


# Indicate the instance you want to read
instance = 'c101C6.txt'
file_path = os.path.join('goeke-2018', instance)


# Read the parameters of the TXT file
def read_vrp_parameters(file_path):
    """A  function to read the parameters of the text file

        Returns:
            data: parameters corresponding to each node
            vehicle_params: general parameters of the problem that doesnt depend on a specific node
        """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = {}
    vehicle_params = {}

    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("StringID"):
            parts = stripped_line.split()
            if len(parts) > 4 and ":" not in parts:
                entry = {
                    'Type': parts[1],
                    'x': float(parts[2]),
                    'y': float(parts[3]),
                    'demand': float(parts[4]),
                    'ReadyTime': float(parts[5]),
                    'DueDate': float(parts[6]),
                    'ServiceTime': float(parts[7]),
                    'PartnerID': parts[8]
                }
                data[parts[0]] = entry
            elif ":" in parts:
                param_name = " ".join(parts[:-2])
                value = float(parts[-1])
                vehicle_params[param_name] = value

    return data, vehicle_params


data, vehicle_params = read_vrp_parameters(file_path)

print('--------------------------------------------------')
print("Vehicle Parameters:")
for key, value in vehicle_params.items():
    print(f"{key}: {value}")

print('--------------------------------------------------')
print(data)
print(data['D0']['DueDate'])


# Now we create a distance matrix - euclidian distance
def euclidean_distance(x1, y1, x2, y2):
    """A  function to calculate the euclidian distance between two nodes

         Returns:
             The euchlidian distance between two nodes
         """
    return math.sqrt((x2 - x1)*2 + (y2 - y1)*2)


string_ids = list(data.keys())
distance_matrix = np.zeros((len(string_ids), len(string_ids)))


for key_i, value_i in enumerate(data):
    # print(key_i)
    # print(value_i)
    for key_j, value_j in enumerate(data):
        xi, yi = data[value_i]['x'] , data[value_i]['y']
        xj, yj = data[value_j]['x'], data[value_j]['y']

        distance_matrix[key_i, key_j] = euclidean_distance(xi, yi , xj, yj)

print('--------------------------------------------------')
print(distance_matrix)