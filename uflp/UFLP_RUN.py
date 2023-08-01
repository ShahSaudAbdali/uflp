import numpy as np
import math
import random

def objective_function(facilities, customers, assignment):
    total_cost = 0
    for j in range(len(customers)):
        min_cost = np.inf
        for i in range(len(facilities)):
            cost = assignment[i, j] * facilities[i].cost + facilities[i].setup_cost
            if cost < min_cost:
                min_cost = cost
        total_cost += min_cost
    return total_cost

def run_optimization(facilities, customers, num_iterations, step_size):
    num_facilities = len(facilities)
    num_customers = len(customers)
    num_dimensions = num_facilities * num_customers

    # Initialize population
    population = np.random.randint(2, size=(num_dimensions,))

    for _ in range(num_iterations):
        # Calculate fitness
        fitness = objective_function(facilities, customers, population.reshape((num_facilities, num_customers)))

        # Runge-Kutta implementation
        derivatives = np.zeros((num_facilities, num_customers))

        for i in range(num_facilities):
            for j in range(num_customers):
                # Drive cost for each facility and location
                cost = facilities[i].cost + facilities[i].setup_cost
                derivatives[i, j] = cost * population[i * num_customers + j] - cost * (
                            1 - population[i * num_customers + j])

        population = population + step_size * derivatives.reshape((num_dimensions,))
        population = np.clip(population, 0, 1)

    # Calculate the best solution
    best_solution = population.reshape((num_facilities, num_customers))
    best_fitness = objective_function(facilities, customers, best_solution)

    return best_solution, best_fitness

class Facility:
    def __init__(self, cost, setup_cost):
        self.cost = cost
        self.setup_cost = setup_cost

class Customer:
    def __init__(self, demand):
        self.demand = demand

file = open('../ORLIB/ORLIB-cap/40/cap41.txt', 'r')
lines = file.readlines()
print(lines)

for index, line in enumerate(lines):
    if index == 0:
        lineValue = line

# Fetch the data inputs from OR-lib dataset.
facilities = [Facility(10, 100), Facility(8, 150), Facility(6, 200)]
customers = [Customer(20), Customer(30), Customer(40)]

print(facilities[0])
print(customers)

# Run the optimization
num_iterations = 100  # Number of iterations
step_size = 0.1  # Step size for Runge-Kutta integration
best_solution, best_fitness = run_optimization(facilities, customers, num_iterations, step_size)

print("Best solution:")
print(best_solution)
print("Best fitness:")
print(best_fitness)
