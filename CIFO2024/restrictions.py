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


def has_battery_violation(route, data, battery_capacity):
    battery_violation = False
    current_battery = battery_capacity

    for rep in route:
        if data[rep][1] == "cd" or data[rep][1] == "cp":
            current_battery += float(data[rep][4])

        elif  data[rep][1] == "f":
            current_battery = battery_capacity

        if current_battery < 0:
            battery_violation = True
            break

    return battery_violation

