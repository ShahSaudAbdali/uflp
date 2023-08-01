import math
import random
from numpy.random import rand
from numpy.random import choice
from numpy import asarray
from numpy import clip
from numpy import argmin
from numpy import min
from numpy import around
from matplotlib import pyplot
import binarization
import transferFunctions

#Parsing the input file from ORLIB. Resource can be found @https://resources.mpi-inf.mpg.de/departments/d1/projects/benchmarks/UflLib/packages.html
fileRef = open("./ORLIB/ORLIB-uncap/70/cap71.txt", "r")
file = fileRef.readlines()
listOfOpeningFacility = []
costOfOpeningFacility = []
costFacilityToLocation = []
singleFacilityCost = []
facilityIndex = 0
subIndex = 0
for index, value in enumerate(file):
    if index == 0:
        getValue = value
        getValue = getValue.split()
        facility_count = int(getValue[0])
        location_count = int(getValue[1])
    elif index <= facility_count:
        getValue = value
        getValue = getValue.split()
        listOfOpeningFacility.append(1 if float(getValue[1]) > 0 else 0)
        costOfOpeningFacility.append(float(getValue[1]))
    else:
        subIndex += 1
        if subIndex > 1:
            getValue = value
            getValue = getValue.split()
            for data in getValue:
                singleFacilityCost.append(float(data))
            if subIndex == 4:
                subIndex = 0
                costFacilityToLocation.append(singleFacilityCost)
                singleFacilityCost = []

sumOpeningCost = 0
for index, value in enumerate(costOfOpeningFacility):
    sumOpeningCost += costOfOpeningFacility[index]*listOfOpeningFacility[index]

servingCostSum = 0
tempArr = []
servingFacilityIndices = []
for index, value in enumerate(costFacilityToLocation):
    for cost in value:
        tempArr.append(cost)
    servingCostSum += min(tempArr)
    servingFacilityIndices.append(tempArr.index(min(tempArr)))
    tempArr = []

print("Facility Count:", facility_count)
print("Location Count:", location_count)
print("Facility Open :", listOfOpeningFacility)
print("Serving Cost  :", servingCostSum)
print("Serving Facility:", servingFacilityIndices)

def obj(x):
    return x[0]**2.0 + x[1]**2.0

def fitness(candidate, facilityToLocationList, openingCostFacility):
    candidate = transferFunctions.F1(candidate)         #calling transfer function F1
    b_candidate = binarization.M1(candidate)            #calling binarization method 1
    F = len(facilityToLocationList)
    L = len(openingCostFacility)
    openingFacilityList = []
    for _index in len(b_candidate):
        if b_candidate[_index] == 1:
            openingFacilityList.append(_index)

    openingCost = 0
    for _index in openingFacilityList:
        openingCost += openingCostFacility[_index]

    totalServingCost = 0
    for _index in range(L):
        tempServCost = []
        for __index in range(L):
            tempServCost.append(facilityToLocationList[__index][_index])

        minServingCost = min(tempServCost)
        totalServingCost += minServingCost

    return (openingCost + totalServingCost)

# # define mutation operation
def mutation(x, F):
    return x[0] + F * (x[1] - x[2])

# # define boundary check operation
def check_bounds(mutated, bounds):
    mutated_bound = [clip(mutated[i], bounds[i, 0], bounds[i, 1]) for i in range(len(bounds))]
    return mutated_bound

# # define crossover operation
def crossover(mutated, target, dims, cr):
    p = rand(dims)
    trial = [mutated[i] if p[i] < cr else target[i] for i in range(dims)]       #generate trial vector
    return trial

def differential_evolution(pop_size, bounds, iter, F, cr):
    # initialise population of candidate solutions randomly within the specified bounds
    pop = bounds[:, 0] + (rand(pop_size, len(bounds)) * (bounds[:, 1] - bounds[:, 0]))
    ##print(pop)
    obj_all = [obj(ind) for ind in pop]     #initial vector
    # find the best performing vector of    initial population
    best_vector = pop[argmin(obj_all)]
    best_obj = min(obj_all)
    prev_obj = best_obj
    # initialise list to store the objective function value at each iteration
    obj_iter = list()

    #define coordinates to plot the graph
    xCoord = list()
    yCoord = list()

    # run iterations of the algorithm
    for i in range(iter):
        # iterate over all candidate solutions
        for j in range(pop_size):
            # choose three candidates, a, b and c, that are not the current one
            candidates = [candidate for candidate in range(pop_size) if candidate != j]
            a, b, c = pop[choice(candidates, 3, replace=False)]
            # perform mutation
            mutated = mutation([a, b, c], F)
            # check that lower and upper bounds are retained after mutation
            mutated = check_bounds(mutated, bounds)
            # perform crossover
            trial = crossover(mutated, pop[j], len(bounds), cr)

            ########################Work On this####################################
            obj_target = obj(pop[j])          #calculate obj func for target vector
            obj_trial = obj(trial)            #calculate obj func for trial vector
            # perform selection
            if obj_trial < obj_target:
                # replace the target vector with the trial vector
                pop[j] = trial
                # store the new objective function value
                obj_all[j] = obj_trial
            ##########################################################################

        #best performing vector at each iteration
        best_obj = min(obj_all)
        # store the lowest objective function value
        if best_obj < prev_obj:
            best_vector = pop[argmin(obj_all)]
            prev_obj = best_obj
            obj_iter.append(best_obj)
            # report progress at each iteration
            print('Iteration: %d f([%s]) = %.5f' % (i, around(best_vector, decimals=5), best_obj))
            xCoord.append(i)
            yCoord.append(best_obj)
    pyplot.plot(xCoord, yCoord)
    pyplot.show()
    return [best_vector, best_obj, obj_iter]

#Applying DE to the transformed binary array
pop_size = 10
bounds = asarray([(-5.0, 5.0), (-5.0, 5.0)])
iter = 1000                     #No of iterations for crossover
F = 0.5                         #SF for mutation
cr = 0.7                        #Cross Over Rate

solution = differential_evolution(pop_size, bounds, iter, F, cr)
print('\nSolution: f([%s]) = %.5f' % (around(solution[0], decimals=5), solution[1]))
