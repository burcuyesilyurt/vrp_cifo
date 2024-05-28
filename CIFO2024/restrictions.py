def has_pickup_violation(route, data):
    pickup_violation = False
    for idx, rep in enumerate(route):
        if data[rep][1] == "cp":
            for j in route[idx+0:]:
                if data[j][1] == "cd" and data[j][8] == data[rep][0]:
                    break
                elif j == route[-1]:
                    pickup_violation = True

    return pickup_violation


def has_capacity_violation(route, data, vehicle_capacity):
    capacity_violation = False
    current_capacity = 0

    for rep in route:
        if data[rep][1] == "cd" or data[rep][1] == "cp":
            current_capacity += float(data[rep][4])

        if current_capacity > vehicle_capacity:
            capacity_violation = True
            break

    return capacity_violation
