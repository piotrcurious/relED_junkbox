import numpy as np
import matplotlib.pyplot as plt
import os
from material_engine import RelMaterial
from config import ENERGY_MIN, ENERGY_MAX, COUPLING_MIN, COUPLING_MAX

def plot_parameter_interactions():
    # Interaction between Energy Density and Coupling Constant
    e_range = np.linspace(ENERGY_MIN, ENERGY_MAX, 50)
    c_range = np.linspace(COUPLING_MIN, COUPLING_MAX, 50)

    E_grid, C_grid = np.meshgrid(e_range, c_range)
    Efficiency = np.zeros_like(E_grid)

    vorticity = [0, 0, 10.0] # Fixed vorticity for this slice

    for i in range(len(c_range)):
        for j in range(len(e_range)):
            mat = RelMaterial(E_grid[i,j], vorticity, C_grid[i,j])
            Efficiency[i,j] = mat.calculate_efficiency()

    plt.figure(figsize=(10, 8))
    cp = plt.contourf(E_grid, C_grid, np.log10(Efficiency + 1e-6), levels=20, cmap='inferno')
    plt.colorbar(cp, label='Log10(Efficiency R-ZT)')

    plt.title('Parameter Interaction: Energy Density vs. Coupling Constant')
    plt.xlabel('Energy Density')
    plt.ylabel('Coupling Constant')
    plt.grid(True, alpha=0.3)

    output_path = os.path.join(os.path.dirname(__file__), 'interaction_map.png')
    plt.savefig(output_path)
    print(f"Interaction map saved to {output_path}")

if __name__ == "__main__":
    plot_parameter_interactions()
