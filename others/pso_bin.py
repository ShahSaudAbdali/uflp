import random
import math
import matplotlib.pyplot as plt
from random import uniform
import numpy

#Transforming Function
def S1(x):
    return 1 / (1 + numpy.exp(-(2 * x)))

#Objective Function
def objective_function(x):
    z = []
    for a in x:
        z.append(1 / (1 + math.exp(-(2 * a))))

    Z = []
    for a in z:
        if random.random() < a:
            Z.append(1)
        else:
            Z.append(0)

    y = [-j**2 +5 for j in x]
    return y

nv = 5  # number of variables
bounds = [(-3, 3)] * nv  # upper and lower bounds of variables
mm = -1  # if minimization problem, mm = -1; if maximization problem, mm = 1

particle_size = 100  # number of particles
iterations = 200  # max number of iterations
w = 0.85  # inertia constant
c1 = 1  # cognative constant
c2 = 2  # social constant

if mm == -1:
    initial_fitness = float("inf")  # for minimization problem
if mm == 1:
    initial_fitness = -float("inf")  # for maximization problem


class Particle:
    def __init__(self, bounds):
        part = []
        for j in range(len(bounds)):
            part.append(uniform(bounds[0][0], bounds[1][1]))
        self.particle_position = part  # particle position

        self.particle_velocity = part  # particle velocity

        self.local_best_particle_position = part  # best position of the particle

    def evaluate(self, objective_function):
        # print(self.particle_position);input()
        self.fitness_particle_position = objective_function(self.particle_position)
        if mm == -1:
            if self.fitness_particle_position < self.local_best_particle_position:
                self.local_best_particle_position = self.particle_position  # update the local best
                self.local_best_particle_position = self.fitness_particle_position  # update the fitness of the local best

    def update_velocity(self, global_best_particle_position):
        for i in range(nv):
            r1 = random.random()
            r2 = random.random()

            cognitive_velocity = c1 * r1 * (self.local_best_particle_position[i] - self.particle_position[i])
            social_velocity = c2 * r2 * (global_best_particle_position[i] - self.particle_position[i])
            self.particle_velocity[i] = w * self.particle_velocity[i] + cognitive_velocity + social_velocity

    def update_position(self, bounds):
        for i in range(nv):
            self.particle_position[i] = self.particle_position[i] + self.particle_velocity[i]

            # check and repair to satisfy the upper bounds
            if self.particle_position[i] > bounds[i][1]:
                self.particle_position[i] = bounds[i][1]

    def printF(self):
        print(self.particle_position)


class PSO:
    def __init__(self, objective_function, bounds, particle_size, iterations):

        fitness_global_best_particle_position = [initial_fitness] * 5
        global_best_particle_position = []

        swarm_particle = []
        for i in range(particle_size):
            swarm_particle.append(Particle(bounds))
        # swarm_particle[0].printF()
        # input("Hello")
        A = []

        for i in range(iterations):
            for j in range(particle_size):
                swarm_particle[j].evaluate(objective_function)

                if mm == -1:
                    if swarm_particle[j].fitness_particle_position < fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = swarm_particle[j].fitness_particle_position.copy()
                if mm == 1:
                    if swarm_particle[j].fitness_particle_position > fitness_global_best_particle_position:
                        global_best_particle_position = list(swarm_particle[j].particle_position)
                        fitness_global_best_particle_position = swarm_particle[j].fitness_particle_position.copy()

            for j in range(particle_size):
                swarm_particle[j].update_velocity(global_best_particle_position)
                swarm_particle[j].update_position(bounds)

            A.append(fitness_global_best_particle_position)  # record for best fitness

        print('optimal solution:', global_best_particle_position)
        print('objective function value:', fitness_global_best_particle_position)
        print('Evolutionary process of the objective function value:')
        plt.plot(A)


# main PSO
PSO(objective_function, bounds, particle_size, iterations)
plt.show()