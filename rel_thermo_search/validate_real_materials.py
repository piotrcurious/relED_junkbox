import numpy as np
import matplotlib.pyplot as plt
import os
from material_engine import RelMaterial
from material_mapping import KNOWN_MATERIALS

def validate():
    print(f"{'Material':<30} | {'Real ZT':<10} | {'Rel R-ZT':<15} | {'Correlation'}")
    print("-" * 75)

    results = []
    for name, props in KNOWN_MATERIALS.items():
        mat = RelMaterial(
            energy_density=props['energy_density'],
            vorticity=props['vorticity'],
            coupling_constant=props['coupling']
        )
        r_zt = mat.calculate_efficiency()
        results.append((props['real_zt'], r_zt))

        print(f"{name:<30} | {props['real_zt']:<10.4f} | {r_zt:<15.4f} | {'...'}")

    # Calculate Pearson correlation coefficient
    real_vals = [r[0] for r in results]
    rel_vals = [r[1] for r in results]
    correlation = np.corrcoef(real_vals, rel_vals)[0, 1]

    print("-" * 75)
    print(f"Overall Pearson Correlation: {correlation:.4f}")

    # Generate Validation Plot
    plt.figure(figsize=(10, 6))
    plt.scatter(real_vals, rel_vals, color='blue', s=100, alpha=0.7)

    # Annotate points
    names = list(KNOWN_MATERIALS.keys())
    for i, name in enumerate(names):
        plt.annotate(name.split('(')[0].strip(), (real_vals[i], rel_vals[i]),
                     xytext=(5, 5), textcoords='offset points', fontsize=9)

    # Best fit line
    m, b = np.polyfit(real_vals, rel_vals, 1)
    plt.plot(np.array(real_vals), m*np.array(real_vals) + b, color='red', linestyle='--', alpha=0.5)

    plt.title(f'Model Validation: Empirical ZT vs. Relativistic R-ZT (Corr: {correlation:.4f})')
    plt.xlabel('Empirical Figure of Merit (ZT)')
    plt.ylabel('Relativistic Figure of Merit (R-ZT)')
    plt.grid(True, linestyle=':', alpha=0.6)

    output_path = os.path.join(os.path.dirname(__file__), 'validation_plot.png')
    plt.savefig(output_path)
    print(f"Validation plot saved to {output_path}")

if __name__ == "__main__":
    validate()
