import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize

# Load problem instance from ORLIB dataset
data = pd.read_csv("uflp1.txt", sep="\t", header=None)
num_facilities, num_customers = data.iloc[0]
facility_cost = data.iloc[1 : num_facilities + 1, 0].values
assignment_cost = data.iloc[num_facilities + 1 : num_facilities + num_customers + 1, :num_facilities].values

# Parameters
num_particles = 50
max_iterations = 100
inertia_weight = 0.7
cognitive_weight = 1.4
social_weight = 1.4

# Define the Particle class
class Particle:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.best_position = position
        self.best_cost = np.inf

# Define the PSO class
class PSO:
    def __init__(self, num_particles, max_iterations):
        self.num_particles = num_particles
        self.max_iterations = max_iterations
        self.swarm = []
        self.global_best_position = None
        self.global_best_cost = np.inf

    def initialize_swarm(self):
        for _ in range(self.num_particles):
            position = np.random.choice(num_facilities, num_customers)
            velocity = np.zeros(num_customers)
            particle = Particle(position, velocity)
            self.swarm.append(particle)

    def update_swarm(self):
        for particle in self.swarm:
            # Update particle's velocity
            particle.velocity = (
                inertia_weight * particle.velocity
                + cognitive_weight * np.random.random() * (particle.best_position - particle.position)
                + social_weight * np.random.random() * (self.global_best_position - particle.position)
            )

            # Update particle's position
            particle.position = np.where(
                np.random.random(num_customers) < self.sigmoid(particle.velocity),
                particle.position,
                np.random.choice(num_facilities, num_customers),
            )

            # Update particle's best position and cost
            particle_cost = self.calculate_cost(particle.position)
            if particle_cost < particle.best_cost:
                particle.best_position = particle.position.copy()
                particle.best_cost = particle_cost

            # Update global best position and cost
            if particle_cost < self.global_best_cost:
                self.global_best_position = particle.position.copy()
                self.global_best_cost = particle_cost

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def calculate_cost(self, position):
        total_cost = np.sum(
            facility_cost[position] + assignment_cost[i, position]
            for i in range(num_customers)
        )
        return total_cost

    def solve(self):
        self.initialize_swarm()
        for _ in range(self.max_iterations):
            self.update_swarm()

        # Print the solution
        print("Global Best Cost:", self.global_best_cost)
        print("Global Best Position:", self.global_best_position)

# Solve the UFLP using PSO
pso = PSO(num_particles, max_iterations)
pso.solve()
