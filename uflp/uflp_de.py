import numpy as np

def uflp_objective(solution, f_cost, c_cost):
    total_cost = np.sum(c_cost * solution) + np.sum(f_cost * (np.sum(solution, axis=1) > 0))
    return total_cost

def differential_evolution_uflp(customers, facilities, f_cost, c_cost, population_size=50, max_generations=100, F=0.8, CR=0.5):
    # Initialize population randomly, Xi
    population = np.random.randint(2, size=facilities)

    for gen in range(max_generations):
        for i in range(population_size):
            # Mutation
            a, b, c = np.random.choice(population_size, 3, replace=False)
            v = population[a] + F * (population[b] - population[c])

            # Crossover
            crossover_mask = np.random.rand(facilities, customers) < CR
            trial_solution = np.where(crossover_mask, v, population[i])

            # Evaluate fitness
            trial_fitness = uflp_objective(trial_solution, f_cost, c_cost)
            current_fitness = uflp_objective(population[i], f_cost, c_cost)

            # Selection
            if trial_fitness < current_fitness:
                population[i] = trial_solution

    best_solution = population[np.argmin([uflp_objective(sol, f_cost, c_cost) for sol in population])]
    return best_solution

# Main Function Call
if __name__ == "__main__":
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
    best_solution = differential_evolution_uflp(customers, facilities, f_cost, c_cost)
    print("Best facility assignment to customers:\n", best_solution)
    # print("Total cost of the solution:", uflp_objective(best_solution, f_cost, c_cost))
