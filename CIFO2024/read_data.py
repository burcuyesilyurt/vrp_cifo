import os

# Indicate the instance you want to read
#instance = 'lc101.txt'
instance = 'c202C16.txt'
file_path = os.path.join('.', 'goeke-2018',instance)

# Read the parameters of the TXT file
def read_vrp_parameters(file_path):
    """A function to read the parameters of the text file

    Returns:
        d0: parameters for the node 'D0'
        data: parameters corresponding to each node
        vehicle_params: general parameters of the problem that doesn't depend on a specific node
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = []
    vehicle_params = {}

    for line in lines:
        stripped_line = line.strip()
        if stripped_line and not stripped_line.startswith("StringID"):
            parts = stripped_line.split()
            if len(parts) > 4 and ":" not in parts:
                entry = [
                    parts[0],  # StringID
                    parts[1],  # Type
                    float(parts[2]),  # x
                    float(parts[3]),  # y
                    float(parts[4]),  # demand
                    float(parts[5]),  # ReadyTime
                    float(parts[6]),  # DueDate
                    float(parts[7]),  # ServiceTime
                    parts[8]  # PartnerID
                ]

                data.append(entry)    

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
print("data:")
print(data)

print('---------- Test --------')
print('Vehicle battery capacity:', vehicle_params['Vehicle battery capacity'])

