# vrp_cifo


# Entities
Vehicles
Customers
Recharging Stations
Depot

# Representation
In order to make our data available to the algorithm we have to represent:
V1X = Vehicle
CPX = Customers Pickup
CD = Customer Delivery
SX = Recharging Stations
D1 = Depot (we're considering only one depot for simplicity)

So for instance, one trip that delivery to customer 1, following by customers 2 and 3 can be represent like `[D1,V1,CP1,CP2,CD1,CP3,CD3,CD2,D1]`, where all routes will start with `D1` followed by the vehicle that will do that route.

# Problem premises
- All routes must start and end at Depot 1 (following the paper)
- All picked up orders must be delivery
- The order must be picked up before delivery

# Fitness Function
## Things to consider
- Capacity
- Number of vehicles used
- Time Windows
	- Should we consider waiting time in the fitness? More waiting time equals worst fitness? I think at first no.
- Battery
- Distance

# Ways to validate feasibility
- Allow it but decrease fitness
	- Can increase computation time, but easier to implement
- Make the modifications and then validate, removing invalid movements.
	- It's easier to implement, but have to validate if there are some side-effects
- Don't allow it at all
	- We should find a way to do this, because it can make the crossover and mutation logic harder to implement

## Feasibility Checks
- Capacity exceeded
- Late order delivery
- Vehicle out of battery


# POC
I would suggest to try to implement a v0 without considering the battery, only to check the difficulty of the problem. But first I'll stress more the problem.

# Implementation steps
- Convert the given datasets into python objects, parsing the problem
- Create the initialization function ensuring that feasibility will be respected
	- This is hard because the representation changes a little, and the library doesn't handle this. For instance, all valid_set is sampled, but in our case this isn't possible because some part allows repetition and others don't
	- Will it be completely random or we'll use some heuristics?
- Do a very very simple cross-over implementation
- Do a very very simple mutation implementation (optional?)
- Build the Benchmarks module to do statistical testing.

## TODOS (so far):
- [ ] Implement initialization method (random at first)
- [ ] Implement fitness functions


# References
Unfortunately, I couldn't find the most updated version of the paper, but I found a old one that can be used as a reference
https://web4.ensiie.fr/~faye/mpro/MPRO_reseau/Projet_2020/The%20electric%20vehicle%20routing%20problem%20with%20time%20windows%20and%20recharging%20stations.pdf