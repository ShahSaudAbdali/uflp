import numpy as np
import random

# Function to calculate the objective value (total cost) for a given solution
def objective_function(solution, cost_matrix):
    total_cost = 0
    num_facilities = cost_matrix.shape[0]
    num_locations = cost_matrix.shape[1]

    for facility in range(num_facilities):
        # Find the index of the location assigned to the facility
        location_index = solution[facility]

        # Add the cost of the connection to the total cost
        total_cost += cost_matrix[facility, location_index]

    return total_cost

# Particle Swarm Optimization (PSO) algorithm
def pso_uflp(cost_matrix, num_particles, num_iterations):
    num_facilities = cost_matrix.shape[0]
    num_locations = cost_matrix.shape[1]

    # Initialize particles with random facility assignments
    particles = np.random.randint(0, num_locations, size=(num_particles, num_facilities))

    # Initialize velocities
    velocities = np.zeros_like(particles)

    # Initialize personal best positions and their corresponding costs
    personal_best_positions = np.copy(particles)
    personal_best_costs = np.zeros(num_particles)

    for i in range(num_particles):
        personal_best_costs[i] = objective_function(particles[i], cost_matrix)

    # Initialize global best position and its corresponding cost
    global_best_index = np.argmin(personal_best_costs)
    global_best_position = np.copy(personal_best_positions[global_best_index])
    global_best_cost = personal_best_costs[global_best_index]

    # PSO parameters
    inertia_weight = 0.5
    cognitive_coefficient = 2.0
    social_coefficient = 2.0

    # Main PSO loop
    for iteration in range(num_iterations):
        for i in range(num_particles):
            # Update velocity
            velocities[i] = (inertia_weight * velocities[i] +
                             cognitive_coefficient * random.random() * (personal_best_positions[i] - particles[i]) +
                             social_coefficient * random.random() * (global_best_position - particles[i]))

            # Update particle position
            particles[i] = np.clip(particles[i] + velocities[i], 0, num_locations - 1)

            # Update personal best if necessary
            current_cost = objective_function(particles[i], cost_matrix)
            if current_cost < personal_best_costs[i]:
                personal_best_positions[i] = np.copy(particles[i])
                personal_best_costs[i] = current_cost

                # Update global best if necessary
                if current_cost < global_best_cost:
                    global_best_position = np.copy(particles[i])
                    global_best_cost = current_cost

    return global_best_position, global_best_cost

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

# cost_matrix = np.array([[1, 2, 3], [4, 5, 6]])
cost_matrix = c_cost
num_particles = 20
num_iterations = 100

best_solution, best_cost = pso_uflp(cost_matrix, num_particles, num_iterations)

print("Best Facility Assignments:", best_solution)
print("Best Cost:", best_cost)