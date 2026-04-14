import sys
import numpy as np
from material_engine import RelMaterial
from chemical_translator import ChemicalTranslator

def analyze_formula(formula):
    print(f"--- RELATIVISTIC ANALYSIS: {formula} ---")
    translator = ChemicalTranslator()

    # 1. Reverse lookup to get field parameters
    params = translator.reverse_lookup(formula)
    energy_density = params['energy_density']
    vorticity = params['vorticity']
    coupling = params['coupling']

    # 2. Simulate material physics
    mat = RelMaterial(energy_density, vorticity, coupling)
    efficiency = mat.calculate_efficiency()

    # 3. Analyze stability and fields
    E, B = mat.simulate_fields()
    e_mag = np.linalg.norm(E)
    b_mag = np.linalg.norm(B)

    print(f"Relativistic Figure of Merit (R-ZT): {efficiency:.4f}")
    print(f"Internal Electric Field Strength: {e_mag:.2f}")
    print(f"Internal Vorticity (B-field): {b_mag:.2f}")

    # Stability assessment
    if e_mag > 500:
        print("Status: UNSTABLE (Vacuum Polarization / Schwinger Decay)")
    elif efficiency > 100:
        print("Status: SUPER-EFFICIENT (Solitonic Resonance)")
    else:
        print("Status: STABLE (Standard Relativistic Phase)")

    print("-" * (26 + len(formula)))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        analyze_formula(sys.argv[1])
    else:
        # Default analysis for Bi2Te3
        analyze_formula("Bi2Te3")
        analyze_formula("SiGe")
