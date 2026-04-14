import numpy as np
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

if __name__ == "__main__":
    validate()
