"""
Adinkra-Stabilized Hypercube Model (ASH Model) Simulation
Author: James Daley
Date: December 23, 2025

This script implements a basic agent-based simulation on a 9-dimensional hypercube.
Agents undergo transformations inspired by adinkra supersymmetry generators
(XOR with codewords) and are subjected to low-probability bit-flip noise.
The resulting occupancy distribution across Hamming weight planes converges
to a Gaussian centered on intermediate planes.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parameters
DIM = 9                    # 9-dimensional hypercube
NUM_AGENTS = 2000          # Number of agents (souls/realms entities)
TICKS = 2000               # Simulation steps
NOISE_PROB = 0.01          # Probability of random bit flip per tick per agent

# Sample adinkra-inspired codewords (linear transformations / SUSY generators)
# These are chosen to mimic raising/lowering operators in adinkra graphs
CODEWORDS = [
    np.array([1, 1, 1, 1, 0, 0, 0, 0, 0], dtype=int),
    np.array([1, 1, 0, 0, 1, 1, 0, 0, 0], dtype=int),
    np.array([1, 0, 1, 0, 1, 0, 1, 0, 0], dtype=int),
    np.array([1, 0, 0, 1, 1, 0, 0, 1, 0], dtype=int),
    np.array([0, 1, 0, 1, 0, 1, 0, 1, 1], dtype=int),
    np.array([0, 0, 1, 1, 0, 0, 1, 1, 1], dtype=int),
]

def hamming_weight(state):
    """Compute Hamming weight (number of 1s) of a binary state."""
    return np.sum(state)

# Initialize agents randomly on the hypercube
agents = np.random.randint(0, 2, size=(NUM_AGENTS, DIM), dtype=int)

# Track occupancy per Hamming weight plane (0 to 9)
occupancy_history = np.zeros((TICKS + 1, DIM + 1), dtype=int)

# Initial occupancy
initial_weights = np.sum(agents, axis=1)
for w in initial_weights:
    occupancy_history[0, w] += 1

# Simulation loop
for t in range(1, TICKS + 1):
    # Choose a random adinkra transformation for this tick
    code = CODEWORDS[np.random.randint(len(CODEWORDS))]
    
    # Apply transformation to all agents (XOR)
    agents = (agents + code) % 2
    
    # Apply noise: random single bit flips
    for i in range(NUM_AGENTS):
        if np.random.rand() < NOISE_PROB:
            flip_bit = np.random.randint(DIM)
            agents[i, flip_bit] ^= 1
    
    # Record occupancy
    weights = np.sum(agents, axis=1)
    for w in weights:
        occupancy_history[t, w] += 1

# Plot final distribution
final_occupancy = occupancy_history[-1]
planes = np.arange(DIM + 1)

plt.figure(figsize=(10, 6))
plt.bar(planes, final_occupancy, color='teal', alpha=0.8, edgecolor='black')
plt.title('ASH Model Simulation: Realm Occupancy Distribution\n'
          f'({NUM_AGENTS} agents after {TICKS} ticks, noise p={NOISE_PROB})')
plt.xlabel('Hamming Weight Plane (Realm Level)')
plt.ylabel('Number of Agents')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('figures/simulation-histogram-generated.png')
plt.show()

print("Simulation complete.")
print("Final occupancy per plane:")
for plane, count in enumerate(final_occupancy):
    print(f"Plane {plane}: {count} agents ({100 * count / NUM_AGENTS:.1f}%)")