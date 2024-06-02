# Project of Computational Intelligence for Optimization - 2024
## Vehicle Routing Problem (vrp)
This project tries to solve the optimization problem of the vrp, with genetic algorithms. The goal is to minimize the distance made by the car, while making the delivers of all the packages. Meanwhile, the car still need to have battery to return to depot.

## Problem definition
### Entities
* Vehicles;
* Customers;
* Recharging stations;
* Depot.

### Representation
In order to make our data available to the algorithm we have to represent:
* **CPX** = Customers Pickup (where X represents the indexed customer);
* **CD** = Customer Delivery;
* **SX** = Recharging Stations (where X represents the indexed station);
* **D1** = Depot (we're considering only one depot for simplicity).

So for instance, one trip of one vehicle, that delivery to customer 1, following by customers 2 and 3 can be represented like `[[CP1,CP2,CD1,CP3,CD3,CD2]]`, where all routes will start with `D1` followed by the vehicle that will do that route.
The route of the different vehicles is defined by the inner lists, within the main list.

### Problem premises
- All routes must start and end at Depot 1;
- All picked up orders must be delivery;
- The order only can be picked up if the time window is ready for pickup;
- The order must be picked up before delivery.

### Fitness Function
The fitness function takes into account the following variables:
* Capacity - `get_fitness_capacity()`;
* Battery level - `get_fitness_batery()`;
* Time - `get_fitness_time()`.

![](CIFO2024/images/equation.png)

### Mutation
* `swap_mutation()`;
* `inversion_mutation()`.

### Crossover
* Single-point crossover - `single_point_xo()`;
* Cycle crossover - `cycle_xo()`;
* Partially-mapped crossover - `vrp_pmx()`;
* Constructive crossover - `sequential_constructive_xo()` .

### Selection
* Tournament Selection;
* Fitness Proportionate Selection.

## Comments
We've implemented a random insertion to avoid introducing bias during the creation of the population. However, for introducing some variability and ensuring that information is distributed across the different generations, we've used several crossover and mutation functions. The combination of all the techniques used gave a good solution for the problem.

## External libraries
* Matplotlib;
* Numpy;
* Pandas;
* Seaborn;
* Chardet.

## Authors
| Name             | ID       |
|------------------|----------|
| Devora Cavaleiro | 20230794 |
| Carlos Rodrigues | 20230543 |
| David Guarin     | 20230602 |
| Burcu Yesilyurt  | 20230763 |
| Lia Henao        | 20230600 |


## References
* Rahmat, R. W., & Zaharuddin, W. M. (2013). Solving the Vehicle Routing Problem using Genetic Algorithm. 
* Toth, P., & Vigo, D. (2002). An overview of vehicle routing problems. European Journal of Operational Research, 144(3), 465-474.
* Keskin, M., & Çatay, B. (2018). The electric vehicle routing problem with time windows and recharging stations. Transportation Research Part C: Emerging Technologies, 87, 113-137. 