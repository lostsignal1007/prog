import numpy as np
import matplotlib.pyplot as plt
import os

# --- Configurations ---
csv_filename = "out.csv"  # Ensure this matches the filename given in C++ app
# ----------------------

if not os.path.exists(csv_filename):
    print(f"Error: {csv_filename} not found! Please run the C++ program first.")
    exit()

# Load trajectory from CSV file
data = np.loadtxt(csv_filename, delimiter=';')
x_steps = data[:, 0]
y_steps = data[:, 1]
z_steps = data[:, 2]

# Define functions to generate contour lines automatically
def F_variant_A(X, Y):
    return (X - 5)**2 * (Y - 4)**2 + (X - 15)**2 + (Y - 4)**2

def F_variant_B(X, Y):
    return -1.0 / ((X - 5)**2 * (Y - 4)**2 + 10.0*(X - 5)**2 + 50.0*(Y - 4)**2 + 1.0)

# Detect which function was used based on the first Z-value
z_init_A = F_variant_A(x_steps[0], y_steps[0])
z_init_B = F_variant_B(x_steps[0], y_steps[0])

if abs(z_steps[0] - z_init_B) < abs(z_steps[0] - z_init_A):
    func = F_variant_B
    func_name = "Function B (Fraction)"
else:
    func = F_variant_A
    func_name = "Function A (Polynomial)"

# Create a grid for contour isolines based on trajectory borders
margin = 2.0
x_min, x_max = min(x_steps) - margin, max(x_steps) + margin
y_min, y_max = min(y_steps) - margin, max(y_steps) + margin

X, Y = np.meshgrid(np.linspace(x_min, x_max, 400), np.linspace(y_min, y_max, 400))
Z = func(X, Y)

# --- Plotting ---
plt.figure(figsize=(10, 8))

# Draw isolines (Contours matching iteration levels)
levels = sorted(list(set(z_steps)))
# If too many iterations, filter to show a clean plot
if len(levels) > 15:
    levels = np.linspace(min(z_steps), max(z_steps), 20)

contours = plt.contour(X, Y, Z, levels=levels, cmap='viridis', alpha=0.6)
plt.clabel(contours, inline=True, fmt='%1.3f', fontsize=8)

# Draw optimization path trajectory
plt.plot(x_steps, y_steps, color='red', linestyle='-', linewidth=2, label='Optimization Path')
plt.scatter(x_steps, y_steps, color='blue', s=30, zorder=5, label='Iteration Steps')

# Mark Start and End positions
plt.scatter(x_steps[0], y_steps[0], color='green', marker='^', s=100, zorder=6, label=f'Start: ({x_steps[0]:.2f}, {y_steps[0]:.2f})')
plt.scatter(x_steps[-1], y_steps[-1], color='gold', marker='*', s=150, zorder=6, label=f'Minimum: ({x_steps[-1]:.4f}, {y_steps[-1]:.4f})')

# Layout and text configurations
plt.title(f"Fletcher-Rieves Method Trajectory & Isolines\n[{func_name}]", fontsize=12, fontweight='bold')
plt.xlabel("X0 Axis", fontsize=10)
plt.ylabel("X1 Axis", fontsize=10)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc='upper right')

# Output short summary to terminal
print(f"Plotting completed for {func_name}!")
print(f"Total points plotted: {len(x_steps)}")
print(f"Final Minimum coordinates: ({x_steps[-1]:.5f}, {y_steps[-1]:.5f})")

plt.show()
