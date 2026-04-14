import numpy as np
from material_engine import RelMaterial

def search_materials(iterations=1000):
    best_efficiency = -1
    best_params = None

    print(f"Starting Relativistic Search for Thermoelectric Materials ({iterations} iterations)...")

    for i in range(iterations):
        # Randomly sample the field parameter space
        energy_density = np.random.uniform(0.1, 100.0)
        vorticity = np.random.uniform(-50.0, 50.0, size=3)
        coupling = np.random.uniform(0.01, 2.0)

        mat = RelMaterial(energy_density, vorticity, coupling)
        eff = mat.calculate_efficiency()

        if eff > best_efficiency:
            best_efficiency = eff
            best_params = {
                'energy_density': energy_density,
                'vorticity': vorticity,
                'coupling': coupling
            }

        if (i+1) % 200 == 0:
            print(f"Iteration {i+1}: Current Best R-ZT = {best_efficiency:.4f}")

    return best_params, best_efficiency

if __name__ == "__main__":
    best_p, best_e = search_materials()
    print("\n--- OPTIMAL THERMOELECTRIC MATERIAL DISCOVERED ---")
    print(f"Energy Density: {best_p['energy_density']:.4f}")
    print(f"Vorticity Vector: {best_p['vorticity']}")
    print(f"Relativistic Coupling: {best_p['coupling']:.4f}")
    print(f"Maximum R-ZT: {best_e:.4f}")
    print("--------------------------------------------------")
