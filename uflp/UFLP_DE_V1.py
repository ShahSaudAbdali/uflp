import numpy as np
from scipy.optimize import differential_evolution

# Function to calculate the objective value (total cost) for a given solution
def objective_function(solution, cost_matrix):
    total_cost = 0
    num_facilities = cost_matrix.shape[0]
    num_locations = cost_matrix.shape[1]

    for facility in range(num_facilities):
        # Find the index of the location assigned to the facility
        location_index = int(solution[facility])

        # Add the cost of the connection to the total cost
        total_cost += cost_matrix[facility, location_index]

    return total_cost


# Objective function wrapper for DE optimization
def de_objective_function(solution, *args):
    cost_matrix = args[0]
    return objective_function(solution, cost_matrix)


# Function to solve UFLP using Differential Evolution
def de_uflp(cost_matrix):
    num_facilities = cost_matrix.shape[0]
    bounds = [(0, cost_matrix.shape[1] - 1)] * num_facilities  # Bounds for each facility assignment

    result = differential_evolution(de_objective_function, bounds, args=(cost_matrix,))

    best_solution = result.x
    best_cost = result.fun

    return best_solution, best_cost

# Assigning the matrix from ORLIB
fileRef = open("../ORLIB/ORLIB-uncap/70/cap711.txt", "r")
file = fileRef.readlines()
listOfOpeningFacility = []
costFacilityToLocation = []

for index, value in enumerate(file):
    if index == 0:
        getValue = value
        getValue = getValue.split()
        facilities = int(getValue[0])
        customers = int(getValue[1])
    elif index <= facilities:
        getValue = value
        getValue = getValue.split()
        listOfOpeningFacility.append(float(getValue[1]))
    else:
        getValue = value
        getValue = getValue.split()
        if len(getValue) > 1:
            singleFacilityCost = []
            for data in getValue:
                singleFacilityCost.append(float(data))
            costFacilityToLocation.append(singleFacilityCost)

f_cost = np.array(listOfOpeningFacility)
c_cost = np.array(costFacilityToLocation)
c_cost = c_cost.transpose()

print("Total Facility: ", facilities, "Total Customers: ", customers)
print("Facility Opening Cost Array: ", f_cost)
print("Customer to Facility Cost Array: \n", c_cost)

cost_matrix = c_cost

best_solution, best_cost = de_uflp(cost_matrix)
print("Best Facility Assignments:", best_solution)
print("Best Cost:", best_cost)
