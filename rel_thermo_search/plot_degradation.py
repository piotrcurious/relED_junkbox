import json
import os
import matplotlib.pyplot as plt

def plot_degradation_tradeoff():
    db_file = os.path.join(os.path.dirname(__file__), "discovered_materials.json")
    if not os.path.exists(db_file): return

    with open(db_file, 'r') as f:
        db = json.load(f)

    if not db: return

    # We need to calculate degradation rate for these (or store it)
    # For now, let's derive it from efficiency/stability if not present
    from material_engine import RelMaterial

    effs = []
    lifetimes = []
    names = []

    for m in db[:50]:
        mat = RelMaterial(m['energy_density'], m['vorticity'], m['coupling'])
        effs.append(m['efficiency'])
        lifetimes.append(mat.calculate_lifetime())
        names.append(m.get('substance', 'Theoretical'))

    plt.figure(figsize=(10, 6))
    plt.scatter(effs, lifetimes, alpha=0.5, c=lifetimes, cmap='plasma')
    plt.colorbar(label='Solitonic Lifetime')
    plt.xlabel('Efficiency (R-ZT)')
    plt.ylabel('Solitonic Lifetime')
    plt.title('Trade-off: Thermoelectric Efficiency vs. Field Stability (Lifetime)')
    plt.grid(True, linestyle='--', alpha=0.5)

    output_path = os.path.join(os.path.dirname(__file__), 'degradation_tradeoff.png')
    plt.savefig(output_path)
    print(f"Trade-off plot saved to {output_path}")

if __name__ == "__main__":
    plot_degradation_tradeoff()
