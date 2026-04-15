import numpy as np
from material_engine import RelMaterial

def test_topological_physics():
    print("--- Testing Topological Physics ---")

    # Material at exactly Q=1 (v=10)
    mat1 = RelMaterial(10, [0, 0, 10.0], 1.0)
    q1 = mat1.calculate_topological_charge()
    eff1 = mat1.calculate_efficiency()

    # Material slightly off Q=1 (v=12)
    mat2 = RelMaterial(10, [0, 0, 12.0], 1.0)
    q2 = mat2.calculate_topological_charge()
    eff2 = mat2.calculate_efficiency()

    print(f"Material 1 (V=10): Charge={q1}, Efficiency={eff1:.4f}")
    print(f"Material 2 (V=12): Charge={q2}, Efficiency={eff2:.4f}")

    if eff1 > eff2:
        print("Success: Resonant stability bonus confirmed at integer charge.")
    else:
        print("Warning: Efficiency did not drop as expected off-resonance.")

    # Material at Q=2 (v=20)
    mat3 = RelMaterial(10, [0, 0, 20.0], 1.0)
    q3 = mat3.calculate_topological_charge()
    lifetime3 = mat3.calculate_lifetime()
    lifetime1 = mat1.calculate_lifetime()

    print(f"Material 1 (Q=1): Lifetime={lifetime1:.4f}")
    print(f"Material 3 (Q=2): Lifetime={lifetime3:.4f}")

    if lifetime3 > lifetime1:
        print("Success: Higher topological charge increases protection/lifetime.")

if __name__ == "__main__":
    test_topological_physics()
