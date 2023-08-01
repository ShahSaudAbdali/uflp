from pulp import *

# Set up the problem
problem = LpProblem("Uncapacitated Facility Location Problem", LpMinimize)

# Data
facilities = ["Facility1", "Facility2", "Facility3"]  # List of facility names
customers = ["Customer1", "Customer2", "Customer3", "Customer4"]  # List of customer names

# Costs: Cost of opening each facility and cost of assigning each customer to each facility
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

# Decision Variables
open_facility = LpVariable.dicts("OpenFacility", facilities, lowBound=0, cat=LpBinary)
assign_customer = LpVariable.dicts(
    "AssignCustomer", (facilities, customers), lowBound=0, cat=LpBinary
)

# Objective Function
problem += (
    lpSum(facility_cost[facility] * open_facility[facility] for facility in facilities)
    + lpSum(
        assignment_cost[facility, customer]
        * assign_customer[facility][customer]
        for facility in facilities
        for customer in customers
    )
)

# Constraints
for customer in customers:
    problem += (
        lpSum(assign_customer[facility][customer] for facility in facilities) == 1
    )  # Each customer must be assigned to exactly one facility

for facility in facilities:
    problem += (
        lpSum(assign_customer[facility][customer] for customer in customers)
        <= len(customers) * open_facility[facility]
    )  # If a facility is not open, no customer can be assigned to it

# Solve the problem
problem.solve()

# Print the solution
print("Objective Function Value:", value(problem.objective))
print("\nFacilities:")
for facility in facilities:
    if open_facility[facility].value() == 1:
        print(facility)

print("\nCustomers and their assigned facilities:")
for customer in customers:
    for facility in facilities:
        if assign_customer[facility][customer].value() == 1:
            print(customer, "->", facility)
