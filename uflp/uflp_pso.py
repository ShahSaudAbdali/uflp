import numpy as np

# Parameters
num_particles = 50
max_iterations = 100
inertia_weight = 0.7
cognitive_weight = 1.4
social_weight = 1.4

# Data
facilities = ["Facility1", "Facility2", "Facility3"]  # List of facility names
customers = ["Customer1", "Customer2", "Customer3", "Customer4"]  # List of customer names

facility_cost = {"Facility1": 50, "Facility2": 40, "Facility3": 30}
assignment_cost = {
    ("Facility1", "Customer1"): 10,
    ("Facility1", "Customer2"): 20,
    ("Facility1", "Customer3"): 30,
    ("Facility1", "Customer4"): 40,
    ("Facility2", "Customer1"): 15,
    ("Facility2", "Customer2"): 25,
    ("Facility2", "Customer3"): 35,
    ("Facility2", "Customer4"): 45,
    ("Facility3", "Customer1"): 12,
    ("Facility3", "Customer2"): 22,
    ("Facility3", "Customer3"): 32,
    ("Facility3", "Customer4"): 42,
}

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
            position = np.random.choice(facilities, len(customers))
            velocity = np.zeros(len(customers))
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
                np.random.random(len(customers)) < self.sigmoid(particle.velocity),
                particle.position,
                np.random.choice(facilities, len(customers)),
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
        total_cost = sum(
            facility_cost[facility] + assignment_cost[facility, customer]
            for facility, customer in zip(position, customers)
        )
        return total_cost

    def solve(self):
        self.initialize_sw
