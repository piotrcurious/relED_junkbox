import numpy as np
import matplotlib.pyplot as plt
import os
from material_engine import RelMaterial

def generate_phase_diagram():
    # Grid of Energy Density and Vorticity
    e_range = np.linspace(1, 600, 50)
    v_range = np.linspace(1, 100, 50)

    E_grid, V_grid = np.meshgrid(e_range, v_range)
    Stability = np.zeros_like(E_grid)
    Efficiency = np.zeros_like(E_grid)

    coupling = 1.0

    for i in range(len(v_range)):
        for j in range(len(e_range)):
            mat = RelMaterial(E_grid[i,j], [0, 0, V_grid[i,j]], coupling)
            Stability[i,j] = mat.calculate_stability()
            Efficiency[i,j] = mat.calculate_efficiency()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    cp1 = ax1.contourf(E_grid, V_grid, Stability, levels=20, cmap='RdYlGn')
    fig.colorbar(cp1, ax=ax1, label='Field Stability')
    ax1.set_title('Relativistic Phase Diagram: Stability')
    ax1.set_xlabel('Energy Density')
    ax1.set_ylabel('Vorticity')

    # Efficiency is often very peaked, log scale or robust levels
    cp2 = ax2.contourf(E_grid, V_grid, np.log10(Efficiency + 1e-6), levels=20, cmap='viridis')
    fig.colorbar(cp2, ax=ax2, label='Log10(R-ZT)')
    ax2.set_title('Relativistic Phase Diagram: Efficiency')
    ax2.set_xlabel('Energy Density')

    plt.tight_layout()
    output_path = os.path.join(os.path.dirname(__file__), 'phase_diagram.png')
    plt.savefig(output_path)
    print(f"Phase diagram saved to {output_path}")

if __name__ == "__main__":
    generate_phase_diagram()
