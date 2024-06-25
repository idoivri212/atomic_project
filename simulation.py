import numpy as np
# Found on the web, need to verify and understand
# Constants
R = 8.314  # Universal gas constant in J/(mol·K)


# Function to calculate separation factor
def separation_factor(delta_m, v, T):
    return np.exp((delta_m * v ** 2) / (2 * R * T))


# Function to simulate stage balance
def stage_balance(feed, x_feed, alpha, Q):
    x_product = x_feed * alpha / (alpha + (1 - x_feed))
    x_waste = (x_feed - x_product) / (1 - x_product)
    product = feed * alpha / (1 + alpha - x_feed)
    waste = feed - product
    return product, waste, x_product, x_waste


# Function to simulate the cascade
def cascade_simulation(feed_rate, x_feed, stages, centrifuge_params, target_concentration, target_amount):
    time_elapsed = 0
    total_product = 0
    feed = feed_rate
    x_current = x_feed

    while total_product < target_amount:
        for stage in range(stages):
            centrifuge = centrifuge_params[stage]
            alpha = centrifuge['alpha']
            Q = centrifuge['Q']

            product, waste, x_product, x_waste = stage_balance(feed, x_current, alpha, Q)

            if x_product >= target_concentration:
                time_to_reach = (target_amount - total_product) / (product * Q)
                time_elapsed += time_to_reach
                total_product += product * time_to_reach
                return time_elapsed

            feed = waste
            x_current = x_waste

        # Update the total product and time elapsed per iteration
        total_product += product * Q
        time_elapsed += 1  # Assuming each iteration represents one unit time step

    return time_elapsed


# Parameters
delta_m = 0.003  # Mass difference in kg/mol
T = 300  # Temperature in K
initial_feed_rate = 100  # Initial feed rate in arbitrary units
x_feed = 0.007  # Initial isotope concentration
stages = 10  # Number of stages in the cascade
target_concentration = 0.90  # Desired product concentration
target_amount = 100  # Desired total amount of enriched product

# Variable centrifuge parameters for different types and stages
centrifuge_params = [
    {'type': 'A', 'alpha': separation_factor(delta_m, 500, T), 'Q': 1.0},
    {'type': 'B', 'alpha': separation_factor(delta_m, 600, T), 'Q': 1.2},
    {'type': 'A', 'alpha': separation_factor(delta_m, 500, T), 'Q': 1.0},
    {'type': 'C', 'alpha': separation_factor(delta_m, 700, T), 'Q': 0.9},
    # Add more stages as needed
]

# Run the simulation
time_required = cascade_simulation(initial_feed_rate, x_feed, stages, centrifuge_params, target_concentration,
                                   target_amount)

print(f"Time required to reach the target enrichment: {time_required:.2f} time units")
