import matplotlib.pyplot as plt
import numpy as np

print("INITIALIZING COLLATZ TURBULENCE PROBE...")

# 1. THE COLLATZ PHYSICS ENGINE
def collatz_flow(n):
    """
    Tracks the 'Energy' (Value) vs 'Time' (Steps).
    Returns the trajectory.
    """
    path = [n]
    while n > 1:
        if n % 2 == 0:
            n = n // 2      # DISSIPATION (Prime 2)
        else:
            n = 3 * n + 1   # INJECTION (Prime 3)
        path.append(n)
    return path

# 2. SIMULATE THE CASCADE
# We simulate a range of integers to see the collective flow
start_range = 10000
trajectories = []
lengths = []
max_vals = []

print(f"Injecting {start_range} particles into the system...")

for i in range(1, start_range + 1):
    path = collatz_flow(i)
    trajectories.append(path)
    lengths.append(len(path))
    max_vals.append(max(path))

# 3. THE DULA INTERPRETATION
# We plot "Mass 3 Injection" vs "Mass 2 Dissipation"
# Logarithmic scale reveals the turbulent scaling laws

plt.figure(figsize=(14, 8), facecolor='black')
ax = plt.gca()
ax.set_facecolor('black')

# Plotting the "Rain" of numbers
# X-axis: Starting Number (Initial Condition)
# Y-axis: Stopping Time (Duration of Turbulence)
# Color: Peak Altitude (Maximum Energy reached)

sc = plt.scatter(
    range(1, start_range + 1), 
    lengths, 
    c=np.log(max_vals), 
    cmap='turbo', 
    s=2, 
    alpha=0.8
)

# Add the "Viscosity Barrier"
# The visual patterns (layers) show the discrete nature of the dissipation
plt.title("The Collatz Turbulent Cascade\nInteraction of Prime 3 (Injection) and Prime 2 (Dissipation)", color='white', fontsize=16)
plt.xlabel("Initial State $n_0$", color='white')
plt.ylabel("Turbulence Duration (Stopping Time)", color='white')
plt.tick_params(colors='white')

cbar = plt.colorbar(sc)
cbar.set_label('Log Maximum Energy (Peak Value)', color='white')
cbar.ax.yaxis.set_tick_params(color='white')

plt.grid(color='gray', linestyle=':', linewidth=0.5, alpha=0.3)

# Annotation of the Mechanics
plt.text(start_range/2, 20, "The 'Mass 2' Viscosity\ndrains all energy to 1", color='cyan', ha='center', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
