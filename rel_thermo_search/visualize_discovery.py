import json
import matplotlib.pyplot as plt
import numpy as np
import os

def visualize():
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file):
        print("No database found to visualize.")
        return

    with open(db_file, 'r') as f:
        db = json.load(f)

    if not db:
        print("Database is empty.")
        return

    energies = [m['energy_density'] for m in db]
    vorticities = [np.linalg.norm(m['vorticity']) for m in db]
    efficiencies = [m['efficiency'] for m in db]
    substances = [m.get('substance', 'N/A') for m in db]

    plt.figure(figsize=(12, 8))
    scatter = plt.scatter(energies, vorticities, c=efficiencies, cmap='viridis', alpha=0.6)

    # Annotate top materials
    top_indices = np.argsort(efficiencies)[-3:]
    for i in top_indices:
        plt.annotate(substances[i], (energies[i], vorticities[i]),
                     xytext=(5, 5), textcoords='offset points', fontsize=8, alpha=0.8)

    # Add Schwinger Stability Contour
    # E = coupling * energy_density. Let's assume average coupling = 1.0
    # Stability limit E < 500 => Energy Density < 500
    plt.axvline(x=500, color='r', linestyle='--', alpha=0.3, label='Schwinger Limit (E=500)')
    plt.text(505, plt.ylim()[1]*0.9, 'Unstable Region', color='r', alpha=0.5, rotation=90)

    plt.colorbar(scatter, label='Efficiency (R-ZT)')
    plt.xlabel('Energy Density')
    plt.ylabel('Vorticity Magnitude')
    plt.title('Discovered Relativistic Thermoelectric Materials')
    plt.grid(True)
    plt.legend()

    output_path = os.path.join(os.path.dirname(__file__), 'discovery_map.png')
    plt.savefig(output_path)
    print(f"Visualization saved to {output_path}")

if __name__ == "__main__":
    visualize()
